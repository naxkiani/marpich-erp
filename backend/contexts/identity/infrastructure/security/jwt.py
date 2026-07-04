"""JWT access + refresh tokens."""
from __future__ import annotations

import hashlib
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from shared.infrastructure.settings import settings


class JwtTokenService:
    def __init__(self) -> None:
        self._secret = settings.jwt_secret
        self._issuer = settings.jwt_issuer
        self._access_ttl = settings.jwt_access_ttl
        self._refresh_ttl = settings.jwt_refresh_ttl

    def sign_access(self, payload: dict[str, Any]) -> str:
        return self._sign(payload, self._access_ttl, token_type="access")

    def sign_refresh(self, payload: dict[str, Any]) -> str:
        data = {**payload, "jti": str(uuid.uuid4())}
        return self._sign(data, self._refresh_ttl, token_type="refresh")

    def verify_access(self, token: str) -> dict[str, Any]:
        return self._verify(token, expected_type="access")

    def verify_refresh(self, token: str) -> dict[str, Any]:
        return self._verify(token, expected_type="refresh")

    @staticmethod
    def hash_refresh_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def _sign(self, payload: dict[str, Any], ttl: int, token_type: str) -> str:
        now = datetime.now(UTC)
        claims = {
            **payload,
            "type": token_type,
            "iss": self._issuer,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(seconds=ttl)).timestamp()),
        }
        return jwt.encode(claims, self._secret, algorithm="HS256")

    def _verify(self, token: str, expected_type: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, self._secret, algorithms=["HS256"])
        except JWTError as exc:
            raise ValueError("Invalid token") from exc
        if payload.get("type") != expected_type:
            raise ValueError("Invalid token type")
        return payload
