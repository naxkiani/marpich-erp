"""Finance DI + event subscription."""
from __future__ import annotations

from contexts.finance.application.service import FinanceApplicationService
from contexts.finance.infrastructure.acl.accounting_events import AccountingEventAdapter
from contexts.finance.infrastructure.persistence.memory_store import (
    InMemoryAccountRepository,
    InMemoryFiscalPeriodRepository,
    InMemoryJournalEntryRepository,
)
from contexts.finance.infrastructure.persistence.postgres_store import (
    PostgresAccountRepository,
    PostgresFiscalPeriodRepository,
    PostgresJournalEntryRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: FinanceApplicationService | None = None
_registered = False


def get_finance_service() -> FinanceApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = FinanceApplicationService(
                accounts=PostgresAccountRepository(),
                periods=PostgresFiscalPeriodRepository(),
                journals=PostgresJournalEntryRepository(),
                accounting_events=AccountingEventAdapter(),
            )
        else:
            _service = FinanceApplicationService(
                accounts=InMemoryAccountRepository(),
                periods=InMemoryFiscalPeriodRepository(),
                journals=InMemoryJournalEntryRepository(),
                accounting_events=AccountingEventAdapter(),
            )
    if not _registered:
        InProcessEventBus.subscribe(
            "accounting.journal.posted",
            _service.handle_accounting_journal_posted,
        )
        _registered = True
    return _service


def reset_finance_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
