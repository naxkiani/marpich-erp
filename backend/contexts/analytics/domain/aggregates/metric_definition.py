"""KPI / metric definition."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class MetricDefinition(AggregateRoot):
    tenant_id: str
    key: str
    name: str
    event_pattern: str
    description: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        key: str,
        name: str,
        event_pattern: str,
        description: str = "",
    ) -> MetricDefinition:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            key=key.strip().lower(),
            name=name.strip(),
            event_pattern=event_pattern.strip(),
            description=description.strip(),
        )

    def matches(self, event_name: str) -> bool:
        if self.event_pattern == "*":
            return True
        return self.event_pattern == event_name

    def to_dict(self, *, current_value: int = 0) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "key": self.key,
            "name": self.name,
            "event_pattern": self.event_pattern,
            "description": self.description,
            "current_value": current_value,
            "created_at": self.created_at.isoformat(),
        }
