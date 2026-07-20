"""ACL: AI Security & Governance ↔ platform peers (P207-M)."""
from __future__ import annotations

from typing import Any

from contexts.identity_intelligence.infrastructure.acl import ii_platform_acl as base


def to_ai_platform_governance(
    *, tenant_id: str, model_ref: str, action: str
) -> dict[str, Any]:
    return {
        "target": "ai_governance",
        "command": "EvaluateGovernancePolicy",
        "payload": {
            "tenant_id": tenant_id,
            "model_ref": model_ref,
            "action": action,
        },
        "pattern": "acl",
        "orchestrate_only": True,
        "duplicates_platform_ai_governance_sor_forbidden": True,
        "platform_ai_gov_peer": "ai_governance",
    }


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    result = base.to_ai_infer(tenant_id=tenant_id, surface=surface, context=context)
    result["explainable_required"] = True
    result["governed_inference"] = True
    result["embeds_llm_sdk_forbidden"] = True
    return result


def to_workflow_approval(
    *, tenant_id: str, agent_ref: str, action_ref: str
) -> dict[str, Any]:
    return {
        "target": "workflow",
        "command": "StartApproval",
        "payload": {
            "tenant_id": tenant_id,
            "agent_ref": agent_ref,
            "action_ref": action_ref,
        },
        "pattern": "acl",
        "human_oversight_required": True,
        "via_workflow_engine": True,
    }


def to_authz_check(*, tenant_id: str, subject_id: str, action: str) -> dict[str, Any]:
    result = base.to_authz_check(
        tenant_id=tenant_id, subject_id=subject_id, action=action
    )
    result["ai_identity_authorization"] = True
    result["bypasses_authorization_pdp_forbidden"] = True
    return result


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["ai_decision_audit"] = True
    result["audit_trail_complete_required"] = True
    result["human_override_logging"] = True
    return result


def to_agent_governance(*, tenant_id: str, agent_ref: str) -> dict[str, Any]:
    return {
        "target": "identity_intelligence.agents",
        "command": "ResolveAgentGovernance",
        "payload": {"tenant_id": tenant_id, "agent_ref": agent_ref},
        "pattern": "internal",
        "via_p207e": True,
        "permission_review_required": True,
    }


def to_graph_governance(*, tenant_id: str, entity_ref: str) -> dict[str, Any]:
    result = base.to_directory_graph(
        tenant_id=tenant_id, projection_ref=entity_ref
    )
    result["ai_entity_chain"] = True
    result["via_p207k"] = True
    return result


def to_compliance_evidence(
    *, tenant_id: str, pack_ref: str, frameworks: list[str]
) -> dict[str, Any]:
    return {
        "target": "compliance",
        "command": "CollectEvidence",
        "payload": {
            "tenant_id": tenant_id,
            "pack_ref": pack_ref,
            "frameworks": list(frameworks),
        },
        "pattern": "acl",
        "regulatory_mapping": True,
        "evidence_collection": True,
    }
