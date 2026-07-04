"""Dashboard layout."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Dashboard(AggregateRoot):
    tenant_id: str
    name: str
    widgets: list[dict]
    is_default: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        name: str,
        widgets: list[dict],
        is_default: bool = False,
    ) -> Dashboard:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            name=name.strip(),
            widgets=widgets,
            is_default=is_default,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "name": self.name,
            "widgets": self.widgets,
            "is_default": self.is_default,
            "created_at": self.created_at.isoformat(),
        }
