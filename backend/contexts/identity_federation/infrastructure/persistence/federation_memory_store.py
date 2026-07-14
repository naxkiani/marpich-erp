"""In-memory identity federation persistence."""
from __future__ import annotations

from contexts.identity_federation.domain.aggregates.federation_platform import (
    ClaimsMapping,
    FederationPartner,
    FederationProfile,
    FederationSession,
    IdentityLink,
    IdentityProvider,
    ProvisioningPolicy,
    SynchronizationJob,
    TenantFederation,
    TrustRelationship,
)
from contexts.identity_federation.domain.ports.federation_repositories import (
    IClaimsMappingRepository,
    IFederationPartnerRepository,
    IFederationProfileRepository,
    IFederationSessionRepository,
    IIdentityLinkRepository,
    IIdentityProviderRepository,
    IProvisioningPolicyRepository,
    ISynchronizationJobRepository,
    ITenantFederationRepository,
    ITrustRelationshipRepository,
)


class InMemoryFederationStore:
    profiles: dict[str, FederationProfile] = {}
    providers: dict[str, IdentityProvider] = {}
    partners: dict[str, FederationPartner] = {}
    trusts: dict[str, TrustRelationship] = {}
    mappings: dict[str, ClaimsMapping] = {}
    links: dict[str, IdentityLink] = {}
    policies: dict[str, ProvisioningPolicy] = {}
    jobs: dict[str, SynchronizationJob] = {}
    sessions: dict[str, FederationSession] = {}
    tenant_feds: dict[str, TenantFederation] = {}
    counters: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls.profiles.clear()
        cls.providers.clear()
        cls.partners.clear()
        cls.trusts.clear()
        cls.mappings.clear()
        cls.links.clear()
        cls.policies.clear()
        cls.jobs.clear()
        cls.sessions.clear()
        cls.tenant_feds.clear()
        cls.counters.clear()

    @classmethod
    def _next(cls, tenant_id: str, prefix: str) -> str:
        key = f"{tenant_id}:{prefix}"
        n = cls.counters.get(key, 0) + 1
        cls.counters[key] = n
        return f"{prefix}-{tenant_id}-{n:04d}"


class InMemoryFederationProfileRepository(IFederationProfileRepository):
    async def find_by_tenant(self, tenant_id: str) -> FederationProfile | None:
        return InMemoryFederationStore.profiles.get(tenant_id)

    async def save(self, profile: FederationProfile) -> None:
        InMemoryFederationStore.profiles[profile.tenant_id] = profile

    def next_profile_ref(self, tenant_id: str) -> str:
        return InMemoryFederationStore._next(tenant_id, "fed-profile")


class InMemoryIdentityProviderRepository(IIdentityProviderRepository):
    async def save(self, provider: IdentityProvider) -> None:
        InMemoryFederationStore.providers[f"{provider.tenant_id}:{provider.provider_ref}"] = provider

    async def find_by_ref(self, tenant_id: str, provider_ref: str) -> IdentityProvider | None:
        return InMemoryFederationStore.providers.get(f"{tenant_id}:{provider_ref}")

    async def list_by_tenant(self, tenant_id: str) -> list[IdentityProvider]:
        return [p for k, p in InMemoryFederationStore.providers.items() if p.tenant_id == tenant_id]

    def next_provider_ref(self, tenant_id: str) -> str:
        return InMemoryFederationStore._next(tenant_id, "idp")


class InMemoryFederationPartnerRepository(IFederationPartnerRepository):
    async def save(self, partner: FederationPartner) -> None:
        InMemoryFederationStore.partners[f"{partner.tenant_id}:{partner.partner_ref}"] = partner

    async def list_by_tenant(self, tenant_id: str) -> list[FederationPartner]:
        return [p for p in InMemoryFederationStore.partners.values() if p.tenant_id == tenant_id]

    def next_partner_ref(self, tenant_id: str) -> str:
        return InMemoryFederationStore._next(tenant_id, "partner")


class InMemoryTrustRelationshipRepository(ITrustRelationshipRepository):
    async def save(self, trust: TrustRelationship) -> None:
        InMemoryFederationStore.trusts[f"{trust.tenant_id}:{trust.trust_ref}"] = trust

    async def list_by_tenant(self, tenant_id: str) -> list[TrustRelationship]:
        return [t for t in InMemoryFederationStore.trusts.values() if t.tenant_id == tenant_id]

    def next_trust_ref(self, tenant_id: str) -> str:
        return InMemoryFederationStore._next(tenant_id, "trust")


