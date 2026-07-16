"""Enterprise Identity Governance Platform repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.identity_governance.domain.aggregates.identity_governance_platform import (
    AccessRequest,
    AccessReview,
    EmergencyAccessGrant,
    GovernanceAuditEntry,
    IdentityGovernanceProfile,
    PrivilegeCertification,
    TemporaryAccessGrant,
)


class IIdentityGovernanceProfileRepository(ABC):
    @abstractmethod
    async def save(self, profile: IdentityGovernanceProfile) -> None: ...

    @abstractmethod
    async def find_by_tenant(self, tenant_id: str) -> IdentityGovernanceProfile | None: ...

    @abstractmethod
    def next_profile_ref(self, tenant_id: str) -> str: ...


class IAccessRequestRepository(ABC):
    @abstractmethod
    async def save(self, request: AccessRequest) -> None: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, request_ref: str) -> AccessRequest | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[AccessRequest]: ...

    @abstractmethod
    def next_request_ref(self, tenant_id: str) -> str: ...


class IAccessReviewRepository(ABC):
    @abstractmethod
    async def save(self, review: AccessReview) -> None: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, review_ref: str) -> AccessReview | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[AccessReview]: ...

    @abstractmethod
    def next_review_ref(self, tenant_id: str) -> str: ...


class IPrivilegeCertificationRepository(ABC):
    @abstractmethod
    async def save(self, certification: PrivilegeCertification) -> None: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, certification_ref: str) -> PrivilegeCertification | None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[PrivilegeCertification]: ...

    @abstractmethod
    def next_certification_ref(self, tenant_id: str) -> str: ...


class ITemporaryAccessGrantRepository(ABC):
    @abstractmethod
    async def save(self, grant: TemporaryAccessGrant) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[TemporaryAccessGrant]: ...

    @abstractmethod
    def next_grant_ref(self, tenant_id: str) -> str: ...


class IEmergencyAccessGrantRepository(ABC):
    @abstractmethod
    async def save(self, grant: EmergencyAccessGrant) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[EmergencyAccessGrant]: ...

    @abstractmethod
    def next_grant_ref(self, tenant_id: str) -> str: ...


class IGovernanceAuditEntryRepository(ABC):
    @abstractmethod
    async def save(self, entry: GovernanceAuditEntry) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[GovernanceAuditEntry]: ...

    @abstractmethod
    def next_entry_ref(self, tenant_id: str) -> str: ...
