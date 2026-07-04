"""Notifications integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class MessageSentIntegration(IntegrationEvent):
    delivery_id: UniqueId
    channel: str
    recipient: str
    template_key: str

    @property
    def event_name(self) -> str:
        return "notifications.message.sent"

    @property
    def source_context(self) -> str:
        return "notifications"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "delivery_id": str(self.delivery_id),
            "channel": self.channel,
            "recipient": self.recipient,
            "template_key": self.template_key,
        }


@dataclass(frozen=True, kw_only=True)
class MessageFailedIntegration(IntegrationEvent):
    delivery_id: UniqueId
    channel: str
    error: str

    @property
    def event_name(self) -> str:
        return "notifications.message.failed"

    @property
    def source_context(self) -> str:
        return "notifications"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "delivery_id": str(self.delivery_id),
            "channel": self.channel,
            "error": self.error,
        }


@dataclass(frozen=True, kw_only=True)
class InboxCreatedIntegration(IntegrationEvent):
    inbox_id: UniqueId
    user_id: str | None
    category: str

    @property
    def event_name(self) -> str:
        return "notifications.inbox.created"

    @property
    def source_context(self) -> str:
        return "notifications"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "inbox_id": str(self.inbox_id),
            "user_id": self.user_id,
            "category": self.category,
        }
