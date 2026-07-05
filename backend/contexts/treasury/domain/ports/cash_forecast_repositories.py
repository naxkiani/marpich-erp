"""Enterprise Cash Forecast repository ports."""
from __future__ import annotations

from typing import Protocol

from contexts.treasury.domain.aggregates.cash_forecast_engine import (
    CashForecastPlan,
    ForecastSimulation,
)


class ICashForecastPlanRepository(Protocol):
    async def save(self, plan: CashForecastPlan) -> None: ...
    async def find_by_id(self, plan_id: str) -> CashForecastPlan | None: ...
    async def list_by_tenant(self, tenant_id: str) -> list[CashForecastPlan]: ...


class IForecastSimulationRepository(Protocol):
    async def save(self, simulation: ForecastSimulation) -> None: ...
    async def find_by_id(self, simulation_id: str) -> ForecastSimulation | None: ...
    async def list_by_tenant(self, tenant_id: str) -> list[ForecastSimulation]: ...
