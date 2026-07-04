"""Notification delivery log aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class DeliveryStatus(StrEnum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


@dataclass(eq=False, kw_only=True)
class NotificationDelivery(AggregateRoot):
    tenant_id: str
    channel: str
    recipient: str
    template_key: str
    source_event: str
    status: DeliveryStatus = DeliveryStatus.PENDING
    error: str | None = None
    payload: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    delivered_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        channel: str,
        recipient: str,
        template_key: str,
        source_event: str,
        payload: dict | None = None,
    ) -> NotificationDelivery:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            channel=channel,
            recipient=recipient,
            template_key=template_key,
            source_event=source_event,
            payload=payload or {},
        )

    def mark_sent(self) -> None:
        self.status = DeliveryStatus.SENT
        self.delivered_at = datetime.now(UTC)

    def mark_failed(self, error: str) -> None:
        self.status = DeliveryStatus.FAILED
        self.error = error

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "channel": self.channel,
            "recipient": self.recipient,
            "template_key": self.template_key,
            "source_event": self.source_event,
            "status": self.status.value,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None,
        }
