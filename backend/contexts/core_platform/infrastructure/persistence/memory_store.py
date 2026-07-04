"""In-memory tenant repository."""
from __future__ import annotations

from contexts.core_platform.domain.aggregates.tenant import Tenant
from contexts.core_platform.domain.ports.repositories import ITenantRepository
from shared.domain.value_objects.unique_id import UniqueId


class PlatformMemoryStore:
    tenants: dict[str, Tenant] = {}
    by_slug: dict[str, str] = {}

    @classmethod
    def reset(cls) -> None:
        cls.tenants.clear()
        cls.by_slug.clear()


class InMemoryTenantRepository(ITenantRepository):
    async def save(self, tenant: Tenant) -> None:
        PlatformMemoryStore.tenants[str(tenant.id)] = tenant
        PlatformMemoryStore.by_slug[tenant.slug] = str(tenant.id)

    async def find_by_slug(self, slug: str) -> Tenant | None:
        tenant_id = PlatformMemoryStore.by_slug.get(slug.lower())
        if not tenant_id:
            return None
        return PlatformMemoryStore.tenants.get(tenant_id)

    async def find_by_id(self, tenant_id: UniqueId) -> Tenant | None:
        return PlatformMemoryStore.tenants.get(str(tenant_id))

    async def exists_by_slug(self, slug: str) -> bool:
        return slug.lower() in PlatformMemoryStore.by_slug

    async def list_tenants(self) -> list[Tenant]:
        return list(PlatformMemoryStore.tenants.values())
