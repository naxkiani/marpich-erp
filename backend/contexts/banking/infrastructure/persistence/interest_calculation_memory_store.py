"""In-memory Interest Calculation Engine repositories."""
from __future__ import annotations

from contexts.banking.domain.aggregates.interest_calculation_engine import (
    InterestCalculationAudit,
    InterestRateChange,
    InterestRateProfile,
)


class InMemoryInterestRateProfileRepository:
    _store: dict[str, InterestRateProfile] = {}
    _counter: dict[str, int] = {}

    async def save(self, profile: InterestRateProfile) -> None:
        self._store[str(profile.id)] = profile

    async def find_by_id(self, profile_id: str) -> InterestRateProfile | None:
        return self._store.get(profile_id)

    async def find_by_ref(self, tenant_id: str, profile_ref: str) -> InterestRateProfile | None:
        for profile in self._store.values():
            if profile.tenant_id == tenant_id and profile.profile_ref == profile_ref:
                return profile
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[InterestRateProfile]:
        return [p for p in self._store.values() if p.tenant_id == tenant_id]

    def next_profile_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"IRP{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}


class InMemoryInterestRateChangeRepository:
    _store: dict[str, InterestRateChange] = {}

    async def save(self, change: InterestRateChange) -> None:
        self._store[str(change.id)] = change

    async def list_by_profile(self, profile_id: str) -> list[InterestRateChange]:
        return sorted(
            [c for c in self._store.values() if c.profile_id == profile_id],
            key=lambda c: c.effective_from,
        )

    async def list_by_tenant(self, tenant_id: str) -> list[InterestRateChange]:
        return sorted(
            [c for c in self._store.values() if c.tenant_id == tenant_id],
            key=lambda c: c.effective_from,
        )

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryInterestCalculationAuditRepository:
    _store: dict[str, InterestCalculationAudit] = {}
    _counter: dict[str, int] = {}

    async def save(self, audit: InterestCalculationAudit) -> None:
        self._store[str(audit.id)] = audit

    async def find_by_id(self, audit_id: str) -> InterestCalculationAudit | None:
        return self._store.get(audit_id)

    async def list_by_tenant(self, tenant_id: str) -> list[InterestCalculationAudit]:
        return sorted(
            [a for a in self._store.values() if a.tenant_id == tenant_id],
            key=lambda a: a.created_at,
            reverse=True,
        )

    async def list_by_profile(self, profile_id: str) -> list[InterestCalculationAudit]:
        return sorted(
            [a for a in self._store.values() if a.profile_id == profile_id],
            key=lambda a: a.created_at,
            reverse=True,
        )

    async def list_by_source_ref(self, tenant_id: str, source_ref: str) -> list[InterestCalculationAudit]:
        return [
            a
            for a in self._store.values()
            if a.tenant_id == tenant_id and a.source_ref == source_ref
        ]

    def next_calc_ref(self, tenant_id: str) -> str:
        self._counter[tenant_id] = self._counter.get(tenant_id, 0) + 1
        return f"ICALC{self._counter[tenant_id]:08d}"

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
        cls._counter = {}
