"""Threshold alert rule."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class AlertRule(AggregateRoot):
    tenant_id: str
    metric_key: str
    name: str
    threshold: int
    operator: str
    is_active: bool = True
    last_triggered_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        metric_key: str,
        name: str,
        threshold: int,
        operator: str = "gte",
    ) -> AlertRule:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            metric_key=metric_key.strip().lower(),
            name=name.strip(),
            threshold=threshold,
            operator=operator,
        )

    def should_trigger(self, value: int) -> bool:
        if not self.is_active:
            return False
        if self.operator == "gte":
            return value >= self.threshold
        if self.operator == "lte":
            return value <= self.threshold
        return value == self.threshold

    def mark_triggered(self) -> None:
        self.last_triggered_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "metric_key": self.metric_key,
            "name": self.name,
            "threshold": self.threshold,
            "operator": self.operator,
            "is_active": self.is_active,
            "last_triggered_at": self.last_triggered_at.isoformat() if self.last_triggered_at else None,
            "created_at": self.created_at.isoformat(),
        }
