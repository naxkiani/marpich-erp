"""Enterprise Financial AI application service."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.financial_ai import (
    AICapability,
    AIJobStatus,
    FinancialAIChatSession,
    FinancialAIJob,
)
from contexts.financial_kernel.domain.events.integration_events import (
    FinancialAIAnalysisCompletedIntegration,
    FinancialAIChatCompletedIntegration,
    FinancialAIDashboardGeneratedIntegration,
)
from contexts.financial_kernel.domain.ports.financial_ai_repositories import (
    IFinancialAIChatRepository,
    IFinancialAIJobRepository,
)
from contexts.financial_kernel.domain.ports.payment_repositories import IPaymentRepository
from contexts.financial_kernel.domain.ports.repositories import (
    IBudgetRepository,
    IChartOfAccountRepository,
    IJournalRepository,
)
from contexts.financial_kernel.domain.services.financial_ai_engine import (
    analyze_expenses,
    analyze_risk,
    build_dashboard,
    cfo_assistant_response,
    chatbot_response,
    classify_invoice,
    detect_fraud,
    extract_document_ocr,
    forecast_budget,
    generate_financial_summary,
    generate_recommendations,
    predict_cash_flow,
    predict_revenue,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class FinancialAIApplicationService:
    CAPABILITIES = [c.value for c in AICapability]

    def __init__(
        self,
        jobs: IFinancialAIJobRepository,
        chats: IFinancialAIChatRepository,
        journals: IJournalRepository,
        accounts: IChartOfAccountRepository,
        budgets: IBudgetRepository,
        payments: IPaymentRepository,
    ) -> None:
        self._jobs = jobs
        self._chats = chats
        self._journals = journals
        self._accounts = accounts
        self._budgets = budgets
        self._payments = payments

    async def _account_types(self, tenant_id: str) -> dict[str, str]:
        accounts = await self._accounts.list_by_tenant(tenant_id)
        return {
            a.code: (a.account_type.value if a.account_type else "")
            for a in accounts
        }

    async def _financial_context(self, tenant_id: str) -> dict:
        journals = [j.to_dict() for j in await self._journals.list_by_tenant(tenant_id)]
        payments = [p.to_dict() for p in await self._payments.list_by_tenant(tenant_id)]
        budgets = [b.to_dict() for b in await self._budgets.list_by_tenant(tenant_id)]
        account_types = await self._account_types(tenant_id)
        return {
            "journals": journals,
            "payments": payments,
            "budgets": budgets,
            "account_types": account_types,
        }

    async def list_capabilities(self) -> Result[list[dict]]:
        return Result.ok(
            [
                {"id": c, "name": c.replace("_", " ").title(), "autonomous_posting": False}
                for c in self.CAPABILITIES
            ]
        )

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
            return Result.fail("financial_kernel.errors.invalid_ai_capability")
        ctx = await self._financial_context(tenant_id)
        data = input_data or {}
        job = FinancialAIJob.create(
            tenant_id=tenant_id,
            capability=capability,
            input_data=data,
            correlation_id=correlation_id,
            created_by=created_by,
        )
        try:
            result, confidence = await self._execute_capability(capability, ctx, data)
        except Exception as exc:
            job.status = AIJobStatus.FAILED
            await self._jobs.save(job)
            return Result.fail(str(exc))
        job.complete(result, confidence)
        await self._jobs.save(job)
        await publish_integration_event(
            FinancialAIAnalysisCompletedIntegration(
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
        payments = ctx["payments"]
        budgets = ctx["budgets"]
        account_types = ctx["account_types"]

        if capability == AICapability.FRAUD_DETECTION.value:
            threshold = float(data.get("threshold", 10000))
            result = detect_fraud(payments=payments, threshold=threshold)
            return result, 0.88

        if capability == AICapability.CASH_FLOW_PREDICTION.value:
            months = int(data.get("months", 3))
            result = predict_cash_flow(
                journals=journals, account_types=account_types, months=months
            )
            return result, 0.82

        if capability == AICapability.BUDGET_FORECAST.value:
            result = forecast_budget(
                budgets=budgets, journals=journals, account_types=account_types
            )
            return result, 0.85

        if capability == AICapability.EXPENSE_ANALYSIS.value:
            result = analyze_expenses(journals=journals, account_types=account_types)
            return result, 0.9

        if capability == AICapability.REVENUE_PREDICTION.value:
            months = int(data.get("months", 3))
            result = predict_revenue(
                journals=journals, account_types=account_types, months=months
            )
            return result, 0.83

        if capability == AICapability.FINANCIAL_SUMMARY.value:
            result = generate_financial_summary(
                journals=journals, payments=payments, account_types=account_types
            )
            return result, 0.95

        if capability == AICapability.RISK_ANALYSIS.value:
            result = analyze_risk(payments=payments, journals=journals, budgets=budgets)
            return result, 0.87

        if capability == AICapability.RECOMMENDATION.value:
            summary = generate_financial_summary(
                journals=journals, payments=payments, account_types=account_types
            )
            risk = analyze_risk(payments=payments, journals=journals, budgets=budgets)
            expenses = analyze_expenses(journals=journals, account_types=account_types)
            result = {"recommendations": generate_recommendations(
                summary=summary, risk=risk, expense_analysis=expenses
            )}
            return result, 0.8

        if capability == AICapability.INVOICE_CLASSIFICATION.value:
            text = data.get("text", "")
            amount = data.get("amount")
            result = classify_invoice(text, amount=float(amount) if amount is not None else None)
            return result, result.get("confidence", 0.85)

        if capability == AICapability.DOCUMENT_OCR.value:
            text = data.get("text", "")
            result = extract_document_ocr(text)
            return result, 0.78

        if capability == AICapability.DASHBOARD.value:
            summary = generate_financial_summary(
                journals=journals, payments=payments, account_types=account_types
            )
            risk = analyze_risk(payments=payments, journals=journals, budgets=budgets)
            fraud = detect_fraud(payments=payments)
            cash_flow = predict_cash_flow(journals=journals, account_types=account_types)
            expenses = analyze_expenses(journals=journals, account_types=account_types)
            recs = generate_recommendations(summary=summary, risk=risk, expense_analysis=expenses)
            result = build_dashboard(
                summary=summary, risk=risk, fraud=fraud, cash_flow=cash_flow, recommendations=recs
            )
            return result, 0.92

        if capability == AICapability.FINANCIAL_CHATBOT.value:
            message = data.get("message", "")
            reply = chatbot_response(message=message, context=ctx)
            return {"reply": reply, "message": message}, 0.75

        if capability == AICapability.CFO_ASSISTANT.value:
            message = data.get("message", "")
            summary = generate_financial_summary(
                journals=journals, payments=payments, account_types=account_types
            )
            risk = analyze_risk(payments=payments, journals=journals, budgets=budgets)
            expenses = analyze_expenses(journals=journals, account_types=account_types)
            recs = generate_recommendations(summary=summary, risk=risk, expense_analysis=expenses)
            result = cfo_assistant_response(
                message=message, summary=summary, recommendations=recs
            )
            return result, 0.86

        return {}, 0.5

    async def get_job(self, tenant_id: str, job_id: str) -> Result[dict]:
        job = await self._jobs.find_by_id(job_id)
        if not job or job.tenant_id != tenant_id:
            return Result.fail("financial_kernel.errors.ai_job_not_found")
        return Result.ok(job.to_dict())

    async def list_jobs(self, tenant_id: str, capability: str | None = None) -> Result[list[dict]]:
        if capability:
            jobs = await self._jobs.list_by_capability(tenant_id, capability)
        else:
            jobs = await self._jobs.list_by_tenant(tenant_id)
        return Result.ok([j.to_dict() for j in jobs])

    async def get_dashboard(
        self, *, tenant_id: str, correlation_id: str = "", created_by: str | None = None
    ) -> Result[dict]:
        result = await self.run_analysis(
            tenant_id=tenant_id,
            capability=AICapability.DASHBOARD.value,
            correlation_id=correlation_id,
            created_by=created_by,
        )
        if result.succeeded:
            dashboard = result.unwrap().get("result", {})
            await publish_integration_event(
                FinancialAIDashboardGeneratedIntegration(
                    tenant_id=TenantId(tenant_id),
                    job_id=result.unwrap()["id"],
                    correlation_id=correlation_id,
                )
            )
            return Result.ok(dashboard)
        return result

    async def chat(
        self,
        *,
        tenant_id: str,
        message: str,
        session_id: str | None = None,
        correlation_id: str = "",
        created_by: str | None = None,
    ) -> Result[dict]:
        session: FinancialAIChatSession
        if session_id:
            existing = await self._chats.find_by_id(session_id)
            if not existing or existing.tenant_id != tenant_id:
                return Result.fail("financial_kernel.errors.chat_session_not_found")
            session = existing
        else:
            session = FinancialAIChatSession.create(
                tenant_id=tenant_id,
                session_type=AICapability.FINANCIAL_CHATBOT.value,
                created_by=created_by,
            )
        session.add_message("user", message)
        ctx = await self._financial_context(tenant_id)
        reply = chatbot_response(message=message, context=ctx)
        session.add_message("assistant", reply)
        await self._chats.save(session)
        await publish_integration_event(
            FinancialAIChatCompletedIntegration(
                tenant_id=TenantId(tenant_id),
                session_id=str(session.id),
                session_type=session.session_type,
                correlation_id=correlation_id,
            )
        )
        return Result.ok({"session_id": str(session.id), "reply": reply, "messages": session.messages})

    async def cfo_assistant(
        self,
        *,
        tenant_id: str,
        message: str,
        session_id: str | None = None,
        correlation_id: str = "",
        created_by: str | None = None,
    ) -> Result[dict]:
        session: FinancialAIChatSession
        if session_id:
            existing = await self._chats.find_by_id(session_id)
            if not existing or existing.tenant_id != tenant_id:
                return Result.fail("financial_kernel.errors.chat_session_not_found")
            session = existing
        else:
            session = FinancialAIChatSession.create(
                tenant_id=tenant_id,
                session_type=AICapability.CFO_ASSISTANT.value,
                created_by=created_by,
            )
        session.add_message("user", message)
        analysis = await self.run_analysis(
            tenant_id=tenant_id,
            capability=AICapability.CFO_ASSISTANT.value,
            input_data={"message": message},
            correlation_id=correlation_id,
            created_by=created_by,
        )
        if not analysis.succeeded:
            return analysis
        payload = analysis.unwrap().get("result", {})
        session.add_message("assistant", payload.get("reply", ""), metadata=payload)
        await self._chats.save(session)
        return Result.ok(
            {
                "session_id": str(session.id),
                **payload,
                "messages": session.messages,
            }
        )

    async def classify_invoice(
        self, *, tenant_id: str, text: str, amount: float | None = None, correlation_id: str = ""
    ) -> Result[dict]:
        return await self.run_analysis(
            tenant_id=tenant_id,
            capability=AICapability.INVOICE_CLASSIFICATION.value,
            input_data={"text": text, "amount": amount},
            correlation_id=correlation_id,
        )

    async def ocr_document(
        self, *, tenant_id: str, text: str, correlation_id: str = ""
    ) -> Result[dict]:
        return await self.run_analysis(
            tenant_id=tenant_id,
            capability=AICapability.DOCUMENT_OCR.value,
            input_data={"text": text},
            correlation_id=correlation_id,
        )
