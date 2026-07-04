"""Accounting integration events."""
from __future__ import annotations

from dataclasses import dataclass, field

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class BillingEncounterCreatedIntegration(IntegrationEvent):
    billing_id: UniqueId
    external_encounter_id: str
    total_amount: float
    currency: str

    @property
    def event_name(self) -> str:
        return "accounting.billing.encounter_created"

    @property
    def source_context(self) -> str:
        return "accounting"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "billing_id": str(self.billing_id),
            "external_encounter_id": self.external_encounter_id,
            "total_amount": self.total_amount,
            "currency": self.currency,
        }


@dataclass(frozen=True, kw_only=True)
class JournalPostedIntegration(IntegrationEvent):
    journal_id: UniqueId
    source_type: str
    source_id: str
    currency: str
    lines: tuple[dict, ...] = field(default_factory=tuple)

    @property
    def event_name(self) -> str:
        return "accounting.journal.posted"

    @property
    def source_context(self) -> str:
        return "accounting"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "journal_id": str(self.journal_id),
            "source_type": self.source_type,
            "source_id": self.source_id,
            "currency": self.currency,
            "lines": list(self.lines),
        }
