"""ACL: Cyber Security mission/vision/scope ↔ peers (P210-B)."""
from __future__ import annotations

from typing import Any


def to_security_incident(*, tenant_id: str, mission_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "mission_ref": mission_ref,
        "via_security_incident": True,
        "ir_lifecycle_owned_by_security_incident": True,
        "peer_ids_only": True,
    }


def to_strategy_plane(*, tenant_id: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "via_p210_a_strategy": True,
        "peer_ids_only": True,
    }


def to_ai_platform(*, tenant_id: str, surface_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "surface_ref": surface_ref,
        "via_ai_platform": True,
        "ai_security_required": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "action": action,
        "resource_ref": resource_ref,
        "via_audit_platform": True,
        "immutable": True,
        "peer_ids_only": True,
    }


def to_secrets_crypto(*, tenant_id: str, trust_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "trust_ref": trust_ref,
        "via_secrets": True,
        "crypto_owned_by_secrets": True,
        "peer_ids_only": True,
    }


def to_authorization(*, tenant_id: str, principal_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "principal_ref": principal_ref,
        "via_authorization": True,
        "zero_trust": True,
        "peer_ids_only": True,
    }
