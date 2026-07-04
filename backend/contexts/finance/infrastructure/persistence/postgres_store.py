"""PostgreSQL repositories — Finance bounded context."""
from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import select

from contexts.finance.domain.aggregates.account import Account, AccountType
from contexts.finance.domain.aggregates.fiscal_period import FiscalPeriod, PeriodStatus
from contexts.finance.domain.aggregates.journal_entry import JournalEntry
from contexts.finance.domain.ports.repositories import (
    IAccountRepository,
    IFiscalPeriodRepository,
    IJournalEntryRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import AccountRow, FiscalPeriodRow, JournalEntryRow


class PostgresAccountRepository(IAccountRepository):
    async def save(self, account: Account) -> None:
        async with session_scope() as session:
            row = await session.get(AccountRow, UUID(str(account.id)))
            if row is None:
                row = AccountRow(
                    id=UUID(str(account.id)),
                    tenant_id=account.tenant_id,
                    code=account.code,
                    name=account.name,
                    account_type=account.account_type.value,
                    balance=account.balance,
                    is_active=account.is_active,
                    created_at=account.created_at,
                )
                session.add(row)
            else:
                row.balance = account.balance
                row.name = account.name
                row.is_active = account.is_active

    async def find_by_code(self, tenant_id: str, code: str) -> Account | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(AccountRow).where(AccountRow.tenant_id == tenant_id, AccountRow.code == code)
            )
            return _account_from_row(row) if row else None

    async def list_accounts(self, tenant_id: str) -> list[Account]:
        async with session_scope() as session:
            rows = (await session.scalars(select(AccountRow).where(AccountRow.tenant_id == tenant_id))).all()
        return [_account_from_row(r) for r in rows]


class PostgresFiscalPeriodRepository(IFiscalPeriodRepository):
    async def save(self, period: FiscalPeriod) -> None:
        async with session_scope() as session:
            row = await session.get(FiscalPeriodRow, UUID(str(period.id)))
            if row is None:
                row = FiscalPeriodRow(
                    id=UUID(str(period.id)),
                    tenant_id=period.tenant_id,
                    name=period.name,
                    start_date=date.fromisoformat(period.start_date),
                    end_date=date.fromisoformat(period.end_date),
                    status=period.status.value,
                    created_at=period.created_at,
                    closed_at=period.closed_at,
                )
                session.add(row)
            else:
                row.status = period.status.value
                row.closed_at = period.closed_at

    async def find_by_id(self, tenant_id: str, period_id: UniqueId) -> FiscalPeriod | None:
        async with session_scope() as session:
            row = await session.get(FiscalPeriodRow, UUID(str(period_id)))
            if row and row.tenant_id == tenant_id:
                return _period_from_row(row)
            return None

    async def list_periods(self, tenant_id: str) -> list[FiscalPeriod]:
        async with session_scope() as session:
            rows = (
                await session.scalars(select(FiscalPeriodRow).where(FiscalPeriodRow.tenant_id == tenant_id))
            ).all()
        return [_period_from_row(r) for r in rows]

    async def find_open_period(self, tenant_id: str) -> FiscalPeriod | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(FiscalPeriodRow).where(
                    FiscalPeriodRow.tenant_id == tenant_id,
                    FiscalPeriodRow.status == "open",
                )
            )
            return _period_from_row(row) if row else None


class PostgresJournalEntryRepository(IJournalEntryRepository):
    async def save(self, entry: JournalEntry) -> None:
        async with session_scope() as session:
            row = await session.get(JournalEntryRow, UUID(str(entry.id)))
            if row is None:
                row = JournalEntryRow(
                    id=UUID(str(entry.id)),
                    tenant_id=entry.tenant_id,
                    external_journal_id=entry.external_journal_id,
                    source_type=entry.source_type,
                    source_id=entry.source_id,
                    currency=entry.currency,
                    lines=list(entry.lines),
                    correlation_id=entry.correlation_id,
                    posted_at=entry.posted_at,
                )
                session.add(row)

    async def find_by_external_journal(
        self, tenant_id: str, external_journal_id: str
    ) -> JournalEntry | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(JournalEntryRow).where(
                    JournalEntryRow.tenant_id == tenant_id,
                    JournalEntryRow.external_journal_id == external_journal_id,
                )
            )
            return _journal_from_row(row) if row else None

    async def find_by_source(
        self, tenant_id: str, source_type: str, source_id: str
    ) -> JournalEntry | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(JournalEntryRow).where(
                    JournalEntryRow.tenant_id == tenant_id,
                    JournalEntryRow.source_type == source_type,
                    JournalEntryRow.source_id == source_id,
                )
            )
            return _journal_from_row(row) if row else None

    async def list_entries(self, tenant_id: str) -> list[JournalEntry]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(JournalEntryRow).where(JournalEntryRow.tenant_id == tenant_id)
                )
            ).all()
        return [_journal_from_row(r) for r in rows]


def _account_from_row(row: AccountRow) -> Account:
    return Account(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        code=row.code,
        name=row.name,
        account_type=AccountType(row.account_type),
        balance=float(row.balance),
        is_active=row.is_active,
        created_at=row.created_at,
    )


def _period_from_row(row: FiscalPeriodRow) -> FiscalPeriod:
    return FiscalPeriod(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        name=row.name,
        start_date=row.start_date.isoformat(),
        end_date=row.end_date.isoformat(),
        status=PeriodStatus(row.status),
        created_at=row.created_at,
        closed_at=row.closed_at,
    )


def _journal_from_row(row: JournalEntryRow) -> JournalEntry:
    return JournalEntry(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        external_journal_id=row.external_journal_id,
        source_type=row.source_type,
        source_id=row.source_id,
        currency=row.currency,
        lines=list(row.lines or []),
        correlation_id=row.correlation_id,
        posted_at=row.posted_at,
    )
