"""In-memory data isolation persistence."""
from __future__ import annotations

from contexts.data_isolation.domain.aggregates.data_isolation_platform import IsolationProfile, Principal
from contexts.data_isolation.domain.ports.data_isolation_repositories import (
    IIsolationProfileRepository,
    IPrincipalRepository,
)


class InMemoryDataIsolationStore:
    profiles: dict[str, IsolationProfile] = {}
    principals: dict[str, Principal] = {}
    profile_counter: dict[str, int] = {}
    principal_counter: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls.profiles.clear()
        cls.principals.clear()
        cls.profile_counter.clear()
        cls.principal_counter.clear()


class InMemoryIsolationProfileRepository(IIsolationProfileRepository):
    async def find_by_tenant(self, tenant_id: str) -> IsolationProfile | None:
        return InMemoryDataIsolationStore.profiles.get(tenant_id)

    async def save(self, profile: IsolationProfile) -> None:
        InMemoryDataIsolationStore.profiles[profile.tenant_id] = profile

    def next_profile_ref(self, tenant_id: str) -> str:
        n = InMemoryDataIsolationStore.profile_counter.get(tenant_id, 0) + 1
        InMemoryDataIsolationStore.profile_counter[tenant_id] = n
        return f"iso-profile-{tenant_id}-{n:04d}"


class InMemoryPrincipalRepository(IPrincipalRepository):
    async def save(self, principal: Principal) -> None:
        InMemoryDataIsolationStore.principals[f"{principal.tenant_id}:{principal.principal_ref}"] = principal

    async def list_by_tenant(self, tenant_id: str) -> list[Principal]:
        return [p for p in InMemoryDataIsolationStore.principals.values() if p.tenant_id == tenant_id]

    async def find_by_ref(self, tenant_id: str, principal_ref: str) -> Principal | None:
        return InMemoryDataIsolationStore.principals.get(f"{tenant_id}:{principal_ref}")

    async def find_by_user_id(self, tenant_id: str, user_id: str) -> Principal | None:
        for principal in InMemoryDataIsolationStore.principals.values():
            if principal.tenant_id == tenant_id and principal.source_user_id == user_id:
                return principal
        return None

    def next_principal_ref(self, tenant_id: str) -> str:
        n = InMemoryDataIsolationStore.principal_counter.get(tenant_id, 0) + 1
        InMemoryDataIsolationStore.principal_counter[tenant_id] = n
        return f"principal-{tenant_id}-{n:04d}"
