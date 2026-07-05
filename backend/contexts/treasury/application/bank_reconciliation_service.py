"""Enterprise Bank Reconciliation application service."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.bank_reconciliation_engine import (
    BankStatementImport,
    EnterpriseBankReconciliation,
    ReconciliationAuditEntry,
    StatementImportSource,
)
from contexts.treasury.domain.aggregates.treasury_transfer import TransferStatus
from contexts.treasury.domain.events.integration_events import TreasuryAIAnalysisCompletedIntegration
from contexts.treasury.domain.ports.bank_reconciliation_repositories import (
    IBankStatementImportRepository,
    IEnterpriseBankReconciliationRepository,
    IReconciliationAuditRepository,
)
from contexts.treasury.domain.ports.repositories import (
    ITreasuryAccountRepository,
    ITreasuryTransferRepository,
)
from contexts.treasury.domain.services.bank_reconciliation_engine import (
    build_reconciliation_dashboard,
    build_reconciliation_report,
    list_bank_reconciliation_catalog,
    list_workflow_states,
    manual_match,
    run_reconciliation,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class BankReconciliationApplicationService:
    def __init__(
        self,
        accounts: ITreasuryAccountRepository,
        transfers: ITreasuryTransferRepository,
        statements: IBankStatementImportRepository,
        reconciliations: IEnterpriseBankReconciliationRepository,
        audits: IReconciliationAuditRepository,
    ) -> None:
        self._accounts = accounts
        self._transfers = transfers
        self._statements = statements
        self._reconciliations = reconciliations
        self._audits = audits

    async def _audit(
        self,
        *,
        tenant_id: str,
        reconciliation_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
        payload: dict | None = None,
    ) -> None:
        entry = ReconciliationAuditEntry.create(
            tenant_id=tenant_id,
            reconciliation_id=reconciliation_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
            payload=payload,
        )
        await self._audits.save(entry)

    async def _book_items(self, tenant_id: str, treasury_account_id: str) -> list[dict]:
        transfers = await self._transfers.list_by_tenant(tenant_id)
        return [
            {
                "reference": t.reference,
                "amount": t.amount,
                "date": t.executed_at.isoformat() if t.executed_at else "",
                "type": "transfer",
            }
            for t in transfers
            if t.status == TransferStatus.EXECUTED
            and t.from_account_id == treasury_account_id
        ]

    async def list_catalog(self) -> Result[list[dict]]:
        return Result.ok(list_bank_reconciliation_catalog())

    async def list_workflow(self) -> Result[list[dict]]:
        return Result.ok(list_workflow_states())

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        recons = await self._reconciliations.list_by_tenant(tenant_id)
        sorted_recons = sorted(recons, key=lambda r: r.created_at, reverse=True)
        return Result.ok(
            build_reconciliation_dashboard(
                reconciliations=[r.to_dict() for r in sorted_recons]
            )
        )

    async def import_statement(
        self,
        *,
        tenant_id: str,
        treasury_account_id: str,
        source: str,
        statement_date: str,
        statement_balance: float,
        items: list[dict],
        actor_id: str | None = None,
    ) -> Result[dict]:
        account = await self._accounts.find_by_id(treasury_account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("treasury.errors.account_not_found")
        try:
            StatementImportSource(source)
        except ValueError:
            return Result.fail("treasury.errors.invalid_import_source")

        statement = BankStatementImport.create(
            tenant_id=tenant_id,
            treasury_account_id=treasury_account_id,
            source=source,
            statement_date=statement_date,
            statement_balance=statement_balance,
            items=items,
        )
        await self._statements.save(statement)
        return Result.ok(statement.to_dict())

    async def import_from_bank_api(
        self,
        *,
        tenant_id: str,
        treasury_account_id: str,
        statement_date: str,
        api_payload: dict,
        actor_id: str | None = None,
    ) -> Result[dict]:
        items = api_payload.get("transactions", api_payload.get("items", []))
        balance = float(api_payload.get("balance", api_payload.get("statement_balance", 0)))
        return await self.import_statement(
            tenant_id=tenant_id,
            treasury_account_id=treasury_account_id,
            source=StatementImportSource.BANK_API.value,
            statement_date=statement_date,
            statement_balance=balance,
            items=items,
            actor_id=actor_id,
        )

    async def list_statements(self, tenant_id: str) -> Result[list[dict]]:
        statements = await self._statements.list_by_tenant(tenant_id)
        return Result.ok([s.to_dict() for s in statements])

    async def create_reconciliation(
        self,
        *,
        tenant_id: str,
        treasury_account_id: str,
        reconciliation_date: str,
        statement_balance: float,
        statement_items: list[dict],
        book_items: list[dict] | None = None,
        statement_import_id: str | None = None,
        actor_id: str | None = None,
    ) -> Result[dict]:
        account = await self._accounts.find_by_id(treasury_account_id)
        if not account or account.tenant_id != tenant_id:
            return Result.fail("treasury.errors.account_not_found")

        book = book_items if book_items is not None else await self._book_items(
            tenant_id, treasury_account_id
        )
        book_balance = account.balance
        result = run_reconciliation(
            statement_items=statement_items,
            book_items=book,
            statement_balance=statement_balance,
            book_balance=book_balance,
        )
        report = build_reconciliation_report(
            reconciliation_date=reconciliation_date,
            treasury_account_id=treasury_account_id,
            statement_balance=statement_balance,
            book_balance=book_balance,
            matched_pairs=result["matched_pairs"],
            exceptions=result["exceptions"],
            outstanding=result["outstanding_transactions"],
            status="in_progress",
            variance=result["variance"],
        )

        recon = EnterpriseBankReconciliation.create(
            tenant_id=tenant_id,
            treasury_account_id=treasury_account_id,
            reconciliation_date=reconciliation_date,
            statement_balance=statement_balance,
            book_balance=book_balance,
            matched_pairs=result["matched_pairs"],
            unmatched_statement=result["unmatched_statement"],
            unmatched_book=result["unmatched_book"],
            duplicates=result["duplicates"],
            exceptions=result["exceptions"],
            outstanding_transactions=result["outstanding_transactions"],
            ai_suggestions=result["ai_suggestions"],
            report_summary=report,
            statement_import_id=statement_import_id,
        )
        await self._reconciliations.save(recon)
        await self._audit(
            tenant_id=tenant_id,
            reconciliation_id=str(recon.id),
            action="reconciliation_created",
            actor_id=actor_id,
            detail=f"Auto-matched {len(result['matched_pairs'])} pairs",
            payload={"match_rate": result["match_rate"]},
        )

        if result["ai_suggestions"]:
            await publish_integration_event(
                TreasuryAIAnalysisCompletedIntegration(
                    tenant_id=TenantId.create(tenant_id),
                    correlation_id=f"bank-recon-{recon.id}",
                    capability="ai_matching_suggestions",
                    result_summary=f"{len(result['ai_suggestions'])} suggestions generated",
                )
            )
        return Result.ok(recon.to_dict())

    async def manual_match_items(
        self,
        reconciliation_id: str,
        *,
        statement_item: dict,
        book_item: dict,
        actor_id: str,
    ) -> Result[dict]:
        recon = await self._reconciliations.find_by_id(reconciliation_id)
        if not recon:
            return Result.fail("treasury.errors.reconciliation_not_found")

        pairs, unmatched_stmt, unmatched_book = manual_match(
            matched_pairs=recon.matched_pairs,
            unmatched_statement=recon.unmatched_statement,
            unmatched_book=recon.unmatched_book,
            statement_item=statement_item,
            book_item=book_item,
            actor_id=actor_id,
        )
        recon.matched_pairs = pairs
        recon.unmatched_statement = unmatched_stmt
        recon.unmatched_book = unmatched_book
        recon.exceptions = [
            e for e in recon.exceptions
            if not (
                e.get("side") == "statement" and e.get("item") == statement_item
                or e.get("side") == "book" and e.get("item") == book_item
            )
        ]
        recon.outstanding_transactions = [
            o for o in recon.outstanding_transactions
            if not (
                o.get("source") == "statement" and o.get("reference") == statement_item.get("reference")
                or o.get("source") == "book" and o.get("reference") == book_item.get("reference")
            )
        ]
        recon.updated_at = recon.created_at
        await self._reconciliations.save(recon)
        await self._audit(
            tenant_id=recon.tenant_id,
            reconciliation_id=reconciliation_id,
            action="manual_match",
            actor_id=actor_id,
            detail=f"Matched {statement_item.get('reference')} to {book_item.get('reference')}",
        )
        return Result.ok(recon.to_dict())

    async def get_exceptions(self, reconciliation_id: str) -> Result[list[dict]]:
        recon = await self._reconciliations.find_by_id(reconciliation_id)
        if not recon:
            return Result.fail("treasury.errors.reconciliation_not_found")
        return Result.ok(recon.exceptions)

    async def get_outstanding(self, reconciliation_id: str) -> Result[list[dict]]:
        recon = await self._reconciliations.find_by_id(reconciliation_id)
        if not recon:
            return Result.fail("treasury.errors.reconciliation_not_found")
        return Result.ok(recon.outstanding_transactions)

    async def get_ai_suggestions(self, reconciliation_id: str) -> Result[list[dict]]:
        recon = await self._reconciliations.find_by_id(reconciliation_id)
        if not recon:
            return Result.fail("treasury.errors.reconciliation_not_found")
        return Result.ok(recon.ai_suggestions)

    async def get_report(self, reconciliation_id: str) -> Result[dict]:
        recon = await self._reconciliations.find_by_id(reconciliation_id)
        if not recon:
            return Result.fail("treasury.errors.reconciliation_not_found")
        return Result.ok(recon.report_summary)

    async def submit_for_approval(
        self, reconciliation_id: str, *, actor_id: str
    ) -> Result[dict]:
        recon = await self._reconciliations.find_by_id(reconciliation_id)
        if not recon:
            return Result.fail("treasury.errors.reconciliation_not_found")
        try:
            recon.submit_for_approval(actor_id)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")
        await self._reconciliations.save(recon)
        await self._audit(
            tenant_id=recon.tenant_id,
            reconciliation_id=reconciliation_id,
            action="submitted_for_approval",
            actor_id=actor_id,
        )
        return Result.ok(recon.to_dict())

    async def approve(self, reconciliation_id: str, *, actor_id: str) -> Result[dict]:
        recon = await self._reconciliations.find_by_id(reconciliation_id)
        if not recon:
            return Result.fail("treasury.errors.reconciliation_not_found")
        try:
            recon.approve(actor_id)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")
        await self._reconciliations.save(recon)
        await self._audit(
            tenant_id=recon.tenant_id,
            reconciliation_id=reconciliation_id,
            action="approved",
            actor_id=actor_id,
        )
        return Result.ok(recon.to_dict())

    async def reject(
        self, reconciliation_id: str, *, actor_id: str, reason: str = ""
    ) -> Result[dict]:
        recon = await self._reconciliations.find_by_id(reconciliation_id)
        if not recon:
            return Result.fail("treasury.errors.reconciliation_not_found")
        try:
            recon.reject(actor_id, reason=reason)
        except ValueError as exc:
            return Result.fail(f"treasury.errors.{exc}")
        await self._reconciliations.save(recon)
        await self._audit(
            tenant_id=recon.tenant_id,
            reconciliation_id=reconciliation_id,
            action="rejected",
            actor_id=actor_id,
            detail=reason,
        )
        return Result.ok(recon.to_dict())

    async def list_reconciliations(self, tenant_id: str) -> Result[list[dict]]:
        recons = await self._reconciliations.list_by_tenant(tenant_id)
        return Result.ok(
            [r.to_dict() for r in sorted(recons, key=lambda x: x.created_at, reverse=True)]
        )

    async def get_reconciliation(self, reconciliation_id: str) -> Result[dict]:
        recon = await self._reconciliations.find_by_id(reconciliation_id)
        if not recon:
            return Result.fail("treasury.errors.reconciliation_not_found")
        return Result.ok(recon.to_dict())

    async def get_audit_trail(self, reconciliation_id: str) -> Result[list[dict]]:
        entries = await self._audits.list_by_reconciliation(reconciliation_id)
        return Result.ok([e.to_dict() for e in entries])

    async def list_audit(self, tenant_id: str) -> Result[list[dict]]:
        entries = await self._audits.list_by_tenant(tenant_id)
        return Result.ok([e.to_dict() for e in entries])
