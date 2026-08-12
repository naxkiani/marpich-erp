"""Inventory stock level aggregate — tenant-scoped SKU balance + reservations."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class StockLevel(AggregateRoot):
    tenant_id: str
    sku: str
    quantity_on_hand: Decimal
    quantity_reserved: Decimal = Decimal("0")
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def seed(cls, *, tenant_id: str, sku: str, quantity: Decimal) -> StockLevel:
        if quantity < 0:
            raise ValueError("inventory.errors.negative_quantity")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            sku=sku.strip().upper(),
            quantity_on_hand=quantity,
            quantity_reserved=Decimal("0"),
        )

    def set_quantity(self, quantity: Decimal) -> None:
        if quantity < 0:
            raise ValueError("inventory.errors.negative_quantity")
        if quantity < self.quantity_reserved:
            raise ValueError("inventory.errors.quantity_below_reserved")
        self.quantity_on_hand = quantity
        self.updated_at = datetime.now(UTC)

    def decrement(self, quantity: Decimal) -> None:
        if quantity <= 0:
            raise ValueError("inventory.errors.invalid_decrement")
        if self.quantity_on_hand < quantity:
            raise ValueError("inventory.errors.insufficient_stock")
        available = self.quantity_on_hand - self.quantity_reserved
        if available < quantity:
            raise ValueError("inventory.errors.insufficient_available")
        self.quantity_on_hand -= quantity
        self.updated_at = datetime.now(UTC)

    def reserve(self, quantity: Decimal) -> None:
        if quantity <= 0:
            raise ValueError("inventory.errors.invalid_reservation")
        available = self.quantity_on_hand - self.quantity_reserved
        if available < quantity:
            raise ValueError("inventory.errors.insufficient_available")
        self.quantity_reserved += quantity
        self.updated_at = datetime.now(UTC)

    @property
    def quantity_available(self) -> Decimal:
        return self.quantity_on_hand - self.quantity_reserved

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "sku": self.sku,
            "quantity_on_hand": str(self.quantity_on_hand),
            "quantity_reserved": str(self.quantity_reserved),
            "quantity_available": str(self.quantity_available),
            "updated_at": self.updated_at.isoformat(),
        }
