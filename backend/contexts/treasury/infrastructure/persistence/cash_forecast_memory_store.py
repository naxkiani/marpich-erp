"""In-memory Enterprise Cash Forecast repositories."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.cash_forecast_engine import (
    CashForecastPlan,
    ForecastSimulation,
)


class InMemoryCashForecastPlanRepository:
    _store: dict[str, CashForecastPlan] = {}

    async def save(self, plan: CashForecastPlan) -> None:
        self._store[str(plan.id)] = plan

    async def find_by_id(self, plan_id: str) -> CashForecastPlan | None:
        return self._store.get(plan_id)

    async def list_by_tenant(self, tenant_id: str) -> list[CashForecastPlan]:
        return [p for p in self._store.values() if p.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}


class InMemoryForecastSimulationRepository:
    _store: dict[str, ForecastSimulation] = {}

    async def save(self, simulation: ForecastSimulation) -> None:
        self._store[str(simulation.id)] = simulation

    async def find_by_id(self, simulation_id: str) -> ForecastSimulation | None:
        return self._store.get(simulation_id)

    async def list_by_tenant(self, tenant_id: str) -> list[ForecastSimulation]:
        return [s for s in self._store.values() if s.tenant_id == tenant_id]

    @classmethod
    def reset(cls) -> None:
        cls._store = {}
