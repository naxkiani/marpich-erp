"""Enterprise Payment aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class PaymentMethod(StrEnum):
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CHEQUE = "cheque"
    CARD = "card"
    WALLET = "wallet"
    MOBILE_MONEY = "mobile_money"


class PaymentKind(StrEnum):
    STANDARD = "standard"
    SPLIT = "split"
    PARTIAL = "partial"
    INSTALLMENT = "installment"
    ADVANCE = "advance"


class PaymentStatus(StrEnum):
    PENDING = "pending"
    PARTIAL = "partial"
    ALLOCATED = "allocated"
    SETTLED = "settled"
    REFUNDED = "refunded"
    CHARGEBACK = "chargeback"
    FAILED = "failed"


@dataclass(eq=False, kw_only=True)
class Payment(AggregateRoot):
    tenant_id: str
    source_context: str
    source_document_id: str
    idempotency_key: str
    payment_method: str
    payment_kind: str
    total_amount: float
    paid_amount: float
    remaining_amount: float
    currency: str
    status: str
    reference: str
    allocations: list[dict] = field(default_factory=list)
    parent_payment_id: str | None = None
    payer_id: str | None = None
    refund_amount: float = 0.0
    chargeback_amount: float = 0.0
    settled_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        source_context: str,
        source_document_id: str,
        idempotency_key: str,
        payment_method: str,
        payment_kind: str,
        total_amount: float,
        currency: str,
        reference: str,
        paid_amount: float | None = None,
        allocations: list[dict] | None = None,
        parent_payment_id: str | None = None,
        payer_id: str | None = None,
    ) -> Payment:
        paid = round(paid_amount if paid_amount is not None else total_amount, 2)
        total = round(total_amount, 2)
        remaining = round(total - paid, 2)
        status = (
            PaymentStatus.SETTLED
            if remaining <= 0
            else PaymentStatus.PARTIAL
            if paid > 0
            else PaymentStatus.PENDING
        )
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=idempotency_key,
            payment_method=payment_method,
            payment_kind=payment_kind,
            total_amount=total,
            paid_amount=paid,
            remaining_amount=max(remaining, 0),
            currency=currency.strip().upper(),
            status=status,
            reference=reference,
            allocations=list(allocations or []),
            parent_payment_id=parent_payment_id,
            payer_id=payer_id,
            settled_at=datetime.now(UTC) if status == PaymentStatus.SETTLED else None,
        )

    def apply_allocation(self, allocations: list[dict]) -> None:
        self.allocations = allocations
        allocated_total = round(sum(a.get("amount", 0) for a in allocations), 2)
        if allocated_total >= self.paid_amount and self.remaining_amount == 0:
            self.status = PaymentStatus.ALLOCATED
        elif self.remaining_amount > 0:
            self.status = PaymentStatus.PARTIAL

    def record_partial(self, amount: float) -> None:
        amount = round(amount, 2)
        if amount <= 0 or amount > self.remaining_amount:
            raise ValueError("invalid_partial_amount")
        self.paid_amount = round(self.paid_amount + amount, 2)
        self.remaining_amount = round(self.total_amount - self.paid_amount, 2)
        if self.remaining_amount <= 0:
            self.remaining_amount = 0
            self.status = PaymentStatus.SETTLED
            self.settled_at = datetime.now(UTC)
        else:
            self.status = PaymentStatus.PARTIAL

    def settle(self) -> None:
        if self.remaining_amount > 0:
            raise ValueError("payment_not_fully_paid")
        self.status = PaymentStatus.SETTLED
        self.settled_at = datetime.now(UTC)

    def refund(self, amount: float) -> None:
        amount = round(amount, 2)
        if amount <= 0 or amount > self.paid_amount:
            raise ValueError("invalid_refund_amount")
        self.refund_amount = round(self.refund_amount + amount, 2)
        self.paid_amount = round(self.paid_amount - amount, 2)
        self.remaining_amount = round(self.total_amount - self.paid_amount, 2)
        self.status = PaymentStatus.REFUNDED if self.paid_amount == 0 else PaymentStatus.PARTIAL

    def chargeback(self, amount: float) -> None:
        amount = round(amount, 2)
        if amount <= 0 or amount > self.paid_amount:
            raise ValueError("invalid_chargeback_amount")
        self.chargeback_amount = round(self.chargeback_amount + amount, 2)
        self.paid_amount = round(self.paid_amount - amount, 2)
        self.remaining_amount = round(self.total_amount - self.paid_amount, 2)
        self.status = PaymentStatus.CHARGEBACK

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "source_context": self.source_context,
            "source_document_id": self.source_document_id,
            "idempotency_key": self.idempotency_key,
            "payment_method": self.payment_method,
            "payment_kind": self.payment_kind,
            "total_amount": self.total_amount,
            "paid_amount": self.paid_amount,
            "remaining_amount": self.remaining_amount,
            "currency": self.currency,
            "status": self.status,
            "reference": self.reference,
            "allocations": self.allocations,
            "parent_payment_id": self.parent_payment_id,
            "payer_id": self.payer_id,
            "refund_amount": self.refund_amount,
            "chargeback_amount": self.chargeback_amount,
            "settled_at": self.settled_at.isoformat() if self.settled_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class InstallmentPlan(AggregateRoot):
    tenant_id: str
    parent_payment_id: str
    source_context: str
    source_document_id: str
    currency: str
    total_amount: float
    installments: list[dict]
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        parent_payment_id: str,
        source_context: str,
        source_document_id: str,
        currency: str,
        total_amount: float,
        installments: list[dict],
    ) -> InstallmentPlan:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            parent_payment_id=parent_payment_id,
            source_context=source_context,
            source_document_id=source_document_id,
            currency=currency,
            total_amount=round(total_amount, 2),
            installments=installments,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "parent_payment_id": self.parent_payment_id,
            "source_context": self.source_context,
            "source_document_id": self.source_document_id,
            "currency": self.currency,
            "total_amount": self.total_amount,
            "installments": self.installments,
            "created_at": self.created_at.isoformat(),
        }
