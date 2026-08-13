"""PostgreSQL repositories — Financial Kernel money-path (CoA / Journal / Fiscal)."""
from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select

from contexts.financial_kernel.domain.aggregates.account_types import AccountCategory
from contexts.financial_kernel.domain.aggregates.chart_of_account import (
    ChartOfAccount,
    TemplateSource,
)
from contexts.financial_kernel.domain.aggregates.fiscal_period import FiscalPeriod, FiscalYear
from contexts.financial_kernel.domain.aggregates.journal import Journal
from contexts.financial_kernel.domain.ports.repositories import (
    IChartOfAccountRepository,
    IFiscalPeriodRepository,
    IFiscalYearRepository,
    IJournalRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    FinancialKernelChartOfAccountRow,
    FinancialKernelFiscalPeriodRow,
    FinancialKernelFiscalYearRow,
    FinancialKernelJournalRow,
)


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _journal_from_doc(doc: dict) -> Journal:
    return Journal(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        organization_id=doc.get("organization_id"),
        branch_id=doc.get("branch_id"),
        fiscal_year_id=doc.get("fiscal_year_id"),
        period_id=doc.get("period_id"),
        source_context=str(doc.get("source_context") or ""),
        source_document_id=str(doc.get("source_document_id") or ""),
        idempotency_key=str(doc["idempotency_key"]),
        currency=str(doc.get("currency") or "USD"),
        base_currency=str(doc.get("base_currency") or "USD"),
        exchange_rate=float(doc.get("exchange_rate") or 1.0),
        lines=list(doc.get("lines") or []),
        posting_mode=str(doc.get("posting_mode") or "automatic"),
        journal_entry_type=str(doc.get("journal_entry_type") or "standard"),
        status=str(doc.get("status") or "draft"),
        reporting_currency=str(doc.get("reporting_currency") or ""),
        reporting_exchange_rate=float(doc.get("reporting_exchange_rate") or 1.0),
        rate_snapshot_id=doc.get("rate_snapshot_id"),
        rate_type=str(doc.get("rate_type") or "spot"),
        correlation_id=str(doc.get("correlation_id") or ""),
        reverses_journal_id=doc.get("reverses_journal_id"),
        reversed_by_journal_id=doc.get("reversed_by_journal_id"),
        recurring_template_id=doc.get("recurring_template_id"),
        journal_type=str(doc.get("journal_type") or "general"),
        version=int(doc.get("version") or 1),
        parent_version_id=doc.get("parent_version_id"),
        is_locked=bool(doc.get("is_locked") or False),
        locked_at=_parse_dt(doc.get("locked_at")),
        digital_signature=doc.get("digital_signature"),
        ai_review=doc.get("ai_review"),
        approval_workflow_id=doc.get("approval_workflow_id"),
        batch_id=doc.get("batch_id"),
        immutable_hash=str(doc.get("immutable_hash") or ""),
        posted_at=_parse_dt(doc.get("posted_at")),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _coa_from_doc(doc: dict) -> ChartOfAccount:
    return ChartOfAccount(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        code=str(doc["code"]),
        name=str(doc.get("name") or ""),
        account_category=AccountCategory(str(doc.get("account_category") or "asset")),
        account_type=str(doc.get("account_type") or "asset"),
        account_key=doc.get("account_key"),
        parent_account_id=doc.get("parent_account_id"),
        tree_id=doc.get("tree_id"),
        level=int(doc.get("level") or 0),
        tree_path=str(doc.get("tree_path") or ""),
        display_order=int(doc.get("display_order") or 0),
        account_group=doc.get("account_group"),
        is_posting=bool(doc.get("is_posting", True)),
        balance=float(doc.get("balance") or 0.0),
        statistical_balance=float(doc.get("statistical_balance") or 0.0),
        cost_center=doc.get("cost_center"),
        profit_center=doc.get("profit_center"),
        template_source=TemplateSource(str(doc.get("template_source") or "tenant")),
        template_key=doc.get("template_key"),
        country_code=doc.get("country_code"),
        currency=doc.get("currency"),
        is_control_account=bool(doc.get("is_control_account") or False),
        reconciliation_required=bool(doc.get("reconciliation_required") or False),
        tax_code=doc.get("tax_code"),
        budget_code=doc.get("budget_code"),
        status=str(doc.get("status") or "active"),
        effective_date=doc.get("effective_date"),
        is_active=bool(doc.get("is_active", True)),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _year_from_doc(doc: dict) -> FiscalYear:
    return FiscalYear(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        organization_id=doc.get("organization_id"),
        calendar_id=doc.get("calendar_id"),
        name=str(doc.get("name") or ""),
        start_date=str(doc.get("start_date") or ""),
        end_date=str(doc.get("end_date") or ""),
        status=str(doc.get("status") or "open"),
        close_level=str(doc.get("close_level") or "none"),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


def _period_from_doc(doc: dict) -> FiscalPeriod:
    return FiscalPeriod(
        id=UniqueId.from_string(str(doc["id"])),
        tenant_id=str(doc["tenant_id"]),
        organization_id=doc.get("organization_id"),
        branch_id=doc.get("branch_id"),
        fiscal_year_id=str(doc["fiscal_year_id"]),
        calendar_id=doc.get("calendar_id"),
        name=str(doc.get("name") or ""),
        start_date=str(doc.get("start_date") or ""),
        end_date=str(doc.get("end_date") or ""),
        status=str(doc.get("status") or "open"),
        period_type=str(doc.get("period_type") or "monthly"),
        close_level=str(doc.get("close_level") or "none"),
        period_number=int(doc.get("period_number") or 1),
        is_adjustment=bool(doc.get("is_adjustment") or False),
        is_financially_locked=bool(doc.get("is_financially_locked") or False),
        locked_at=_parse_dt(doc.get("locked_at")),
        created_at=_parse_dt(doc.get("created_at")) or datetime.now(UTC),
    )


class PostgresChartOfAccountRepository(IChartOfAccountRepository):
    async def save(self, account: ChartOfAccount) -> None:
        doc = account.to_dict()
        async with session_scope() as session:
            row = await session.get(FinancialKernelChartOfAccountRow, UUID(str(account.id)))
            if row is None:
                session.add(
                    FinancialKernelChartOfAccountRow(
                        id=UUID(str(account.id)),
                        tenant_id=account.tenant_id,
                        code=account.code,
                        account_key=account.account_key,
                        parent_account_id=account.parent_account_id,
                        tree_id=account.tree_id,
                        document=doc,
                    )
                )
            else:
                row.code = account.code
                row.account_key = account.account_key
                row.parent_account_id = account.parent_account_id
                row.tree_id = account.tree_id
                row.document = doc

    async def list_by_tenant(self, tenant_id: str) -> list[ChartOfAccount]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(FinancialKernelChartOfAccountRow).where(
                        FinancialKernelChartOfAccountRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_coa_from_doc(r.document) for r in rows]

    async def find_by_id(self, account_id: str) -> ChartOfAccount | None:
        async with session_scope() as session:
            row = await session.get(FinancialKernelChartOfAccountRow, UUID(account_id))
            return _coa_from_doc(row.document) if row else None

    async def find_by_code(self, tenant_id: str, code: str) -> ChartOfAccount | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(FinancialKernelChartOfAccountRow).where(
                    FinancialKernelChartOfAccountRow.tenant_id == tenant_id,
                    FinancialKernelChartOfAccountRow.code == code,
                )
            )
            return _coa_from_doc(row.document) if row else None

    async def find_by_key(self, tenant_id: str, account_key: str) -> ChartOfAccount | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(FinancialKernelChartOfAccountRow).where(
                    FinancialKernelChartOfAccountRow.tenant_id == tenant_id,
                    FinancialKernelChartOfAccountRow.account_key == account_key,
                )
            )
            return _coa_from_doc(row.document) if row else None

    async def list_children(self, tenant_id: str, parent_account_id: str) -> list[ChartOfAccount]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(FinancialKernelChartOfAccountRow).where(
                        FinancialKernelChartOfAccountRow.tenant_id == tenant_id,
                        FinancialKernelChartOfAccountRow.parent_account_id == parent_account_id,
                    )
                )
            ).all()
        return [_coa_from_doc(r.document) for r in rows]

    async def list_by_tree(self, tenant_id: str, tree_id: str) -> list[ChartOfAccount]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(FinancialKernelChartOfAccountRow).where(
                        FinancialKernelChartOfAccountRow.tenant_id == tenant_id,
                        FinancialKernelChartOfAccountRow.tree_id == tree_id,
                    )
                )
            ).all()
        return [_coa_from_doc(r.document) for r in rows]


