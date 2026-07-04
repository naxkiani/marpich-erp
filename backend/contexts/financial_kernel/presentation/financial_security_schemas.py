"""Enterprise Financial Security API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class SubmitMakerCheckerRequest(BaseModel):
    control_type: str
    resource_type: str
    resource_id: str
    payload: dict
    idempotency_key: str | None = None
    checker_id: str | None = None
    second_approver_id: str | None = None


class LockTransactionRequest(BaseModel):
    resource_type: str
    resource_id: str
    reason: str


class PeriodCloseRequestBody(BaseModel):
    close_type: str
    target_id: str


class CreateSecurityPolicyRequest(BaseModel):
    name: str
    policy_type: str
    resource_type: str
    rules: dict


class EvaluateAccessRequest(BaseModel):
    resource_type: str
    permission: str
    role: str = ""
    attributes: dict | None = None


class GuardedModificationRequest(BaseModel):
    resource_type: str
    resource_id: str
    action: str
    payload: dict = Field(default_factory=dict)
