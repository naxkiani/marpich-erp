"""Policy API schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class CreatePolicyRequest(BaseModel):
    domain: str = Field(min_length=2, max_length=32)
    key: str = Field(min_length=2, max_length=128, pattern=r"^[a-z][a-z0-9_.]*$")
    name: str = Field(min_length=2, max_length=256)
    description: str | None = None
    effective_from: str | None = None
    expires_at: str | None = None
    priority: int = Field(default=100, ge=0, le=10000)
    conditions: list[dict] = Field(default_factory=list)
    rules: list[dict] = Field(min_length=1)
    exceptions: list[dict] | None = None
    approval_required: bool = True


class CreateVersionRequest(BaseModel):
    effective_from: str | None = None
    expires_at: str | None = None
    priority: int = Field(default=100, ge=0, le=10000)
    conditions: list[dict] = Field(default_factory=list)
    rules: list[dict] = Field(min_length=1)
    exceptions: list[dict] | None = None
    approval_required: bool = True
    change_reason: str | None = None


class UpdateDraftVersionRequest(BaseModel):
    effective_from: str | None = None
    expires_at: str | None = None
    priority: int | None = Field(default=None, ge=0, le=10000)
    conditions: list[dict] | None = None
    rules: list[dict] | None = None
    exceptions: list[dict] | None = None


class EvaluateRequest(BaseModel):
    domain: str = Field(min_length=2, max_length=32)
    policy_key: str = Field(min_length=2, max_length=128)
    facts: dict = Field(default_factory=dict)
    as_of: str | None = None


class SimulateRequest(BaseModel):
    domain: str
    policy_key: str
    facts: dict = Field(default_factory=dict)
    candidate_versions: list[int] | None = None
    as_of: str | None = None


class TestCase(BaseModel):
    name: str
    facts: dict = Field(default_factory=dict)
    expect: dict = Field(default_factory=dict)


class RunTestsRequest(BaseModel):
    test_cases: list[TestCase] = Field(min_length=1)


class RollbackRequest(BaseModel):
    target_version: int = Field(ge=1)
    reason: str = Field(min_length=3, max_length=512)
