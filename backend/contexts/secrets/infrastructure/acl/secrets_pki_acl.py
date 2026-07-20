"""ACL: Secrets PKI ↔ peers (P209-D)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_hsm_root_ca(*, tenant_id: str, ca_ref: str) -> dict[str, Any]:
    result = base.to_hsm(
        tenant_id=tenant_id, operation="protect_root_ca", key_ref=ca_ref
    )
    result["root_ca_hsm_required"] = True
    result["offline_root"] = True
    return result


def to_workflow_ra(*, tenant_id: str, request_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "request_ref": request_ref,
        "via_workflow": True,
        "ra_approval_required": True,
        "manual_cert_bypass_forbidden": True,
        "peer_ids_only": True,
    }


def to_kms_boundary(*, tenant_id: str, key_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "key_ref": key_ref,
        "pki_kms_separated": True,
        "pki_does_not_own_kms": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["pki_audit_evidence_required"] = True
    return result


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    return base.to_ai_infer(
        tenant_id=tenant_id, surface=surface, context=context
    )


def to_spiffe(*, tenant_id: str, workload_ref: str, spiffe_id: str) -> dict[str, Any]:
    return base.to_spiffe(
        tenant_id=tenant_id,
        workload_ref=workload_ref,
        spiffe_id=spiffe_id,
    )


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": ["hsm", "workflow", "kms", "audit", "ai", "spiffe"],
        "root_ca_hsm_required": True,
        "via_workflow_ra": True,
        "pki_kms_separated": True,
        "pki_audit_evidence_required": True,
    }
