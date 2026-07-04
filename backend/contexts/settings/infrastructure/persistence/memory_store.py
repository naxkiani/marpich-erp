"""In-memory settings repository."""
from __future__ import annotations

from contexts.settings.domain.aggregates.tenant_settings import TenantSettings
from contexts.settings.domain.ports.repositories import ITenantSettingsRepository


class SettingsMemoryStore:
    by_tenant: dict[str, TenantSettings] = {}

    @classmethod
    def reset(cls) -> None:
        cls.by_tenant.clear()


class InMemoryTenantSettingsRepository(ITenantSettingsRepository):
    async def save(self, settings: TenantSettings) -> None:
        SettingsMemoryStore.by_tenant[settings.tenant_id] = settings

    async def find_by_tenant(self, tenant_id: str) -> TenantSettings | None:
        return SettingsMemoryStore.by_tenant.get(tenant_id)

    async def exists(self, tenant_id: str) -> bool:
        return tenant_id in SettingsMemoryStore.by_tenant
