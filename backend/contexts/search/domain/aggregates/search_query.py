"""Search query audit record."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class SearchQuery(AggregateRoot):
    tenant_id: str
    query_text: str
    entity_types: list[str]
    result_count: int
    filters: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        query_text: str,
        entity_types: list[str],
        result_count: int,
        filters: dict | None = None,
    ) -> SearchQuery:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            query_text=query_text,
            entity_types=entity_types,
            result_count=result_count,
            filters=filters or {},
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "query_text": self.query_text,
            "entity_types": self.entity_types,
            "result_count": self.result_count,
            "filters": self.filters,
            "created_at": self.created_at.isoformat(),
        }
