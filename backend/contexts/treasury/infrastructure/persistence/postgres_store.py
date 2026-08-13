"""PostgreSQL repositories — Treasury money-path (accounts / transfers / cash / bank accounts)."""
from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select

from contexts.treasury.domain.aggregates.bank_account import BankAccount
from contexts.treasury.domain.aggregates.bank_reconciliation_engine import (
    BankStatementImport,
    EnterpriseBankReconciliation,
    ReconciliationAuditEntry,
)
from contexts.treasury.domain.aggregates.cash_management import CashLocation, CashTransaction
from contexts.treasury.domain.aggregates.cash_reconciliation_engine import (
    CashReconciliationAudit,
    CashReconciliationRun,
)
from contexts.treasury.domain.aggregates.liquidity_engine import (
    CashPool,
    FundingNeed,
    LiquiditySnapshot,
)
from contexts.treasury.domain.aggregates.treasury_account import TreasuryAccount
from contexts.treasury.domain.aggregates.treasury_transfer import TreasuryTransfer
from contexts.treasury.domain.ports.bank_account_repositories import IBankAccountRepository
from contexts.treasury.domain.ports.cash_management_repositories import (
    ICashLocationRepository,
    ICashTransactionRepository,
)
from contexts.treasury.domain.ports.repositories import (
    ITreasuryAccountRepository,
    ITreasuryTransferRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    TreasuryAccountRow,
    TreasuryBankAccountRow,
    TreasuryBankReconciliationAuditRow,
    TreasuryBankReconciliationRow,
    TreasuryBankStatementImportRow,
    TreasuryCashPoolRow,
    TreasuryCashReconciliationAuditRow,
    TreasuryCashReconciliationRunRow,
    TreasuryCashLocationRow,
    TreasuryCashTransactionRow,
    TreasuryFundingNeedRow,
    TreasuryLiquiditySnapshotRow,
    TreasuryTransferRow,
)


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _account_from_doc(doc: dict) -> TreasuryAccount:
    return TreasuryAccount(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        code=str(doc["code"]),
        name=str(doc.get("name") or ""),
        account_type=str(doc.get("account_type") or "cash"),
        currency=str(doc.get("currency") or "USD"),
        balance=float(doc.get("balance") or 0.0),
        bank_name=doc.get("bank_name"),
        account_number=doc.get("account_number"),
        is_active=bool(doc.get("is_active", True)),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _transfer_from_doc(doc: dict) -> TreasuryTransfer:
    return TreasuryTransfer(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        from_account_id=str(doc["from_account_id"]),
        to_account_id=str(doc["to_account_id"]),
        amount=float(doc.get("amount") or 0.0),
        currency=str(doc.get("currency") or "USD"),
        instrument=str(doc.get("instrument") or "cash"),
        status=str(doc.get("status") or "draft"),
        reference=str(doc.get("reference") or ""),
        description=doc.get("description"),
        cheque_number=doc.get("cheque_number"),
        workflow_instance_id=doc.get("workflow_instance_id"),
        executed_at=_parse_dt(doc.get("executed_at")),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _cash_location_from_doc(doc: dict) -> CashLocation:
    return CashLocation(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        organization_id=doc.get("organization_id"),
        branch_id=doc.get("branch_id"),
        department_id=doc.get("department_id"),
        code=str(doc["code"]),
        name=str(doc.get("name") or ""),
        location_type=str(doc.get("location_type") or "cash_register"),
        currency=str(doc.get("currency") or "USD"),
        balance=float(doc.get("balance") or 0.0),
        status=str(doc.get("status") or "active"),
        gl_account_code=doc.get("gl_account_code"),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _cash_transaction_from_doc(doc: dict) -> CashTransaction:
    return CashTransaction(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        organization_id=doc.get("organization_id"),
        location_id=str(doc["location_id"]),
        transaction_type=str(doc.get("transaction_type") or "deposit"),
        amount=float(doc.get("amount") or 0.0),
        currency=str(doc.get("currency") or "USD"),
        reference=str(doc.get("reference") or ""),
        description=doc.get("description"),
        counterpart_location_id=doc.get("counterpart_location_id"),
        direction=str(doc.get("direction") or "in"),
        created_by=doc.get("created_by"),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _bank_account_from_doc(doc: dict) -> BankAccount:
    return BankAccount(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        organization_id=doc.get("organization_id"),
        bank_id=str(doc["bank_id"]),
        branch_id=doc.get("branch_id"),
        code=str(doc["code"]),
        name=str(doc.get("name") or ""),
        account_type=str(doc.get("account_type") or "current"),
        currency=str(doc.get("currency") or "USD"),
        iban=doc.get("iban"),
        swift_bic=doc.get("swift_bic"),
        routing_number=doc.get("routing_number"),
        account_number=doc.get("account_number"),
        virtual_account_ref=doc.get("virtual_account_ref"),
        gl_account_code=doc.get("gl_account_code"),
        status=str(doc.get("status") or "draft"),
        balance=float(doc.get("balance") or 0.0),
        workflow_instance_id=doc.get("workflow_instance_id"),
        approved_by=doc.get("approved_by"),
        approved_at=_parse_dt(doc.get("approved_at")),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _cash_pool_from_doc(doc: dict) -> CashPool:
    return CashPool(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        code=str(doc["code"]),
        name=str(doc.get("name") or ""),
        currency=str(doc.get("currency") or "USD"),
        target_balance=float(doc.get("target_balance") or 0.0),
        minimum_balance=float(doc.get("minimum_balance") or 0.0),
        member_account_ids=list(doc.get("member_account_ids") or []),
        status=str(doc.get("status") or "active"),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _liquidity_snapshot_from_doc(doc: dict) -> LiquiditySnapshot:
    return LiquiditySnapshot(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        period_type=str(doc["period_type"]),
        as_of_date=str(doc["as_of_date"]),
        currency=str(doc.get("currency") or "USD"),
        opening_balance=float(doc.get("opening_balance") or 0.0),
        closing_balance=float(doc.get("closing_balance") or 0.0),
        total_inflow=float(doc.get("total_inflow") or 0.0),
        total_outflow=float(doc.get("total_outflow") or 0.0),
        liquidity_gap=float(doc.get("liquidity_gap") or 0.0),
        working_capital=float(doc.get("working_capital") or 0.0),
        lines=list(doc.get("lines") or []),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _funding_need_from_doc(doc: dict) -> FundingNeed:
    return FundingNeed(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        label=str(doc.get("label") or ""),
        currency=str(doc.get("currency") or "USD"),
        required_amount=float(doc.get("required_amount") or 0.0),
        available_amount=float(doc.get("available_amount") or 0.0),
        gap_amount=float(doc.get("gap_amount") or 0.0),
        due_date=str(doc.get("due_date") or ""),
        status=str(doc.get("status") or "open"),
        source=str(doc.get("source") or "liquidity_engine"),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _bank_statement_import_from_doc(doc: dict) -> BankStatementImport:
    return BankStatementImport(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        treasury_account_id=str(doc["treasury_account_id"]),
        source=str(doc.get("source") or "manual"),
        statement_date=str(doc.get("statement_date") or ""),
        statement_balance=float(doc.get("statement_balance") or 0.0),
        items=list(doc.get("items") or []),
        status=str(doc.get("status") or "imported"),
        imported_at=_parse_dt(doc.get("imported_at")) or datetime.now(UTC),
    )


def _bank_reconciliation_from_doc(doc: dict) -> EnterpriseBankReconciliation:
    return EnterpriseBankReconciliation(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        treasury_account_id=str(doc["treasury_account_id"]),
        statement_import_id=doc.get("statement_import_id"),
        reconciliation_date=str(doc.get("reconciliation_date") or ""),
        statement_balance=float(doc.get("statement_balance") or 0.0),
        book_balance=float(doc.get("book_balance") or 0.0),
        matched_pairs=list(doc.get("matched_pairs") or []),
        unmatched_statement=list(doc.get("unmatched_statement") or []),
        unmatched_book=list(doc.get("unmatched_book") or []),
        duplicates=list(doc.get("duplicates") or []),
        exceptions=list(doc.get("exceptions") or []),
        outstanding_transactions=list(doc.get("outstanding_transactions") or []),
        ai_suggestions=list(doc.get("ai_suggestions") or []),
        report_summary=dict(doc.get("report_summary") or {}),
        variance=float(doc.get("variance") or 0.0),
        status=str(doc.get("status") or "draft"),
        approval_status=str(doc.get("approval_status") or "none"),
        submitted_by=doc.get("submitted_by"),
        approved_by=doc.get("approved_by"),
        rejection_reason=str(doc.get("rejection_reason") or ""),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
        updated_at=_parse_dt(doc.get("updated_at")) or datetime.now(UTC),
    )


def _reconciliation_audit_from_doc(doc: dict) -> ReconciliationAuditEntry:
    return ReconciliationAuditEntry(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        reconciliation_id=str(doc["reconciliation_id"]),
        action=str(doc.get("action") or ""),
        actor_id=doc.get("actor_id"),
        detail=str(doc.get("detail") or ""),
        payload=dict(doc.get("payload") or {}),
        occurred_at=_parse_dt(doc.get("occurred_at")) or datetime.now(UTC),
    )


def _cash_reconciliation_run_from_doc(doc: dict) -> CashReconciliationRun:
    return CashReconciliationRun(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        location_id=str(doc["location_id"]),
        branch_id=doc.get("branch_id"),
        closing_type=str(doc.get("closing_type") or "cash_closing"),
        system_balance=float(doc.get("system_balance") or 0.0),
        counted_amount=float(doc.get("counted_amount") or 0.0),
        variance=float(doc.get("variance") or 0.0),
        variance_type=str(doc.get("variance_type") or "balanced"),
        currency=str(doc.get("currency") or "USD"),
        status=str(doc.get("status") or "draft"),
        requires_manager_approval=bool(doc.get("requires_manager_approval", False)),
        counted_by=doc.get("counted_by"),
        verified_by=doc.get("verified_by"),
        approved_by=doc.get("approved_by"),
        rejection_reason=str(doc.get("rejection_reason") or ""),
        ai_anomalies=list(doc.get("ai_anomalies") or []),
        discrepancy_report=dict(doc.get("discrepancy_report") or {}),
        notes=doc.get("notes"),
        closed_at=_parse_dt(doc.get("closed_at")),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
        updated_at=_parse_dt(doc.get("updated_at")) or datetime.now(UTC),
    )


def _cash_reconciliation_audit_from_doc(doc: dict) -> CashReconciliationAudit:
    return CashReconciliationAudit(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        reconciliation_id=str(doc["reconciliation_id"]),
        action=str(doc.get("action") or ""),
        actor_id=doc.get("actor_id"),
        detail=str(doc.get("detail") or ""),
        occurred_at=_parse_dt(doc.get("occurred_at")) or datetime.now(UTC),
    )


class PostgresTreasuryAccountRepository(ITreasuryAccountRepository):
    async def save(self, account: TreasuryAccount) -> None:
        doc = account.to_dict()
        async with session_scope() as session:
            row = await session.get(TreasuryAccountRow, UUID(str(account.id)))
            if row is None:
                session.add(
                    TreasuryAccountRow(
                        id=UUID(str(account.id)),
                        tenant_id=account.tenant_id,
                        code=account.code,
                        account_type=account.account_type,
                        currency=account.currency,
                        document=doc,
                        updated_at=datetime.now(UTC),
                    )
                )
            else:
                row.code = account.code
                row.account_type = account.account_type
                row.currency = account.currency
                row.document = doc
                row.updated_at = datetime.now(UTC)

    async def find_by_id(self, account_id: str) -> TreasuryAccount | None:
        async with session_scope() as session:
            row = await session.get(TreasuryAccountRow, UUID(account_id))
            return _account_from_doc(row.document) if row else None

    async def find_by_code(self, tenant_id: str, code: str) -> TreasuryAccount | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(TreasuryAccountRow).where(
                    TreasuryAccountRow.tenant_id == tenant_id,
                    TreasuryAccountRow.code == code.upper(),
                )
            )
            return _account_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryAccount]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(TreasuryAccountRow).where(TreasuryAccountRow.tenant_id == tenant_id)
                )
            ).all()
        return [_account_from_doc(r.document) for r in rows]


class PostgresTreasuryTransferRepository(ITreasuryTransferRepository):
    async def save(self, transfer: TreasuryTransfer) -> None:
        doc = transfer.to_dict()
        async with session_scope() as session:
            row = await session.get(TreasuryTransferRow, UUID(str(transfer.id)))
            if row is None:
                session.add(
                    TreasuryTransferRow(
                        id=UUID(str(transfer.id)),
                        tenant_id=transfer.tenant_id,
                        reference=transfer.reference,
                        status=transfer.status,
                        from_account_id=transfer.from_account_id,
                        to_account_id=transfer.to_account_id,
                        document=doc,
                        created_at=transfer.created_at,
                    )
                )
            else:
                row.reference = transfer.reference
                row.status = transfer.status
                row.from_account_id = transfer.from_account_id
                row.to_account_id = transfer.to_account_id
                row.document = doc

    async def find_by_id(self, transfer_id: str) -> TreasuryTransfer | None:
        async with session_scope() as session:
            row = await session.get(TreasuryTransferRow, UUID(transfer_id))
            return _transfer_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[TreasuryTransfer]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(TreasuryTransferRow).where(TreasuryTransferRow.tenant_id == tenant_id)
                )
            ).all()
        return [_transfer_from_doc(r.document) for r in rows]


class PostgresCashLocationRepository(ICashLocationRepository):
    async def save(self, location: CashLocation) -> None:
        doc = location.to_dict()
        async with session_scope() as session:
            row = await session.get(TreasuryCashLocationRow, UUID(str(location.id)))
            if row is None:
                session.add(
                    TreasuryCashLocationRow(
                        id=UUID(str(location.id)),
                        tenant_id=location.tenant_id,
                        code=location.code,
                        status=location.status,
                        currency=location.currency,
                        document=doc,
                        updated_at=datetime.now(UTC),
                    )
                )
            else:
                row.code = location.code
                row.status = location.status
                row.currency = location.currency
                row.document = doc
                row.updated_at = datetime.now(UTC)

    async def find_by_id(self, location_id: str) -> CashLocation | None:
        async with session_scope() as session:
            row = await session.get(TreasuryCashLocationRow, UUID(location_id))
            return _cash_location_from_doc(row.document) if row else None

    async def find_by_code(self, tenant_id: str, code: str) -> CashLocation | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(TreasuryCashLocationRow).where(
                    TreasuryCashLocationRow.tenant_id == tenant_id,
                    TreasuryCashLocationRow.code == code.upper(),
                )
            )
            return _cash_location_from_doc(row.document) if row else None

    async def list_by_tenant(
        self, tenant_id: str, organization_id: str | None = None
    ) -> list[CashLocation]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(TreasuryCashLocationRow).where(
                        TreasuryCashLocationRow.tenant_id == tenant_id
                    )
                )
            ).all()
        locs = [_cash_location_from_doc(r.document) for r in rows]
        if organization_id:
            locs = [loc for loc in locs if loc.organization_id == organization_id]
        return locs


