"""Notifications application service."""
from __future__ import annotations

import json
from datetime import UTC, datetime

from contexts.notifications.application.commands.deliver_from_event import DeliverFromEventCommand
from contexts.notifications.application.ports.channels import IEmailChannel, INotificationEventAdapter
from contexts.notifications.domain.aggregates.inbox_message import InboxMessage
from contexts.notifications.domain.aggregates.notification_delivery import NotificationDelivery
from contexts.notifications.domain.events.integration_events import (
    InboxCreatedIntegration,
    MessageFailedIntegration,
    MessageSentIntegration,
)
from contexts.notifications.domain.ports.repositories import IDeliveryRepository, IInboxRepository
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event

DEFAULT_TEMPLATES: list[dict] = [
    {"key": "welcome", "channel": "inbox", "category": "onboarding", "description": "New user welcome"},
    {"key": "tenant_provisioned", "channel": "inbox", "category": "platform", "description": "Tenant ready"},
    {"key": "encounter_completed", "channel": "inbox", "category": "healthcare", "description": "Hospital encounter"},
    {"key": "journal_recorded", "channel": "inbox", "category": "finance", "description": "GL journal posted"},
    {"key": "task_assigned", "channel": "inbox", "category": "workflow", "description": "Workflow task assigned"},
    {"key": "custom", "channel": "inbox", "category": "general", "description": "Manual notification"},
]


class ConsoleNotificationAudit:
    async def log(self, **kwargs: object) -> None:
        entry = {
            "type": "audit",
            "context": "notifications",
            **kwargs,
            "occurred_at": datetime.now(UTC).isoformat(),
        }
        print(json.dumps(entry, default=str))


class NotificationApplicationService:
    def __init__(
        self,
        inbox: IInboxRepository,
        deliveries: IDeliveryRepository,
        event_adapter: INotificationEventAdapter,
        email: IEmailChannel,
        audit: ConsoleNotificationAudit | None = None,
    ) -> None:
        self._inbox = inbox
        self._deliveries = deliveries
        self._event_adapter = event_adapter
        self._email = email
        self._audit = audit or ConsoleNotificationAudit()

    async def handle_integration_event(self, envelope: dict) -> None:
        command = await self._event_adapter.parse_integration_event(envelope)
        if command:
            await self.deliver_from_event(command)

    async def deliver_from_event(self, command: DeliverFromEventCommand) -> Result[dict]:
        if command.channel == "inbox":
            return await self._deliver_inbox(command)
        if command.channel == "email":
            return await self._deliver_email(command)
        return Result.fail("notifications.errors.unknown_channel")

    async def send(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        user_id: str | None,
        channel: str,
        title: str,
        body: str,
        category: str = "general",
        recipient_email: str | None = None,
    ) -> Result[dict]:
        command = DeliverFromEventCommand(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            source_event="manual",
            user_id=user_id,
            recipient_email=recipient_email,
            template_key="custom",
            title=title,
            body=body,
            category=category,
            channel=channel,
        )
        if channel == "email":
            if not recipient_email:
                return Result.fail("notifications.errors.email_required")
            return await self._deliver_email(command)
        return await self._deliver_inbox(command)

    async def _deliver_inbox(self, command: DeliverFromEventCommand) -> Result[dict]:
        message = InboxMessage.create(
            tenant_id=command.tenant_id,
            user_id=command.user_id,
            channel="inbox",
            title=command.title,
            body=command.body,
            category=command.category,
            source_event=command.source_event,
            metadata={"template_key": command.template_key},
        )
        await self._inbox.save(message)

        delivery = NotificationDelivery.create(
            tenant_id=command.tenant_id,
            channel="inbox",
            recipient=command.user_id or "tenant-broadcast",
            template_key=command.template_key,
            source_event=command.source_event,
        )
        delivery.mark_sent()
        await self._deliveries.save(delivery)

        sent = MessageSentIntegration(
            tenant_id=TenantId.create(command.tenant_id),
            correlation_id=command.correlation_id,
            delivery_id=delivery.id,
            channel="inbox",
            recipient=delivery.recipient,
            template_key=command.template_key,
        )
        inbox_evt = InboxCreatedIntegration(
            tenant_id=TenantId.create(command.tenant_id),
            correlation_id=command.correlation_id,
            inbox_id=message.id,
            user_id=command.user_id,
            category=command.category,
        )
        await publish_integration_event(sent)
        await publish_integration_event(inbox_evt)

        await self._audit.log(
            tenant_id=command.tenant_id,
            correlation_id=command.correlation_id,
            action="notifications.inbox.created",
            resource_type="inbox_message",
            resource_id=str(message.id),
        )
        return Result.ok({"inbox": message.to_dict(), "delivery": delivery.to_dict()})

    async def _deliver_email(self, command: DeliverFromEventCommand) -> Result[dict]:
        delivery = NotificationDelivery.create(
            tenant_id=command.tenant_id,
            channel="email",
            recipient=command.recipient_email or "",
            template_key=command.template_key,
            source_event=command.source_event,
        )
        try:
            await self._email.send(
                recipient=command.recipient_email or "",
                subject=command.title,
                body=command.body,
            )
            delivery.mark_sent()
            await self._deliveries.save(delivery)
            await publish_integration_event(
                MessageSentIntegration(
                    tenant_id=TenantId.create(command.tenant_id),
                    correlation_id=command.correlation_id,
                    delivery_id=delivery.id,
                    channel="email",
                    recipient=delivery.recipient,
                    template_key=command.template_key,
                )
            )
            return Result.ok({"delivery": delivery.to_dict()})
        except Exception as exc:  # noqa: BLE001 — channel adapter boundary
            delivery.mark_failed(str(exc))
            await self._deliveries.save(delivery)
            await publish_integration_event(
                MessageFailedIntegration(
                    tenant_id=TenantId.create(command.tenant_id),
                    correlation_id=command.correlation_id,
                    delivery_id=delivery.id,
                    channel="email",
                    error=str(exc),
                )
            )
            return Result.fail("notifications.errors.delivery_failed")

    async def list_inbox(
        self, tenant_id: str, user_id: str, *, unread_only: bool = False
    ) -> Result[list[dict]]:
        messages = await self._inbox.list_for_user(tenant_id, user_id, unread_only=unread_only)
        return Result.ok([m.to_dict() for m in messages])

    async def mark_read(self, tenant_id: str, user_id: str, message_id: str) -> Result[dict]:
        from shared.domain.value_objects.unique_id import UniqueId

        message = await self._inbox.find_by_id(tenant_id, UniqueId.from_string(message_id))
        if not message:
            return Result.fail("notifications.errors.message_not_found")
        if message.user_id and message.user_id != user_id:
            return Result.fail("notifications.errors.forbidden")
        message.mark_read()
        await self._inbox.save(message)
        return Result.ok(message.to_dict())

    async def list_templates(self) -> Result[list[dict]]:
        return Result.ok(DEFAULT_TEMPLATES)

    async def list_deliveries(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._deliveries.list_deliveries(tenant_id)
        return Result.ok([d.to_dict() for d in items])
