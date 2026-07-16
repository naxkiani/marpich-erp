"""Document integrity + QR verification (Document Exchange).

QR tokens: HMAC-SHA256 over shared secret (compact public URL binding).
Content integrity: RSA-PSS-SHA256 via IDocumentContentSigner (infrastructure).
"""
from __future__ import annotations

import base64
import hashlib
import hmac
from datetime import UTC, datetime

from shared.infrastructure.settings import settings


def _signing_secret() -> bytes:
    secret = (settings.document_signing_secret or settings.jwt_secret or "").encode()
    if not secret:
        secret = b"marpich-documents-dev-only"
    return secret


def generate_qr_token(
    *,
    tenant_id: str,
    document_id: str,
    version_number: int,
    checksum: str,
) -> str:
    payload = f"{tenant_id}:{document_id}:{version_number}:{checksum}"
    sig = hmac.new(_signing_secret(), payload.encode(), hashlib.sha256).hexdigest()[:24]
    raw = f"{payload}:{sig}"
    return base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")


def verify_qr_token(token: str) -> dict | None:
    try:
        padded = token + "=" * (-len(token) % 4)
        raw = base64.urlsafe_b64decode(padded.encode()).decode()
    except (ValueError, UnicodeDecodeError):
        return None
    parts = raw.rsplit(":", 1)
    if len(parts) != 2:
        return None
    payload, sig = parts
    expected = hmac.new(_signing_secret(), payload.encode(), hashlib.sha256).hexdigest()[:24]
    if not hmac.compare_digest(sig, expected):
        return None
    try:
        tenant_id, document_id, version_number, checksum = payload.split(":", 3)
        return {
            "tenant_id": tenant_id,
            "document_id": document_id,
            "version_number": int(version_number),
            "checksum": checksum,
            "valid": True,
        }
    except ValueError:
        return None


def build_watermark(*, tenant_id: str, actor_id: str | None, document_id: str) -> dict:
    return {
        "text": f"{tenant_id} · {actor_id or 'anonymous'} · {document_id}",
        "tenant_id": tenant_id,
        "actor_id": actor_id,
        "document_id": document_id,
        "applied_at": datetime.now(UTC).isoformat(),
        "mutate_stored": False,
    }
