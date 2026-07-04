"""ACL — translate Accounting events to Finance commands."""
from __future__ import annotations

from contexts.finance.application.commands.record_journal_from_accounting import (
    RecordJournalFromAccountingCommand,
)


class AccountingEventAdapter:
    async def parse_journal_posted(self, envelope: dict) -> RecordJournalFromAccountingCommand:
        payload = envelope["payload"]
        return RecordJournalFromAccountingCommand(
            tenant_id=envelope["tenant_id"],
            correlation_id=envelope["correlation_id"],
            external_journal_id=payload["journal_id"],
            source_type=payload["source_type"],
            source_id=payload["source_id"],
            currency=payload["currency"],
            lines=list(payload.get("lines", [])),
        )


async def on_journal_posted(envelope: dict) -> RecordJournalFromAccountingCommand:
    return await AccountingEventAdapter().parse_journal_posted(envelope)
