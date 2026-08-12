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


@dataclass(frozen=True, kw_only=True)
class StockReservedIntegration(IntegrationEvent):
    stock_id: UniqueId
    sku: str
    quantity_reserved_delta: str
    quantity_reserved: str
    quantity_available: str
    order_id: str
    reason: str = "sales.order.placed"

    @property
    def event_name(self) -> str:
        return "inventory.stock.reserved"

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
            "quantity_reserved_delta": self.quantity_reserved_delta,
            "quantity_reserved": self.quantity_reserved,
            "quantity_available": self.quantity_available,
            "order_id": self.order_id,
            "reason": self.reason,
        }


@dataclass(frozen=True, kw_only=True)
class ReorderTriggeredIntegration(IntegrationEvent):
    stock_id: UniqueId
    sku: str
    quantity_available: str
    quantity_on_hand: str
    quantity_reserved: str
    reorder_threshold: str
    suggested_reorder_quantity: str

    @property
    def event_name(self) -> str:
        return "inventory.reorder.triggered"

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
            "quantity_available": self.quantity_available,
            "quantity_on_hand": self.quantity_on_hand,
            "quantity_reserved": self.quantity_reserved,
            "reorder_threshold": self.reorder_threshold,
            "suggested_reorder_quantity": self.suggested_reorder_quantity,
        }
