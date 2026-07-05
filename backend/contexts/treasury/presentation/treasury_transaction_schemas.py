"""Treasury Transaction Engine API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateTreasuryTransactionRequest(BaseModel):
    transaction_type: str
    amount: float = Field(gt=0)
    currency: str = "USD"
    reference: str
    description: str | None = None
    from_account_id: str | None = None
    to_account_id: str | None = None
    metadata: dict | None = None
    auto_submit: bool = False


class ApproveTransactionRequest(BaseModel):
    comment: str | None = None


class RejectTransactionRequest(BaseModel):
    comment: str | None = None
