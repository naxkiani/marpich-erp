"""Authorization PDP presentation schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AuthorizationCheckRequest(BaseModel):
    principal_id: str | None = None
    resource: str = ""
    action: str = ""
    permission_code: str | None = None
    context: dict = Field(default_factory=dict)


class AuthorizationBatchCheckRequest(BaseModel):
    principal_id: str | None = None
    checks: list[dict] = Field(default_factory=list)
    simulate: bool = False


class AuthorizationSimulateRequest(BaseModel):
    principal_id: str | None = None
    resource: str = ""
    action: str = ""
    permission_code: str | None = None
    context: dict = Field(default_factory=dict)
