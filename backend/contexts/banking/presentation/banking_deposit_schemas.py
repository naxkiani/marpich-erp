"""Deposit Management API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class OpenDepositRequest(BaseModel):
    account_id: str
    deposit_type: str = Field(..., description="savings | current | term | recurring")
    principal: float = Field(0.0, ge=0)
    interest_rate_annual: float | None = None
    profit_rule_id: str | None = None
    tenure_months: int | None = None
    auto_renew: bool = False
    recurring_amount: float = 0.0
    recurring_day: int = Field(1, ge=1, le=28)


class DepositTransactionRequest(BaseModel):
    deposit_id: str
    transaction_type: str = Field(..., description="deposit | withdrawal")
    amount: float = Field(..., gt=0)


class ApproveDepositRequest(BaseModel):
    approver_id: str


class ApproveTransactionRequest(BaseModel):
    approver_id: str


class AccrueInterestRequest(BaseModel):
    deposit_id: str
    days: int = Field(1, ge=1)


class PostInterestRequest(BaseModel):
    deposit_id: str
    approver_id: str = "system"


class RenewDepositRequest(BaseModel):
    tenure_months: int = Field(..., ge=1)
    interest_rate_annual: float | None = None


class ProfitRuleRequest(BaseModel):
    rule_code: str
    name: str
    deposit_type: str
    method: str = "interest"
    rate_annual: float = 0.0
    profit_share_pct: float = Field(0.0, ge=0, le=100)


class GenerateStatementRequest(BaseModel):
    period_days: int = Field(30, ge=1, le=365)
