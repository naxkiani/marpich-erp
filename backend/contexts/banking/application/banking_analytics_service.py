"""Banking Analytics Platform application service."""
from __future__ import annotations

from contexts.banking.domain.aggregates.banking_analytics_engine import (
    AnalyticsCapability,
    BankingAnalyticsJob,
)
from contexts.banking.domain.events.banking_analytics_integration_events import (
    BankingAnalyticsForecastCompletedIntegration,
    BankingAnalyticsInsightRaisedIntegration,
    BankingAnalyticsRecommendationGeneratedIntegration,
    BankingAnalyticsReportGeneratedIntegration,
)
from contexts.banking.domain.ports.banking_analytics_repositories import IBankingAnalyticsJobRepository
from contexts.banking.domain.ports.banking_security_repositories import ITransactionMonitorRepository
from contexts.banking.domain.ports.branch_banking_repositories import (
    IBranchKPIRepository,
    IBranchOfficeRepository,
)
from contexts.banking.domain.ports.customer_account_repositories import (
    IAccountRepository,
    ICustomerRepository,
)
from contexts.banking.domain.ports.deposit_management_repositories import (
    IDepositAccrualRepository,
    IDepositProfileRepository,
    IDepositTransactionRepository,
)
from contexts.banking.domain.ports.loan_management_repositories import (
    ILoanCreditRiskRepository,
    ILoanInstallmentRepository,
    ILoanProfileRepository,
    ILoanTransactionRepository,
)
from contexts.banking.domain.ports.payment_platform_repositories import (
    IPaymentFraudRepository,
    IPaymentTransferRepository,
)
from contexts.banking.domain.services.banking_analytics_engine import (
    CAPABILITY_BUILDERS,
    CAPABILITY_POLICY_KEY,
    build_analytics_dashboard,
    build_branch_performance,
    build_customer_insights,
    build_customer_segmentation,
    build_delinquency_analysis,
    build_deposit_trends,
    build_executive_dashboard,
    build_forecasting,
    build_fraud_detection,
    build_liquidity_kpis,
    build_loan_portfolio,
    build_portfolio_quality,
    build_revenue_analysis,
    build_risk_indicators,
    generate_ai_banking_assistant,
    generate_banking_recommendations,
    list_analytics_catalog,
    list_analytics_policy_keys,
)
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class BankingAnalyticsPlatformApplicationService:
    def __init__(
        self,
        jobs: IBankingAnalyticsJobRepository,
        customers: ICustomerRepository,
        accounts: IAccountRepository,
        deposits: IDepositProfileRepository,
        deposit_transactions: IDepositTransactionRepository,
        interest_accruals: IDepositAccrualRepository,
        loans: ILoanProfileRepository,
        installments: ILoanInstallmentRepository,
        loan_transactions: ILoanTransactionRepository,
        credit_risks: ILoanCreditRiskRepository,
        transfers: IPaymentTransferRepository,
        fraud_checks: IPaymentFraudRepository,
        branch_offices: IBranchOfficeRepository,
        branch_kpis: IBranchKPIRepository,
        security_alerts: ITransactionMonitorRepository,
        policy: IPolicyEvaluator,
    ) -> None:
        self._jobs = jobs
        self._customers = customers
        self._accounts = accounts
        self._deposits = deposits
        self._deposit_transactions = deposit_transactions
        self._interest_accruals = interest_accruals
        self._loans = loans
        self._installments = installments
        self._loan_transactions = loan_transactions
        self._credit_risks = credit_risks
        self._transfers = transfers
        self._fraud_checks = fraud_checks
        self._branch_offices = branch_offices
        self._branch_kpis = branch_kpis
        self._security_alerts = security_alerts
        self._policy = policy

    async def _policy_params(self, tenant_id: str, policy_key: str) -> dict:
        result = await self._policy.evaluate(
            tenant_id=tenant_id, domain="bank", policy_key=policy_key, facts={}
        )
        return result.parameters

    async def _context(self, tenant_id: str) -> dict:
        policy_params = {
            "liquidity": await self._policy_params(tenant_id, "analytics.liquidity.threshold"),
            "delinquency": await self._policy_params(tenant_id, "analytics.delinquency.warning"),
            "fraud": await self._policy_params(tenant_id, "analytics.fraud.alert_threshold"),
            "forecast": await self._policy_params(tenant_id, "analytics.forecast.horizon"),
            "segmentation": await self._policy_params(tenant_id, "analytics.segmentation.rules"),
            "revenue": await self._policy_params(tenant_id, "analytics.revenue.target"),
            "risk": await self._policy_params(tenant_id, "analytics.risk.indicator_threshold"),
            "portfolio": await self._policy_params(tenant_id, "analytics.portfolio.quality_minimum"),
        }
        ctx = {
            "customers": [c.to_dict() for c in await self._customers.list_by_tenant(tenant_id)],
            "accounts": [a.to_dict() for a in await self._accounts.list_by_tenant(tenant_id)],
            "deposits": [d.to_dict() for d in await self._deposits.list_by_tenant(tenant_id)],
            "deposit_transactions": [t.to_dict() for t in await self._deposit_transactions.list_by_tenant(tenant_id)],
            "interest_accruals": [a.to_dict() for a in await self._interest_accruals.list_by_tenant(tenant_id)],
            "loans": [l.to_dict() for l in await self._loans.list_by_tenant(tenant_id)],
            "loan_installments": [],
            "loan_transactions": [t.to_dict() for t in await self._loan_transactions.list_by_tenant(tenant_id)],
            "credit_risks": [r.to_dict() for r in await self._credit_risks.list_by_tenant(tenant_id)],
            "transfers": [t.to_dict() for t in await self._transfers.list_by_tenant(tenant_id)],
            "fraud_checks": [f.to_dict() for f in await self._fraud_checks.list_by_tenant(tenant_id)],
            "branch_offices": [o.to_dict() for o in await self._branch_offices.list_by_tenant(tenant_id)],
            "branch_kpis": [k.to_dict() for k in await self._branch_kpis.list_by_tenant(tenant_id)],
            "security_alerts": [a.to_dict() for a in await self._security_alerts.list_by_tenant(tenant_id)],
            "policy_params": policy_params,
        }
        for loan in await self._loans.list_by_tenant(tenant_id):
            for inst in await self._installments.list_by_loan(str(loan.id)):
                ctx["loan_installments"].append(inst.to_dict())
        ctx["recommendations"] = generate_banking_recommendations(
            ctx=ctx, policy_params=policy_params
        )["recommendations"]
        return ctx

    async def handle_tenant_provisioned(self, event: dict) -> None:
        pass

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_analytics_catalog())

    async def list_policy_keys(self) -> Result[list[dict]]:
        return Result.ok(list_analytics_policy_keys())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_analytics_dashboard(ctx=ctx, policy_params=ctx["policy_params"]))

    async def get_liquidity_kpis(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_liquidity_kpis(ctx=ctx, policy_params=ctx["policy_params"]["liquidity"]))

    async def get_deposit_trends(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_deposit_trends(ctx=ctx))

    async def get_loan_portfolio(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_loan_portfolio(ctx=ctx))

    async def get_customer_segmentation(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_customer_segmentation(ctx=ctx, policy_params=ctx["policy_params"]["segmentation"]))

    async def get_branch_performance(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_branch_performance(ctx=ctx))

    async def get_revenue_analysis(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_revenue_analysis(ctx=ctx, policy_params=ctx["policy_params"]["revenue"]))

    async def get_risk_indicators(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_risk_indicators(ctx=ctx, policy_params=ctx["policy_params"]["risk"]))

    async def get_portfolio_quality(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_portfolio_quality(ctx=ctx, policy_params=ctx["policy_params"]["portfolio"]))

    async def get_delinquency_analysis(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_delinquency_analysis(ctx=ctx, policy_params=ctx["policy_params"]["delinquency"]))

    async def get_forecasting(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        result = build_forecasting(ctx=ctx, policy_params=ctx["policy_params"]["forecast"])
        await publish_integration_event(
            BankingAnalyticsForecastCompletedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"forecast-{tenant_id}",
                horizon_days=result["horizon_days"],
                forecast_type="deposit_transfer",
            )
        )
        return Result.ok(result)

    async def get_fraud_detection(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_fraud_detection(ctx=ctx, policy_params=ctx["policy_params"]["fraud"]))

    async def get_customer_insights(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_customer_insights(ctx=ctx))

    async def get_executive_dashboard(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        return Result.ok(build_executive_dashboard(ctx=ctx, policy_params=ctx["policy_params"]))

    async def get_recommendations(self, tenant_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        recs = generate_banking_recommendations(ctx=ctx, policy_params=ctx["policy_params"])
        await publish_integration_event(
            BankingAnalyticsRecommendationGeneratedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"recs-{tenant_id}",
                recommendation_count=recs["recommendation_count"],
                capability="recommendations",
            )
        )
        return Result.ok(recs)

    async def run_ai_assistant(self, tenant_id: str, *, correlation_id: str) -> Result[dict]:
        ctx = await self._context(tenant_id)
        result = generate_ai_banking_assistant(ctx=ctx, policy_params=ctx["policy_params"])
        if result["insights"]:
            await publish_integration_event(
                BankingAnalyticsInsightRaisedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=correlation_id,
                    insight_type="banking_ai",
                    severity="info",
                )
            )
        return Result.ok(result)

    async def run_analysis(
        self,
        tenant_id: str,
        capability: str,
        *,
        correlation_id: str,
        input_data: dict | None = None,
        created_by: str | None = None,
    ) -> Result[dict]:
        if capability not in CAPABILITY_BUILDERS:
            return Result.fail("banking.errors.invalid_analytics_capability")
        ctx = await self._context(tenant_id)
        job = BankingAnalyticsJob.create(
            tenant_id=tenant_id,
            capability=capability,
            input_data=input_data or {},
            correlation_id=correlation_id,
            created_by=created_by,
        )
        builder = CAPABILITY_BUILDERS[capability]
        if capability in {
            AnalyticsCapability.EXECUTIVE_DASHBOARD.value,
            AnalyticsCapability.AI_BANKING_ASSISTANT.value,
        }:
            params = ctx["policy_params"]
        else:
            policy_key = CAPABILITY_POLICY_KEY.get(capability, "liquidity")
            params = ctx["policy_params"].get(policy_key, ctx["policy_params"]["liquidity"])
        result = builder(ctx, params)
        confidence = float(result.get("confidence", 0.8))
        recommendations = result.get("recommendations") or result.get("top_recommendations", [])
        job.complete(result=result, confidence=confidence, recommendations=recommendations if isinstance(recommendations, list) else [])
        await self._jobs.save(job)
        await publish_integration_event(
            BankingAnalyticsReportGeneratedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                report_type=capability,
                capability=capability,
            )
        )
        return Result.ok(job.to_dict())

    async def list_jobs(self, tenant_id: str, capability: str | None = None) -> Result[list[dict]]:
        jobs = await self._jobs.list_by_tenant(tenant_id, capability)
        return Result.ok([j.to_dict() for j in jobs])

    async def get_job(self, tenant_id: str, job_id: str) -> Result[dict]:
        job = await self._jobs.find_by_id(job_id)
        if not job or job.tenant_id != tenant_id:
            return Result.fail("banking.errors.analytics_job_not_found")
        return Result.ok(job.to_dict())
