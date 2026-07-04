"""Organization root aggregate — one per tenant."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class Organization(AggregateRoot):
    tenant_id: str
    name: str
    legal_name: str
    root_unit_id: UniqueId | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, name: str, legal_name: str | None = None) -> Organization:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            name=name.strip(),
            legal_name=(legal_name or name).strip(),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "name": self.name,
            "legal_name": self.legal_name,
            "root_unit_id": str(self.root_unit_id) if self.root_unit_id else None,
            "created_at": self.created_at.isoformat(),
        }
