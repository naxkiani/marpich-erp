"""Repository port — Settings."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.settings.domain.aggregates.tenant_settings import TenantSettings


class ITenantSettingsRepository(ABC):
    @abstractmethod
    async def save(self, settings: TenantSettings) -> None: ...

    @abstractmethod
    async def find_by_tenant(self, tenant_id: str) -> TenantSettings | None: ...

    @abstractmethod
    async def exists(self, tenant_id: str) -> bool: ...
