"""Repository port — implemented in infrastructure/persistence/."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.module_id.domain.aggregates.example import ExampleAggregate


class IExampleRepository(ABC):
    @abstractmethod
    async def save(self, aggregate: ExampleAggregate) -> None: ...

    @abstractmethod
    async def list_by_tenant(
        self, tenant_id: str, *, limit: int, offset: int
    ) -> list[ExampleAggregate]: ...
