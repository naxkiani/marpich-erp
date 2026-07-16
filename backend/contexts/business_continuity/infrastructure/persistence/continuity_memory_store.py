"""In-memory Enterprise Business Continuity Platform persistence."""
from __future__ import annotations

from contexts.business_continuity.domain.aggregates.continuity_platform import (
    BackupStrategy,
    ContinuityPlan,
    ContinuityTenantProfile,
    FailoverRecord,
    RecoveryTest,
)
from contexts.business_continuity.domain.ports.continuity_repositories import (
    IBackupStrategyRepository,
    IContinuityPlanRepository,
    IContinuityTenantProfileRepository,
    IFailoverRecordRepository,
    IRecoveryTestRepository,
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


class InMemoryContinuityTenantProfileRepository(IContinuityTenantProfileRepository):
    _store: dict[str, ContinuityTenantProfile] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, profile: ContinuityTenantProfile) -> None:
        self._store[str(profile.id)] = profile

    async def find_by_tenant(self, tenant_id: str) -> ContinuityTenantProfile | None:
        for p in self._store.values():
            if p.tenant_id == tenant_id:
                return p
        return None

    def next_profile_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-BCP-PRF")


class InMemoryContinuityPlanRepository(IContinuityPlanRepository):
    _store: dict[str, ContinuityPlan] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, plan: ContinuityPlan) -> None:
        self._store[str(plan.id)] = plan

    async def find_by_ref(self, tenant_id: str, plan_ref: str) -> ContinuityPlan | None:
        for item in self._store.values():
            if item.tenant_id == tenant_id and item.plan_ref == plan_ref:
                return item
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[ContinuityPlan]:
        items = [p for p in self._store.values() if p.tenant_id == tenant_id]
        return sorted(items, key=lambda p: p.created_at)

    def next_plan_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-BCP")


class InMemoryBackupStrategyRepository(IBackupStrategyRepository):
    _store: dict[str, BackupStrategy] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, strategy: BackupStrategy) -> None:
        self._store[str(strategy.id)] = strategy

    async def list_by_tenant(self, tenant_id: str) -> list[BackupStrategy]:
        items = [s for s in self._store.values() if s.tenant_id == tenant_id]
        return sorted(items, key=lambda s: s.created_at)

    def next_strategy_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-BAK")


class InMemoryFailoverRecordRepository(IFailoverRecordRepository):
    _store: dict[str, FailoverRecord] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, record: FailoverRecord) -> None:
        self._store[str(record.id)] = record

    async def find_by_ref(self, tenant_id: str, failover_ref: str) -> FailoverRecord | None:
        for item in self._store.values():
            if item.tenant_id == tenant_id and item.failover_ref == failover_ref:
                return item
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[FailoverRecord]:
        items = [f for f in self._store.values() if f.tenant_id == tenant_id]
        return sorted(items, key=lambda f: f.created_at, reverse=True)

    def next_failover_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-FOV")


class InMemoryRecoveryTestRepository(IRecoveryTestRepository):
    _store: dict[str, RecoveryTest] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, test: RecoveryTest) -> None:
        self._store[str(test.id)] = test

    async def list_by_tenant(self, tenant_id: str) -> list[RecoveryTest]:
        items = [t for t in self._store.values() if t.tenant_id == tenant_id]
        return sorted(items, key=lambda t: t.created_at, reverse=True)

    def next_test_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-TST")
