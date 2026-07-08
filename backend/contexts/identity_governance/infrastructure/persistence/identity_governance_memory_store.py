"""In-memory Enterprise Identity Governance Platform persistence."""
from __future__ import annotations

from contexts.identity_governance.domain.aggregates.identity_governance_platform import (
    AccessRequest,
    AccessReview,
    EmergencyAccessGrant,
    GovernanceAuditEntry,
    IdentityGovernanceProfile,
    PrivilegeCertification,
    TemporaryAccessGrant,
)
from contexts.identity_governance.domain.ports.identity_governance_repositories import (
    IAccessRequestRepository,
    IAccessReviewRepository,
    IEmergencyAccessGrantRepository,
    IGovernanceAuditEntryRepository,
    IIdentityGovernanceProfileRepository,
    IPrivilegeCertificationRepository,
    ITemporaryAccessGrantRepository,
)


class _RefCounter:
    _counters: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls._counters = {}

    @classmethod
    def next(cls, tenant_id: str, prefix: str) -> str:
        key = f"{tenant_id}:{prefix}"
        n = cls._counters.get(key, 0) + 1
        cls._counters[key] = n
        return f"{prefix}-{tenant_id[:4].upper()}-{n:05d}"


class InMemoryIdentityGovernanceProfileRepository(IIdentityGovernanceProfileRepository):
    _store: dict[str, IdentityGovernanceProfile] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, profile: IdentityGovernanceProfile) -> None:
        self._store[str(profile.id)] = profile

    async def find_by_tenant(self, tenant_id: str) -> IdentityGovernanceProfile | None:
        for p in self._store.values():
            if p.tenant_id == tenant_id:
                return p
        return None

    def next_profile_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-IGP-PRF")


class InMemoryAccessRequestRepository(IAccessRequestRepository):
    _store: dict[str, AccessRequest] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, request: AccessRequest) -> None:
        self._store[str(request.id)] = request

    async def find_by_ref(self, tenant_id: str, request_ref: str) -> AccessRequest | None:
        for item in self._store.values():
            if item.tenant_id == tenant_id and item.request_ref == request_ref:
                return item
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[AccessRequest]:
        items = [r for r in self._store.values() if r.tenant_id == tenant_id]
        return sorted(items, key=lambda r: r.created_at, reverse=True)

    def next_request_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-ARQ")


class InMemoryAccessReviewRepository(IAccessReviewRepository):
    _store: dict[str, AccessReview] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, review: AccessReview) -> None:
        self._store[str(review.id)] = review

    async def find_by_ref(self, tenant_id: str, review_ref: str) -> AccessReview | None:
        for item in self._store.values():
            if item.tenant_id == tenant_id and item.review_ref == review_ref:
                return item
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[AccessReview]:
        items = [r for r in self._store.values() if r.tenant_id == tenant_id]
        return sorted(items, key=lambda r: r.created_at, reverse=True)

    def next_review_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-ARV")


class InMemoryPrivilegeCertificationRepository(IPrivilegeCertificationRepository):
    _store: dict[str, PrivilegeCertification] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, certification: PrivilegeCertification) -> None:
        self._store[str(certification.id)] = certification

    async def find_by_ref(self, tenant_id: str, certification_ref: str) -> PrivilegeCertification | None:
        for item in self._store.values():
            if item.tenant_id == tenant_id and item.certification_ref == certification_ref:
                return item
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[PrivilegeCertification]:
        items = [c for c in self._store.values() if c.tenant_id == tenant_id]
        return sorted(items, key=lambda c: c.created_at, reverse=True)

    def next_certification_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-CERT")


class InMemoryTemporaryAccessGrantRepository(ITemporaryAccessGrantRepository):
    _store: dict[str, TemporaryAccessGrant] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, grant: TemporaryAccessGrant) -> None:
        self._store[str(grant.id)] = grant

    async def list_by_tenant(self, tenant_id: str) -> list[TemporaryAccessGrant]:
        items = [g for g in self._store.values() if g.tenant_id == tenant_id]
        return sorted(items, key=lambda g: g.created_at, reverse=True)

    def next_grant_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-TMP")


class InMemoryEmergencyAccessGrantRepository(IEmergencyAccessGrantRepository):
    _store: dict[str, EmergencyAccessGrant] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, grant: EmergencyAccessGrant) -> None:
        self._store[str(grant.id)] = grant

    async def list_by_tenant(self, tenant_id: str) -> list[EmergencyAccessGrant]:
        items = [g for g in self._store.values() if g.tenant_id == tenant_id]
        return sorted(items, key=lambda g: g.created_at, reverse=True)

    def next_grant_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-EMG")


class InMemoryGovernanceAuditEntryRepository(IGovernanceAuditEntryRepository):
    _store: dict[str, GovernanceAuditEntry] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, entry: GovernanceAuditEntry) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_tenant(self, tenant_id: str) -> list[GovernanceAuditEntry]:
        items = [e for e in self._store.values() if e.tenant_id == tenant_id]
        return sorted(items, key=lambda e: e.created_at, reverse=True)

    def next_entry_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-IGA")
