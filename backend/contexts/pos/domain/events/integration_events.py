"""POS integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(frozen=True, kw_only=True)
class SaleCompletedIntegration(IntegrationEvent):
    sale_id: UniqueId
    shift_id: UniqueId
    terminal_id: UniqueId
    total: str
    payment_method: str

    @property
    def event_name(self) -> str:
        return "pos.sale.completed"

    @property
    def source_context(self) -> str:
        return "pos"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "sale_id": str(self.sale_id),
            "shift_id": str(self.shift_id),
            "terminal_id": str(self.terminal_id),
            "total": self.total,
            "payment_method": self.payment_method,
        }


@dataclass(frozen=True, kw_only=True)
class ShiftClosedIntegration(IntegrationEvent):
    shift_id: UniqueId
    terminal_id: UniqueId
    total_sales: str

    @property
    def event_name(self) -> str:
        return "pos.shift.closed"

    @property
    def source_context(self) -> str:
        return "pos"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "shift_id": str(self.shift_id),
            "terminal_id": str(self.terminal_id),
            "total_sales": self.total_sales,
        }


@dataclass(frozen=True, kw_only=True)
class ReceiptIssuedIntegration(IntegrationEvent):
    receipt_id: UniqueId
    sale_id: UniqueId
    receipt_number: str

    @property
    def event_name(self) -> str:
        return "pos.receipt.issued"

    @property
    def source_context(self) -> str:
        return "pos"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "receipt_id": str(self.receipt_id),
            "sale_id": str(self.sale_id),
            "receipt_number": self.receipt_number,
        }
