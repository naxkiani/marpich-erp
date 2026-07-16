"""In-memory Enterprise Regulatory Reporting Platform persistence."""
from __future__ import annotations

from contexts.regulatory_reporting.domain.aggregates.regulatory_reporting_platform import (
    CountryAdapter,
    DigitalSubmission,
    RegulatoryTenantProfile,
)
from contexts.regulatory_reporting.domain.ports.regulatory_reporting_repositories import (
    ICountryAdapterRepository,
    IDigitalSubmissionRepository,
    IRegulatoryTenantProfileRepository,
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


class InMemoryRegulatoryTenantProfileRepository(IRegulatoryTenantProfileRepository):
    _store: dict[str, RegulatoryTenantProfile] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, profile: RegulatoryTenantProfile) -> None:
        self._store[str(profile.id)] = profile

    async def find_by_tenant(self, tenant_id: str) -> RegulatoryTenantProfile | None:
        for p in self._store.values():
            if p.tenant_id == tenant_id:
                return p
        return None

    def next_profile_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-REG-PRF")


class InMemoryCountryAdapterRepository(ICountryAdapterRepository):
    _store: dict[str, CountryAdapter] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, adapter: CountryAdapter) -> None:
        self._store[str(adapter.id)] = adapter

    async def find_by_ref(self, tenant_id: str, adapter_ref: str) -> CountryAdapter | None:
        for item in self._store.values():
            if item.tenant_id == tenant_id and item.adapter_ref == adapter_ref:
                return item
        return None

    async def find_by_country(self, tenant_id: str, country_code: str) -> CountryAdapter | None:
        code = country_code.upper()
        for item in self._store.values():
            if item.tenant_id == tenant_id and item.country_code == code:
                return item
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[CountryAdapter]:
        items = [a for a in self._store.values() if a.tenant_id == tenant_id]
        return sorted(items, key=lambda a: a.country_code)

    def next_adapter_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-ADP")


class InMemoryDigitalSubmissionRepository(IDigitalSubmissionRepository):
    _store: dict[str, DigitalSubmission] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, submission: DigitalSubmission) -> None:
        self._store[str(submission.id)] = submission

    async def find_by_ref(self, tenant_id: str, submission_ref: str) -> DigitalSubmission | None:
        for item in self._store.values():
            if item.tenant_id == tenant_id and item.submission_ref == submission_ref:
                return item
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[DigitalSubmission]:
        items = [s for s in self._store.values() if s.tenant_id == tenant_id]
        return sorted(items, key=lambda s: s.created_at, reverse=True)

    def next_submission_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-DSUB")
