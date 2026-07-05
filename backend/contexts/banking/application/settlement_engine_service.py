"""Banking Settlement Engine application service."""
from __future__ import annotations

from contexts.banking.domain.aggregates.settlement_engine import (
    BankReconciliationRun,
    ReconciliationMatch,
    SettlementAdjustment,
    SettlementAuditEntry,
    SettlementBatch,
    SettlementDifference,
    SettlementException,
    SettlementItem,
    SettlementReport,
    SettlementType,
)
from contexts.banking.domain.events.settlement_integration_events import (
    BankingReconciliationCompletedIntegration,
    BankingSettlementExceptionRaisedIntegration,
    BankingSettlementPostedIntegration,
)
from contexts.banking.domain.ports.payment_platform_repositories import IPaymentTransferRepository
from contexts.banking.domain.ports.settlement_repositories import (
    IReconciliationMatchRepository,
    IReconciliationRunRepository,
    ISettlementAdjustmentRepository,
    ISettlementAuditRepository,
    ISettlementBatchRepository,
    ISettlementDifferenceRepository,
    ISettlementExceptionRepository,
    ISettlementItemRepository,
    ISettlementReportRepository,
)
from contexts.banking.domain.services.settlement_engine import (
    analyze_differences,
    automatic_match,
    build_settlement_dashboard,
    build_settlement_report,
    list_settlement_catalog,
    list_settlement_policy_keys,
    resolve_posting_rule,
)
from shared.application.ports.financial_kernel import IFinancialKernel
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class BankingSettlementEngineApplicationService:
    def __init__(
        self,
        batches: ISettlementBatchRepository,
        items: ISettlementItemRepository,
        reconciliations: IReconciliationRunRepository,
        matches: IReconciliationMatchRepository,
        exceptions: ISettlementExceptionRepository,
        differences: ISettlementDifferenceRepository,
        adjustments: ISettlementAdjustmentRepository,
        audits: ISettlementAuditRepository,
        reports: ISettlementReportRepository,
        transfers: IPaymentTransferRepository,
        kernel: IFinancialKernel,
        policy: IPolicyEvaluator,
    ) -> None:
        self._batches = batches
        self._items = items
        self._reconciliations = reconciliations
        self._matches = matches
        self._exceptions = exceptions
        self._differences = differences
        self._adjustments = adjustments
        self._audits = audits
        self._reports = reports
        self._transfers = transfers
        self._kernel = kernel
        self._policy = policy

    async def _audit(
        self,
        *,
        tenant_id: str,
        source_type: str,
        source_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
    ) -> None:
        await self._audits.save(
            SettlementAuditEntry.create(
                tenant_id=tenant_id,
                source_type=source_type,
                source_id=source_id,
                action=action,
                actor_id=actor_id,
                detail=detail,
            )
        )

    async def _resolve_gl_code(self, tenant_id: str, account_key: str) -> str | None:
        accounts = await self._kernel.list_accounts(tenant_id=tenant_id)
        for acct in accounts:
            if acct.get("account_key") == account_key:
                return acct.get("code") or acct.get("account_code")
        return None

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_settlement_catalog())

    async def list_policy_keys(self) -> Result[list[dict]]:
        return Result.ok(list_settlement_policy_keys())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        batches = await self._batches.list_by_tenant(tenant_id)
        reconciliations = await self._reconciliations.list_by_tenant(tenant_id)
        exceptions = await self._exceptions.list_by_tenant(tenant_id)
        adjustments = await self._adjustments.list_by_tenant(tenant_id)
        reports = await self._reports.list_by_tenant(tenant_id)
        return Result.ok(
            build_settlement_dashboard(
                batches=[b.to_dict() for b in batches],
                reconciliations=[r.to_dict() for r in reconciliations],
                exceptions=[e.to_dict() for e in exceptions],
                adjustments=[a.to_dict() for a in adjustments],
                reports=[r.to_dict() for r in reports],
            )
        )

    async def create_settlement_batch(
        self,
        *,
        tenant_id: str,
        settlement_type: str,
        currency: str = "USD",
        items: list[dict],
    ) -> Result[dict]:
        if settlement_type not in {t.value for t in SettlementType}:
            return Result.fail("banking.errors.invalid_settlement_type")
        if not items:
            return Result.fail("banking.errors.empty_settlement_batch")

        batch_ref = self._batches.next_batch_ref(tenant_id)
        batch = SettlementBatch.create(
            tenant_id=tenant_id,
            batch_ref=batch_ref,
            settlement_type=settlement_type,
            currency=currency,
        )
        total = 0.0
        created_items: list[dict] = []
        for raw in items:
            item_ref = self._items.next_item_ref(tenant_id)
            item = SettlementItem.create(
                tenant_id=tenant_id,
                batch_id=str(batch.id),
                item_ref=item_ref,
                source_ref=raw.get("source_ref", ""),
                amount=float(raw.get("amount", 0)),
                currency=currency,
                counterparty=raw.get("counterparty", ""),
                narrative=raw.get("narrative", ""),
            )
            await self._items.save(item)
            total += item.amount
            created_items.append(item.to_dict())

        batch.add_items(count=len(created_items), total_amount=total)
        await self._batches.save(batch)
        await self._audit(
            tenant_id=tenant_id,
            source_type="batch",
            source_id=str(batch.id),
            action="batch.created",
            detail=batch_ref,
        )
        return Result.ok({**batch.to_dict(), "items": created_items})

    async def submit_batch(self, *, batch_id: str) -> Result[dict]:
        batch = await self._batches.find_by_id(batch_id)
        if not batch:
            return Result.fail("banking.errors.batch_not_found")
        try:
            batch.submit()
        except ValueError:
            return Result.fail("banking.errors.cannot_submit_batch")
        await self._batches.save(batch)
        await self._audit(
            tenant_id=batch.tenant_id,
            source_type="batch",
            source_id=batch_id,
            action="batch.submitted",
            detail=batch.batch_ref,
        )
        return Result.ok(batch.to_dict())

    async def run_clearing(self, *, batch_id: str) -> Result[dict]:
        batch = await self._batches.find_by_id(batch_id)
        if not batch:
            return Result.fail("banking.errors.batch_not_found")
        if batch.settlement_type != SettlementType.CLEARING.value:
            return Result.fail("banking.errors.not_clearing_batch")

        policy = await self._policy.evaluate(
            tenant_id=batch.tenant_id,
            domain="bank",
            policy_key="settlement.clearing.window",
            facts={"batch_ref": batch.batch_ref, "amount": batch.total_amount},
        )
        if policy.outcome == "deny":
            batch.fail("clearing_window_closed")
            await self._batches.save(batch)
            return Result.fail("banking.errors.clearing_window_closed")

        try:
            batch.start_clearing()
        except ValueError:
            return Result.fail("banking.errors.cannot_start_clearing")

        clearing_ref = f"CLR-{batch.batch_ref}"
        batch.complete_clearing(clearing_ref)
        await self._batches.save(batch)
        await self._audit(
            tenant_id=batch.tenant_id,
            source_type="batch",
            source_id=batch_id,
            action="batch.cleared",
            detail=clearing_ref,
        )
        return Result.ok(batch.to_dict())

    async def settle_batch(self, *, batch_id: str) -> Result[dict]:
        batch = await self._batches.find_by_id(batch_id)
        if not batch:
            return Result.fail("banking.errors.batch_not_found")

        if batch.status == "draft":
            submit = await self.submit_batch(batch_id=batch_id)
            if not submit.succeeded:
                return submit
            batch = await self._batches.find_by_id(batch_id)
            assert batch

        if batch.settlement_type == SettlementType.CLEARING.value and batch.status == "pending_clearing":
            clearing = await self.run_clearing(batch_id=batch_id)
            if not clearing.succeeded:
                return clearing
            batch = await self._batches.find_by_id(batch_id)
            assert batch

        try:
            batch.start_settlement()
        except ValueError:
            return Result.fail("banking.errors.cannot_settle_batch")

        rule_id = resolve_posting_rule(batch.settlement_type)
        debit_key, credit_key = self._gl_accounts_for_type(batch.settlement_type)
        debit_gl = await self._resolve_gl_code(batch.tenant_id, debit_key)
        credit_gl = await self._resolve_gl_code(batch.tenant_id, credit_key)
        if not debit_gl or not credit_gl:
            batch.fail("missing_gl_mapping")
            await self._batches.save(batch)
            return Result.fail("banking.errors.missing_gl_mapping")

        journal_id = await self._post_gl(
            tenant_id=batch.tenant_id,
            batch_id=str(batch.id),
            batch_ref=batch.batch_ref,
            rule_id=rule_id,
            amount=batch.total_amount,
            currency=batch.currency,
            debit_gl=debit_gl,
            credit_gl=credit_gl,
        )

        items = await self._items.list_by_batch(batch_id)
        for item in items:
            item.settle()
            await self._items.save(item)

        batch.complete(journal_id=journal_id)
        await self._batches.save(batch)

        await publish_integration_event(
            BankingSettlementPostedIntegration(
                tenant_id=TenantId.create(batch.tenant_id),
                correlation_id=f"settlement-{batch.id}",
                batch_id=str(batch.id),
                batch_ref=batch.batch_ref,
                settlement_type=batch.settlement_type,
                amount=batch.total_amount,
                currency=batch.currency,
                debit_gl_code=debit_gl,
                credit_gl_code=credit_gl,
            )
        )
        await self._audit(
            tenant_id=batch.tenant_id,
            source_type="batch",
            source_id=batch_id,
            action="batch.settled",
            detail=batch.batch_ref,
        )
        return Result.ok(batch.to_dict())

    def _gl_accounts_for_type(self, settlement_type: str) -> tuple[str, str]:
        if settlement_type == SettlementType.INTERBANK.value:
            return "cash_reserves", "bank"
        if settlement_type == SettlementType.CLEARING.value:
            return "customer_deposits", "cash_reserves"
        return "customer_deposits", "customer_deposits"

    async def _post_gl(
        self,
        *,
        tenant_id: str,
        batch_id: str,
        batch_ref: str,
        rule_id: str,
        amount: float,
        currency: str,
        debit_gl: str,
        credit_gl: str,
    ) -> str | None:
        try:
            result = await self._kernel.execute_posting(
                tenant_id=tenant_id,
                rule_id=rule_id,
                source_context="banking",
                source_document_id=batch_id,
                amount=amount,
                currency=currency,
                correlation_id=f"banking-settlement-{batch_id}",
                idempotency_key=f"posting:{rule_id}:{batch_ref}",
                description=f"Settlement {batch_ref}",
                account_mappings={"debit": debit_gl, "credit": credit_gl},
            )
            return result.journal_id
        except ValueError:
            return None

    async def create_reconciliation_run(
        self,
        *,
        tenant_id: str,
        settlement_account: str = "",
        statement_items: list[dict] | None = None,
        book_items: list[dict] | None = None,
        use_completed_transfers: bool = False,
    ) -> Result[dict]:
        run_ref = self._reconciliations.next_run_ref(tenant_id)
        book = list(book_items or [])
        if use_completed_transfers and not book:
            transfers = await self._transfers.list_by_tenant(tenant_id)
            book = [
                {
                    "id": str(t.id),
                    "reference": t.transfer_ref,
                    "amount": t.amount,
                    "currency": t.currency,
                    "type": t.transfer_type,
                }
                for t in transfers
                if t.status == "completed"
            ]

        run = BankReconciliationRun.create(
            tenant_id=tenant_id,
            run_ref=run_ref,
            settlement_account=settlement_account,
            statement_items=list(statement_items or []),
            book_items=book,
        )
        run.start()
        await self._reconciliations.save(run)
        await self._audit(
            tenant_id=tenant_id,
            source_type="reconciliation",
            source_id=str(run.id),
            action="reconciliation.started",
            detail=run_ref,
        )
        return Result.ok(run.to_dict())

    async def auto_match_reconciliation(self, *, run_id: str) -> Result[dict]:
        run = await self._reconciliations.find_by_id(run_id)
        if not run:
            return Result.fail("banking.errors.reconciliation_not_found")

        policy = await self._policy.evaluate(
            tenant_id=run.tenant_id,
            domain="bank",
            policy_key="settlement.match.tolerance",
            facts={"run_ref": run.run_ref},
        )
        tolerance = float(policy.parameters.get("amount_tolerance", 0.01))

        matched, unmatched_stmt, unmatched_book = automatic_match(
            run.statement_items,
            run.book_items,
            amount_tolerance=tolerance,
        )
        for m in matched:
            match = ReconciliationMatch.create(
                tenant_id=run.tenant_id,
                run_id=run_id,
                statement_item=m["statement"],
                book_item=m["book"],
                match_type=m["match_type"],
                match_score=m["match_score"],
            )
            await self._matches.save(match)

        stmt_total = sum(float(i.get("amount", 0)) for i in run.statement_items)
        book_total = sum(float(i.get("amount", 0)) for i in run.book_items)
        diff_amount = round(stmt_total - book_total, 2)

        run.apply_match_results(
            matched_count=len(matched),
            unmatched_stmt=len(unmatched_stmt),
            unmatched_book=len(unmatched_book),
            difference_amount=diff_amount,
        )
        await self._reconciliations.save(run)
        await self._audit(
            tenant_id=run.tenant_id,
            source_type="reconciliation",
            source_id=run_id,
            action="reconciliation.matched",
            detail=f"matched={len(matched)}",
        )
        saved_matches = await self._matches.list_by_run(run_id)
        return Result.ok(
            {
                **run.to_dict(),
                "matches": [m.to_dict() for m in saved_matches],
                "unmatched_statement": unmatched_stmt,
                "unmatched_book": unmatched_book,
            }
        )

    async def analyze_reconciliation_differences(self, *, run_id: str) -> Result[dict]:
        run = await self._reconciliations.find_by_id(run_id)
        if not run:
            return Result.fail("banking.errors.reconciliation_not_found")

        matches = await self._matches.list_by_run(run_id)
        matched_stmt_ids = {m.statement_item.get("id") for m in matches}
        matched_book_ids = {m.book_item.get("id") for m in matches}
        unmatched_stmt = [
            i for i in run.statement_items if i.get("id") not in matched_stmt_ids
        ]
        unmatched_book = [i for i in run.book_items if i.get("id") not in matched_book_ids]

        stmt_total = sum(float(i.get("amount", 0)) for i in run.statement_items)
        book_total = sum(float(i.get("amount", 0)) for i in run.book_items)
        diff_amount = round(stmt_total - book_total, 2)
        analysis = analyze_differences(
            statement_items=run.statement_items,
            book_items=run.book_items,
            unmatched_statement=unmatched_stmt,
            unmatched_book=unmatched_book,
        )

        diff_ref = self._differences.next_difference_ref(run.tenant_id)
        difference = SettlementDifference.create(
            tenant_id=run.tenant_id,
            run_id=run_id,
            difference_ref=diff_ref,
            statement_total=stmt_total,
            book_total=book_total,
            difference_amount=diff_amount,
            unmatched_statement=unmatched_stmt,
            unmatched_book=unmatched_book,
            analysis=analysis,
        )
        await self._differences.save(difference)
        await self._audit(
            tenant_id=run.tenant_id,
            source_type="reconciliation",
            source_id=run_id,
            action="reconciliation.differences_analyzed",
            detail=diff_ref,
        )
        return Result.ok(difference.to_dict())

    async def raise_exception(
        self,
        *,
        tenant_id: str,
        source_type: str,
        source_id: str,
        reason: str,
    ) -> Result[dict]:
        policy = await self._policy.evaluate(
            tenant_id=tenant_id,
            domain="bank",
            policy_key="settlement.retry.max_attempts",
            facts={"source_type": source_type},
        )
        max_retries = int(policy.parameters.get("max_attempts", 3))

        exc_ref = self._exceptions.next_exception_ref(tenant_id)
        exception = SettlementException.create(
            tenant_id=tenant_id,
            exception_ref=exc_ref,
            source_type=source_type,
            source_id=source_id,
            reason=reason,
            max_retries=max_retries,
        )
        await self._exceptions.save(exception)

        if source_type == "batch":
            batch = await self._batches.find_by_id(source_id)
            if batch:
                batch.mark_exception()
                await self._batches.save(batch)
        elif source_type == "reconciliation":
            run = await self._reconciliations.find_by_id(source_id)
            if run:
                run.status = "exception"
                await self._reconciliations.save(run)

        await publish_integration_event(
            BankingSettlementExceptionRaisedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=f"exception-{exception.id}",
                exception_id=str(exception.id),
                exception_ref=exc_ref,
                source_type=source_type,
                source_id=source_id,
                reason=reason,
            )
        )
        await self._audit(
            tenant_id=tenant_id,
            source_type="exception",
            source_id=str(exception.id),
            action="exception.raised",
            detail=reason,
        )
        return Result.ok(exception.to_dict())

    async def retry_exception(self, *, exception_id: str) -> Result[dict]:
        exception = await self._exceptions.find_by_id(exception_id)
        if not exception:
            return Result.fail("banking.errors.exception_not_found")
        try:
            exception.retry()
        except ValueError as exc:
            await self._exceptions.save(exception)
            return Result.fail(f"banking.errors.{str(exc)}")

        await self._exceptions.save(exception)
        await self._audit(
            tenant_id=exception.tenant_id,
            source_type="exception",
            source_id=exception_id,
            action="exception.retried",
            detail=f"attempt={exception.retry_count}",
        )

        if exception.source_type == "batch":
            result = await self.settle_batch(batch_id=exception.source_id)
            if result.succeeded:
                exception.resolve()
                await self._exceptions.save(exception)
        elif exception.source_type == "reconciliation":
            result = await self.auto_match_reconciliation(run_id=exception.source_id)
            if result.succeeded:
                exception.resolve()
                await self._exceptions.save(exception)

        return Result.ok(exception.to_dict())

    async def create_adjustment(
        self,
        *,
        tenant_id: str,
        run_id: str,
        amount: float,
        currency: str = "USD",
        reason: str = "",
    ) -> Result[dict]:
        run = await self._reconciliations.find_by_id(run_id)
        if not run or run.tenant_id != tenant_id:
            return Result.fail("banking.errors.reconciliation_not_found")

        adj_ref = self._adjustments.next_adjustment_ref(tenant_id)
        adjustment = SettlementAdjustment.create(
            tenant_id=tenant_id,
            adjustment_ref=adj_ref,
            run_id=run_id,
            amount=amount,
            currency=currency,
            reason=reason,
        )
        adjustment.submit()
        await self._adjustments.save(adjustment)
        await self._audit(
            tenant_id=tenant_id,
            source_type="adjustment",
            source_id=str(adjustment.id),
            action="adjustment.created",
            detail=adj_ref,
        )
        return Result.ok(adjustment.to_dict())

    async def approve_adjustment(self, *, adjustment_id: str, approver_id: str) -> Result[dict]:
        adjustment = await self._adjustments.find_by_id(adjustment_id)
        if not adjustment:
            return Result.fail("banking.errors.adjustment_not_found")

        policy = await self._policy.evaluate(
            tenant_id=adjustment.tenant_id,
            domain="bank",
            policy_key="settlement.adjustment.approval_level",
            facts={"amount": adjustment.amount},
        )
        if policy.outcome == "deny":
            adjustment.reject()
            await self._adjustments.save(adjustment)
            return Result.fail("banking.errors.adjustment_denied")

        try:
            adjustment.approve(approver_id)
        except ValueError:
            return Result.fail("banking.errors.cannot_approve_adjustment")

        debit_gl = await self._resolve_gl_code(adjustment.tenant_id, "customer_deposits")
        credit_gl = await self._resolve_gl_code(adjustment.tenant_id, "cash_reserves")
        journal_id = None
        if debit_gl and credit_gl:
            try:
                result = await self._kernel.execute_posting(
                    tenant_id=adjustment.tenant_id,
                    rule_id="bank_settlement",
                    source_context="banking",
                    source_document_id=str(adjustment.id),
                    amount=abs(adjustment.amount),
                    currency=adjustment.currency,
                    correlation_id=f"adjustment-{adjustment.id}",
                    idempotency_key=f"posting:adjustment:{adjustment.adjustment_ref}",
                    description=f"Reconciliation adjustment {adjustment.adjustment_ref}",
                    account_mappings={"debit": debit_gl, "credit": credit_gl},
                )
                journal_id = result.journal_id
            except ValueError:
                journal_id = None

        adjustment.post(journal_id=journal_id)
        await self._adjustments.save(adjustment)
        await self._audit(
            tenant_id=adjustment.tenant_id,
            source_type="adjustment",
            source_id=adjustment_id,
            action="adjustment.approved",
            actor_id=approver_id,
            detail=adjustment.adjustment_ref,
        )
        return Result.ok(adjustment.to_dict())

    async def approve_reconciliation(self, *, run_id: str, approver_id: str) -> Result[dict]:
        run = await self._reconciliations.find_by_id(run_id)
        if not run:
            return Result.fail("banking.errors.reconciliation_not_found")
        try:
            run.request_approval()
            run.approve()
        except ValueError:
            return Result.fail("banking.errors.cannot_approve_reconciliation")
        await self._reconciliations.save(run)
        await publish_integration_event(
            BankingReconciliationCompletedIntegration(
                tenant_id=TenantId.create(run.tenant_id),
                correlation_id=f"recon-{run.id}",
                run_id=str(run.id),
                run_ref=run.run_ref,
                status=run.status,
                matched_count=run.matched_count,
                difference_amount=run.difference_amount,
            )
        )
        await self._audit(
            tenant_id=run.tenant_id,
            source_type="reconciliation",
            source_id=run_id,
            action="reconciliation.approved",
            actor_id=approver_id,
            detail=run.run_ref,
        )
        return Result.ok(run.to_dict())

    async def generate_report(self, *, tenant_id: str, report_type: str = "settlement_summary") -> Result[dict]:
        batches = await self._batches.list_by_tenant(tenant_id)
        reconciliations = await self._reconciliations.list_by_tenant(tenant_id)
        exceptions = await self._exceptions.list_by_tenant(tenant_id)
        summary = build_settlement_report(
            batches=[b.to_dict() for b in batches],
            reconciliations=[r.to_dict() for r in reconciliations],
            exceptions=[e.to_dict() for e in exceptions],
        )
        report_ref = self._reports.next_report_ref(tenant_id)
        report = SettlementReport.create(
            tenant_id=tenant_id,
            report_ref=report_ref,
            report_type=report_type,
            summary=summary,
        )
        await self._reports.save(report)
        await self._audit(
            tenant_id=tenant_id,
            source_type="report",
            source_id=str(report.id),
            action="report.generated",
            detail=report_ref,
        )
        return Result.ok(report.to_dict())

    async def get_reconciliation_audit(self, *, run_id: str) -> Result[list[dict]]:
        run = await self._reconciliations.find_by_id(run_id)
        if not run:
            return Result.fail("banking.errors.reconciliation_not_found")
        entries = await self._audits.list_by_source("reconciliation", run_id)
        return Result.ok([e.to_dict() for e in entries])

    async def get_batch(self, *, batch_id: str) -> Result[dict]:
        batch = await self._batches.find_by_id(batch_id)
        if not batch:
            return Result.fail("banking.errors.batch_not_found")
        items = await self._items.list_by_batch(batch_id)
        return Result.ok({**batch.to_dict(), "items": [i.to_dict() for i in items]})

    async def list_batches(self, tenant_id: str) -> Result[list[dict]]:
        batches = await self._batches.list_by_tenant(tenant_id)
        return Result.ok([b.to_dict() for b in batches])

    async def handle_tenant_provisioned(self, envelope: dict) -> None:
        pass