class PostgresCashTransactionRepository(ICashTransactionRepository):
    async def save(self, transaction: CashTransaction) -> None:
        doc = transaction.to_dict()
        async with session_scope() as session:
            row = await session.get(TreasuryCashTransactionRow, UUID(str(transaction.id)))
            if row is None:
                session.add(
                    TreasuryCashTransactionRow(
                        id=UUID(str(transaction.id)),
                        tenant_id=transaction.tenant_id,
                        location_id=transaction.location_id,
                        transaction_type=transaction.transaction_type,
                        document=doc,
                        created_at=transaction.created_at,
                    )
                )
            else:
                row.location_id = transaction.location_id
                row.transaction_type = transaction.transaction_type
                row.document = doc

    async def find_by_id(self, transaction_id: str) -> CashTransaction | None:
        async with session_scope() as session:
            row = await session.get(TreasuryCashTransactionRow, UUID(transaction_id))
            return _cash_transaction_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[CashTransaction]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(TreasuryCashTransactionRow).where(
                        TreasuryCashTransactionRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_cash_transaction_from_doc(r.document) for r in rows]

    async def list_by_location(self, location_id: str) -> list[CashTransaction]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(TreasuryCashTransactionRow).where(
                        TreasuryCashTransactionRow.location_id == location_id
                    )
                )
            ).all()
        return [_cash_transaction_from_doc(r.document) for r in rows]


