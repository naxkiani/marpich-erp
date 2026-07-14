"""Federation gateway API schemas — RFC 9457 compatible."""
from __future__ import annotations

from pydantic import BaseModel, Field


class ProblemDetail(BaseModel):
    type: str = "about:blank"
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None
    error_code: str | None = None


class FederationLoginRequest(BaseModel):
    protocol: str | None = None
    email: str | None = None
    provider_ref: str | None = None
    client_id: str | None = None
    redirect_uri: str | None = None
    scope: str = "openid profile email"
    state: str = ""
    code_challenge: str | None = None
    code_challenge_method: str | None = None
    user_id: str | None = None
    callback_code: str | None = None
    callback_state: str | None = None
    saml_response: str | None = None
    relay_state: str | None = None


class FederationLogoutRequest(BaseModel):
    session_ref: str | None = None
    id_token_hint: str | None = None
    post_logout_redirect_uri: str | None = None


class FederationTokenRequest(BaseModel):
    grant_type: str
    client_id: str
    client_secret: str | None = None
    code: str | None = None
    redirect_uri: str | None = None
    code_verifier: str | None = None
    refresh_token: str | None = None
    scope: str | None = None
    user_id: str | None = None
    nonce: str | None = None


class FederationIntrospectRequest(BaseModel):
    token: str


class FederationRevokeRequest(BaseModel):
    token: str
    token_type_hint: str | None = None


class FederationProvisionRequest(BaseModel):
    resource_type: str = "User"
    operation: str = "create"
    payload: dict = Field(default_factory=dict)
    resource_id: str | None = None


class FederationSyncRequest(BaseModel):
    provider_ref: str
    connector_ref: str | None = None


class RegisterOAuthClientRequest(BaseModel):
    client_name: str
    redirect_uris: list[str]
    grant_types: list[str] | None = None
    scopes: list[str] | None = None
    require_pkce: bool = True
