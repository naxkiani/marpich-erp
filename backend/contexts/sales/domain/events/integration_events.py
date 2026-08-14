"""Sales integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class QuotationSentIntegration(IntegrationEvent):
    quotation_id: UniqueId
    contact_id: UniqueId
    title: str
    amount: str
    currency: str
    opportunity_id: UniqueId | None = None

    @property
    def event_name(self) -> str:
        return "sales.quotation.sent"

    @property
    def source_context(self) -> str:
        return "sales"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "quotation_id": str(self.quotation_id),
            "contact_id": str(self.contact_id),
            "opportunity_id": str(self.opportunity_id) if self.opportunity_id else None,
            "title": self.title,
            "amount": self.amount,
            "currency": self.currency,
        }


@dataclass(frozen=True, kw_only=True)
class OrderPlacedIntegration(IntegrationEvent):
    order_id: UniqueId
    contact_id: UniqueId
    title: str
    amount: str
    currency: str
    quotation_id: UniqueId | None = None
    opportunity_id: UniqueId | None = None

    @property
    def event_name(self) -> str:
        return "sales.order.placed"

    @property
    def source_context(self) -> str:
        return "sales"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "order_id": str(self.order_id),
            "customer_id": str(self.contact_id),
            "contact_id": str(self.contact_id),
            "quotation_id": str(self.quotation_id) if self.quotation_id else None,
            "opportunity_id": str(self.opportunity_id) if self.opportunity_id else None,
            "title": self.title,
            "total_amount": float(self.amount),
            "amount": self.amount,
            "currency": self.currency,
            "lines": [
                {
                    "item_id": str(self.quotation_id or self.order_id),
                    "sku": "SALES-STD",
                    "quantity": 1,
                    "unit_price": float(self.amount),
                }
            ],
        }