class PostgresBankAccountRepository(IBankAccountRepository):
    async def save(self, account: BankAccount) -> None:
        # Persist unmasked sensitive fields for SoR reconstruction.
        doc = account.to_dict(mask_sensitive=False)
        async with session_scope() as session:
            row = await session.get(TreasuryBankAccountRow, UUID(str(account.id)))
            if row is None:
                session.add(
                    TreasuryBankAccountRow(
                        id=UUID(str(account.id)),
                        tenant_id=account.tenant_id,
                        bank_id=account.bank_id,
                        code=account.code,
                        status=account.status,
                        currency=account.currency,
                        document=doc,
                        updated_at=datetime.now(UTC),
                    )
                )
            else:
                row.bank_id = account.bank_id
                row.code = account.code
                row.status = account.status
                row.currency = account.currency
                row.document = doc
                row.updated_at = datetime.now(UTC)

    async def find_by_id(self, account_id: str) -> BankAccount | None:
        async with session_scope() as session:
            row = await session.get(TreasuryBankAccountRow, UUID(account_id))
            return _bank_account_from_doc(row.document) if row else None

    async def find_by_code(self, tenant_id: str, code: str) -> BankAccount | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(TreasuryBankAccountRow).where(
                    TreasuryBankAccountRow.tenant_id == tenant_id,
                    TreasuryBankAccountRow.code == code.upper(),
                )
            )
            return _bank_account_from_doc(row.document) if row else None

    async def list_by_tenant(
        self, tenant_id: str, organization_id: str | None = None
    ) -> list[BankAccount]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(TreasuryBankAccountRow).where(
                        TreasuryBankAccountRow.tenant_id == tenant_id
                    )
                )
            ).all()
        accounts = [_bank_account_from_doc(r.document) for r in rows]
        if organization_id:
            accounts = [a for a in accounts if a.organization_id == organization_id]
        return accounts

    async def list_by_bank(self, tenant_id: str, bank_id: str) -> list[BankAccount]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(TreasuryBankAccountRow).where(
                        TreasuryBankAccountRow.tenant_id == tenant_id,
                        TreasuryBankAccountRow.bank_id == bank_id,
                    )
                )
            ).all()
        return [_bank_account_from_doc(r.document) for r in rows]


