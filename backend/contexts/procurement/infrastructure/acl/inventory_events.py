"""ACL — inventory.reorder.triggered → purchase requisition draft."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class DraftRequisitionFromReorderCommand:
    tenant_id: str
    correlation_id: str
    sku: str
    quantity: str
    quantity_available: str
    reorder_threshold: str
    stock_id: str | None


class InventoryReorderEventAdapter:
    async def parse_integration_event(
        self, envelope: dict
    ) -> DraftRequisitionFromReorderCommand | None:
        if envelope.get("event_name") != "inventory.reorder.triggered":
            return None
        payload = envelope.get("payload") or {}
        sku = payload.get("sku")
        if not sku:
            return None
        return DraftRequisitionFromReorderCommand(
            tenant_id=str(envelope["tenant_id"]),
            correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
            sku=str(sku),
            quantity=str(payload.get("suggested_reorder_quantity") or "0"),
            quantity_available=str(payload.get("quantity_available") or "0"),
            reorder_threshold=str(payload.get("reorder_threshold") or "0"),
            stock_id=str(payload["stock_id"]) if payload.get("stock_id") else None,
        )
