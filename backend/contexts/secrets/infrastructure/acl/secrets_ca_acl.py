"""ACL: Secrets CA / Trust Chain ↔ peers (P209-E)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_hsm_root_ca(*, tenant_id: str, ca_ref: str) -> dict[str, Any]:
    result = base.to_hsm(
        tenant_id=tenant_id, operation="protect_root_ca", key_ref=ca_ref
    )
    result["root_ca_hsm_required"] = True
    result["offline_root"] = True
    result["ca_private_keys_hsm_required"] = True
    return result


def to_workflow_ceremony(*, tenant_id: str, ceremony_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "ceremony_ref": ceremony_ref,
        "via_workflow": True,
        "dual_control_required": True,
        "multi_person_approval_required": True,
        "peer_ids_only": True,
    }


def to_trust_distribution(
    *, tenant_id: str, trust_anchor_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "trust_anchor_ref": trust_anchor_ref,
        "trust_store_distribution": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["ca_audit_trail_complete_required"] = True
    return result


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    return base.to_ai_infer(
        tenant_id=tenant_id, surface=surface, context=context
    )


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": ["hsm", "workflow", "trust_distribution", "audit", "ai"],
        "root_ca_hsm_required": True,
        "ca_private_keys_hsm_required": True,
        "via_workflow_ceremony": True,
        "ca_audit_trail_complete_required": True,
    }
