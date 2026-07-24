"""ACL: Secrets Workload Identity ↔ peers (P209-H)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_spiffe(
    *, tenant_id: str, workload_ref: str, spiffe_id: str
) -> dict[str, Any]:
    result = base.to_spiffe(
        tenant_id=tenant_id,
        workload_ref=workload_ref,
        spiffe_id=spiffe_id,
    )
    result["cryptographic_workload_identity_required"] = True
    result["static_credentials_forbidden"] = True
    return result


def to_authorization_workload(
    *, tenant_id: str, workload_ref: str, principal_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "workload_ref": workload_ref,
        "principal_ref": principal_ref,
        "via_authorization": True,
        "via_p208": True,
        "identity_aware_authorization": True,
        "peer_ids_only": True,
    }


def to_mesh_mtls(*, tenant_id: str, mesh_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "mesh_ref": mesh_ref,
        "mtls_enforceable_required": True,
        "via_service_mesh": True,
        "peer_ids_only": True,
    }


def to_pki_svid(*, tenant_id: str, identity_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "identity_ref": identity_ref,
        "via_pki_ca": True,
        "svid_issuance": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["service_communication_audited_required"] = True
    return result


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    return base.to_ai_infer(
        tenant_id=tenant_id, surface=surface, context=context
    )


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": [
            "spiffe",
            "authorization",
            "service_mesh",
            "pki",
            "audit",
            "ai",
        ],
        "cryptographic_workload_identity_required": True,
        "static_credentials_forbidden": True,
        "mtls_enforceable_required": True,
        "via_p208": True,
        "service_communication_audited_required": True,
    }
