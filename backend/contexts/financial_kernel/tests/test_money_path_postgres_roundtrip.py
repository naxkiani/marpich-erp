"""Unit — Financial Kernel postgres document round-trip (no live DB)."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.account_types import AccountCategory
from contexts.financial_kernel.domain.aggregates.chart_of_account import ChartOfAccount
from contexts.financial_kernel.domain.aggregates.fiscal_period import FiscalPeriod, FiscalYear
from contexts.financial_kernel.domain.aggregates.journal import Journal
from contexts.financial_kernel.infrastructure.persistence import postgres_store as pg


def test_journal_document_round_trip():
    journal = Journal.create_draft(
        tenant_id="t1",
        organization_id=None,
        branch_id=None,
        fiscal_year_id="fy1",
        period_id="p1",
        source_context="test",
        source_document_id="doc-1",
        idempotency_key="idem-1",
        currency="USD",
        base_currency="USD",
        exchange_rate=1.0,
        lines=[{"account_code": "1000", "debit": 10, "credit": 0}],
        posting_mode="automatic",
        correlation_id="c1",
    )
    restored = pg._journal_from_doc(journal.to_dict())
    assert str(restored.id) == str(journal.id)
    assert restored.idempotency_key == "idem-1"
    assert restored.lines[0]["debit"] == 10


def test_coa_document_round_trip():
    account = ChartOfAccount.create(
        tenant_id="t1",
        code="1000",
        name="Cash",
        account_category=AccountCategory.ASSET,
        account_type="asset",
    )
    restored = pg._coa_from_doc(account.to_dict())
    assert restored.code == "1000"
    assert restored.account_category == AccountCategory.ASSET


def test_fiscal_round_trip():
    year = FiscalYear.create(
        tenant_id="t1",
        organization_id=None,
        name="FY2026",
        start_date="2026-01-01",
        end_date="2026-12-31",
    )
    period = FiscalPeriod.open_period(
        tenant_id="t1",
        organization_id=None,
        branch_id=None,
        fiscal_year_id=str(year.id),
        name="2026-01",
        start_date="2026-01-01",
        end_date="2026-01-31",
    )
    assert pg._year_from_doc(year.to_dict()).name == "FY2026"
    assert pg._period_from_doc(period.to_dict()).fiscal_year_id == str(year.id)
