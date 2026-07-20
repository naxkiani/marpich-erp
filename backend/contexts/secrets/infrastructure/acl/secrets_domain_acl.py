"""ACL: Secrets Domain Architecture ↔ peers (P209-C)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_pki_context(*, tenant_id: str, certificate_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "certificate_ref": certificate_ref,
        "logical_context": "pki_management",
        "does_not_own_kms_keys": True,
        "pki_kms_separated": True,
        "peer_ids_only": True,
    }


def to_kms_context(*, tenant_id: str, key_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "key_ref": key_ref,
        "logical_context": "key_management",
        "does_not_own_cas": True,
        "pki_kms_separated": True,
        "peer_ids_only": True,
    }


def to_secrets_context(*, tenant_id: str, secret_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "secret_ref": secret_ref,
        "logical_context": "secrets_management",
        "managed_required": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["domain_event_trail"] = True
    return result


def to_hsm(*, tenant_id: str, operation: str, key_ref: str) -> dict[str, Any]:
    return base.to_hsm(
        tenant_id=tenant_id, operation=operation, key_ref=key_ref
    )


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": ["pki", "kms", "secrets", "hsm", "audit"],
        "pki_kms_separated": True,
        "secrets_managed": True,
        "logical_contexts_only": True,
    }
