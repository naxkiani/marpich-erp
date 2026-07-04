"""Base repository port — generic persistence boundary."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from shared.domain.value_objects.unique_id import UniqueId

T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    @abstractmethod
    async def save(self, entity: T) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, entity_id: UniqueId) -> T | None: ...

    @abstractmethod
    async def delete(self, tenant_id: str, entity_id: UniqueId) -> None: ...
