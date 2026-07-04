"""Integration application service."""
from __future__ import annotations

from contexts.integration.application.commands.provision_connectors import ProvisionConnectorsCommand
from contexts.integration.application.ports.channels import IIntegrationPlatformAdapter, IWebhookChannel
from contexts.integration.domain.aggregates.connector import Connector, ConnectorType
from contexts.integration.domain.aggregates.integration_log import IntegrationLog, LogStatus
from contexts.integration.domain.aggregates.sync_job import SyncJob
from contexts.integration.domain.aggregates.webhook_subscription import WebhookSubscription
from contexts.integration.domain.events.integration_events import (
    ConnectorRegisteredIntegration,
    SyncCompletedIntegration,
    WebhookDeliveredIntegration,
    WebhookFailedIntegration,
)
from contexts.integration.domain.ports.repositories import (
    IConnectorRepository,
    IIntegrationLogRepository,
    ISyncJobRepository,
    IWebhookRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event

DEFAULT_CONNECTOR_SLOTS = (
    (ConnectorType.CRM, "CRM Connector Slot"),
    (ConnectorType.ERP, "ERP Connector Slot"),
)


class IntegrationApplicationService:
    def __init__(
        self,
        connectors: IConnectorRepository,
        webhooks: IWebhookRepository,
        sync_jobs: ISyncJobRepository,
        logs: IIntegrationLogRepository,
        platform_events: IIntegrationPlatformAdapter,
        webhook_channel: IWebhookChannel,
    ) -> None:
        self._connectors = connectors
        self._webhooks = webhooks
        self._sync_jobs = sync_jobs
        self._logs = logs
        self._platform_events = platform_events
        self._webhook_channel = webhook_channel

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        command = await self._platform_events.parse_tenant_provisioned(envelope)
        await self.provision_default_connectors(command)

    async def handle_integration_event(self, envelope: dict) -> None:
        if envelope.get("source_context") == "integration":
            return

        tenant_id = envelope.get("tenant_id", "")
        event_name = envelope.get("event_name", "")
        correlation_id = envelope.get("correlation_id", "")

        subscriptions = await self._webhooks.list_active_for_event(tenant_id, event_name)
        for webhook in subscriptions:
            await self._deliver_webhook(
                tenant_id=tenant_id,
                correlation_id=correlation_id,
                webhook=webhook,
                envelope=envelope,
            )

    async def provision_default_connectors(self, command: ProvisionConnectorsCommand) -> Result[list[dict]]:
        existing = await self._connectors.list_by_tenant(command.tenant_id)
        if existing:
            return Result.ok([c.to_dict() for c in existing])

        created: list[dict] = []
        for connector_type, name in DEFAULT_CONNECTOR_SLOTS:
            connector = Connector.create(
                tenant_id=command.tenant_id,
                connector_type=connector_type,
                name=name,
                config={"slot": True},
                is_active=False,
            )
            await self._connectors.save(connector)
            created.append(connector.to_dict())
        return Result.ok(created)

    async def register_connector(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        connector_type: str,
        name: str,
        config: dict | None,
    ) -> Result[dict]:
        try:
            ctype = ConnectorType(connector_type)
        except ValueError:
            return Result.fail("integration.errors.invalid_connector_type")

        connector = Connector.create(
            tenant_id=tenant_id,
            connector_type=ctype,
            name=name,
            config=config,
            is_active=True,
        )
        await self._connectors.save(connector)

        await publish_integration_event(
            ConnectorRegisteredIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                connector_id=connector.id,
                connector_type=connector.connector_type.value,
                name=connector.name,
            )
        )
        return Result.ok(connector.to_dict())

    async def list_connectors(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._connectors.list_by_tenant(tenant_id)
        return Result.ok([c.to_dict() for c in items])

    async def create_webhook(
        self,
        *,
        tenant_id: str,
        target_url: str,
        event_pattern: str,
        secret: str,
        description: str,
    ) -> Result[dict]:
        webhook = WebhookSubscription.create(
            tenant_id=tenant_id,
            target_url=target_url,
            event_pattern=event_pattern,
            secret=secret,
            description=description,
        )
        await self._webhooks.save(webhook)
        return Result.ok(webhook.to_dict())

    async def list_webhooks(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._webhooks.list_by_tenant(tenant_id)
        return Result.ok([w.to_dict() for w in items])

    async def test_webhook(
        self, tenant_id: str, correlation_id: str, webhook_id: str
    ) -> Result[dict]:
        webhook = await self._webhooks.find_by_id(tenant_id, UniqueId.from_string(webhook_id))
        if not webhook:
            return Result.fail("integration.errors.webhook_not_found")

        test_envelope = {
            "event_name": "integration.webhook.test",
            "tenant_id": tenant_id,
            "correlation_id": correlation_id,
            "source_context": "integration",
            "payload": {"test": True},
        }
        return await self._deliver_webhook(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            webhook=webhook,
            envelope=test_envelope,
            force=True,
        )

    async def _deliver_webhook(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        webhook: WebhookSubscription,
        envelope: dict,
        force: bool = False,
    ) -> Result[dict]:
        event_name = envelope.get("event_name", "")
        if not force and not webhook.matches(event_name):
            return Result.fail("integration.errors.event_not_matched")

        payload = {
            "event": envelope,
            "webhook_id": str(webhook.id),
        }
        try:
            if webhook.target_url.startswith("fail://"):
                raise RuntimeError("Simulated webhook delivery failure")

            await self._webhook_channel.deliver(
                target_url=webhook.target_url,
                payload=payload,
                secret=webhook.secret,
            )
            log = IntegrationLog.record(
                tenant_id=tenant_id,
                log_type="webhook",
                status=LogStatus.DELIVERED,
                reference_id=str(webhook.id),
                event_name=event_name,
                detail={"target_url": webhook.target_url},
            )
            await self._logs.append(log)

            await publish_integration_event(
                WebhookDeliveredIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=correlation_id,
                    webhook_id=webhook.id,
                    source_event=event_name,
                    target_url=webhook.target_url,
                )
            )
            return Result.ok({"status": "delivered", "log": log.to_dict()})
        except Exception as exc:  # noqa: BLE001 — channel boundary
            log = IntegrationLog.record(
                tenant_id=tenant_id,
                log_type="webhook",
                status=LogStatus.FAILED,
                reference_id=str(webhook.id),
                event_name=event_name,
                detail={"error": str(exc), "target_url": webhook.target_url},
            )
            await self._logs.append(log)

            await publish_integration_event(
                WebhookFailedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=correlation_id,
                    webhook_id=webhook.id,
                    source_event=event_name,
                    error=str(exc),
                )
            )
            return Result.fail("integration.errors.delivery_failed")

    async def trigger_sync_job(
        self,
        *,
        tenant_id: str,
        correlation_id: str,
        connector_id: str,
        job_type: str,
    ) -> Result[dict]:
        connector = await self._connectors.find_by_id(tenant_id, UniqueId.from_string(connector_id))
        if not connector:
            return Result.fail("integration.errors.connector_not_found")

        job = SyncJob.create(
            tenant_id=tenant_id,
            connector_id=connector.id,
            job_type=job_type,
        )
        job.complete({"records_synced": 0, "connector": connector.name})
        await self._sync_jobs.save(job)

        log = IntegrationLog.record(
            tenant_id=tenant_id,
            log_type="sync",
            status=LogStatus.DELIVERED,
            reference_id=str(job.id),
            detail={"connector_id": str(connector.id), "job_type": job_type},
        )
        await self._logs.append(log)

        await publish_integration_event(
            SyncCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                sync_job_id=job.id,
                connector_id=connector.id,
                job_type=job.job_type,
            )
        )
        return Result.ok(job.to_dict())

    async def list_logs(self, tenant_id: str) -> Result[list[dict]]:
        items = await self._logs.list_by_tenant(tenant_id)
        return Result.ok([log.to_dict() for log in items])
