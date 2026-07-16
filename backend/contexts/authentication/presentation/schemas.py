"""Authentication API schemas."""
from __future__ import annotations

from pydantic import BaseModel


class PasskeyRegistrationVerifyRequest(BaseModel):
    challenge_id: str
    credential: dict
    nickname: str = "Passkey"


class PasskeyLoginBeginRequest(BaseModel):
    email: str


class PasskeyLoginVerifyRequest(BaseModel):
    challenge_id: str
    credential: dict


class RegisterOidcProviderRequest(BaseModel):
    name: str
    issuer_url: str
    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: str | None = None


class OidcAuthorizeRequest(BaseModel):
    provider_ref: str


class OidcCallbackRequest(BaseModel):
    code: str
    state: str
