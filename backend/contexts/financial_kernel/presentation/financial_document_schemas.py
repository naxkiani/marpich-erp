"""Enterprise Financial Documents API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class DocumentLineItem(BaseModel):
    description: str
    quantity: float = 1
    unit_price: float = 0
    amount: float | None = None
    account_code: str | None = None


class CreateFinancialDocumentRequest(BaseModel):
    source_context: str
    source_document_id: str
    document_type: str
    total_amount: float = Field(gt=0)
    currency: str = "USD"
    counterparty_name: str
    reference: str
    idempotency_key: str | None = None
    counterparty_id: str | None = None
    lines: list[DocumentLineItem] | None = None
    metadata: dict | None = None


class AddDocumentVersionRequest(BaseModel):
    lines: list[DocumentLineItem] | None = None
    total_amount: float | None = Field(default=None, gt=0)
    metadata: dict | None = None


class SignFinancialDocumentRequest(BaseModel):
    signer_id: str | None = None
