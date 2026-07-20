"""ACL: Identity Digital Twin Platform ↔ peers (P207-F)."""
from __future__ import annotations

from typing import Any

from contexts.identity_intelligence.infrastructure.acl import ii_platform_acl as base


def to_digital_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    result = base.to_digital_twin(tenant_id=tenant_id, twin_ref=twin_ref)
    result["orchestrate_only"] = True
    result["duplicates_twin_sor_forbidden"] = True
    result["not_data_copy_only"] = True
    result["simulation_before_execution"] = True
    return result


def to_directory_graph(*, tenant_id: str, projection_ref: str) -> dict[str, Any]:
    result = base.to_directory_graph(
        tenant_id=tenant_id, projection_ref=projection_ref
    )
    result["twin_relationship_reasoning"] = True
    result["attack_path_analysis"] = True
    return result


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    result = base.to_ai_infer(tenant_id=tenant_id, surface=surface, context=context)
    result["twin_prediction"] = True
    result["ai_strong_required"] = True
    result["weak_ai_forbidden"] = True
    result["embeds_llm_sdk_forbidden"] = True
    return result


def to_authz_check(*, tenant_id: str, subject_id: str, action: str) -> dict[str, Any]:
    result = base.to_authz_check(
        tenant_id=tenant_id, subject_id=subject_id, action=action
    )
    result["twin_access_control"] = True
    return result


def to_workflow_approval(*, tenant_id: str, decision_ref: str) -> dict[str, Any]:
    return {
        "target": "workflow",
        "command": "StartApproval",
        "payload": {"tenant_id": tenant_id, "decision_ref": decision_ref},
        "pattern": "customer_supplier",
        "hitl_required": True,
        "local_approval_engine_forbidden": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["twin_actions_audited"] = True
    result["simulation_audit_trail"] = True
    return result


def to_agent_task(*, tenant_id: str, agent_kind: str, twin_ref: str) -> dict[str, Any]:
    return {
        "target": "identity_intelligence.agents",
        "command": "CreateAgentTask",
        "payload": {
            "tenant_id": tenant_id,
            "agent_kind": agent_kind,
            "twin_ref": twin_ref,
        },
        "pattern": "internal",
        "via_p207e": True,
        "ai_strong_required": True,
    }


def to_observability(
    *, tenant_id: str, metric_name: str, value: float
) -> dict[str, Any]:
    result = base.to_observability(
        tenant_id=tenant_id, metric_name=metric_name, value=value
    )
    result["twin_health_metrics"] = True
    return result
