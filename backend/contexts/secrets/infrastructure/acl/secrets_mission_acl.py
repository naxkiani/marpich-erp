"""ACL: Secrets Mission / Vision / Scope ↔ peers (P209-B)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["mission_charter_audit"] = True
    return result


def to_pam_ref(*, tenant_id: str, secret_ref: str) -> dict[str, Any]:
    result = base.to_pam_ref(tenant_id=tenant_id, secret_ref=secret_ref)
    result["does_not_replace_pam_sor"] = True
    return result


def to_authorization_boundary(*, tenant_id: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "does_not_own_business_authorization": True,
        "peer_sor": "authorization",
        "peer_ids_only": True,
    }


def to_identity_boundary(*, tenant_id: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "does_not_replace_identity_sor": True,
        "provides_identity_trust_certificates": True,
        "peer_sor": "identity",
        "peer_ids_only": True,
    }


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    return base.to_ai_infer(
        tenant_id=tenant_id, surface=surface, context=context
    )


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": ["audit", "pam", "authorization", "identity", "ai"],
        "does_not_own_business_authorization": True,
        "does_not_replace_peer_sors": True,
        "pam_orchestrates_refs_only": True,
    }
