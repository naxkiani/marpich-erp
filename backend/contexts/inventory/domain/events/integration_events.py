"""Inventory integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class StockAdjustedIntegration(IntegrationEvent):
    stock_id: UniqueId
    sku: str
    quantity_delta: str
    quantity_on_hand: str
    reason: str
    source_document_id: str

    @property
    def event_name(self) -> str:
        return "inventory.stock.adjusted"

    @property
    def source_context(self) -> str:
        return "inventory"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "stock_id": str(self.stock_id),
            "sku": self.sku,
            "quantity_delta": self.quantity_delta,
            "quantity_on_hand": self.quantity_on_hand,
            "reason": self.reason,
            "source_document_id": self.source_document_id,
        }
