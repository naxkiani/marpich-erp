"""Enterprise Payment Platform API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class PaymentAllocationItem(BaseModel):
    document_type: str = "invoice"
    document_id: str
    amount: float


class OpenItemRequest(BaseModel):
    document_type: str = "invoice"
    document_id: str
    amount_due: float
    due_date: str = ""


class CreatePaymentRequest(BaseModel):
    source_context: str
    source_document_id: str
    payment_method: str
    amount: float = Field(gt=0)
    currency: str = "USD"
    reference: str
    idempotency_key: str | None = None
    paid_amount: float | None = None
    allocations: list[PaymentAllocationItem] | None = None
    open_items: list[OpenItemRequest] | None = None
    payer_id: str | None = None


class SplitItemRequest(BaseModel):
    amount: float = Field(gt=0)
    payment_method: str | None = None
    allocations: list[PaymentAllocationItem] | None = None


class CreateSplitPaymentRequest(BaseModel):
    source_context: str
    source_document_id: str
    payment_method: str
    total_amount: float = Field(gt=0)
    currency: str = "USD"
    reference: str
    idempotency_key: str | None = None
    splits: list[SplitItemRequest]


class PartialPaymentRequest(BaseModel):
    amount: float = Field(gt=0)


class RefundRequest(BaseModel):
    amount: float = Field(gt=0)


class ChargebackRequest(BaseModel):
    amount: float = Field(gt=0)


class AllocatePaymentRequest(BaseModel):
    allocations: list[PaymentAllocationItem] | None = None
    open_items: list[OpenItemRequest] | None = None


class CreateInstallmentRequest(BaseModel):
    source_context: str
    source_document_id: str
    payment_method: str
    total_amount: float = Field(gt=0)
    currency: str = "USD"
    reference: str
    installment_count: int = Field(ge=2, le=60)
    due_dates: list[str]
    idempotency_key: str | None = None


class ReconciliationItemRequest(BaseModel):
    reference: str
    amount: float
    payment_id: str | None = None


class CreatePaymentReconciliationRequest(BaseModel):
    reconciliation_date: str
    payment_items: list[ReconciliationItemRequest]
    bank_items: list[ReconciliationItemRequest]
    bank_reference: str | None = None


class MatchPaymentsRequest(BaseModel):
    bank_items: list[ReconciliationItemRequest]
