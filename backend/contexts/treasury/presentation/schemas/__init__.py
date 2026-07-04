"""Treasury API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateTreasuryAccountRequest(BaseModel):
    code: str
    name: str
    account_type: str
    currency: str = "USD"
    bank_name: str | None = None
    account_number: str | None = None
    opening_balance: float = 0.0


class CreateTransferRequest(BaseModel):
    from_account_id: str
    to_account_id: str
    amount: float = Field(gt=0)
    currency: str = "USD"
    instrument: str
    reference: str
    description: str | None = None
    cheque_number: str | None = None
    require_approval: bool = True


class ApproveTransferRequest(BaseModel):
    workflow_instance_id: str | None = None


class ReconciliationItem(BaseModel):
    reference: str
    amount: float
    date: str | None = None


class CreateReconciliationRequest(BaseModel):
    treasury_account_id: str
    statement_date: str
    statement_balance: float
    statement_items: list[ReconciliationItem]
    book_items: list[ReconciliationItem] | None = None


class ForecastLineRequest(BaseModel):
    date: str
    label: str = ""
    inflow: float = 0.0
    outflow: float = 0.0


class CreateForecastRequest(BaseModel):
    name: str
    period_start: str
    period_end: str
    scenario: str = "base"
    currency: str = "USD"
    opening_balance: float | None = None
    projected_lines: list[ForecastLineRequest]
