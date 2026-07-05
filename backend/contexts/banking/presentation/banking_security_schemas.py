"""Banking Security Platform API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class EvaluateAccessRequest(BaseModel):
    roles: list[str] = Field(default_factory=list)
    permission: str
    attributes: dict = Field(default_factory=dict)


class CheckLimitsRequest(BaseModel):
    user_id: str
    amount: float = Field(..., gt=0)
    currency: str = "USD"


class RegisterDeviceRequest(BaseModel):
    user_id: str
    device_fingerprint: str


class VerifyDeviceRequest(BaseModel):
    user_id: str
    device_fingerprint: str


class RegisterSessionRequest(BaseModel):
    user_id: str
    device_id: str | None = None
    ip_address: str = ""


class SessionHeartbeatRequest(BaseModel):
    risk_score: float | None = None


class MonitorTransactionRequest(BaseModel):
    user_id: str
    action_type: str
    amount: float = Field(..., ge=0)
    currency: str = "USD"
    risk_score: float = 100.0
    factors: list[dict] = Field(default_factory=list)


class AssessRiskRequest(BaseModel):
    user_id: str
    amount: float = Field(..., ge=0)
    device_trusted: bool = False
    session_id: str | None = None


class SubmitApprovalRequest(BaseModel):
    action_type: str
    resource_id: str
    maker_id: str
    payload: dict = Field(default_factory=dict)
    required_approvals: int | None = None


class ApproveRequestRequest(BaseModel):
    approver_id: str


class AuthorizeActionRequest(BaseModel):
    user_id: str
    roles: list[str] = Field(default_factory=lambda: ["admin"])
    action_type: str
    resource_id: str
    amount: float = 0.0
    attributes: dict = Field(default_factory=dict)
    device_fingerprint: str = ""
    session_id: str | None = None
    payload: dict = Field(default_factory=dict)


class SignPayloadRequest(BaseModel):
    resource_id: str
    payload: dict = Field(default_factory=dict)
    signer_id: str


class EncryptDataRequest(BaseModel):
    payload: dict = Field(default_factory=dict)


class ActivateFreezeRequest(BaseModel):
    activated_by: str
    reason: str = ""
    scope: str = "tenant"


class ReleaseFreezeRequest(BaseModel):
    released_by: str
