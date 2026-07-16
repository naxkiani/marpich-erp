"""Identity federation repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

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


class IFederationProfileRepository(ABC):
    @abstractmethod
    async def find_by_tenant(self, tenant_id: str) -> FederationProfile | None: ...

    @abstractmethod
    async def save(self, profile: FederationProfile) -> None: ...

    @abstractmethod
    def next_profile_ref(self, tenant_id: str) -> str: ...


class IIdentityProviderRepository(ABC):
    @abstractmethod
    async def save(self, provider: IdentityProvider) -> None: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, provider_ref: str) -> IdentityProvider | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[IdentityProvider]: ...

    @abstractmethod
    def next_provider_ref(self, tenant_id: str) -> str: ...


class IFederationPartnerRepository(ABC):
    @abstractmethod
    async def save(self, partner: FederationPartner) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[FederationPartner]: ...

    @abstractmethod
    def next_partner_ref(self, tenant_id: str) -> str: ...


class ITrustRelationshipRepository(ABC):
    @abstractmethod
    async def save(self, trust: TrustRelationship) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[TrustRelationship]: ...

    @abstractmethod
    def next_trust_ref(self, tenant_id: str) -> str: ...


class IClaimsMappingRepository(ABC):
    @abstractmethod
    async def save(self, mapping: ClaimsMapping) -> None: ...

    @abstractmethod
    async def list_by_provider(self, tenant_id: str, provider_id: str) -> list[ClaimsMapping]: ...

    @abstractmethod
    def next_mapping_ref(self, tenant_id: str) -> str: ...


class IIdentityLinkRepository(ABC):
    @abstractmethod
    async def save(self, link: IdentityLink) -> None: ...

    @abstractmethod
    async def find_by_external(
        self, tenant_id: str, provider_id: str, external_subject: str
    ) -> IdentityLink | None: ...

    @abstractmethod
    async def list_by_user(self, tenant_id: str, user_id: str) -> list[IdentityLink]: ...

    @abstractmethod
    def next_link_ref(self, tenant_id: str) -> str: ...


class IProvisioningPolicyRepository(ABC):
    @abstractmethod
    async def save(self, policy: ProvisioningPolicy) -> None: ...

    @abstractmethod
    async def find_by_provider(self, tenant_id: str, provider_id: str) -> ProvisioningPolicy | None: ...

    @abstractmethod
    def next_policy_ref(self, tenant_id: str) -> str: ...


class ISynchronizationJobRepository(ABC):
    @abstractmethod
    async def save(self, job: SynchronizationJob) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str, *, limit: int = 20) -> list[SynchronizationJob]: ...

    @abstractmethod
    def next_job_ref(self, tenant_id: str) -> str: ...


class IFederationSessionRepository(ABC):
    @abstractmethod
    async def save(self, session: FederationSession) -> None: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, session_ref: str) -> FederationSession | None: ...

    @abstractmethod
    def next_session_ref(self, tenant_id: str) -> str: ...


class ITenantFederationRepository(ABC):
    @abstractmethod
    async def save(self, federation: TenantFederation) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[TenantFederation]: ...

    @abstractmethod
    def next_federation_ref(self, tenant_id: str) -> str: ...
