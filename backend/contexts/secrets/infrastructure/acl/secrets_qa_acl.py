"""ACL: Secrets QA / Assurance / DoD ↔ peers (P209-O)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_compliance_evidence(
    *, tenant_id: str, control_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "control_ref": control_ref,
        "via_compliance_platform": True,
        "compliance_evidence_available_required": True,
        "peer_ids_only": True,
    }


def to_policy_validate(
    *, tenant_id: str, policy_ref: str, context: dict
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "context": context,
        "via_policy_engine": True,
        "cryptographic_controls_validated_required": True,
        "peer_ids_only": True,
    }


def to_workflow_release(
    *, tenant_id: str, release_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "release_ref": release_ref,
        "via_workflow": True,
        "security_failures_block_deployment_required": True,
        "approval_required": True,
        "peer_ids_only": True,
    }


def to_deploy_gate(*, tenant_id: str, gate_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "gate_ref": gate_ref,
        "via_deploy_gates": True,
        "security_failures_block_deployment_required": True,
        "can_reject_deployment": True,
        "peer_ids_only": True,
    }


def to_ai_assurance_infer(
    *, tenant_id: str, surface: str, context: dict
) -> dict[str, Any]:
    result = base.to_ai_infer(
        tenant_id=tenant_id, surface=surface, context=context
    )
    result["via_ai_platform"] = True
    result["advisor_not_authority"] = True
    return result


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["audit_trails_complete_required"] = True
    result["security_testing_complete_required"] = True
    return result


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": [
            "compliance",
            "policy_engine",
            "workflow",
            "deploy_gates",
            "ai",
            "audit",
        ],
        "security_testing_complete_required": True,
        "compliance_evidence_available_required": True,
        "security_failures_block_deployment_required": True,
        "via_compliance_platform": True,
        "via_deploy_gates": True,
    }
