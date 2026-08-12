"""ACL — translate sales.order.placed → AR invoice draft command."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DraftInvoiceFromSalesOrderCommand:
    tenant_id: str
    correlation_id: str
    sales_order_id: str
    contact_id: str
    title: str
    amount: str
    currency: str
    line_items: tuple[dict, ...]


class SalesOrderEventAdapter:
    async def parse_integration_event(
        self, envelope: dict
    ) -> DraftInvoiceFromSalesOrderCommand | None:
        if envelope.get("event_name") != "sales.order.placed":
            return None
        payload = envelope.get("payload") or {}
        order_id = payload.get("order_id")
        contact_id = payload.get("contact_id") or payload.get("customer_id")
        if not order_id or not contact_id:
            return None
        amount = payload.get("amount")
        if amount is None and payload.get("total_amount") is not None:
            amount = str(payload.get("total_amount"))
        lines = payload.get("lines") or []
        return DraftInvoiceFromSalesOrderCommand(
            tenant_id=str(envelope["tenant_id"]),
            correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
            sales_order_id=str(order_id),
            contact_id=str(contact_id),
            title=str(payload.get("title") or "Sales invoice"),
            amount=str(amount or "0"),
            currency=str(payload.get("currency") or "USD"),
            line_items=tuple(dict(line) for line in lines if isinstance(line, dict)),
        )
