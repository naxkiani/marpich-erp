"""Treasury Analytics application service."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.risk_engine import AlertStatus
from contexts.treasury.domain.events.integration_events import TreasuryAIAnalysisCompletedIntegration
from contexts.treasury.domain.ports.cash_forecast_repositories import ICashForecastPlanRepository
from contexts.treasury.domain.ports.investment_repositories import IInvestmentRepository
from contexts.treasury.domain.ports.liquidity_repositories import (
    ICashPoolRepository,
    IFundingNeedRepository,
)
from contexts.treasury.domain.ports.multi_currency_repositories import (
    IExchangeRateRepository,
    IFxTransactionRepository,
)
from contexts.treasury.domain.ports.repositories import (
    ICashForecastRepository,
    ITreasuryAccountRepository,
)
from contexts.treasury.domain.ports.risk_repositories import IRiskAlertRepository
from contexts.treasury.domain.services.liquidity_engine import compute_funding_needs
from contexts.treasury.domain.services.multi_currency_engine import (
    build_fx_report,
    compute_currency_positions,
)
from contexts.treasury.domain.services.risk_engine import compute_all_exposures
from contexts.treasury.domain.services.treasury_analytics_engine import (
    build_analytics_dashboard,
    build_bank_balance_analysis,
    build_cash_flow_analysis,
    build_cfo_dashboard,
    build_currency_exposure,
    build_executive_dashboard,
    build_forecast_accuracy,
    build_funding_analysis,
    build_liquidity_trends,
    build_treasury_kpis,
    build_working_capital_kpis,
    generate_ai_treasury_assistant,
    generate_treasury_recommendations,
    list_analytics_catalog,
)
from contexts.treasury.domain.services.investment_engine import compute_portfolio_performance
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class TreasuryAnalyticsApplicationService:
    def __init__(
        self,
        accounts: ITreasuryAccountRepository,
        forecasts: ICashForecastRepository,
        forecast_plans: ICashForecastPlanRepository,
        pools: ICashPoolRepository,
        funding_needs: IFundingNeedRepository,
        investments: IInvestmentRepository,
        rates: IExchangeRateRepository,
        fx_transactions: IFxTransactionRepository,
        alerts: IRiskAlertRepository,
    ) -> None:
        self._accounts = accounts
        self._forecasts = forecasts
        self._forecast_plans = forecast_plans
        self._pools = pools
        self._funding_needs = funding_needs
        self._investments = investments
        self._rates = rates
        self._fx_transactions = fx_transactions
        self._alerts = alerts

    async def _context(self, tenant_id: str) -> dict:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        forecasts = await self._forecasts.list_by_tenant(tenant_id)
        forecast_plans = await self._forecast_plans.list_by_tenant(tenant_id)
        pools = await self._pools.list_by_tenant(tenant_id)
        needs = await self._funding_needs.list_by_tenant(tenant_id)
        investments = await self._investments.list_by_tenant(tenant_id)
        rates = await self._rates.list_by_tenant(tenant_id)
        fx_txns = await self._fx_transactions.list_by_tenant(tenant_id)
        alerts = await self._alerts.list_by_tenant(tenant_id)

        rate_dicts = [r.to_dict() for r in rates]
        inv_dicts = [i.to_dict() for i in investments]
        fx_dicts = [t.to_dict() for t in sorted(fx_txns, key=lambda x: x.created_at, reverse=True)]
        forecast_dicts = [f.to_dict() for f in forecasts]
        plan_dicts = [p.to_dict() for p in forecast_plans]
        pool_dicts = [p.to_dict() for p in pools]
        need_dicts = [n.to_dict() for n in needs]

        funding = compute_funding_needs(
            accounts=accounts,
            forecasts=forecast_dicts,
            funding_needs=need_dicts,
        )
        positions = compute_currency_positions(
            accounts=accounts, investments=inv_dicts, rates=rate_dicts
        )
        fx_report = build_fx_report(positions=positions, transactions=fx_dicts, rates=rate_dicts)
        open_alerts = len([a for a in alerts if a.status == AlertStatus.OPEN.value])
        exposures = compute_all_exposures(
            accounts=accounts,
            investments=inv_dicts,
            funding_gap=funding.get("total_funding_gap", 0),
            open_alerts=open_alerts,
        )

        ctx = {
            "accounts": accounts,
            "forecasts": forecast_dicts,
            "forecast_plans": plan_dicts,
            "pools": pool_dicts,
            "funding_needs": need_dicts,
            "investments": inv_dicts,
            "rates": rate_dicts,
            "fx_transactions": fx_dicts,
            "exposures": exposures,
            "open_alerts": open_alerts,
            "fx_net_impact": fx_report["summary"]["net_fx_impact"],
        }
        ctx["recommendations"] = generate_treasury_recommendations(ctx=ctx)["recommendations"]
        return ctx

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_analytics_catalog())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_analytics_dashboard(ctx=ctx))

    async def get_cash_flow_analysis(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            build_cash_flow_analysis(accounts=ctx["accounts"], forecasts=ctx["forecasts"])
        )

    async def get_liquidity_trends(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            build_liquidity_trends(accounts=ctx["accounts"], forecasts=ctx["forecasts"])
        )

    async def get_treasury_kpis(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_treasury_kpis(ctx=ctx))

    async def get_bank_balance_analysis(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_bank_balance_analysis(accounts=ctx["accounts"]))

    async def get_forecast_accuracy(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            build_forecast_accuracy(
                forecast_plans=ctx["forecast_plans"], accounts=ctx["accounts"]
            )
        )

    async def get_investment_performance(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(compute_portfolio_performance(investments=ctx["investments"]))

    async def get_funding_analysis(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            build_funding_analysis(
                accounts=ctx["accounts"],
                forecasts=ctx["forecasts"],
                funding_needs=ctx["funding_needs"],
            )
        )

    async def get_currency_exposure(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            build_currency_exposure(
                accounts=ctx["accounts"],
                investments=ctx["investments"],
                rates=ctx["rates"],
                fx_transactions=ctx["fx_transactions"],
            )
        )

    async def get_working_capital_kpis(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_working_capital_kpis(accounts=ctx["accounts"]))

    async def get_executive_dashboard(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_executive_dashboard(ctx=ctx))

    async def get_cfo_dashboard(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_cfo_dashboard(ctx=ctx))

    async def get_recommendations(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(generate_treasury_recommendations(ctx=ctx))

    async def run_ai_assistant(self, tenant_id: str, *, correlation_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        result = generate_ai_treasury_assistant(ctx=ctx)
        await publish_integration_event(
            TreasuryAIAnalysisCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                capability="ai_treasury_assistant",
                result_summary=result["explanation"],
            )
        )
        return Result.ok(result)

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        return
