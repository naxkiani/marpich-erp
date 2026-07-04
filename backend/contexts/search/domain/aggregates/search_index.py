"""Per-tenant search index configuration."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SearchIndex(AggregateRoot):
    tenant_id: str
    entity_type: str
    is_active: bool = True
    mapping: dict = field(default_factory=dict)
    document_count: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, entity_type: str, mapping: dict | None = None) -> SearchIndex:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            entity_type=entity_type.lower(),
            mapping=mapping or {},
        )

    def increment_count(self, delta: int = 1) -> None:
        self.document_count += delta

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "entity_type": self.entity_type,
            "is_active": self.is_active,
            "mapping": self.mapping,
            "document_count": self.document_count,
            "created_at": self.created_at.isoformat(),
        }
