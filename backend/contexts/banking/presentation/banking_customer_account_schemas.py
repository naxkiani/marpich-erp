"""Banking Customer and Account API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateCustomerRequest(BaseModel):
    customer_type: str
    display_name: str
    legal_name: str
    email: str
    phone: str
    organization_id: str | None = None
    branch_id: str | None = None
    registration_number: str | None = None
    tax_id: str | None = None
    risk_rating: str = "low"
    auto_submit: bool = False


class UpdateKycStatusRequest(BaseModel):
    status: str


class UpdateRiskRatingRequest(BaseModel):
    rating: str


class CreateKycRequest(BaseModel):
    tier: str
    document_type: str
    document_ref: str
    notes: str = ""


class VerifyKycRequest(BaseModel):
    verified_by: str


class CreateProductRequest(BaseModel):
    product_code: str
    name: str
    account_type: str
    currency: str = "USD"
    interest_rate_annual: float = 0.0
    minimum_balance: float = 0.0
    overdraft_limit: float = 0.0
    overdraft_enabled: bool = False


class OpenAccountRequest(BaseModel):
    customer_id: str
    product_code: str
    organization_id: str | None = None
    branch_id: str | None = None
    is_joint: bool = False
    joint_holders: list[str] = Field(default_factory=list)
    opening_balance: float = 0.0
    currency: str | None = None


class TransitionStatusRequest(BaseModel):
    status: str
    reason: str = ""


class OverdraftCheckRequest(BaseModel):
    amount: float
