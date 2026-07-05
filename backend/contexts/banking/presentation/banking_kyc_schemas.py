"""Enterprise KYC Platform API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class OpenKycCaseRequest(BaseModel):
    customer_id: str
    due_diligence_level: str = "standard"
    organization_id: str | None = None
    branch_id: str | None = None


class SubmitDocumentRequest(BaseModel):
    document_type: str
    document_ref: str
    issuing_country: str = ""
    expiry_date: str | None = None
    metadata: dict = Field(default_factory=dict)


class VerifyDocumentRequest(BaseModel):
    verified_by: str


class SubmitAddressRequest(BaseModel):
    address_line: str
    city: str
    country: str
    postal_code: str = ""
    proof_document_id: str | None = None


class VerifyAddressRequest(BaseModel):
    verified_by: str


class ScreeningRequest(BaseModel):
    match_score: float = 0.0
    match_details: dict = Field(default_factory=dict)
    provider_ref: str = ""
    screened_by: str | None = None


class ApproveCaseRequest(BaseModel):
    approver_id: str


class RejectCaseRequest(BaseModel):
    approver_id: str
    reason: str = ""


class ScheduleReviewRequest(BaseModel):
    due_in_days: int | None = None


class CompleteReviewRequest(BaseModel):
    completed_by: str
    outcome: str


class BiometricHookRequest(BaseModel):
    provider: str
    hook_ref: str
    callback_url: str = ""


class CompleteBiometricRequest(BaseModel):
    status: str
    result_payload: dict = Field(default_factory=dict)


class EvaluatePolicyRequest(BaseModel):
    policy_key: str
    facts: dict = Field(default_factory=dict)
