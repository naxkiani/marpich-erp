"""Time-series metric data point."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class MetricSnapshot(AggregateRoot):
    tenant_id: str
    metric_key: str
    value: int
    event_name: str | None
    recorded_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        metric_key: str,
        value: int,
        event_name: str | None = None,
    ) -> MetricSnapshot:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            metric_key=metric_key,
            value=value,
            event_name=event_name,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "metric_key": self.metric_key,
            "value": self.value,
            "event_name": self.event_name,
            "recorded_at": self.recorded_at.isoformat(),
        }
