"""ACL: Secrets Signing / Supply Chain ↔ peers (P209-J)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_kms_signing_key(*, tenant_id: str, key_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "key_ref": key_ref,
        "via_kms": True,
        "signing_keys_managed_required": True,
        "peer_ids_only": True,
    }


def to_hsm_sign(*, tenant_id: str, key_ref: str) -> dict[str, Any]:
    result = base.to_hsm(
        tenant_id=tenant_id, operation="sign_artifact", key_ref=key_ref
    )
    result["hsm_signing_required"] = True
    return result


def to_pki_code_signing_cert(
    *, tenant_id: str, cert_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "cert_ref": cert_ref,
        "via_pki": True,
        "code_signing_certificate": True,
        "peer_ids_only": True,
    }


def to_workflow_release(
    *, tenant_id: str, release_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "release_ref": release_ref,
        "via_workflow": True,
        "multi_person_approval_required": True,
        "peer_ids_only": True,
    }


def to_integration_cicd(
    *, tenant_id: str, pipeline_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "pipeline_ref": pipeline_ref,
        "via_integration_platform": True,
        "no_embedded_vendor_sdk": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["signature_operations_audited_required"] = True
    return result


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    return base.to_ai_infer(
        tenant_id=tenant_id, surface=surface, context=context
    )


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": [
            "kms",
            "hsm",
            "pki",
            "workflow",
            "integration",
            "audit",
            "ai",
        ],
        "signing_keys_managed_required": True,
        "via_pki": True,
        "via_workflow": True,
        "via_integration_cicd": True,
        "signature_operations_audited_required": True,
    }
