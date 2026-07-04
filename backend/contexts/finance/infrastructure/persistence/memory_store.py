"""Finance in-memory repositories."""
from __future__ import annotations

from contexts.finance.domain.aggregates.account import Account
from contexts.finance.domain.aggregates.fiscal_period import FiscalPeriod
from contexts.finance.domain.aggregates.journal_entry import JournalEntry
from contexts.finance.domain.ports.repositories import (
    IAccountRepository,
    IFiscalPeriodRepository,
    IJournalEntryRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class FinanceMemoryStore:
    accounts: dict[str, Account] = {}
    periods: dict[str, FiscalPeriod] = {}
    journals: dict[str, JournalEntry] = {}
    seeded_tenants: set[str] = set()

    @classmethod
    def reset(cls) -> None:
        cls.accounts.clear()
        cls.periods.clear()
        cls.journals.clear()
        cls.seeded_tenants.clear()


class InMemoryAccountRepository(IAccountRepository):
    async def save(self, account: Account) -> None:
        FinanceMemoryStore.accounts[f"{account.tenant_id}:{account.code}"] = account

    async def find_by_code(self, tenant_id: str, code: str) -> Account | None:
        return FinanceMemoryStore.accounts.get(f"{tenant_id}:{code}")

    async def list_accounts(self, tenant_id: str) -> list[Account]:
        return [
            a for key, a in FinanceMemoryStore.accounts.items() if key.startswith(f"{tenant_id}:")
        ]


class InMemoryFiscalPeriodRepository(IFiscalPeriodRepository):
    async def save(self, period: FiscalPeriod) -> None:
        FinanceMemoryStore.periods[str(period.id)] = period

    async def find_by_id(self, tenant_id: str, period_id: UniqueId) -> FiscalPeriod | None:
        p = FinanceMemoryStore.periods.get(str(period_id))
        return p if p and p.tenant_id == tenant_id else None

    async def list_periods(self, tenant_id: str) -> list[FiscalPeriod]:
        return [p for p in FinanceMemoryStore.periods.values() if p.tenant_id == tenant_id]

    async def find_open_period(self, tenant_id: str) -> FiscalPeriod | None:
        for p in FinanceMemoryStore.periods.values():
            if p.tenant_id == tenant_id and p.status.value == "open":
                return p
        return None


class InMemoryJournalEntryRepository(IJournalEntryRepository):
    async def save(self, entry: JournalEntry) -> None:
        FinanceMemoryStore.journals[str(entry.id)] = entry

    async def find_by_external_journal(
        self, tenant_id: str, external_journal_id: str
    ) -> JournalEntry | None:
        for e in FinanceMemoryStore.journals.values():
            if e.tenant_id == tenant_id and e.external_journal_id == external_journal_id:
                return e
        return None

    async def find_by_source(
        self, tenant_id: str, source_type: str, source_id: str
    ) -> JournalEntry | None:
        for e in FinanceMemoryStore.journals.values():
            if (
                e.tenant_id == tenant_id
                and e.source_type == source_type
                and e.source_id == source_id
            ):
                return e
        return None

    async def list_entries(self, tenant_id: str) -> list[JournalEntry]:
        return [e for e in FinanceMemoryStore.journals.values() if e.tenant_id == tenant_id]
