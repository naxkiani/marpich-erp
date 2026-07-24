"""ACL: Secrets Cryptography Services ↔ peers (P209-I)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_kms_key_ref(*, tenant_id: str, key_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "key_ref": key_ref,
        "via_kms": True,
        "key_refs_only": True,
        "keys_exposed_forbidden": True,
        "peer_ids_only": True,
    }


def to_hsm_accelerate(*, tenant_id: str, operation_ref: str) -> dict[str, Any]:
    result = base.to_hsm(
        tenant_id=tenant_id,
        operation="accelerate_crypto",
        key_ref=operation_ref,
    )
    result["hsm_acceleration"] = True
    return result


def to_policy_algorithm(
    *, tenant_id: str, algorithm_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "algorithm_ref": algorithm_ref,
        "via_policy_engine": True,
        "algorithms_controlled_required": True,
        "peer_ids_only": True,
    }


def to_authorization_crypto(
    *, tenant_id: str, operation_ref: str, principal_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "operation_ref": operation_ref,
        "principal_ref": principal_ref,
        "via_authorization": True,
        "zero_trust_crypto_access": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["crypto_operations_audited_required"] = True
    return result


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    return base.to_ai_infer(
        tenant_id=tenant_id, surface=surface, context=context
    )


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": ["kms", "hsm", "policy", "authorization", "audit", "ai"],
        "keys_exposed_forbidden": True,
        "via_kms": True,
        "via_policy_engine": True,
        "algorithms_controlled_required": True,
        "crypto_operations_audited_required": True,
    }
