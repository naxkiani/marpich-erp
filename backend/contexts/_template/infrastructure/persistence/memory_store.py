"""In-memory repository adapter."""
from __future__ import annotations

from contexts.module_id.domain.aggregates.example import ExampleAggregate
from contexts.module_id.domain.ports.example_repository import IExampleRepository


class InMemoryExampleRepository(IExampleRepository):
    def __init__(self) -> None:
        self._store: dict[str, ExampleAggregate] = {}

    async def save(self, aggregate: ExampleAggregate) -> None:
        self._store[aggregate.id] = aggregate

    async def list_by_tenant(
        self, tenant_id: str, *, limit: int, offset: int
    ) -> list[ExampleAggregate]:
        rows = [a for a in self._store.values() if a.tenant_id == tenant_id]
        return rows[offset : offset + limit]
