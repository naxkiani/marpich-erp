"""Authentication engine — catalog, policy keys, OIDC helpers."""
from __future__ import annotations

import secrets
from urllib.parse import urlencode

from contexts.authentication.domain.aggregates.authentication_platform import AuthenticationCapability

POLICY_KEYS = [
    "authentication.webauthn.enabled",
    "authentication.passkeys.required",
    "authentication.oidc.enabled",
    "authentication.password.enabled",
]

CAPABILITY_LABELS = {
    AuthenticationCapability.WEBAUTHN_REGISTRATION.value: "WebAuthn Registration",
    AuthenticationCapability.WEBAUTHN_AUTHENTICATION.value: "WebAuthn Authentication",
    AuthenticationCapability.PASSKEY_MANAGEMENT.value: "Passkey Management",
    AuthenticationCapability.OIDC_PROVIDER_REGISTRY.value: "OIDC Provider Registry",
    AuthenticationCapability.OIDC_AUTHORIZATION.value: "OIDC Authorization",
    AuthenticationCapability.OIDC_CALLBACK.value: "OIDC Callback",
    AuthenticationCapability.AUTH_METHOD_CATALOG.value: "Auth Method Catalog",
    AuthenticationCapability.POLICY_DRIVEN_AUTHENTICATION.value: "Policy-Driven Authentication",
    AuthenticationCapability.AUTHENTICATION_DASHBOARD.value: "Authentication Dashboard",
    AuthenticationCapability.AUTHENTICATION_API.value: "Authentication API",
}

AUTH_METHODS = [
    {"method": "password", "label": "Password", "mfa_capable": True},
    {"method": "webauthn", "label": "WebAuthn / Passkeys", "mfa_capable": False},
    {"method": "oidc", "label": "OIDC Federation", "mfa_capable": True},
]


def list_capability_catalog() -> list[dict]:
    return [
        {"capability": c.value, "label": CAPABILITY_LABELS.get(c.value, c.name.replace("_", " ").title())}
        for c in AuthenticationCapability
    ]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def list_auth_methods() -> list[dict]:
    return list(AUTH_METHODS)


def dependency_map() -> dict:
    return {
        "nodes": [
            {"id": "authentication", "type": "platform", "label": "Authentication"},
            {"id": "identity", "type": "platform", "label": "Identity Core"},
            {"id": "authorization", "type": "platform", "label": "Authorization PDP"},
        ],
        "edges": [
            {"from": "authentication", "to": "identity", "type": "token_delegate"},
            {"from": "authorization", "to": "identity", "type": "principal_delegate"},
        ],
    }


def build_oidc_authorize_url(
    *,
    issuer_url: str,
    client_id: str,
    redirect_uri: str,
    scopes: str,
    state: str,
    nonce: str,
) -> str:
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scopes,
        "state": state,
        "nonce": nonce,
    }
    return f"{issuer_url.rstrip('/')}/authorize?{urlencode(params)}"


def new_oidc_state() -> str:
    return secrets.token_urlsafe(32)


def new_oidc_nonce() -> str:
    return secrets.token_urlsafe(24)
