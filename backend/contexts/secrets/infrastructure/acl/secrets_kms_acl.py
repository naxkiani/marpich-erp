"""ACL: Secrets KMS ↔ peers (P209-F)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_hsm_key(*, tenant_id: str, key_ref: str) -> dict[str, Any]:
    result = base.to_hsm(
        tenant_id=tenant_id, operation="protect_key", key_ref=key_ref
    )
    result["hsm_capability_required"] = True
    result["keys_protected_required"] = True
    result["non_exportable_default"] = True
    return result


def to_integration_cloud_kms(
    *, tenant_id: str, provider_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "provider_ref": provider_ref,
        "via_integration_platform": True,
        "no_embedded_vendor_sdk": True,
        "peer_ids_only": True,
    }


def to_authorization_key_access(
    *, tenant_id: str, key_ref: str, principal_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "key_ref": key_ref,
        "principal_ref": principal_ref,
        "via_authorization": True,
        "zero_trust_key_access": True,
        "peer_ids_only": True,
    }


def to_policy_crypto(*, tenant_id: str, policy_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_policy_engine": True,
        "cryptographic_policies_required": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["key_operations_audited_required"] = True
    return result


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    return base.to_ai_infer(
        tenant_id=tenant_id, surface=surface, context=context
    )


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": [
            "hsm",
            "integration",
            "authorization",
            "policy",
            "audit",
            "ai",
        ],
        "hsm_capability_required": True,
        "keys_protected_required": True,
        "via_integration_cloud_kms": True,
        "via_authorization": True,
        "cryptographic_policies_required": True,
        "key_operations_audited_required": True,
    }
