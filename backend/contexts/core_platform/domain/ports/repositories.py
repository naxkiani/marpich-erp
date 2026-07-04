"""Repository ports — Core Platform."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.core_platform.domain.aggregates.tenant import Tenant
from shared.domain.value_objects.unique_id import UniqueId


class ITenantRepository(ABC):
    @abstractmethod
    async def save(self, tenant: Tenant) -> None: ...

    @abstractmethod
    async def find_by_slug(self, slug: str) -> Tenant | None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: UniqueId) -> Tenant | None: ...

    @abstractmethod
    async def exists_by_slug(self, slug: str) -> bool: ...

    @abstractmethod
    async def list_tenants(self) -> list[Tenant]: ...
