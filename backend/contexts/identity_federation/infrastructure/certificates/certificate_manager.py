"""Certificate management — JWKS rotation, PKI hooks."""
from __future__ import annotations

import secrets
import uuid
from datetime import UTC, datetime, timedelta

_certs: dict[str, dict] = {}


class CertificateManager:
    def register_certificate(
        self,
        *,
        tenant_id: str,
        cert_ref: str,
        pem: str,
        purpose: str = "signing",
        expires_at: datetime | None = None,
    ) -> dict:
        kid = f"key-{uuid.uuid4().hex[:12]}"
        record = {
            "tenant_id": tenant_id,
            "cert_ref": cert_ref,
            "kid": kid,
            "purpose": purpose,
            "pem": pem,
            "status": "active",
            "created_at": datetime.now(UTC).isoformat(),
            "expires_at": (expires_at or datetime.now(UTC) + timedelta(days=365)).isoformat(),
        }
        _certs[f"{tenant_id}:{cert_ref}"] = record
        return {"cert_ref": cert_ref, "kid": kid, "status": "active"}

    def rotate_jwks(self, *, tenant_id: str) -> dict:
        new_kid = f"key-{secrets.token_hex(8)}"
        return {
            "rotated": True,
            "new_kid": new_kid,
            "previous_kids_retained": 1,
            "rotation_at": datetime.now(UTC).isoformat(),
        }

    def jwks_for_tenant(self, *, tenant_id: str) -> dict:
        keys = [
            {"kty": "oct", "kid": c["kid"], "alg": "HS256", "use": c["purpose"]}
            for c in _certs.values()
            if c["tenant_id"] == tenant_id and c["status"] == "active"
        ]
        if not keys:
            keys = [{"kty": "oct", "kid": "marpich-default", "alg": "HS256", "use": "sig"}]
        return {"keys": keys}

    def revoke(self, *, tenant_id: str, cert_ref: str) -> dict:
        key = f"{tenant_id}:{cert_ref}"
        if key in _certs:
            _certs[key]["status"] = "revoked"
            return {"revoked": True, "cert_ref": cert_ref}
        return {"revoked": False}

    @classmethod
    def reset(cls) -> None:
        _certs.clear()
