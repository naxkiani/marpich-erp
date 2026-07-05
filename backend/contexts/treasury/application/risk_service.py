"""Enterprise Treasury Risk Platform application service."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.risk_engine import (
    AlertStatus,
    LimitUnit,
    RiskAlert,
    RiskType,
    StressTestRun,
    TreasuryRiskLimit,
)
from contexts.treasury.domain.events.integration_events import (
    TreasuryAIAnalysisCompletedIntegration,
    TreasuryRiskBreachIntegration,
)
from contexts.treasury.domain.ports.investment_repositories import IInvestmentRepository
from contexts.treasury.domain.ports.liquidity_repositories import IFundingNeedRepository
from contexts.treasury.domain.ports.repositories import ITreasuryAccountRepository
from contexts.treasury.domain.ports.risk_repositories import (
    IRiskAlertRepository,
    IRiskLimitRepository,
    IStressTestRepository,
)
from contexts.treasury.domain.services.liquidity_engine import compute_funding_needs
from contexts.treasury.domain.services.risk_engine import (
    build_risk_dashboard,
    check_limit_breaches,
    compute_all_exposures,
    generate_ai_risk_scoring,
    list_risk_catalog,
    list_stress_scenarios,
    run_stress_test,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class RiskApplicationService:
    def __init__(
        self,
        accounts: ITreasuryAccountRepository,
        investments: IInvestmentRepository,
        funding_needs: IFundingNeedRepository,
        limits: IRiskLimitRepository,
        alerts: IRiskAlertRepository,
        stress_tests: IStressTestRepository,
    ) -> None:
        self._accounts = accounts
        self._investments = investments
        self._funding_needs = funding_needs
        self._limits = limits
        self._alerts = alerts
        self._stress_tests = stress_tests

    async def _context(self, tenant_id: str) -> dict:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        investments = await self._investments.list_by_tenant(tenant_id)
        needs = await self._funding_needs.list_by_tenant(tenant_id)
        limits = await self._limits.list_by_tenant(tenant_id)
        alerts = await self._alerts.list_by_tenant(tenant_id)
        stress_runs = await self._stress_tests.list_by_tenant(tenant_id)

        funding = compute_funding_needs(
            accounts=accounts,
            forecasts=[],
            funding_needs=[n.to_dict() for n in needs],
        )
        funding_gap = funding.get("total_gap", 0)
        open_alerts = [a for a in alerts if a.status == AlertStatus.OPEN.value]

        exposures = compute_all_exposures(
            accounts=accounts,
            investments=[i.to_dict() for i in investments],
            funding_gap=funding_gap,
            open_alerts=len(open_alerts),
        )
        return {
            "accounts": accounts,
            "investments": investments,
            "limits": [l.to_dict() for l in limits],
            "alerts": [a.to_dict() for a in alerts],
            "stress_runs": [s.to_dict() for s in sorted(stress_runs, key=lambda x: x.run_at, reverse=True)],
            "exposures": exposures,
            "funding_gap": funding_gap,
        }

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_risk_catalog())

    async def list_scenarios(self) -> Result[list[dict]]:
        return Result.ok(list_stress_scenarios())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(
            build_risk_dashboard(
                exposures=ctx["exposures"],
                limits=ctx["limits"],
                alerts=ctx["alerts"],
                stress_runs=ctx["stress_runs"],
            )
        )

    async def get_exposures(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        breaches = check_limit_breaches(exposures=ctx["exposures"], limits=ctx["limits"])
        return Result.ok({"exposures": ctx["exposures"], "breaches": breaches})

    async def list_limits(self, tenant_id: str) -> Result[list[dict]]:
        limits = await self._limits.list_by_tenant(tenant_id)
        return Result.ok([l.to_dict() for l in limits])

    async def create_limit(
        self,
        *,
        tenant_id: str,
        risk_type: str,
        name: str,
        threshold_value: float,
        threshold_unit: str,
        currency: str = "USD",
        description: str = "",
    ) -> Result[dict]:
        try:
            RiskType(risk_type)
            LimitUnit(threshold_unit)
        except ValueError:
            return Result.fail("treasury.errors.invalid_risk_limit")

        limit = TreasuryRiskLimit.create(
            tenant_id=tenant_id,
            risk_type=risk_type,
            name=name,
            threshold_value=threshold_value,
            threshold_unit=threshold_unit,
            currency=currency,
            description=description,
        )
        await self._limits.save(limit)
        await self._evaluate_and_alert(tenant_id)
        return Result.ok(limit.to_dict())

    async def update_limit(
        self, limit_id: str, *, tenant_id: str, threshold_value: float
    ) -> Result[dict]:
        limit = await self._limits.find_by_id(limit_id)
        if not limit or limit.tenant_id != tenant_id:
            return Result.fail("treasury.errors.risk_limit_not_found")
        limit.update_threshold(threshold_value)
        await self._limits.save(limit)
        await self._evaluate_and_alert(tenant_id)
        return Result.ok(limit.to_dict())

    async def list_alerts(self, tenant_id: str, status: str | None = None) -> Result[list[dict]]:
        alerts = await self._alerts.list_by_tenant(tenant_id)
        if status:
            alerts = [a for a in alerts if a.status == status]
        return Result.ok(
            [a.to_dict() for a in sorted(alerts, key=lambda x: x.created_at, reverse=True)]
        )

    async def acknowledge_alert(
        self, alert_id: str, *, tenant_id: str, actor_id: str
    ) -> Result[dict]:
        alert = await self._alerts.find_by_id(alert_id)
        if not alert or alert.tenant_id != tenant_id:
            return Result.fail("treasury.errors.risk_alert_not_found")
        alert.acknowledge(actor_id)
        await self._alerts.save(alert)
        return Result.ok(alert.to_dict())

    async def resolve_alert(self, alert_id: str, *, tenant_id: str) -> Result[dict]:
        alert = await self._alerts.find_by_id(alert_id)
        if not alert or alert.tenant_id != tenant_id:
            return Result.fail("treasury.errors.risk_alert_not_found")
        alert.resolve()
        await self._alerts.save(alert)
        return Result.ok(alert.to_dict())

    async def run_stress_test_scenario(
        self, tenant_id: str, scenario: str
    ) -> Result[dict]:
        ctx = await self._context(tenant_id)
        try:
            result = run_stress_test(
                scenario=scenario,
                exposures=ctx["exposures"],
                accounts=ctx["accounts"],
                investments=[i.to_dict() for i in ctx["investments"]],
            )
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")

        run = StressTestRun.create(
            tenant_id=tenant_id,
            scenario=scenario,
            parameters=result["parameters"],
            results=result["results"],
            impact_score=result["impact_score"],
        )
        await self._stress_tests.save(run)
        return Result.ok({**result, "run_id": str(run.id)})

    async def list_stress_tests(self, tenant_id: str) -> Result[list[dict]]:
        runs = await self._stress_tests.list_by_tenant(tenant_id)
        return Result.ok(
            [r.to_dict() for r in sorted(runs, key=lambda x: x.run_at, reverse=True)]
        )

    async def run_ai_risk_scoring(
        self, tenant_id: str, *, correlation_id: str = ""
    ) -> Result[dict]:
        ctx = await self._context(tenant_id)
        analysis = generate_ai_risk_scoring(
            exposures=ctx["exposures"],
            limits=ctx["limits"],
            alerts=ctx["alerts"],
        )
        await publish_integration_event(
            TreasuryAIAnalysisCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id or f"risk-ai-{tenant_id}",
                capability="ai_risk_scoring",
                result_summary=f"Composite score {analysis['composite_score']['score']} ({analysis['composite_score']['level']})",
            )
        )
        return Result.ok(analysis)

    async def _evaluate_and_alert(self, tenant_id: str) -> None:
        ctx = await self._context(tenant_id)
        breaches = check_limit_breaches(exposures=ctx["exposures"], limits=ctx["limits"])
        existing_open = {
            (a.risk_type, a.limit_id)
            for a in await self._alerts.list_by_tenant(tenant_id)
            if a.status == AlertStatus.OPEN.value
        }

        for breach in breaches:
            key = (breach["risk_type"], breach["limit_id"])
            if key in existing_open:
                continue
            alert = RiskAlert.create(
                tenant_id=tenant_id,
                risk_type=breach["risk_type"],
                limit_id=breach["limit_id"],
                exposure_value=breach["exposure_value"],
                limit_value=breach["limit_value"],
                severity=breach["severity"],
                message=breach["message"],
            )
            await self._alerts.save(alert)
            await publish_integration_event(
                TreasuryRiskBreachIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=f"risk-breach-{alert.id}",
                    alert_id=str(alert.id),
                    risk_type=breach["risk_type"],
                    exposure_value=breach["exposure_value"],
                    limit_value=breach["limit_value"],
                    severity=breach["severity"],
                )
            )

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        tenant_id = envelope["tenant_id"]
        if await self._limits.list_by_tenant(tenant_id):
            return

        defaults = [
            (RiskType.LIQUIDITY_RISK.value, "Minimum Liquidity Ratio", 25.0, LimitUnit.PERCENT.value),
            (RiskType.INTEREST_RATE_RISK.value, "Max Rate Shock Impact", 100000.0, LimitUnit.AMOUNT.value),
            (RiskType.FOREIGN_EXCHANGE_RISK.value, "Max Non-USD Exposure", 30.0, LimitUnit.PERCENT.value),
            (RiskType.COUNTERPARTY_RISK.value, "Max Bank Concentration", 40.0, LimitUnit.PERCENT.value),
            (RiskType.OPERATIONAL_RISK.value, "Max Operational Score", 25.0, LimitUnit.COUNT.value),
        ]
        for risk_type, name, threshold, unit in defaults:
            limit = TreasuryRiskLimit.create(
                tenant_id=tenant_id,
                risk_type=risk_type,
                name=name,
                threshold_value=threshold,
                threshold_unit=unit,
            )
            await self._limits.save(limit)

        await self._evaluate_and_alert(tenant_id)
