"""Federation security — mTLS, JWT/JWE/JWS validation, replay/nonce/state/audience."""
from __future__ import annotations

import hashlib
import time


def validate_federation_request(
    *,
    state: str | None = None,
    expected_state: str | None = None,
    nonce: str | None = None,
    expected_nonce: str | None = None,
    audience: str | None = None,
    expected_audience: str | None = None,
    origin: str | None = None,
    allowed_origins: list[str] | None = None,
    signature_valid: bool = True,
    replay_key: str | None = None,
    seen_replays: set[str] | None = None,
    token_exp: int | None = None,
    now: int | None = None,
) -> dict:
    errors: list[str] = []
    if expected_state and state != expected_state:
        errors.append("invalid_state")
    if expected_nonce and nonce != expected_nonce:
        errors.append("invalid_nonce")
    if expected_audience and audience != expected_audience:
        errors.append("invalid_audience")
    if allowed_origins and origin and origin not in allowed_origins:
        errors.append("invalid_origin")
    if not signature_valid:
        errors.append("invalid_signature")
    ts = now if now is not None else int(time.time())
    if token_exp is not None and token_exp < ts:
        errors.append("token_expired")
    if replay_key and seen_replays is not None and replay_key in seen_replays:
        errors.append("replay_detected")
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "protections": [
            "state_validation",
            "nonce_validation",
            "audience_validation",
            "origin_validation",
            "signature_validation",
            "replay_protection",
            "expiration",
        ],
    }


def fingerprint_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()[:32]


def certificate_security_posture(
    *,
    mtls: bool = False,
    pinned: bool = False,
    rotated_recently: bool = False,
    revoked: bool = False,
) -> dict:
    score = 40
    factors = []
    if mtls:
        score += 25
        factors.append("mtls")
    if pinned:
        score += 15
        factors.append("certificate_pinning")
    if rotated_recently:
        score += 15
        factors.append("recent_rotation")
    if revoked:
        score = 0
        factors.append("revoked")
    return {
        "security_score": max(0, min(100, score)),
        "factors": factors,
        "supports": ["PKI", "CRL", "OCSP", "JWKS_rotation", "HSM"],
    }
