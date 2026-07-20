"""ACL: Secrets Governance / AI Security / Compliance ↔ peers (P209-M)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_policy_evaluate(
    *, tenant_id: str, policy_ref: str, context: dict
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "context": context,
        "via_policy_engine": True,
        "crypto_policies_managed_required": True,
        "peer_ids_only": True,
    }


def to_compliance_evidence(
    *, tenant_id: str, control_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "control_ref": control_ref,
        "via_compliance_platform": True,
        "compliance_evidence_automated_required": True,
        "not_manual_only": True,
        "peer_ids_only": True,
    }


def to_workflow_oversight(
    *, tenant_id: str, decision_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "decision_ref": decision_ref,
        "via_workflow": True,
        "human_oversight_required": True,
        "peer_ids_only": True,
    }


def to_ai_gov_infer(
    *, tenant_id: str, surface: str, context: dict
) -> dict[str, Any]:
    result = base.to_ai_infer(
        tenant_id=tenant_id, surface=surface, context=context
    )
    result["ai_decisions_explainable_required"] = True
    result["advisor_not_authority"] = True
    return result


def to_authorization_gov(
    *, tenant_id: str, principal_ref: str, action: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "principal_ref": principal_ref,
        "action": action,
        "via_authorization": True,
        "zero_trust_governance": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["audit_trails_complete_required"] = True
    result["ai_decisions_explainable_required"] = True
    return result


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": [
            "policy_engine",
            "compliance",
            "workflow",
            "ai",
            "authorization",
            "audit",
        ],
        "ai_decisions_explainable_required": True,
        "crypto_policies_managed_required": True,
        "compliance_evidence_automated_required": True,
        "via_policy_engine": True,
        "via_compliance_platform": True,
    }
