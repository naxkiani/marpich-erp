"""Token federation — exchange, translation, validation across protocols."""
from __future__ import annotations


SUPPORTED_TOKEN_TYPES = (
    "access_token",
    "refresh_token",
    "id_token",
    "saml_assertion",
    "opaque",
    "legacy",
)


def exchange_token(
    *,
    source_type: str,
    target_type: str,
    subject: str,
    audience: str,
    scopes: list[str] | None = None,
    claims: dict | None = None,
) -> dict:
    if source_type not in SUPPORTED_TOKEN_TYPES or target_type not in SUPPORTED_TOKEN_TYPES:
        return {"exchanged": False, "error": "unsupported_token_type"}
    return {
        "exchanged": True,
        "source_type": source_type,
        "target_type": target_type,
        "subject": subject,
        "audience": audience,
        "scopes": scopes or [],
        "claims": claims or {},
        "translation": f"{source_type}->{target_type}",
    }


def validate_federated_token(
    *,
    token_type: str,
    expired: bool = False,
    audience_ok: bool = True,
    signature_ok: bool = True,
    issuer_ok: bool = True,
    revoked: bool = False,
) -> dict:
    errors = []
    if expired:
        errors.append("expired")
    if not audience_ok:
        errors.append("audience")
    if not signature_ok:
        errors.append("signature")
    if not issuer_ok:
        errors.append("issuer")
    if revoked:
        errors.append("revoked")
    return {
        "token_type": token_type,
        "valid": len(errors) == 0,
        "errors": errors,
        "engine": "token_federation_validation",
    }


def translate_claims_for_protocol(*, protocol: str, claims: dict) -> dict:
    """Normalize claims toward federation fabric claim set."""
    mapping = {
        "oidc": {"sub": "sub", "email": "email", "name": "name"},
        "saml": {"NameID": "sub", "emailAddress": "email", "displayName": "name"},
        "legacy": {"user_id": "sub", "mail": "email", "cn": "name"},
    }
    rules = mapping.get(protocol, mapping["oidc"])
    out = {}
    for src, dst in rules.items():
        if src in claims:
            out[dst] = claims[src]
    for k, v in claims.items():
        if k not in rules and k not in out:
            out[k] = v
    return out
