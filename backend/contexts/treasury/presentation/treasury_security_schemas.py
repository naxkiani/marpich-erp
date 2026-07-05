"""Treasury Security API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreateSecurityPolicyRequest(BaseModel):
    name: str
    policy_type: str
    rules: dict = Field(default_factory=dict)
    description: str = ""


class CreateTransactionLimitRequest(BaseModel):
    operation_type: str
    name: str
    max_amount: float
    currency: str = "USD"
    daily_limit: float | None = None


class CreateApprovalMatrixRequest(BaseModel):
    operation_type: str
    role: str
    min_amount: float
    max_amount: float
    approval_level: int
    currency: str = "USD"


class CreateAccessRuleRequest(BaseModel):
    rule_type: str
    name: str
    roles: list[str] = Field(default_factory=list)
    attributes: dict = Field(default_factory=dict)
    allowed_operations: list[str] = Field(default_factory=list)
    denied_operations: list[str] = Field(default_factory=list)


class EvaluateAccessRequest(BaseModel):
    maker_id: str
    checker_id: str | None = None
    roles: list[str] = Field(default_factory=list)
    attributes: dict = Field(default_factory=dict)
    operation_type: str
    amount: float
    risk_score: float = 0.0
    device_verified: bool = False


class CreateSecurityOperationRequest(BaseModel):
    operation_type: str
    subject_ref: str
    amount: float
    currency: str = "USD"
    roles: list[str] = Field(default_factory=list)
    attributes: dict = Field(default_factory=dict)
    risk_score: float = 0.0
    device_verified: bool = False


class ApproveOperationRequest(BaseModel):
    with_signature: bool = True


class RejectOperationRequest(BaseModel):
    reason: str = ""


class LockTransactionRequest(BaseModel):
    subject_ref: str
    subject_type: str
    reason: str


class EmergencyFreezeRequest(BaseModel):
    reason: str