class PostgresCashPoolRepository:
    async def save(self, pool: CashPool) -> None:
        doc = pool.to_dict()
        async with session_scope() as session:
            row = await session.get(TreasuryCashPoolRow, UUID(str(pool.id)))
            if row is None:
                session.add(TreasuryCashPoolRow(id=UUID(str(pool.id)), tenant_id=pool.tenant_id, code=pool.code, status=pool.status, document=doc))
            else:
                row.code, row.status, row.document = pool.code, pool.status, doc

    async def find_by_id(self, pool_id: str) -> CashPool | None:
        async with session_scope() as session:
            row = await session.get(TreasuryCashPoolRow, UUID(pool_id))
            return _cash_pool_from_doc(row.document) if row else None

    async def find_by_code(self, tenant_id: str, code: str) -> CashPool | None:
        async with session_scope() as session:
            row = await session.scalar(select(TreasuryCashPoolRow).where(TreasuryCashPoolRow.tenant_id == tenant_id, TreasuryCashPoolRow.code == code.upper()))
            return _cash_pool_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[CashPool]:
        async with session_scope() as session:
            rows = (await session.scalars(select(TreasuryCashPoolRow).where(TreasuryCashPoolRow.tenant_id == tenant_id))).all()
        return [_cash_pool_from_doc(row.document) for row in rows]


