"""POS sale aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

from contexts.pos.domain.events.integration_events import SaleCompletedIntegration


@dataclass(eq=False, kw_only=True)
class PosSale(AggregateRoot):
    tenant_id: str
    shift_id: UniqueId
    terminal_id: UniqueId
    items: list[dict]
    subtotal: Decimal
    tax: Decimal
    total: Decimal
    payment_method: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def checkout(
        cls,
        *,
        tenant_id: str,
        shift_id: UniqueId,
        terminal_id: UniqueId,
        items: list[dict],
        subtotal: Decimal,
        tax: Decimal,
        payment_method: str,
        correlation_id: str,
    ) -> tuple[PosSale, SaleCompletedIntegration]:
        total = subtotal + tax
        sale = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            shift_id=shift_id,
            terminal_id=terminal_id,
            items=items,
            subtotal=subtotal,
            tax=tax,
            total=total,
            payment_method=payment_method,
        )
        event = SaleCompletedIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            sale_id=sale.id,
            shift_id=shift_id,
            terminal_id=terminal_id,
            total=str(total),
            payment_method=payment_method,
        )
        return sale, event

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "shift_id": str(self.shift_id),
            "terminal_id": str(self.terminal_id),
            "items": self.items,
            "subtotal": str(self.subtotal),
            "tax": str(self.tax),
            "total": str(self.total),
            "payment_method": self.payment_method,
            "created_at": self.created_at.isoformat(),
        }
