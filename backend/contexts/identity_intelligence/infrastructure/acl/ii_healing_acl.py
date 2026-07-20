"""ACL: Self-Healing Identity Fabric ↔ peers (P207-I)."""
from __future__ import annotations

from typing import Any

from contexts.identity_intelligence.infrastructure.acl import ii_platform_acl as base


def to_digital_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    result = base.to_digital_twin(tenant_id=tenant_id, twin_ref=twin_ref)
    result["recovery_simulation"] = True
    result["via_p207f"] = True
    result["twin_simulation_required"] = True
    result["simulation_absent_forbidden"] = True
    return result


def to_directory_graph(*, tenant_id: str, projection_ref: str) -> dict[str, Any]:
    result = base.to_directory_graph(
        tenant_id=tenant_id, projection_ref=projection_ref
    )
    result["failure_propagation_analysis"] = True
    result["dependency_discovery"] = True
    return result


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    result = base.to_ai_infer(tenant_id=tenant_id, surface=surface, context=context)
    result["root_cause_analysis"] = True
    result["embeds_llm_sdk_forbidden"] = True
    result["rca_required"] = True
    return result


def to_workflow_approval(*, tenant_id: str, run_ref: str) -> dict[str, Any]:
    return {
        "target": "workflow",
        "command": "StartApproval",
        "payload": {"tenant_id": tenant_id, "run_ref": run_ref},
        "pattern": "customer_supplier",
        "hitl_for_level_2_plus": True,
        "remediation_governed": True,
        "local_approval_engine_forbidden": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["actions_auditable_required"] = True
    result["healing_decision_trail"] = True
    return result


def to_authz_check(*, tenant_id: str, subject_id: str, action: str) -> dict[str, Any]:
    result = base.to_authz_check(
        tenant_id=tenant_id, subject_id=subject_id, action=action
    )
    result["verify_before_repair"] = True
    result["bypasses_authorization_pdp_forbidden"] = True
    return result


def to_autonomous_orchestrate(
    *, tenant_id: str, incident_ref: str
) -> dict[str, Any]:
    return {
        "target": "identity_intelligence.autonomous",
        "command": "StartAutonomousRun",
        "payload": {"tenant_id": tenant_id, "incident_ref": incident_ref},
        "pattern": "internal",
        "via_p207d": True,
        "governed_required": True,
    }


def to_agent_task(*, tenant_id: str, agent_kind: str, incident_ref: str) -> dict[str, Any]:
    return {
        "target": "identity_intelligence.agents",
        "command": "CreateAgentTask",
        "payload": {
            "tenant_id": tenant_id,
            "agent_kind": agent_kind,
            "incident_ref": incident_ref,
        },
        "pattern": "internal",
        "via_p207e": True,
    }
