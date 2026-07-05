"""Cash Management API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateCashLocationRequest(BaseModel):
    code: str
    name: str
    location_type: str
    currency: str = "USD"
    organization_id: str | None = None
    branch_id: str | None = None
    department_id: str | None = None
    opening_balance: float = 0.0
    gl_account_code: str | None = None


class CashTransactionRequest(BaseModel):
    location_id: str
    transaction_type: str
    amount: float = Field(gt=0)
    reference: str
    description: str | None = None
    counterpart_location_id: str | None = None


class CashCountRequest(BaseModel):
    location_id: str
    counted_amount: float = Field(ge=0)
    notes: str | None = None


class CashVerifyRequest(BaseModel):
    approved: bool = True
    notes: str | None = None


class CashCloseRequest(BaseModel):
    counted_amount: float = Field(ge=0)


class OpenClosingRequest(BaseModel):
    location_id: str


class CashReconcileRequest(BaseModel):
    location_id: str
    period_start: str
    period_end: str
    counted_balance: float


class CashForecastLineRequest(BaseModel):
    date: str
    label: str = ""
    inflow: float = 0.0
    outflow: float = 0.0


class CashForecastRequest(BaseModel):
    name: str
    period_start: str
    period_end: str
    scenario: str = "base"
    currency: str = "USD"
    opening_balance: float = 0.0
    projected_lines: list[CashForecastLineRequest]