class PostgresJournalRepository(IJournalRepository):
    async def save(self, journal: Journal) -> None:
        doc = journal.to_dict()
        async with session_scope() as session:
            row = await session.get(FinancialKernelJournalRow, UUID(str(journal.id)))
            if row is None:
                session.add(
                    FinancialKernelJournalRow(
                        id=UUID(str(journal.id)),
                        tenant_id=journal.tenant_id,
                        idempotency_key=journal.idempotency_key,
                        status=journal.status,
                        period_id=journal.period_id,
                        posted_at=journal.posted_at,
                        document=doc,
                        created_at=journal.created_at,
                    )
                )
            else:
                row.status = journal.status
                row.period_id = journal.period_id
                row.posted_at = journal.posted_at
                row.document = doc

    async def find_by_id(self, journal_id: str) -> Journal | None:
        async with session_scope() as session:
            row = await session.get(FinancialKernelJournalRow, UUID(journal_id))
            return _journal_from_doc(row.document) if row else None

    async def find_by_idempotency(self, tenant_id: str, key: str) -> Journal | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(FinancialKernelJournalRow).where(
                    FinancialKernelJournalRow.tenant_id == tenant_id,
                    FinancialKernelJournalRow.idempotency_key == key,
                )
            )
            return _journal_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[Journal]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(FinancialKernelJournalRow).where(
                        FinancialKernelJournalRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_journal_from_doc(r.document) for r in rows]


