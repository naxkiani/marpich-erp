"""ACL — translate CRM opportunity won → sales quotation draft command."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DraftQuotationFromOpportunityCommand:
    tenant_id: str
    correlation_id: str
    opportunity_id: str
    contact_id: str
    title: str
    amount: str
    currency: str


class SalesCrmEventAdapter:
    async def parse_integration_event(
        self, envelope: dict
    ) -> DraftQuotationFromOpportunityCommand | None:
        if envelope.get("event_name") != "crm.opportunity.won":
            return None
        payload = envelope.get("payload") or {}
        opportunity_id = payload.get("opportunity_id")
        contact_id = payload.get("contact_id")
        if not opportunity_id or not contact_id:
            return None
        return DraftQuotationFromOpportunityCommand(
            tenant_id=str(envelope["tenant_id"]),
            correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
            opportunity_id=str(opportunity_id),
            contact_id=str(contact_id),
            title=str(payload.get("title") or "Won opportunity"),
            amount=str(payload.get("amount") or "0"),
            currency=str(payload.get("currency") or "USD"),
        )