class PostgresLiquiditySnapshotRepository:
    async def save(self, snapshot: LiquiditySnapshot) -> None:
        doc = snapshot.to_dict()
        async with session_scope() as session:
            row = await session.get(TreasuryLiquiditySnapshotRow, UUID(str(snapshot.id)))
            if row is None:
                session.add(TreasuryLiquiditySnapshotRow(id=UUID(str(snapshot.id)), tenant_id=snapshot.tenant_id, period_type=snapshot.period_type, as_of_date=snapshot.as_of_date, document=doc))
            else:
                row.period_type, row.as_of_date, row.document = snapshot.period_type, snapshot.as_of_date, doc

    async def list_by_tenant(self, tenant_id: str) -> list[LiquiditySnapshot]:
        async with session_scope() as session:
            rows = (await session.scalars(select(TreasuryLiquiditySnapshotRow).where(TreasuryLiquiditySnapshotRow.tenant_id == tenant_id))).all()
        return [_liquidity_snapshot_from_doc(row.document) for row in rows]


class PostgresFundingNeedRepository:
    async def save(self, need: FundingNeed) -> None:
        doc = need.to_dict()
        async with session_scope() as session:
            row = await session.get(TreasuryFundingNeedRow, UUID(str(need.id)))
            if row is None:
                session.add(TreasuryFundingNeedRow(id=UUID(str(need.id)), tenant_id=need.tenant_id, status=need.status, document=doc))
            else:
                row.status, row.document = need.status, doc

    async def list_by_tenant(self, tenant_id: str) -> list[FundingNeed]:
        async with session_scope() as session:
            rows = (await session.scalars(select(TreasuryFundingNeedRow).where(TreasuryFundingNeedRow.tenant_id == tenant_id))).all()
        return [_funding_need_from_doc(row.document) for row in rows]


