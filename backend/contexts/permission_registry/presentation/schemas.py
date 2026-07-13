"""Permission Registry presentation schemas."""
from __future__ import annotations

from pydantic import BaseModel, Field


class RegisterPermissionItem(BaseModel):
    code: str
    description: str = ""


class RegisterPermissionsRequest(BaseModel):
    module: str
    permissions: list[RegisterPermissionItem]


class CreateRoleRequest(BaseModel):
    code: str
    name: str
    description: str = ""
    permission_codes: list[str] = Field(default_factory=list)


class AssignRoleRequest(BaseModel):
    principal_id: str
    scope_type: str = "tenant"
    scope_id: str | None = None


class CreatePermissionSetRequest(BaseModel):
    module: str
    name: str
    description: str = ""
    permission_codes: list[str] = Field(default_factory=list)
