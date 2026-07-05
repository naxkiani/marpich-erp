"""Enterprise Cash Forecast application service."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.cash_forecast_engine import (
    CashForecastPlan,
    ForecastPeriodType,
    ForecastScenarioType,
    ForecastSimulation,
)
from contexts.treasury.domain.events.integration_events import TreasuryAIAnalysisCompletedIntegration
from contexts.treasury.domain.ports.cash_forecast_repositories import (
    ICashForecastPlanRepository,
    IForecastSimulationRepository,
)
from contexts.treasury.domain.ports.repositories import ITreasuryAccountRepository
from contexts.treasury.domain.services.cash_forecast_engine import (
    build_forecast_dashboard,
    compute_category_breakdown,
    compute_confidence_score,
    compute_period_forecast,
    generate_ai_forecast,
    list_cash_forecast_catalog,
    list_line_categories,
    run_scenario_simulation,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class CashForecastApplicationService:
    def __init__(
        self,
        accounts: ITreasuryAccountRepository,
        plans: ICashForecastPlanRepository,
        simulations: IForecastSimulationRepository,
    ) -> None:
        self._accounts = accounts
        self._plans = plans
        self._simulations = simulations

    async def _context(self, tenant_id: str) -> dict:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        plans = await self._plans.list_by_tenant(tenant_id)
        return {
            "accounts": accounts,
            "plans": [p.to_dict() for p in plans],
        }

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_cash_forecast_catalog())

    async def list_categories(self) -> Result[list[dict]]:
        return Result.ok(list_line_categories())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            build_forecast_dashboard(accounts=ctx["accounts"], forecast_plans=ctx["plans"])
        )

    async def get_period_forecast(
        self, tenant_id: str, period: str, periods: int, scenario: str = "base"
    ) -> Result[dict]:
        try:
            ForecastPeriodType(period)
            ForecastScenarioType(scenario)
        except ValueError:
            return Result.fail("treasury.errors.invalid_forecast_period_or_scenario")
        ctx = await self._context(tenant_id)
        return Result.ok(
            compute_period_forecast(
                accounts=ctx["accounts"],
                forecast_plans=ctx["plans"],
                period=period,
                periods=periods,
                scenario=scenario,
            )
        )

    async def get_category_breakdown(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(compute_category_breakdown(forecast_plans=ctx["plans"]))

    async def create_plan(
        self,
        *,
        tenant_id: str,
        name: str,
        period_type: str,
        period_start: str,
        period_end: str,
        scenario: str,
        currency: str,
        opening_balance: float | None = None,
        projected_lines: list[dict],
    ) -> Result[dict]:
        try:
            ForecastPeriodType(period_type)
            ForecastScenarioType(scenario)
        except ValueError:
            return Result.fail("treasury.errors.invalid_forecast_period_or_scenario")

        if opening_balance is None:
            accounts = await self._accounts.list_by_tenant(tenant_id)
            opening_balance = round(
                sum(a.balance for a in accounts if a.is_active and a.currency == currency), 2
            )

        confidence = compute_confidence_score(
            lines=projected_lines, scenario=scenario, has_historical=True
        )
        plan = CashForecastPlan.create(
            tenant_id=tenant_id,
            name=name,
            period_type=period_type,
            period_start=period_start,
            period_end=period_end,
            scenario=scenario,
            currency=currency,
            opening_balance=opening_balance,
            projected_lines=projected_lines,
            confidence_score=confidence,
        )
        await self._plans.save(plan)
        return Result.ok(plan.to_dict())

    async def list_plans(self, tenant_id: str) -> Result[list[dict]]:
        plans = await self._plans.list_by_tenant(tenant_id)
        return Result.ok(
            [p.to_dict() for p in sorted(plans, key=lambda x: x.created_at, reverse=True)]
        )

    async def get_plan(self, plan_id: str) -> Result[dict]:
        plan = await self._plans.find_by_id(plan_id)
        if not plan:
            return Result.fail("treasury.errors.forecast_plan_not_found")
        return Result.ok(plan.to_dict())

    async def run_ai_forecast(
        self,
        *,
        tenant_id: str,
        horizon_days: int = 90,
        correlation_id: str = "",
    ) -> Result[dict]:
        ctx = await self._context(tenant_id)
        result = generate_ai_forecast(
            accounts=ctx["accounts"],
            forecast_plans=ctx["plans"],
            horizon_days=horizon_days,
        )
        await publish_integration_event(
            TreasuryAIAnalysisCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id or f"cash-forecast-ai-{tenant_id}",
                capability="ai_forecast",
                result_summary=result.get("explanation", ""),
            )
        )
        return Result.ok(result)

    async def run_scenario_simulation(
        self,
        *,
        tenant_id: str,
        plan_id: str,
        name: str | None = None,
        correlation_id: str = "",
    ) -> Result[dict]:
        plan = await self._plans.find_by_id(plan_id)
        if not plan or plan.tenant_id != tenant_id:
            return Result.fail("treasury.errors.forecast_plan_not_found")

        scenarios = run_scenario_simulation(base_plan=plan.to_dict())
        simulation = ForecastSimulation.create(
            tenant_id=tenant_id,
            name=name or f"Scenario simulation — {plan.name}",
            base_forecast_id=str(plan.id),
            scenarios=scenarios,
        )
        await self._simulations.save(simulation)

        await publish_integration_event(
            TreasuryAIAnalysisCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id or f"cash-forecast-sim-{plan_id}",
                capability="scenario_simulation",
                result_summary=f"Simulated {len(scenarios)} scenarios for {plan.name}",
            )
        )
        return Result.ok(simulation.to_dict())

    async def list_simulations(self, tenant_id: str) -> Result[list[dict]]:
        sims = await self._simulations.list_by_tenant(tenant_id)
        return Result.ok([s.to_dict() for s in sims])

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        if await self._plans.list_by_tenant(tenant_id):
            return
        accounts = await self._accounts.list_by_tenant(tenant_id)
        if not accounts:
            return
        opening = round(sum(a.balance for a in accounts if a.is_active), 2)
        plan = CashForecastPlan.create(
            tenant_id=tenant_id,
            name="Default Enterprise Cash Forecast",
            period_type=ForecastPeriodType.MONTHLY.value,
            period_start="2025-07-01",
            period_end="2025-12-31",
            scenario=ForecastScenarioType.BASE.value,
            currency="USD",
            opening_balance=opening,
            projected_lines=[
                {"date": "2025-07-15", "label": "Payroll", "category": "payroll", "outflow": 12000},
                {"date": "2025-07-20", "label": "Hospital collections", "category": "hospital_revenue", "inflow": 25000},
                {"date": "2025-07-25", "label": "Tuition intake", "category": "student_tuition", "inflow": 8000},
                {"date": "2025-08-01", "label": "Tax remittance", "category": "tax", "outflow": 4500},
                {"date": "2025-08-05", "label": "Loan payment", "category": "loan_payments", "outflow": 3000},
                {"date": "2025-08-10", "label": "Construction draw", "category": "construction_expenses", "outflow": 15000},
                {"date": "2025-08-15", "label": "Inventory restock", "category": "inventory_purchases", "outflow": 6000},
                {"date": "2025-08-20", "label": "AR collections", "category": "incoming_payments", "inflow": 18000},
            ],
            confidence_score=0.82,
        )
        await self._plans.save(plan)
