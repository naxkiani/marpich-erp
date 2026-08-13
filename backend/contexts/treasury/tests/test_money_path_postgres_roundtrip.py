"""Unit — Treasury money-path postgres document round-trip (no live DB)."""
from __future__ import annotations

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
from contexts.treasury.infrastructure.persistence import postgres_store as pg


def test_treasury_account_and_transfer_round_trip():
    account = TreasuryAccount.create(
        tenant_id="t1",
        code="CASH-MAIN",
        name="Main Cash",
        account_type="cash",
        currency="USD",
    )
    account.credit(100.0)
    transfer = TreasuryTransfer.create_draft(
        tenant_id="t1",
        from_account_id=str(account.id),
        to_account_id="acc-2",
        amount=25.5,
        currency="USD",
        instrument="electronic_transfer",
        reference="TRF-001",
    )
    restored_account = pg._account_from_doc(account.to_dict())
    restored_transfer = pg._transfer_from_doc(transfer.to_dict())
    assert restored_account.balance == 100.0
    assert restored_account.code == "CASH-MAIN"
    assert restored_transfer.amount == 25.5
    assert restored_transfer.reference == "TRF-001"


def test_cash_and_bank_account_round_trip():
    location = CashLocation.create(
        tenant_id="t1",
        code="REG-01",
        name="Register 1",
        location_type="cash_register",
        opening_balance=50.0,
    )
    tx = CashTransaction.record(
        tenant_id="t1",
        location_id=str(location.id),
        transaction_type="deposit",
        amount=10.0,
        currency="USD",
        reference="DEP-1",
        direction="in",
    )
    bank = BankAccount.create_draft(
        tenant_id="t1",
        bank_id="bank-1",
        code="BA-001",
        name="Operating",
        account_type="current",
        iban="DE89370400440532013000",
        account_number="32013000",
        opening_balance=1000.0,
        require_approval=False,
    )
    assert pg._cash_location_from_doc(location.to_dict()).balance == 50.0
    assert pg._cash_transaction_from_doc(tx.to_dict()).amount == 10.0
    restored_bank = pg._bank_account_from_doc(bank.to_dict(mask_sensitive=False))
    assert restored_bank.iban == "DE89370400440532013000"
    assert restored_bank.account_number == "32013000"
    assert restored_bank.status == "active"


def test_liquidity_satellites_round_trip():
    pool = CashPool.create(
        tenant_id="t1",
        code="MAIN",
        name="Main Pool",
        target_balance=500.0,
        minimum_balance=100.0,
        member_account_ids=["acc-1"],
    )
    snapshot = LiquiditySnapshot.create(
        tenant_id="t1",
        period_type="daily",
        as_of_date="2026-08-01",
        currency="USD",
        opening_balance=100.0,
        closing_balance=150.0,
        total_inflow=75.0,
        total_outflow=25.0,
        liquidity_gap=0.0,
        working_capital=150.0,
        lines=[{"account_id": "acc-1", "balance": 150.0}],
    )
    need = FundingNeed.create(
        tenant_id="t1",
        label="Payroll",
        currency="USD",
        required_amount=200.0,
        available_amount=150.0,
        due_date="2026-08-15",
    )
    assert pg._cash_pool_from_doc(pool.to_dict()).member_account_ids == ["acc-1"]
    assert pg._liquidity_snapshot_from_doc(snapshot.to_dict()).as_of_date == "2026-08-01"
    assert pg._funding_need_from_doc(need.to_dict()).gap_amount == 50.0


def test_reconciliation_satellites_round_trip():
    statement = BankStatementImport.create(
        tenant_id="t1",
        treasury_account_id="acc-1",
        source="file_import",
        statement_date="2026-08-01",
        statement_balance=100.0,
        items=[{"reference": "DEP-1", "amount": 100.0}],
    )
    reconciliation = EnterpriseBankReconciliation.create(
        tenant_id="t1",
        treasury_account_id="acc-1",
        statement_import_id=str(statement.id),
        reconciliation_date="2026-08-01",
        statement_balance=100.0,
        book_balance=100.0,
        matched_pairs=[{"statement_ref": "DEP-1", "book_ref": "DEP-1"}],
        unmatched_statement=[],
        unmatched_book=[],
        duplicates=[],
        exceptions=[],
        outstanding_transactions=[],
        ai_suggestions=[],
        report_summary={"matched": 1},
    )
    bank_audit = ReconciliationAuditEntry.create(
        tenant_id="t1",
        reconciliation_id=str(reconciliation.id),
        action="created",
        payload={"source": "test"},
    )
    cash_run = CashReconciliationRun.create(
        tenant_id="t1",
        location_id="location-1",
        branch_id="branch-1",
        closing_type="cash_closing",
        system_balance=50.0,
        counted_amount=50.0,
        currency="USD",
    )
    cash_audit = CashReconciliationAudit.create(
        tenant_id="t1",
        reconciliation_id=str(cash_run.id),
        action="counted",
    )
    assert pg._bank_statement_import_from_doc(statement.to_dict()).items[0]["reference"] == "DEP-1"
    assert pg._bank_reconciliation_from_doc(reconciliation.to_dict()).status == "matched"
    assert pg._reconciliation_audit_from_doc(bank_audit.to_dict()).payload == {"source": "test"}
    assert pg._cash_reconciliation_run_from_doc(cash_run.to_dict()).branch_id == "branch-1"
    assert pg._cash_reconciliation_audit_from_doc(cash_audit.to_dict()).action == "counted"
