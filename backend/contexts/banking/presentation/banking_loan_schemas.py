"""Loan Management API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ApplyLoanRequest(BaseModel):
    account_id: str
    loan_type: str = Field(..., description="personal | business | education | construction | mortgage | microfinance | agriculture")
    principal: float = Field(..., gt=0)
    tenure_months: int = Field(12, ge=1)
    interest_rate_annual: float | None = None


class ApproveLoanRequest(BaseModel):
    approver_id: str


class CollateralRequest(BaseModel):
    collateral_type: str
    description: str
    estimated_value: float = Field(..., gt=0)


class GuarantorRequest(BaseModel):
    guarantor_name: str
    guarantor_id_ref: str
    relationship: str = ""
    guaranteed_amount: float = 0.0


class CreditRiskAnalysisRequest(BaseModel):
    monthly_income: float = Field(..., gt=0)
    existing_obligations: float = Field(0.0, ge=0)
    ai_provider_ref: str | None = None


class DisburseLoanRequest(BaseModel):
    approver_id: str = "system"


class PayInstallmentRequest(BaseModel):
    installment_id: str
    approver_id: str = "system"
    days_overdue: int = Field(0, ge=0)


class RestructureLoanRequest(BaseModel):
    tenure_months: int = Field(..., ge=1)
    interest_rate_annual: float | None = None
    approver_id: str = "system"


class SettleLoanRequest(BaseModel):
    settlement_amount: float = Field(..., gt=0)
    approver_id: str


class EarlyCloseLoanRequest(BaseModel):
    closure_amount: float = Field(..., gt=0)
    approver_id: str
