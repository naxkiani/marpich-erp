"""Procurement integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class RequisitionCreatedIntegration(IntegrationEvent):
    requisition_id: UniqueId
    sku: str
    quantity: str
    quantity_available: str
    reorder_threshold: str

    @property
    def event_name(self) -> str:
        return "procurement.requisition.created"

    @property
    def source_context(self) -> str:
        return "procurement"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "requisition_id": str(self.requisition_id),
            "sku": self.sku,
            "quantity": self.quantity,
            "quantity_available": self.quantity_available,
            "reorder_threshold": self.reorder_threshold,
        }


@dataclass(frozen=True, kw_only=True)
class RequisitionSubmittedIntegration(IntegrationEvent):
    requisition_id: UniqueId
    sku: str
    quantity: str

    @property
    def event_name(self) -> str:
        return "procurement.requisition.submitted"

    @property
    def source_context(self) -> str:
        return "procurement"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "requisition_id": str(self.requisition_id),
            "sku": self.sku,
            "quantity": self.quantity,
        }


@dataclass(frozen=True, kw_only=True)
class PurchaseOrderApprovedIntegration(IntegrationEvent):
    requisition_id: UniqueId
    sku: str
    quantity: str

    @property
    def event_name(self) -> str:
        return "procurement.po.approved"

    @property
    def source_context(self) -> str:
        return "procurement"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "requisition_id": str(self.requisition_id),
            "purchase_order_id": str(self.requisition_id),
            "sku": self.sku,
            "quantity": self.quantity,
        }
