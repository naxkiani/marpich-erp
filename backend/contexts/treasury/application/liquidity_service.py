"""Enterprise Liquidity Engine application service."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.liquidity_engine import CashPool, FundingNeed, LiquiditySnapshot
from contexts.treasury.domain.events.integration_events import TreasuryAIAnalysisCompletedIntegration
from contexts.treasury.domain.ports.liquidity_repositories import (
    ICashPoolRepository,
    IFundingNeedRepository,
    ILiquiditySnapshotRepository,
)
from contexts.treasury.domain.ports.repositories import ICashForecastRepository, ITreasuryAccountRepository
from contexts.treasury.domain.services.liquidity_engine import (
    build_liquidity_dashboard,
    compute_cash_position,
    compute_cash_pools_view,
    compute_funding_needs,
    compute_liquidity_gap,
    compute_period_liquidity,
    compute_rolling_forecast,
    compute_working_capital,
    list_liquidity_catalog,
    optimization_recommendations,
    predict_liquidity_ai,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class LiquidityApplicationService:
    def __init__(
        self,
        accounts: ITreasuryAccountRepository,
        forecasts: ICashForecastRepository,
        pools: ICashPoolRepository,
        snapshots: ILiquiditySnapshotRepository,
        funding_needs: IFundingNeedRepository,
    ) -> None:
        self._accounts = accounts
        self._forecasts = forecasts
        self._pools = pools
        self._snapshots = snapshots
        self._funding_needs = funding_needs

    async def _context(self, tenant_id: str) -> dict:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        forecasts = await self._forecasts.list_by_tenant(tenant_id)
        pools = await self._pools.list_by_tenant(tenant_id)
        needs = await self._funding_needs.list_by_tenant(tenant_id)
        return {
            "accounts": accounts,
            "forecasts": [f.to_dict() for f in forecasts],
            "pools": [p.to_dict() for p in pools],
            "funding_needs": [n.to_dict() for n in needs],
        }

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_liquidity_catalog())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            build_liquidity_dashboard(
                accounts=ctx["accounts"],
                forecasts=ctx["forecasts"],
                pools=ctx["pools"],
                funding_needs=ctx["funding_needs"],
            )
        )

    async def get_cash_position(self, tenant_id: str) -> Result[dict]:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        return Result.ok(compute_cash_position(accounts=accounts))

    async def get_daily_liquidity(self, tenant_id: str, days: int = 30) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            compute_period_liquidity(
                accounts=ctx["accounts"],
                forecasts=ctx["forecasts"],
                period="daily",
                periods=days,
            )
        )

    async def get_weekly_liquidity(self, tenant_id: str, weeks: int = 12) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            compute_period_liquidity(
                accounts=ctx["accounts"],
                forecasts=ctx["forecasts"],
                period="weekly",
                periods=weeks,
            )
        )

    async def get_monthly_liquidity(self, tenant_id: str, months: int = 12) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            compute_period_liquidity(
                accounts=ctx["accounts"],
                forecasts=ctx["forecasts"],
                period="monthly",
                periods=months,
            )
        )

    async def get_rolling_forecast(self, tenant_id: str, horizon_weeks: int = 13) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            compute_rolling_forecast(
                accounts=ctx["accounts"],
                forecasts=ctx["forecasts"],
                horizon_weeks=horizon_weeks,
            )
        )

    async def list_cash_pools(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(compute_cash_pools_view(pools=ctx["pools"], accounts=ctx["accounts"]))

    async def create_cash_pool(
        self,
        *,
        tenant_id: str,
        code: str,
        name: str,
        currency: str = "USD",
        target_balance: float = 0.0,
        minimum_balance: float = 0.0,
        member_account_ids: list[str] | None = None,
    ) -> Result[dict]:
        if await self._pools.find_by_code(tenant_id, code):
            return Result.fail("treasury.errors.pool_exists")
        pool = CashPool.create(
            tenant_id=tenant_id,
            code=code,
            name=name,
            currency=currency,
            target_balance=target_balance,
            minimum_balance=minimum_balance,
            member_account_ids=member_account_ids,
        )
        await self._pools.save(pool)
        return Result.ok(pool.to_dict())

    async def get_funding_needs(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            compute_funding_needs(
                accounts=ctx["accounts"],
                forecasts=ctx["forecasts"],
                funding_needs=ctx["funding_needs"],
            )
        )

    async def create_funding_need(
        self,
        *,
        tenant_id: str,
        label: str,
        currency: str,
        required_amount: float,
        available_amount: float,
        due_date: str,
    ) -> Result[dict]:
        need = FundingNeed.create(
            tenant_id=tenant_id,
            label=label,
            currency=currency,
            required_amount=required_amount,
            available_amount=available_amount,
            due_date=due_date,
        )
        await self._funding_needs.save(need)
        return Result.ok(need.to_dict())

    async def get_liquidity_gap(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            compute_liquidity_gap(accounts=ctx["accounts"], forecasts=ctx["forecasts"])
        )

    async def get_working_capital(self, tenant_id: str) -> Result[dict]:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        return Result.ok(compute_working_capital(accounts=accounts))

    async def predict_liquidity(
        self,
        *,
        tenant_id: str,
        horizon_days: int = 30,
        correlation_id: str = "",
    ) -> Result[dict]:
        ctx = await self._context(tenant_id)
        result = predict_liquidity_ai(
            accounts=ctx["accounts"],
            forecasts=ctx["forecasts"],
            horizon_days=horizon_days,
        )
        await publish_integration_event(
            TreasuryAIAnalysisCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id or f"liquidity-ai-{tenant_id}",
                capability="ai_liquidity_prediction",
                result_summary=result.get("explanation", ""),
            )
        )
        return Result.ok(result)

    async def get_optimization_recommendations(
        self,
        *,
        tenant_id: str,
        correlation_id: str = "",
    ) -> Result[dict]:
        ctx = await self._context(tenant_id)
        result = optimization_recommendations(
            accounts=ctx["accounts"],
            forecasts=ctx["forecasts"],
            pools=ctx["pools"],
        )
        await publish_integration_event(
            TreasuryAIAnalysisCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id or f"liquidity-opt-{tenant_id}",
                capability="optimization_recommendations",
                result_summary=f"{result['recommendation_count']} recommendations generated",
            )
        )
        return Result.ok(result)

    async def save_snapshot(self, tenant_id: str, period_type: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        period_data = compute_period_liquidity(
            accounts=ctx["accounts"],
            forecasts=ctx["forecasts"],
            period=period_type,
            periods=30 if period_type == "daily" else 12,
        )
        gap = compute_liquidity_gap(accounts=ctx["accounts"], forecasts=ctx["forecasts"])
        wc = compute_working_capital(accounts=ctx["accounts"])
        snapshot = LiquiditySnapshot.create(
            tenant_id=tenant_id,
            period_type=period_type,
            as_of_date=period_data["lines"][-1]["period"] if period_data["lines"] else "",
            currency="USD",
            opening_balance=period_data["opening_balance"],
            closing_balance=period_data["closing_balance"],
            total_inflow=period_data["total_inflow"],
            total_outflow=period_data["total_outflow"],
            liquidity_gap=gap["liquidity_gap"],
            working_capital=wc["working_capital"],
            lines=period_data["lines"],
        )
        await self._snapshots.save(snapshot)
        return Result.ok(snapshot.to_dict())

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        if await self._pools.list_by_tenant(tenant_id):
            return
        accounts = await self._accounts.list_by_tenant(tenant_id)
        if not accounts:
            return
        member_ids = [str(a.id) for a in accounts if a.account_type in {"cash", "bank", "petty_cash"}]
        pool = CashPool.create(
            tenant_id=tenant_id,
            code="OPERATING-POOL",
            name="Operating Cash Pool",
            target_balance=50000.0,
            minimum_balance=10000.0,
            member_account_ids=member_ids[:3],
        )
        await self._pools.save(pool)
