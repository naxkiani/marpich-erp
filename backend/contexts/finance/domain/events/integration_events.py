"""Finance integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class PeriodClosedIntegration(IntegrationEvent):
    period_id: UniqueId
    period_name: str

    @property
    def event_name(self) -> str:
        return "finance.period.closed"

    @property
    def source_context(self) -> str:
        return "finance"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "period_id": str(self.period_id),
            "period_name": self.period_name,
        }


@dataclass(frozen=True, kw_only=True)
class JournalRecordedIntegration(IntegrationEvent):
    journal_entry_id: UniqueId
    source_type: str
    source_id: str

    @property
    def event_name(self) -> str:
        return "finance.journal.recorded"

    @property
    def source_context(self) -> str:
        return "finance"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "journal_entry_id": str(self.journal_entry_id),
            "source_type": self.source_type,
            "source_id": self.source_id,
        }
