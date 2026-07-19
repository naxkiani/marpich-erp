"""In-memory cross-tenant delegation / partner / external stores (P200-B8)."""
from __future__ import annotations

from contexts.identity_federation.domain.aggregates.cross_tenant_platform import (
    DelegationAgreement,
    ExternalIdentity,
    PartnerAccess,
)
from contexts.identity_federation.domain.ports.cross_tenant_repositories import (
    IDelegationRepository,
    IExternalIdentityRepository,
    IPartnerAccessRepository,
)


class CrossTenantMemoryStore:
    delegations: dict[str, DelegationAgreement] = {}
    partners: dict[str, PartnerAccess] = {}
    externals: dict[str, ExternalIdentity] = {}
    counters: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls.delegations.clear()
        cls.partners.clear()
        cls.externals.clear()
        cls.counters.clear()

    @classmethod
    def _next(cls, tenant_id: str, prefix: str) -> str:
        key = f"{tenant_id}:{prefix}"
        cls.counters[key] = cls.counters.get(key, 0) + 1
        return f"{prefix}-{cls.counters[key]:04d}"


class InMemoryDelegationRepository(IDelegationRepository):
    async def save(self, agreement: DelegationAgreement) -> None:
        CrossTenantMemoryStore.delegations[
            f"{agreement.tenant_id}:{agreement.delegation_ref}"
        ] = agreement

    async def list_by_tenant(self, tenant_id: str, *, limit: int = 50) -> list[DelegationAgreement]:
        items = [d for d in CrossTenantMemoryStore.delegations.values() if d.tenant_id == tenant_id]
        return items[:limit]

    def next_ref(self, tenant_id: str) -> str:
        return CrossTenantMemoryStore._next(tenant_id, "deleg")


class InMemoryPartnerAccessRepository(IPartnerAccessRepository):
    async def save(self, partner: PartnerAccess) -> None:
        CrossTenantMemoryStore.partners[f"{partner.tenant_id}:{partner.partner_ref}"] = partner

    async def list_by_tenant(self, tenant_id: str, *, limit: int = 50) -> list[PartnerAccess]:
        items = [p for p in CrossTenantMemoryStore.partners.values() if p.tenant_id == tenant_id]
        return items[:limit]

    def next_ref(self, tenant_id: str) -> str:
        return CrossTenantMemoryStore._next(tenant_id, "partner")


class InMemoryExternalIdentityRepository(IExternalIdentityRepository):
    async def save(self, identity: ExternalIdentity) -> None:
        CrossTenantMemoryStore.externals[
            f"{identity.tenant_id}:{identity.external_ref}"
        ] = identity

    async def list_by_tenant(self, tenant_id: str, *, limit: int = 50) -> list[ExternalIdentity]:
        items = [e for e in CrossTenantMemoryStore.externals.values() if e.tenant_id == tenant_id]
        return items[:limit]

    def next_ref(self, tenant_id: str) -> str:
        return CrossTenantMemoryStore._next(tenant_id, "ext")
