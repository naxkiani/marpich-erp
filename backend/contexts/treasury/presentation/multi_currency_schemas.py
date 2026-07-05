"""Multi-Currency Treasury API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateRateRequest(BaseModel):
    quote_currency: str
    rate: float = Field(gt=0)
    rate_type: str
    effective_date: str | None = None
    source: str = ""
    base_currency: str = "USD"


class ConvertCurrencyRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float = Field(gt=0)
    rate_type: str | None = None
    transaction_date: str | None = None
    notes: str | None = None


class CrossCurrencyTransferRequest(BaseModel):
    from_account_id: str
    to_account_id: str
    amount: float = Field(gt=0)
    rate_type: str | None = None
    transaction_date: str | None = None
    notes: str | None = None


class RevaluationRequest(BaseModel):
    currency: str
    new_rate: float = Field(gt=0)
    rate_type: str = "market"
    transaction_date: str | None = None
