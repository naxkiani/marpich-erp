"""Accounting integration event adapter port."""
from __future__ import annotations

from typing import Protocol

from contexts.finance.application.commands.record_journal_from_accounting import (
    RecordJournalFromAccountingCommand,
)


class IAccountingEventAdapter(Protocol):
    async def parse_journal_posted(self, envelope: dict) -> RecordJournalFromAccountingCommand: ...