class PostgresBankStatementImportRepository:
    async def save(self, statement: BankStatementImport) -> None:
        doc = statement.to_dict()
        async with session_scope() as session:
            row = await session.get(TreasuryBankStatementImportRow, UUID(str(statement.id)))
            if row is None:
                session.add(TreasuryBankStatementImportRow(id=UUID(str(statement.id)), tenant_id=statement.tenant_id, treasury_account_id=statement.treasury_account_id, status=statement.status, document=doc))
            else:
                row.treasury_account_id, row.status, row.document = statement.treasury_account_id, statement.status, doc

    async def find_by_id(self, statement_id: str) -> BankStatementImport | None:
        async with session_scope() as session:
            row = await session.get(TreasuryBankStatementImportRow, UUID(statement_id))
            return _bank_statement_import_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[BankStatementImport]:
        async with session_scope() as session:
            rows = (await session.scalars(select(TreasuryBankStatementImportRow).where(TreasuryBankStatementImportRow.tenant_id == tenant_id))).all()
        return [_bank_statement_import_from_doc(row.document) for row in rows]


class PostgresEnterpriseBankReconciliationRepository:
    async def save(self, reconciliation: EnterpriseBankReconciliation) -> None:
        doc = reconciliation.to_dict()
        async with session_scope() as session:
            row = await session.get(TreasuryBankReconciliationRow, UUID(str(reconciliation.id)))
            if row is None:
                session.add(TreasuryBankReconciliationRow(id=UUID(str(reconciliation.id)), tenant_id=reconciliation.tenant_id, treasury_account_id=reconciliation.treasury_account_id, status=reconciliation.status, document=doc))
            else:
                row.treasury_account_id, row.status, row.document = reconciliation.treasury_account_id, reconciliation.status, doc

    async def find_by_id(self, reconciliation_id: str) -> EnterpriseBankReconciliation | None:
        async with session_scope() as session:
            row = await session.get(TreasuryBankReconciliationRow, UUID(reconciliation_id))
            return _bank_reconciliation_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[EnterpriseBankReconciliation]:
        async with session_scope() as session:
            rows = (await session.scalars(select(TreasuryBankReconciliationRow).where(TreasuryBankReconciliationRow.tenant_id == tenant_id))).all()
        return [_bank_reconciliation_from_doc(row.document) for row in rows]