class PostgresFiscalYearRepository(IFiscalYearRepository):
    async def save(self, year: FiscalYear) -> None:
        doc = year.to_dict()
        async with session_scope() as session:
            row = await session.get(FinancialKernelFiscalYearRow, UUID(str(year.id)))
            if row is None:
                session.add(
                    FinancialKernelFiscalYearRow(
                        id=UUID(str(year.id)),
                        tenant_id=year.tenant_id,
                        name=year.name,
                        document=doc,
                    )
                )
            else:
                row.name = year.name
                row.document = doc

    async def list_by_tenant(self, tenant_id: str) -> list[FiscalYear]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(FinancialKernelFiscalYearRow).where(
                        FinancialKernelFiscalYearRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_year_from_doc(r.document) for r in rows]

    async def find_by_id(self, year_id: str) -> FiscalYear | None:
        async with session_scope() as session:
            row = await session.get(FinancialKernelFiscalYearRow, UUID(year_id))
            return _year_from_doc(row.document) if row else None


class PostgresFiscalPeriodRepository(IFiscalPeriodRepository):
    async def save(self, period: FiscalPeriod) -> None:
        doc = period.to_dict()
        async with session_scope() as session:
            row = await session.get(FinancialKernelFiscalPeriodRow, UUID(str(period.id)))
            if row is None:
                session.add(
                    FinancialKernelFiscalPeriodRow(
                        id=UUID(str(period.id)),
                        tenant_id=period.tenant_id,
                        fiscal_year_id=period.fiscal_year_id,
                        status=period.status,
                        organization_id=period.organization_id,
                        document=doc,
                    )
                )
            else:
                row.status = period.status
                row.organization_id = period.organization_id
                row.document = doc

    async def find_open(
        self, tenant_id: str, organization_id: str | None = None
    ) -> FiscalPeriod | None:
        async with session_scope() as session:
            stmt = select(FinancialKernelFiscalPeriodRow).where(
                FinancialKernelFiscalPeriodRow.tenant_id == tenant_id,
                FinancialKernelFiscalPeriodRow.status == "open",
            )
            if organization_id is not None:
                stmt = stmt.where(
                    FinancialKernelFiscalPeriodRow.organization_id == organization_id
                )
            row = await session.scalar(stmt)
            return _period_from_doc(row.document) if row else None

    async def find_by_id(self, period_id: str) -> FiscalPeriod | None:
        async with session_scope() as session:
            row = await session.get(FinancialKernelFiscalPeriodRow, UUID(period_id))
            return _period_from_doc(row.document) if row else None

    async def list_by_tenant(self, tenant_id: str) -> list[FiscalPeriod]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(FinancialKernelFiscalPeriodRow).where(
                        FinancialKernelFiscalPeriodRow.tenant_id == tenant_id
                    )
                )
            ).all()
        return [_period_from_doc(r.document) for r in rows]

    async def list_by_fiscal_year(self, tenant_id: str, fiscal_year_id: str) -> list[FiscalPeriod]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(FinancialKernelFiscalPeriodRow).where(
                        FinancialKernelFiscalPeriodRow.tenant_id == tenant_id,
                        FinancialKernelFiscalPeriodRow.fiscal_year_id == fiscal_year_id,
                    )
                )
            ).all()
        return [_period_from_doc(r.document) for r in rows]