class InMemoryClaimsMappingRepository(IClaimsMappingRepository):
    async def save(self, mapping: ClaimsMapping) -> None:
        InMemoryFederationStore.mappings[f"{mapping.tenant_id}:{mapping.mapping_ref}"] = mapping

    async def list_by_provider(self, tenant_id: str, provider_id: str) -> list[ClaimsMapping]:
        return [
            m for m in InMemoryFederationStore.mappings.values()
            if m.tenant_id == tenant_id and m.provider_id == provider_id
        ]

    def next_mapping_ref(self, tenant_id: str) -> str:
        return InMemoryFederationStore._next(tenant_id, "claim-map")


class InMemoryIdentityLinkRepository(IIdentityLinkRepository):
    async def save(self, link: IdentityLink) -> None:
        InMemoryFederationStore.links[f"{link.tenant_id}:{link.link_ref}"] = link

    async def find_by_external(
        self, tenant_id: str, provider_id: str, external_subject: str
    ) -> IdentityLink | None:
        for link in InMemoryFederationStore.links.values():
            if (
                link.tenant_id == tenant_id
                and link.provider_id == provider_id
                and link.external_subject == external_subject
            ):
                return link
        return None

    async def list_by_user(self, tenant_id: str, user_id: str) -> list[IdentityLink]:
        return [
            l for l in InMemoryFederationStore.links.values()
            if l.tenant_id == tenant_id and l.user_id == user_id
        ]

    def next_link_ref(self, tenant_id: str) -> str:
        return InMemoryFederationStore._next(tenant_id, "link")


class InMemoryProvisioningPolicyRepository(IProvisioningPolicyRepository):
    async def save(self, policy: ProvisioningPolicy) -> None:
        InMemoryFederationStore.policies[f"{policy.tenant_id}:{policy.policy_ref}"] = policy

    async def find_by_provider(self, tenant_id: str, provider_id: str) -> ProvisioningPolicy | None:
        for p in InMemoryFederationStore.policies.values():
            if p.tenant_id == tenant_id and p.provider_id == provider_id:
                return p
        return None

    def next_policy_ref(self, tenant_id: str) -> str:
        return InMemoryFederationStore._next(tenant_id, "prov-policy")


class InMemorySynchronizationJobRepository(ISynchronizationJobRepository):
    async def save(self, job: SynchronizationJob) -> None:
        InMemoryFederationStore.jobs[f"{job.tenant_id}:{job.job_ref}"] = job

    async def list_by_tenant(self, tenant_id: str, *, limit: int = 20) -> list[SynchronizationJob]:
        items = [j for j in InMemoryFederationStore.jobs.values() if j.tenant_id == tenant_id]
        items.sort(key=lambda j: j.created_at, reverse=True)
        return items[:limit]

    def next_job_ref(self, tenant_id: str) -> str:
        return InMemoryFederationStore._next(tenant_id, "sync-job")


class InMemoryFederationSessionRepository(IFederationSessionRepository):
    async def save(self, session: FederationSession) -> None:
        InMemoryFederationStore.sessions[f"{session.tenant_id}:{session.session_ref}"] = session

    async def find_by_ref(self, tenant_id: str, session_ref: str) -> FederationSession | None:
        return InMemoryFederationStore.sessions.get(f"{tenant_id}:{session_ref}")

    def next_session_ref(self, tenant_id: str) -> str:
        return InMemoryFederationStore._next(tenant_id, "fed-sess")


class InMemoryTenantFederationRepository(ITenantFederationRepository):
    async def save(self, federation: TenantFederation) -> None:
        InMemoryFederationStore.tenant_feds[f"{federation.tenant_id}:{federation.federation_ref}"] = federation

    async def list_by_tenant(self, tenant_id: str) -> list[TenantFederation]:
        return [f for f in InMemoryFederationStore.tenant_feds.values() if f.tenant_id == tenant_id]

    def next_federation_ref(self, tenant_id: str) -> str:
        return InMemoryFederationStore._next(tenant_id, "tenant-fed")
