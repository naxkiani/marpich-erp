"""POS shift aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId

from contexts.pos.domain.events.integration_events import ShiftClosedIntegration


class ShiftStatus(StrEnum):
    OPEN = "open"
    CLOSED = "closed"


@dataclass(eq=False, kw_only=True)
class Shift(AggregateRoot):
    tenant_id: str
    terminal_id: UniqueId
    cashier_name: str
    status: ShiftStatus = ShiftStatus.OPEN
    total_sales: Decimal = Decimal("0")
    opened_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    closed_at: datetime | None = None

    @classmethod
    def open(cls, *, tenant_id: str, terminal_id: UniqueId, cashier_name: str) -> Shift:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            terminal_id=terminal_id,
            cashier_name=cashier_name.strip(),
        )

    def add_sale(self, amount: Decimal) -> None:
        if self.status != ShiftStatus.OPEN:
            raise ValueError("pos.errors.shift_closed")
        if amount <= 0:
            raise ValueError("pos.errors.invalid_sale_amount")
        self.total_sales += amount

    def close(self, *, correlation_id: str) -> ShiftClosedIntegration:
        if self.status == ShiftStatus.CLOSED:
            raise ValueError("pos.errors.shift_already_closed")
        self.status = ShiftStatus.CLOSED
        self.closed_at = datetime.now(UTC)
        return ShiftClosedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            shift_id=self.id,
            terminal_id=self.terminal_id,
            total_sales=str(self.total_sales),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "terminal_id": str(self.terminal_id),
            "cashier_name": self.cashier_name,
            "status": self.status.value,
            "total_sales": str(self.total_sales),
            "opened_at": self.opened_at.isoformat(),
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
        }
