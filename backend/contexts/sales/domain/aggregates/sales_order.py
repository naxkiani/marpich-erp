"""Sales Order aggregate — CAP-ENT-002."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from contexts.sales.domain.events.integration_events import OrderPlacedIntegration
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


class SalesOrderStatus(StrEnum):
    CONFIRMED = "confirmed"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"


@dataclass(eq=False, kw_only=True)
class SalesOrder(AggregateRoot):
    tenant_id: str
    contact_id: UniqueId
    title: str
    amount: Decimal
    currency: str = "USD"
    status: SalesOrderStatus = SalesOrderStatus.CONFIRMED
    quotation_id: UniqueId | None = None
    opportunity_id: UniqueId | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def from_quotation(
        cls,
        *,
        tenant_id: str,
        quotation_id: UniqueId,
        contact_id: UniqueId,
        title: str,
        amount: Decimal,
        currency: str,
        opportunity_id: UniqueId | None,
        correlation_id: str,
    ) -> tuple[SalesOrder, OrderPlacedIntegration]:
        order = cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            contact_id=contact_id,
            quotation_id=quotation_id,
            opportunity_id=opportunity_id,
            title=title,
            amount=amount,
            currency=currency,
        )
        event = OrderPlacedIntegration(
            tenant_id=TenantId.create(tenant_id),
            correlation_id=correlation_id,
            order_id=order.id,
            contact_id=contact_id,
            quotation_id=quotation_id,
            opportunity_id=opportunity_id,
            title=title,
            amount=str(amount),
            currency=currency,
        )
        return order, event

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "contact_id": str(self.contact_id),
            "quotation_id": str(self.quotation_id) if self.quotation_id else None,
            "opportunity_id": str(self.opportunity_id) if self.opportunity_id else None,
            "title": self.title,
            "amount": str(self.amount),
            "currency": self.currency,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
