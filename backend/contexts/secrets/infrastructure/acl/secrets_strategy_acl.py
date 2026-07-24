"""ACL: Secrets Strategy ↔ peers (P209-A)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_governed_store(*, tenant_id: str, store_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "store_ref": store_ref,
        "governed_stores_only": True,
        "outside_governed_forbidden": True,
        "peer_ids_only": True,
    }


def to_key_export_policy(*, tenant_id: str, key_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "key_ref": key_ref,
        "export_requires_policy": True,
        "export_without_policy_forbidden": True,
        "peer_ids_only": True,
    }


def to_hsm(*, tenant_id: str, operation: str, key_ref: str) -> dict[str, Any]:
    result = base.to_hsm(
        tenant_id=tenant_id, operation=operation, key_ref=key_ref
    )
    result["hsm_strategy_required"] = True
    return result


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["crypto_ops_must_be_audited"] = True
    result["strategy_audit"] = True
    return result


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    return base.to_ai_infer(
        tenant_id=tenant_id, surface=surface, context=context
    )


def to_pam_ref(*, tenant_id: str, secret_ref: str) -> dict[str, Any]:
    return base.to_pam_ref(tenant_id=tenant_id, secret_ref=secret_ref)


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": ["governed_store", "kms", "hsm", "audit", "ai", "pam"],
        "governed_stores_only": True,
        "export_requires_policy": True,
        "hsm_required": True,
        "crypto_ops_audited": True,
        "pam_orchestrates_refs_only": True,
    }
