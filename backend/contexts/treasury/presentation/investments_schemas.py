"""Enterprise Investment Management API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateInvestmentRequest(BaseModel):
    portfolio_name: str = "Core Treasury Portfolio"
    investment_type: str
    name: str
    instrument_code: str
    principal_amount: float = Field(gt=0)
    currency: str = "USD"
    interest_rate: float = Field(default=0.0, ge=0)
    purchase_date: str
    maturity_date: str | None = None
    risk_rating: str | None = None
    treasury_account_id: str | None = None
    notes: str | None = None


class AccrueInterestRequest(BaseModel):
    days: int = Field(default=1, ge=1, le=365)
    accrual_date: str | None = None


class RecordIncomeRequest(BaseModel):
    amount: float = Field(gt=0)
    transaction_date: str | None = None
    notes: str | None = None


class MatureInvestmentRequest(BaseModel):
    maturity_date: str | None = None
