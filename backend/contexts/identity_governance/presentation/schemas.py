"""Enterprise Identity Governance Platform API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class SodCheckRequest(BaseModel):
    existing_roles: list[str] = Field(default_factory=list)
    requested_roles: list[str] = Field(default_factory=list)


class SubmitAccessRequest(BaseModel):
    target_user_id: str
    requested_roles: list[str]
    justification: str
    existing_roles: list[str] = Field(default_factory=list)


class ScheduleAccessReviewRequest(BaseModel):
    title: str
    reviewer_id: str = ""
    scope_user_ids: list[str] = Field(default_factory=list)


class CompleteAccessReviewRequest(BaseModel):
    findings: list[dict] = Field(default_factory=list)


class InitiateCertificationRequest(BaseModel):
    user_id: str
    role_ids: list[str]


class CertifyPrivilegesRequest(BaseModel):
    notes: str = ""


class GrantTemporaryAccessRequest(BaseModel):
    user_id: str
    roles: list[str]
    hours: int | None = None
    justification: str = ""


class GrantEmergencyAccessRequest(BaseModel):
    user_id: str
    roles: list[str]
    incident_ref: str = ""
    justification: str = ""
