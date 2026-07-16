"""OpenID Connect Provider — discovery, userinfo, JWKS, ID tokens."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt

from shared.infrastructure.settings import settings


class OidcProvider:
    def discovery(self, *, issuer: str) -> dict:
        base = issuer.rstrip("/")
        return {
            "issuer": base,
            "authorization_endpoint": f"{base}/authorize",
            "token_endpoint": f"{base}/token",
            "userinfo_endpoint": f"{base}/userinfo",
            "jwks_uri": f"{base}/jwks",
            "end_session_endpoint": f"{base}/logout",
            "response_types_supported": ["code"],
            "grant_types_supported": ["authorization_code", "refresh_token", "client_credentials"],
            "subject_types_supported": ["public"],
            "id_token_signing_alg_values_supported": ["HS256", "RS256"],
            "scopes_supported": ["openid", "profile", "email", "offline_access"],
            "token_endpoint_auth_methods_supported": ["client_secret_post", "client_secret_basic"],
            "code_challenge_methods_supported": ["S256"],
            "claims_supported": ["sub", "email", "name", "preferred_username", "tenant_id"],
            "backchannel_logout_supported": True,
            "frontchannel_logout_supported": True,
        }

    def jwks(self) -> dict:
        return {
            "keys": [
                {
                    "kty": "oct",
                    "kid": "marpich-default",
                    "alg": "HS256",
                    "use": "sig",
                }
            ]
        }

    def userinfo(self, *, claims: dict[str, Any]) -> dict:
        return {
            "sub": claims.get("sub"),
            "email": claims.get("email"),
            "name": claims.get("name"),
            "preferred_username": claims.get("preferred_username"),
            "tenant_id": claims.get("tenant_id"),
        }

    def id_token(
        self,
        *,
        sub: str,
        tenant_id: str,
        client_id: str,
        nonce: str | None = None,
        email: str | None = None,
        name: str | None = None,
        custom_claims: dict | None = None,
    ) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": sub,
            "iss": settings.jwt_issuer,
            "aud": client_id,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=settings.jwt_access_ttl)).timestamp()),
            "tenant_id": tenant_id,
        }
        if nonce:
            payload["nonce"] = nonce
        if email:
            payload["email"] = email
        if name:
            payload["name"] = name
        if custom_claims:
            payload.update(custom_claims)
        return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")

    def validate_state_nonce(self, *, state: str | None, expected_state: str | None, nonce: str | None, id_token_nonce: str | None) -> dict:
        errors = []
        if expected_state and state != expected_state:
            errors.append("invalid_state")
        if nonce and id_token_nonce and nonce != id_token_nonce:
            errors.append("invalid_nonce")
        return {"valid": len(errors) == 0, "errors": errors}
