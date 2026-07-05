"""General Ledger AI application service."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.gl_ai import GLAICapability, GLAIJob, GLAIJobStatus
from contexts.financial_kernel.domain.events.integration_events import (
    GLAIAnalysisCompletedIntegration,
    GLAICFODashboardGeneratedIntegration,
)
from contexts.financial_kernel.domain.ports.gl_ai_repositories import IGLAIJobRepository
from contexts.financial_kernel.domain.ports.repositories import (
    IBudgetRepository,
    IChartOfAccountRepository,
    IJournalRepository,
)
from contexts.financial_kernel.domain.services.gl_ai_engine import (
    analyze_variance,
    build_gl_cfo_dashboard,
    classify_journal,
    closing_assistant,
    detect_anomalies,
    detect_duplicate_journals,
    detect_journal_fraud,
    explain_journal,
    forecast_gl,
    generate_financial_insights,
    list_gl_ai_catalog,
    suggest_accounts,
    suggest_posting_lines,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class GLAIApplicationService:
    CAPABILITIES = [c.value for c in GLAICapability]

    def __init__(
        self,
        jobs: IGLAIJobRepository,
        journals: IJournalRepository,
        accounts: IChartOfAccountRepository,
        budgets: IBudgetRepository,
    ) -> None:
        self._jobs = jobs
        self._journals = journals
        self._accounts = accounts
        self._budgets = budgets

    async def _gl_context(self, tenant_id: str) -> dict:
        journal_entities = await self._journals.list_by_tenant(tenant_id)
        account_entities = await self._accounts.list_by_tenant(tenant_id)
        budget_entities = await self._budgets.list_by_tenant(tenant_id)
        account_types = {a.code: a.account_category.value for a in account_entities}
        account_names = {a.code: a.name for a in account_entities}
        accounts = [{"code": a.code, "name": a.name} for a in account_entities]
        return {
            "journals": [j.to_dict() for j in journal_entities],
            "budgets": [b.to_dict() for b in budget_entities],
            "account_types": account_types,
            "account_names": account_names,
            "accounts": accounts,
        }

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_gl_ai_catalog())

    async def run_analysis(
        self,
        *,
        tenant_id: str,
        capability: str,
        input_data: dict | None = None,
        correlation_id: str = "",
        created_by: str | None = None,
    ) -> Result[dict]:
        if capability not in self.CAPABILITIES:
            return Result.fail("financial_kernel.errors.invalid_gl_ai_capability")
        ctx = await self._gl_context(tenant_id)
        data = input_data or {}
        job = GLAIJob.create(
            tenant_id=tenant_id,
            capability=capability,
            input_data=data,
            correlation_id=correlation_id,
            created_by=created_by,
        )
        try:
            result, confidence = await self._execute_capability(capability, ctx, data)
        except Exception as exc:
            job.status = GLAIJobStatus.FAILED
            await self._jobs.save(job)
            return Result.fail(str(exc))
        job.complete(result, confidence)
        await self._jobs.save(job)
        await publish_integration_event(
            GLAIAnalysisCompletedIntegration(
                tenant_id=TenantId(tenant_id),
                job_id=str(job.id),
                capability=capability,
                confidence=confidence,
                correlation_id=correlation_id,
            )
        )
        return Result.ok(job.to_dict())

    async def _execute_capability(
        self, capability: str, ctx: dict, data: dict
    ) -> tuple[dict, float]:
        journals = ctx["journals"]
        budgets = ctx["budgets"]
        account_types = ctx["account_types"]
        accounts = ctx["accounts"]
        account_names = ctx["account_names"]

        if capability == GLAICapability.POSTING_SUGGESTIONS.value:
            result = suggest_posting_lines(
                description=data.get("description", ""),
                amount=float(data.get("amount", 0)),
                accounts=accounts,
                account_types=account_types,
            )
            return result, 0.78

        if capability == GLAICapability.ACCOUNT_SUGGESTIONS.value:
            amount = data.get("amount")
            result = suggest_accounts(
                description=data.get("description", ""),
                amount=float(amount) if amount is not None else None,
                accounts=accounts,
                account_types=account_types,
            )
            return result, result["suggestions"][0]["confidence"] if result["suggestions"] else 0.5

        if capability == GLAICapability.DUPLICATE_DETECTION.value:
            result = detect_duplicate_journals(journals)
            return result, 0.91 if result["duplicate_count"] else 0.95

        if capability == GLAICapability.FRAUD_DETECTION.value:
            threshold = float(data.get("threshold", 50000))
            result = detect_journal_fraud(journals, threshold=threshold)
            return result, max(0.5, 1.0 - result["fraud_score"])

        if capability == GLAICapability.CLOSING_ASSISTANT.value:
            result = closing_assistant(
                journals=journals,
                account_types=account_types,
                period_status=data.get("period_status", "open"),
            )
            return result, 0.95 if result["ready_to_close"] else 0.7

        if capability == GLAICapability.ANOMALY_DETECTION.value:
            multiplier = float(data.get("std_multiplier", 2.0))
            result = detect_anomalies(journals, std_multiplier=multiplier)
            return result, 0.82

        if capability == GLAICapability.FINANCIAL_INSIGHTS.value:
            result = generate_financial_insights(journals=journals, account_types=account_types)
            return result, 0.88

        if capability == GLAICapability.AUTOMATIC_CLASSIFICATION.value:
            journal_id = data.get("journal_id")
            journal = next((j for j in journals if j.get("id") == journal_id), journals[0] if journals else {})
            result = classify_journal(journal, account_types)
            return result, result["confidence"]

        if capability == GLAICapability.FORECASTING.value:
            months = int(data.get("months", 3))
            result = forecast_gl(journals=journals, account_types=account_types, months=months)
            return result, 0.8

        if capability == GLAICapability.JOURNAL_EXPLANATION.value:
            journal_id = data.get("journal_id")
            journal = next((j for j in journals if j.get("id") == journal_id), None)
            if not journal:
                return {"error": "journal_not_found", "recommendations": []}, 0.0
            result = explain_journal(journal, account_types, account_names)
            return result, 0.95

        if capability == GLAICapability.VARIANCE_ANALYSIS.value:
            result = analyze_variance(
                journals=journals, budgets=budgets, account_types=account_types
            )
            return result, 0.9

        if capability == GLAICapability.AI_CFO_DASHBOARD.value:
            result = build_gl_cfo_dashboard(
                journals=journals,
                budgets=budgets,
                account_types=account_types,
                accounts=accounts,
            )
            return result, 0.92

        return {}, 0.5

    async def get_job(self, tenant_id: str, job_id: str) -> Result[dict]:
        job = await self._jobs.find_by_id(job_id)
        if not job or job.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.gl_ai_job_not_found")
        return Result.ok(job.to_dict())

    async def list_jobs(self, tenant_id: str, capability: str | None = None) -> Result[list[dict]]:
        if capability:
            jobs = await self._jobs.list_by_capability(tenant_id, capability)
        else:
            jobs = await self._jobs.list_by_tenant(tenant_id)
        return Result.ok([j.to_dict() for j in jobs])

    async def get_cfo_dashboard(
        self, *, tenant_id: str, correlation_id: str = "", created_by: str | None = None
    ) -> Result[dict]:
        result = await self.run_analysis(
            tenant_id=tenant_id,
            capability=GLAICapability.AI_CFO_DASHBOARD.value,
            correlation_id=correlation_id,
            created_by=created_by,
        )
        if result.succeeded:
            dashboard = result.unwrap().get("result", {})
            await publish_integration_event(
                GLAICFODashboardGeneratedIntegration(
                    tenant_id=TenantId(tenant_id),
                    job_id=result.unwrap()["id"],
                    correlation_id=correlation_id,
                )
            )
            return Result.ok(dashboard)
        return result

    async def explain_journal(
        self,
        *,
        tenant_id: str,
        journal_id: str,
        correlation_id: str = "",
        created_by: str | None = None,
    ) -> Result[dict]:
        return await self.run_analysis(
            tenant_id=tenant_id,
            capability=GLAICapability.JOURNAL_EXPLANATION.value,
            input_data={"journal_id": journal_id},
            correlation_id=correlation_id,
            created_by=created_by,
        )

    async def list_recommendations(
        self, tenant_id: str, capability: str | None = None
    ) -> Result[list[dict]]:
        jobs_result = await self.list_jobs(tenant_id, capability)
        if not jobs_result.succeeded:
            return jobs_result
        recs: list[dict] = []
        for job in jobs_result.unwrap():
            for rec in job.get("recommendations", []):
                recs.append({**rec, "job_id": job["id"], "capability": job["capability"]})
        recs.sort(key=lambda r: {"high": 0, "medium": 1, "low": 2}.get(r.get("priority", "low"), 3))
        return Result.ok(recs)