class PostgresReconciliationAuditRepository:
    async def save(self, entry: ReconciliationAuditEntry) -> None:
        doc = entry.to_dict()
        async with session_scope() as session:
            row = await session.get(TreasuryBankReconciliationAuditRow, UUID(str(entry.id)))
            if row is None:
                session.add(TreasuryBankReconciliationAuditRow(id=UUID(str(entry.id)), tenant_id=entry.tenant_id, reconciliation_id=entry.reconciliation_id, document=doc))
            else:
                row.reconciliation_id, row.document = entry.reconciliation_id, doc

    async def list_by_reconciliation(self, reconciliation_id: str) -> list[ReconciliationAuditEntry]:
        async with session_scope() as session:
            rows = (await session.scalars(select(TreasuryBankReconciliationAuditRow).where(TreasuryBankReconciliationAuditRow.reconciliation_id == reconciliation_id))).all()
        return [_reconciliation_audit_from_doc(row.document) for row in rows]

    async def list_by_tenant(self, tenant_id: str) -> list[ReconciliationAuditEntry]:
        async with session_scope() as session:
            rows = (await session.scalars(select(TreasuryBankReconciliationAuditRow).where(TreasuryBankReconciliationAuditRow.tenant_id == tenant_id))).all()
        return [_reconciliation_audit_from_doc(row.document) for row in rows]


class PostgresCashReconciliationRunRepository:
    async def save(self, run: CashReconciliationRun) -> None:
        doc = run.to_dict()
        async with session_scope() as session:
            row = await session.get(TreasuryCashReconciliationRunRow, UUID(str(run.id)))
            if row is None:
                session.add(TreasuryCashReconciliationRunRow(id=UUID(str(run.id)), tenant_id=run.tenant_id, location_id=run.location_id, branch_id=run.branch_id, status=run.status, document=doc))
            else:
                row.location_id, row.branch_id, row.status, row.document = run.location_id, run.branch_id, run.status, doc

    async def find_by_id(self, run_id: str) -> CashReconciliationRun | None:
        async with session_scope() as session:
            row = await session.get(TreasuryCashReconciliationRunRow, UUID(run_id))
            return _cash_reconciliation_run_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[CashReconciliationRun]:
        async with session_scope() as session:
            rows = (await session.scalars(select(TreasuryCashReconciliationRunRow).where(TreasuryCashReconciliationRunRow.tenant_id == tenant_id))).all()
        return [_cash_reconciliation_run_from_doc(row.document) for row in rows]

    async def list_by_location(self, location_id: str) -> list[CashReconciliationRun]:
        async with session_scope() as session:
            rows = (await session.scalars(select(TreasuryCashReconciliationRunRow).where(TreasuryCashReconciliationRunRow.location_id == location_id))).all()
        return [_cash_reconciliation_run_from_doc(row.document) for row in rows]

    async def list_by_branch(self, tenant_id: str, branch_id: str) -> list[CashReconciliationRun]:
        async with session_scope() as session:
            rows = (await session.scalars(select(TreasuryCashReconciliationRunRow).where(TreasuryCashReconciliationRunRow.tenant_id == tenant_id, TreasuryCashReconciliationRunRow.branch_id == branch_id))).all()
        return [_cash_reconciliation_run_from_doc(row.document) for row in rows]


class PostgresCashReconciliationAuditRepository:
    async def save(self, entry: CashReconciliationAudit) -> None:
        doc = entry.to_dict()
        async with session_scope() as session:
            row = await session.get(TreasuryCashReconciliationAuditRow, UUID(str(entry.id)))
            if row is None:
                session.add(TreasuryCashReconciliationAuditRow(id=UUID(str(entry.id)), tenant_id=entry.tenant_id, reconciliation_id=entry.reconciliation_id, document=doc))
            else:
                row.reconciliation_id, row.document = entry.reconciliation_id, doc

    async def list_by_reconciliation(self, reconciliation_id: str) -> list[CashReconciliationAudit]:
        async with session_scope() as session:
            rows = (await session.scalars(select(TreasuryCashReconciliationAuditRow).where(TreasuryCashReconciliationAuditRow.reconciliation_id == reconciliation_id))).all()
        return [_cash_reconciliation_audit_from_doc(row.document) for row in rows]

    async def list_by_tenant(self, tenant_id: str) -> list[CashReconciliationAudit]:
        async with session_scope() as session:
            rows = (await session.scalars(select(TreasuryCashReconciliationAuditRow).where(TreasuryCashReconciliationAuditRow.tenant_id == tenant_id))).all()
        return [_cash_reconciliation_audit_from_doc(row.document) for row in rows]
