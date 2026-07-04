"""Command from accounting.journal.posted integration event."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RecordJournalFromAccountingCommand:
    tenant_id: str
    correlation_id: str
    external_journal_id: str
    source_type: str
    source_id: str
    currency: str
    lines: list[dict]
