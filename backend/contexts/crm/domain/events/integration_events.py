"""CRM integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class ContactCreatedIntegration(IntegrationEvent):
    contact_id: UniqueId
    email: str
    full_name: str

    @property
    def event_name(self) -> str:
        return "crm.contact.created"

    @property
    def source_context(self) -> str:
        return "crm"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "contact_id": str(self.contact_id),
            "email": self.email,
            "full_name": self.full_name,
        }


@dataclass(frozen=True, kw_only=True)
class OpportunityWonIntegration(IntegrationEvent):
    opportunity_id: UniqueId
    contact_id: UniqueId
    title: str
    amount: str
    currency: str

    @property
    def event_name(self) -> str:
        return "crm.opportunity.won"

    @property
    def source_context(self) -> str:
        return "crm"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "opportunity_id": str(self.opportunity_id),
            "contact_id": str(self.contact_id),
            "title": self.title,
            "amount": self.amount,
            "currency": self.currency,
        }


@dataclass(frozen=True, kw_only=True)
class OpportunityLostIntegration(IntegrationEvent):
    opportunity_id: UniqueId
    contact_id: UniqueId
    title: str
    reason: str

    @property
    def event_name(self) -> str:
        return "crm.opportunity.lost"

    @property
    def source_context(self) -> str:
        return "crm"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "opportunity_id": str(self.opportunity_id),
            "contact_id": str(self.contact_id),
            "title": self.title,
            "reason": self.reason,
        }
