"""Outbound webhook subscription."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class WebhookSubscription(AggregateRoot):
    tenant_id: str
    target_url: str
    event_pattern: str
    secret: str
    description: str
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        target_url: str,
        event_pattern: str,
        secret: str = "",
        description: str = "",
    ) -> WebhookSubscription:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            target_url=target_url.strip(),
            event_pattern=event_pattern.strip(),
            secret=secret,
            description=description.strip(),
        )

    def matches(self, event_name: str) -> bool:
        if not self.is_active:
            return False
        if self.event_pattern == "*":
            return True
        return self.event_pattern == event_name

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "target_url": self.target_url,
            "event_pattern": self.event_pattern,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }
