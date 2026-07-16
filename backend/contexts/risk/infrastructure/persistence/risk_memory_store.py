"""In-memory Enterprise Risk Platform persistence."""
from __future__ import annotations

from contexts.risk.domain.aggregates.risk_platform import (
    EnterpriseRiskItem,
    RiskMatrixSnapshot,
    RiskPrediction,
    RiskTenantProfile,
)
from contexts.risk.domain.ports.risk_repositories import (
    IEnterpriseRiskItemRepository,
    IRiskMatrixSnapshotRepository,
    IRiskPredictionRepository,
    IRiskTenantProfileRepository,
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


class InMemoryRiskTenantProfileRepository(IRiskTenantProfileRepository):
    _store: dict[str, RiskTenantProfile] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, profile: RiskTenantProfile) -> None:
        self._store[str(profile.id)] = profile

    async def find_by_tenant(self, tenant_id: str) -> RiskTenantProfile | None:
        for p in self._store.values():
            if p.tenant_id == tenant_id:
                return p
        return None

    def next_profile_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-PRF")


class InMemoryEnterpriseRiskItemRepository(IEnterpriseRiskItemRepository):
    _store: dict[str, EnterpriseRiskItem] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, item: EnterpriseRiskItem) -> None:
        self._store[str(item.id)] = item

    async def find_by_ref(self, tenant_id: str, risk_ref: str) -> EnterpriseRiskItem | None:
        for item in self._store.values():
            if item.tenant_id == tenant_id and item.risk_ref == risk_ref:
                return item
        return None

    async def list_by_tenant(self, tenant_id: str) -> list[EnterpriseRiskItem]:
        items = [i for i in self._store.values() if i.tenant_id == tenant_id]
        return sorted(items, key=lambda i: i.created_at)

    def next_risk_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-RSK")


class InMemoryRiskMatrixSnapshotRepository(IRiskMatrixSnapshotRepository):
    _store: dict[str, RiskMatrixSnapshot] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, snapshot: RiskMatrixSnapshot) -> None:
        self._store[str(snapshot.id)] = snapshot

    async def list_by_tenant(self, tenant_id: str) -> list[RiskMatrixSnapshot]:
        items = [s for s in self._store.values() if s.tenant_id == tenant_id]
        return sorted(items, key=lambda s: s.created_at, reverse=True)

    def next_matrix_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-MTX")


class InMemoryRiskPredictionRepository(IRiskPredictionRepository):
    _store: dict[str, RiskPrediction] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, prediction: RiskPrediction) -> None:
        self._store[str(prediction.id)] = prediction

    async def list_by_tenant(self, tenant_id: str) -> list[RiskPrediction]:
        items = [p for p in self._store.values() if p.tenant_id == tenant_id]
        return sorted(items, key=lambda p: p.created_at, reverse=True)

    def next_prediction_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-PRD")
