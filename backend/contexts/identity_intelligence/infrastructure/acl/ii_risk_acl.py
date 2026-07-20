"""ACL: Predictive Identity Risk Engine ↔ peers (P207-G)."""
from __future__ import annotations

from typing import Any

from contexts.identity_intelligence.infrastructure.acl import ii_platform_acl as base


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    result = base.to_ai_infer(tenant_id=tenant_id, surface=surface, context=context)
    result["risk_prediction"] = True
    result["ai_decisions_auditable_required"] = True
    result["embeds_llm_sdk_forbidden"] = True
    result["explanation_required"] = True
    return result


def to_authz_check(*, tenant_id: str, subject_id: str, action: str) -> dict[str, Any]:
    result = base.to_authz_check(
        tenant_id=tenant_id, subject_id=subject_id, action=action
    )
    result["trust_score_consumer"] = True
    result["does_not_replace_pdp"] = True
    result["bypasses_authorization_pdp_forbidden"] = True
    return result


def to_directory_graph(*, tenant_id: str, projection_ref: str) -> dict[str, Any]:
    result = base.to_directory_graph(
        tenant_id=tenant_id, projection_ref=projection_ref
    )
    result["attack_path_discovery"] = True
    result["relationship_risk_analysis"] = True
    return result


def to_digital_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    result = base.to_digital_twin(tenant_id=tenant_id, twin_ref=twin_ref)
    result["risk_simulation"] = True
    result["via_p207f"] = True
    return result


def to_workflow_approval(*, tenant_id: str, mitigation_ref: str) -> dict[str, Any]:
    return {
        "target": "workflow",
        "command": "StartApproval",
        "payload": {"tenant_id": tenant_id, "mitigation_ref": mitigation_ref},
        "pattern": "customer_supplier",
        "hitl_for_high_critical": True,
        "automated_response_governed": True,
        "local_approval_engine_forbidden": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["ai_decisions_auditable_required"] = True
    result["risk_decision_trail"] = True
    return result


def to_autonomous_remediate(
    *, tenant_id: str, subject_ref: str, tier: str
) -> dict[str, Any]:
    return {
        "target": "identity_intelligence.autonomous",
        "command": "StartAutonomousRun",
        "payload": {
            "tenant_id": tenant_id,
            "subject_ref": subject_ref,
            "tier": tier,
        },
        "pattern": "internal",
        "via_p207d": True,
        "governed_required": True,
        "ungoverned_forbidden": True,
    }


def to_agent_task(*, tenant_id: str, agent_kind: str, subject_ref: str) -> dict[str, Any]:
    return {
        "target": "identity_intelligence.agents",
        "command": "CreateAgentTask",
        "payload": {
            "tenant_id": tenant_id,
            "agent_kind": agent_kind,
            "subject_ref": subject_ref,
        },
        "pattern": "internal",
        "via_p207e": True,
        "ai_auditable": True,
    }


def to_policy_evaluate(
    *, tenant_id: str, policy_key: str, context: dict
) -> dict[str, Any]:
    result = base.to_policy_evaluate(
        tenant_id=tenant_id, policy_key=policy_key, context=context
    )
    result["risk_policy_alignment"] = True
    return result
