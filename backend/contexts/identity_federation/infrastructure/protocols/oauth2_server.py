"""OAuth 2.1 Authorization Server — policy-driven token issuance."""
from __future__ import annotations

import hashlib
import secrets
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt

from shared.infrastructure.settings import settings

# In-memory registries — production uses PostgreSQL + Vault
_clients: dict[str, dict] = {}
_auth_codes: dict[str, dict] = {}
_tokens: dict[str, dict] = {}
_revoked: set[str] = set()


class OAuth2AuthorizationServer:
    """OAuth 2.1 AS with PKCE, client credentials, refresh, revoke, introspect."""

    def register_client(
        self,
        *,
        tenant_id: str,
        client_name: str,
        redirect_uris: list[str],
        grant_types: list[str] | None = None,
        scopes: list[str] | None = None,
        require_pkce: bool = True,
    ) -> dict:
        client_id = f"client-{uuid.uuid4().hex[:16]}"
        client_secret = secrets.token_urlsafe(32)
        record = {
            "tenant_id": tenant_id,
            "client_id": client_id,
            "client_secret_hash": hashlib.sha256(client_secret.encode()).hexdigest(),
            "client_name": client_name,
            "redirect_uris": redirect_uris,
            "grant_types": grant_types or ["authorization_code", "refresh_token", "client_credentials"],
            "scopes": scopes or ["openid", "profile", "email"],
            "require_pkce": require_pkce,
            "created_at": datetime.now(UTC).isoformat(),
        }
        _clients[f"{tenant_id}:{client_id}"] = record
        return {"client_id": client_id, "client_secret": client_secret, **{k: v for k, v in record.items() if k != "client_secret_hash"}}

    def authorize(
        self,
        *,
        tenant_id: str,
        client_id: str,
        redirect_uri: str,
        scope: str,
        state: str,
        code_challenge: str | None = None,
        code_challenge_method: str | None = None,
        user_id: str | None = None,
    ) -> dict:
        client = _clients.get(f"{tenant_id}:{client_id}")
        if not client:
            return {"error": "invalid_client"}
        if redirect_uri not in client["redirect_uris"]:
            return {"error": "invalid_redirect_uri"}
        if client.get("require_pkce") and not code_challenge:
            return {"error": "pkce_required"}
        code = secrets.token_urlsafe(32)
        _auth_codes[code] = {
            "tenant_id": tenant_id,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": code_challenge_method or "S256",
            "user_id": user_id,
            "expires_at": (datetime.now(UTC) + timedelta(minutes=10)).isoformat(),
        }
        return {
            "authorization_code": code,
            "redirect_uri": redirect_uri,
            "state": state,
            "expires_in": 600,
        }

    def token(
        self,
        *,
        tenant_id: str,
        grant_type: str,
        client_id: str,
        client_secret: str | None = None,
        code: str | None = None,
        redirect_uri: str | None = None,
        code_verifier: str | None = None,
        refresh_token: str | None = None,
        scope: str | None = None,
        user_id: str | None = None,
    ) -> dict:
        client = _clients.get(f"{tenant_id}:{client_id}")
        if not client:
            return {"error": "invalid_client", "error_description": "Unknown client"}

        if grant_type == "authorization_code":
            return self._exchange_code(tenant_id, client, code, redirect_uri, code_verifier)
        if grant_type == "client_credentials":
            if not self._verify_client_secret(client, client_secret):
                return {"error": "invalid_client"}
            return self._issue_tokens(tenant_id, client_id, user_id or "service", scope or " ".join(client["scopes"]))
        if grant_type == "refresh_token":
            return self._refresh(refresh_token, tenant_id, client_id)
        return {"error": "unsupported_grant_type"}

    def _exchange_code(
        self,
        tenant_id: str,
        client: dict,
        code: str | None,
        redirect_uri: str | None,
        code_verifier: str | None,
    ) -> dict:
        if not code or code not in _auth_codes:
            return {"error": "invalid_grant"}
        auth = _auth_codes.pop(code)
        if auth["tenant_id"] != tenant_id or auth["client_id"] != client["client_id"]:
            return {"error": "invalid_grant"}
        if redirect_uri and auth["redirect_uri"] != redirect_uri:
            return {"error": "invalid_grant"}
        if auth.get("code_challenge"):
            if not code_verifier:
                return {"error": "invalid_grant", "error_description": "PKCE verifier required"}
            challenge = hashlib.sha256(code_verifier.encode()).digest()
            import base64
            expected = base64.urlsafe_b64encode(challenge).rstrip(b"=").decode()
            if expected != auth["code_challenge"]:
                return {"error": "invalid_grant", "error_description": "PKCE verification failed"}
        return self._issue_tokens(tenant_id, client["client_id"], auth.get("user_id", "user"), auth["scope"])

    def _issue_tokens(self, tenant_id: str, client_id: str, user_id: str, scope: str) -> dict:
        now = datetime.now(UTC)
        access_jti = uuid.uuid4().hex
        refresh_jti = uuid.uuid4().hex
        access_token = jwt.encode(
            {
                "sub": user_id,
                "tenant_id": tenant_id,
                "client_id": client_id,
                "scope": scope,
                "type": "access",
                "jti": access_jti,
                "iss": settings.jwt_issuer,
                "iat": int(now.timestamp()),
                "exp": int((now + timedelta(seconds=settings.jwt_access_ttl)).timestamp()),
            },
            settings.jwt_secret,
            algorithm="HS256",
        )
        refresh_token = secrets.token_urlsafe(48)
        _tokens[refresh_jti] = {
            "tenant_id": tenant_id,
            "client_id": client_id,
            "user_id": user_id,
            "scope": scope,
            "refresh_token_hash": hashlib.sha256(refresh_token.encode()).hexdigest(),
            "expires_at": (now + timedelta(seconds=settings.jwt_refresh_ttl)).isoformat(),
        }
        _tokens[access_jti] = {"type": "access", "active": True, "tenant_id": tenant_id, "user_id": user_id}
        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": settings.jwt_access_ttl,
            "refresh_token": refresh_token,
            "scope": scope,
        }

    def _refresh(self, refresh_token: str | None, tenant_id: str, client_id: str) -> dict:
        if not refresh_token:
            return {"error": "invalid_grant"}
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        for jti, record in _tokens.items():
            if record.get("refresh_token_hash") == token_hash and record["tenant_id"] == tenant_id:
                return self._issue_tokens(tenant_id, client_id, record["user_id"], record["scope"])
        return {"error": "invalid_grant"}

    def revoke(self, *, token: str, token_type_hint: str | None = None) -> dict:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
            jti = payload.get("jti")
            if jti:
                _revoked.add(jti)
                if jti in _tokens:
                    _tokens[jti]["active"] = False
        except Exception:
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            for jti, record in _tokens.items():
                if record.get("refresh_token_hash") == token_hash:
                    _revoked.add(jti)
                    record["active"] = False
        return {"revoked": True}

    def introspect(self, *, token: str) -> dict:
        if not token:
            return {"active": False}
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
            jti = payload.get("jti", "")
            active = jti not in _revoked and _tokens.get(jti, {}).get("active", True)
            return {
                "active": active,
                "sub": payload.get("sub"),
                "client_id": payload.get("client_id"),
                "scope": payload.get("scope"),
                "exp": payload.get("exp"),
                "iss": payload.get("iss"),
            }
        except Exception:
            return {"active": False}

    @staticmethod
    def _verify_client_secret(client: dict, secret: str | None) -> bool:
        if not secret:
            return False
        return hashlib.sha256(secret.encode()).hexdigest() == client.get("client_secret_hash")

    @classmethod
    def reset(cls) -> None:
        _clients.clear()
        _auth_codes.clear()
        _tokens.clear()
        _revoked.clear()
