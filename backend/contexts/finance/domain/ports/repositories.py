"""Repository ports — Finance."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.finance.domain.aggregates.account import Account
from contexts.finance.domain.aggregates.fiscal_period import FiscalPeriod
from contexts.finance.domain.aggregates.journal_entry import JournalEntry
from shared.domain.value_objects.unique_id import UniqueId


class IAccountRepository(ABC):
    @abstractmethod
    async def save(self, account: Account) -> None: ...

    @abstractmethod
    async def find_by_code(self, tenant_id: str, code: str) -> Account | None: ...

    @abstractmethod
    async def list_accounts(self, tenant_id: str) -> list[Account]: ...


class IFiscalPeriodRepository(ABC):
    @abstractmethod
    async def save(self, period: FiscalPeriod) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, period_id: UniqueId) -> FiscalPeriod | None: ...

    @abstractmethod
    async def list_periods(self, tenant_id: str) -> list[FiscalPeriod]: ...

    @abstractmethod
    async def find_open_period(self, tenant_id: str) -> FiscalPeriod | None: ...


class IJournalEntryRepository(ABC):
    @abstractmethod
    async def save(self, entry: JournalEntry) -> None: ...

    @abstractmethod
    async def find_by_external_journal(
        self, tenant_id: str, external_journal_id: str
    ) -> JournalEntry | None: ...

    @abstractmethod
    async def find_by_source(
        self, tenant_id: str, source_type: str, source_id: str
    ) -> JournalEntry | None: ...

    @abstractmethod
    async def list_entries(self, tenant_id: str) -> list[JournalEntry]: ...
