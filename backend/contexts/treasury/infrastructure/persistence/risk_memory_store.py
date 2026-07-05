"""In-memory Enterprise Treasury Risk Platform repositories."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.risk_engine import RiskAlert, StressTestRun, TreasuryRiskLimit


class InMemoryRiskLimitRepository:
    _store: dict[str, TreasuryRiskLimit] = {}

    async def save(self, limit: TreasuryRiskLimit) -> None:
        self._store[str(limit.id)] = limit

    async def find_by_id(self, limit_id: str) -> TreasuryRiskLimit | None:
        return self._store.get(limit_id)

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryRiskLimit]:
        return [l for l in self._store.values() if l.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryRiskAlertRepository:
    _store: dict[str, RiskAlert] = {}

    async def save(self, alert: RiskAlert) -> None:
        self._store[str(alert.id)] = alert

    async def find_by_id(self, alert_id: str) -> RiskAlert | None:
        return self._store.get(alert_id)

    async def list_by_tenant(self, tenant_id: str) -> list[RiskAlert]:
        return [a for a in self._store.values() if a.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryStressTestRepository:
    _store: dict[str, StressTestRun] = {}

    async def save(self, run: StressTestRun) -> None:
        self._store[str(run.id)] = run

    async def list_by_tenant(self, tenant_id: str) -> list[StressTestRun]:
        return [r for r in self._store.values() if r.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
