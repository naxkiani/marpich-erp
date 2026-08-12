"""Sales Quotation aggregate — CAP-ENT-002 Sales Lifecycle."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from enum import StrEnum

from contexts.sales.domain.events.integration_events import QuotationSentIntegration
from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId


class QuotationStatus(StrEnum):
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CONVERTED = "converted"


@dataclass(eq=False, kw_only=True)
class Quotation(AggregateRoot):
    tenant_id: str
    contact_id: UniqueId
    title: str
    amount: Decimal
    currency: str = "USD"
    status: QuotationStatus = QuotationStatus.DRAFT
    opportunity_id: UniqueId | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    sent_at: datetime | None = None
    accepted_at: datetime | None = None

    @classmethod
    def draft_from_opportunity(
        cls,
        *,
        tenant_id: str,
        contact_id: UniqueId,
        opportunity_id: UniqueId,
        title: str,
        amount: Decimal,
        currency: str = "USD",
    ) -> Quotation:
        if amount < 0:
            raise ValueError("sales.errors.amount_negative")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            contact_id=contact_id,
            opportunity_id=opportunity_id,
            title=title.strip(),
            amount=amount,
            currency=currency.strip().upper() or "USD",
        )

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        contact_id: UniqueId,
        title: str,
        amount: Decimal,
        currency: str = "USD",
        opportunity_id: UniqueId | None = None,
    ) -> Quotation:
        if amount < 0:
            raise ValueError("sales.errors.amount_negative")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            contact_id=contact_id,
            opportunity_id=opportunity_id,
            title=title.strip(),
            amount=amount,
            currency=currency.strip().upper() or "USD",
        )

    def send(self, *, correlation_id: str) -> QuotationSentIntegration:
        if self.status != QuotationStatus.DRAFT:
            raise ValueError("sales.errors.quotation_not_draft")
        self.status = QuotationStatus.SENT
        self.sent_at = datetime.now(UTC)
        self.updated_at = self.sent_at
        return QuotationSentIntegration(
            tenant_id=TenantId.create(self.tenant_id),
            correlation_id=correlation_id,
            quotation_id=self.id,
            contact_id=self.contact_id,
            opportunity_id=self.opportunity_id,
            title=self.title,
            amount=str(self.amount),
            currency=self.currency,
        )

    def accept(self) -> None:
        if self.status not in (QuotationStatus.SENT, QuotationStatus.DRAFT):
            raise ValueError("sales.errors.quotation_not_acceptable")
        self.status = QuotationStatus.ACCEPTED
        self.accepted_at = datetime.now(UTC)
        self.updated_at = self.accepted_at

    def mark_converted(self) -> None:
        self.status = QuotationStatus.CONVERTED
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "contact_id": str(self.contact_id),
            "opportunity_id": str(self.opportunity_id) if self.opportunity_id else None,
            "title": self.title,
            "amount": str(self.amount),
            "currency": self.currency,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "accepted_at": self.accepted_at.isoformat() if self.accepted_at else None,
        }
