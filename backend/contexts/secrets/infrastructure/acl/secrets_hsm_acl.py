"""ACL: Secrets HSM / AI Crypto / PQC ↔ peers (P209-K)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_integration_hsm(*, tenant_id: str, hsm_ref: str) -> dict[str, Any]:
    result = base.to_hsm(
        tenant_id=tenant_id, operation="manage_hsm", key_ref=hsm_ref
    )
    result["hsm_protection_required"] = True
    result["via_integration_hsm"] = True
    result["no_embedded_vendor_sdk"] = True
    return result


def to_ai_crypto_infer(
    *, tenant_id: str, surface: str, context: dict
) -> dict[str, Any]:
    result = base.to_ai_infer(
        tenant_id=tenant_id, surface=surface, context=context
    )
    result["ai_crypto_decisions_auditable_required"] = True
    result["advisor_not_authority"] = True
    return result


def to_workflow_dual_control(
    *, tenant_id: str, ceremony_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "ceremony_ref": ceremony_ref,
        "via_workflow": True,
        "dual_control_required": True,
        "multi_person_authorization_required": True,
        "peer_ids_only": True,
    }


def to_authorization_hsm(
    *, tenant_id: str, hsm_ref: str, principal_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "hsm_ref": hsm_ref,
        "principal_ref": principal_ref,
        "via_authorization": True,
        "zero_trust_hsm_access": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["ai_crypto_decisions_auditable_required"] = True
    result["hardware_trust_validated_required"] = True
    return result


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": [
            "integration_hsm",
            "ai",
            "workflow",
            "authorization",
            "audit",
        ],
        "hsm_protection_required": True,
        "ai_crypto_decisions_auditable_required": True,
        "via_workflow": True,
        "via_authorization": True,
    }
