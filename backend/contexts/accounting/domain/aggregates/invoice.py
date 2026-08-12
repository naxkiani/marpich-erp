"""AR Invoice aggregate — CAP-ENT-023 Accounts Receivable (commercial sales)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from contexts.accounting.domain.events.integration_events import InvoiceIssuedIntegration
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


class InvoiceStatus(StrEnum):
    DRAFT = "draft"
    ISSUED = "issued"
    PAID = "paid"
    VOID = "void"


@dataclass(eq=False, kw_only=True)
class Invoice(AggregateRoot):
    tenant_id: str
    sales_order_id: UniqueId
    contact_id: UniqueId
    title: str
    amount: Decimal
    currency: str = "USD"
    status: InvoiceStatus = InvoiceStatus.DRAFT
    line_items: list[dict] = field(default_factory=list)
    correlation_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    issued_at: datetime | None = None

    @classmethod
    def draft_from_sales_order(
        cls,
        *,
        tenant_id: str,
        sales_order_id: UniqueId,
        contact_id: UniqueId,
        title: str,
        amount: Decimal,
        currency: str,
        line_items: list[dict],
        correlation_id: str,
    ) -> Invoice:
        if amount < 0:
            raise ValueError("accounting.errors.amount_negative")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            sales_order_id=sales_order_id,
            contact_id=contact_id,
            title=title.strip() or "Sales invoice",
            amount=amount,
            currency=(currency or "USD").strip().upper(),
            line_items=list(line_items),
            correlation_id=correlation_id,
        )

    def issue(self, *, correlation_id: str) -> InvoiceIssuedIntegration:
        if self.status != InvoiceStatus.DRAFT:
            raise ValueError("accounting.errors.invoice_not_draft")
        self.status = InvoiceStatus.ISSUED
        self.issued_at = datetime.now(UTC)
        self.updated_at = self.issued_at
        self.correlation_id = correlation_id or self.correlation_id
        return InvoiceIssuedIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=self.correlation_id,
            invoice_id=self.id,
            sales_order_id=self.sales_order_id,
            contact_id=self.contact_id,
            title=self.title,
            amount=str(self.amount),
            currency=self.currency,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "sales_order_id": str(self.sales_order_id),
            "contact_id": str(self.contact_id),
            "title": self.title,
            "amount": str(self.amount),
            "currency": self.currency,
            "status": self.status.value,
            "line_items": list(self.line_items),
            "correlation_id": self.correlation_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "issued_at": self.issued_at.isoformat() if self.issued_at else None,
        }
