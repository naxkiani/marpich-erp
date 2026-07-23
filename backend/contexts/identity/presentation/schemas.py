"""Pydantic request/response schemas."""
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=2, max_length=128)
    locale: str = Field(default="en-US", max_length=16)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    mfa_code: str | None = None
    mfa_token: str | None = None


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str | None = None
    revoke_all: bool = False


class MfaVerifyRequest(BaseModel):
    code: str = Field(min_length=6, max_length=8)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)
    revoke_other_sessions: bool = True


class AssignRolesRequest(BaseModel):
    role_codes: list[str] = Field(min_length=1, max_length=16)


class ApiResponse(BaseModel):
    data: dict | list
    meta: dict | None = None
