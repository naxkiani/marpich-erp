"""Identity lifecycle API schemas."""
from __future__ import annotations

from pydantic import BaseModel


class RegisterLifecycleRequest(BaseModel):
    email: str
    display_name: str
    identity_ref: str | None = None
    user_id: str | None = None


class RegisterIdentityRequest(BaseModel):
    email: str
    display_name: str
    identity_type: str = "employee"
    channel: str = "rest_api"
    source: str = "api"
    method: str = "self_registration"
    national_id: str = ""
    employee_number: str = ""
    phone: str = ""
    organization_ref: str = ""
    approval_mode: str = "automatic"
    zt_context: dict = {}
    metadata: dict = {}
    auto_advance: bool = True


class DetectDuplicatesRequest(BaseModel):
    threshold: float = 0.85


class ApproveRegistrationRequest(BaseModel):
    force: bool = False


class RejectRegistrationRequest(BaseModel):
    reason: str = ""


class VerificationRequest(BaseModel):
    verification_type: str
    payload: dict = {}


class ReasonRequest(BaseModel):
    reason: str = ""


class MergeIdentityRequest(BaseModel):
    target_case_ref: str


class SplitIdentityRequest(BaseModel):
    new_identity_ref: str


class DeleteIdentityRequest(BaseModel):
    deletion_type: str = "soft"
    reason: str = ""


class ConsentRequest(BaseModel):
    purpose: str
    granted: bool = True
    version: str = "1.0"
