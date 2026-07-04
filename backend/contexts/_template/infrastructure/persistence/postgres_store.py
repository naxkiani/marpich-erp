"""PostgreSQL repository adapter — own schema only."""
from __future__ import annotations

from contexts.module_id.domain.aggregates.example import ExampleAggregate
from contexts.module_id.domain.ports.example_repository import IExampleRepository


class PostgresExampleRepository(IExampleRepository):
    async def save(self, aggregate: ExampleAggregate) -> None:
        raise NotImplementedError("Wire ORM row in shared/infrastructure/database/orm.py")

    async def list_by_tenant(
        self, tenant_id: str, *, limit: int, offset: int
    ) -> list[ExampleAggregate]:
        raise NotImplementedError("Wire ORM query for module schema")
