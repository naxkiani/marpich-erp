"""ACL: Secrets Vault ↔ peers (P209-G)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_kms_encrypt(*, tenant_id: str, secret_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "secret_ref": secret_ref,
        "via_kms": True,
        "encryption_at_rest_required": True,
        "plaintext_forbidden": True,
        "peer_ids_only": True,
    }


def to_authorization_secret_access(
    *, tenant_id: str, secret_ref: str, principal_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "secret_ref": secret_ref,
        "principal_ref": principal_ref,
        "via_authorization": True,
        "zero_trust_secret_access": True,
        "peer_ids_only": True,
    }


def to_workflow_approval(
    *, tenant_id: str, request_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "request_ref": request_ref,
        "via_workflow": True,
        "secret_access_approval_required": True,
        "peer_ids_only": True,
    }


def to_pam_ref_only(*, tenant_id: str, secret_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "secret_ref": secret_ref,
        "pam_refs_only": True,
        "ciphertext_stays_in_secrets": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["secret_access_audited_required"] = True
    return result


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    return base.to_ai_infer(
        tenant_id=tenant_id, surface=surface, context=context
    )


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": [
            "kms",
            "authorization",
            "workflow",
            "pam",
            "audit",
            "ai",
        ],
        "plaintext_forbidden": True,
        "via_authorization": True,
        "via_workflow": True,
        "pam_refs_only": True,
        "secret_access_audited_required": True,
    }
