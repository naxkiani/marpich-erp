"""P311 — JWT sign/verify: valid, expired, tampered, wrong issuer, wrong type."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from jose import jwt

from contexts.identity.infrastructure.security.jwt import JwtTokenService
from shared.infrastructure.settings import settings


def test_valid_access_roundtrip():
    svc = JwtTokenService()
    token = svc.sign_access({"sub": "user-1", "tenant_id": "t1", "permissions": ["a.read"]})
    payload = svc.verify_access(token)
    assert payload["sub"] == "user-1"
    assert payload["type"] == "access"
    assert payload["iss"] == settings.jwt_issuer


def test_refresh_rejected_as_access():
    svc = JwtTokenService()
    token = svc.sign_refresh({"sub": "user-1"})
    with pytest.raises(ValueError, match="Invalid token"):
        svc.verify_access(token)


def test_tampered_signature_rejected():
    svc = JwtTokenService()
    token = svc.sign_access({"sub": "user-1"})
    tampered = token[:-4] + "abcd"
    with pytest.raises(ValueError, match="Invalid token"):
        svc.verify_access(tampered)


def test_expired_token_rejected():
    svc = JwtTokenService()
    now = datetime.now(UTC)
    claims = {
        "sub": "user-1",
        "type": "access",
        "iss": settings.jwt_issuer,
        "iat": int((now - timedelta(hours=2)).timestamp()),
        "exp": int((now - timedelta(hours=1)).timestamp()),
    }
    token = jwt.encode(claims, settings.jwt_secret, algorithm="HS256")
    with pytest.raises(ValueError, match="Invalid token"):
        svc.verify_access(token)


def test_wrong_issuer_rejected():
    svc = JwtTokenService()
    now = datetime.now(UTC)
    claims = {
        "sub": "user-1",
        "type": "access",
        "iss": "not-marpich",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=1)).timestamp()),
    }
    token = jwt.encode(claims, settings.jwt_secret, algorithm="HS256")
    with pytest.raises(ValueError, match="Invalid token"):
        svc.verify_access(token)


def test_missing_token_not_verified_here():
    svc = JwtTokenService()
    with pytest.raises(ValueError):
        svc.verify_access("")
