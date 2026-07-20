"""ACL: Autonomous Identity Operations ↔ peers (P207-D)."""
from __future__ import annotations

from typing import Any

from contexts.identity_intelligence.infrastructure.acl import ii_platform_acl as base


def to_workflow_start(
    *, tenant_id: str, workflow_key: str, payload: dict
) -> dict[str, Any]:
    return {
        "target": "workflow",
        "command": "StartInstance",
        "payload": {
            "tenant_id": tenant_id,
            "workflow_key": workflow_key,
            "body": dict(payload),
        },
        "pattern": "customer_supplier",
        "local_approval_engine_forbidden": True,
        "via_workflow_engine": True,
        "automation_governance_required": True,
    }


def to_policy_evaluate(
    *, tenant_id: str, policy_key: str, context: dict
) -> dict[str, Any]:
    result = base.to_policy_evaluate(
        tenant_id=tenant_id, policy_key=policy_key, context=context
    )
    result["policy_validation_required"] = True
    result["security_bypass_forbidden"] = True
    return result


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    result = base.to_ai_infer(tenant_id=tenant_id, surface=surface, context=context)
    result["explainable_required"] = True
    result["hitl_required"] = True
    result["no_hidden_decisions"] = True
    return result


def to_authz_check(*, tenant_id: str, subject_id: str, action: str) -> dict[str, Any]:
    result = base.to_authz_check(
        tenant_id=tenant_id, subject_id=subject_id, action=action
    )
    result["action_authorization_required"] = True
    result["security_bypass_forbidden"] = True
    return result


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["actions_auditable_required"] = True
    result["execution_logging"] = True
    return result


def to_digital_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    result = base.to_digital_twin(tenant_id=tenant_id, twin_ref=twin_ref)
    result["impact_simulation_before_action"] = True
    return result


def to_directory_graph(*, tenant_id: str, projection_ref: str) -> dict[str, Any]:
    result = base.to_directory_graph(
        tenant_id=tenant_id, projection_ref=projection_ref
    )
    result["attack_path_and_impact"] = True
    return result


def to_observability(
    *, tenant_id: str, metric_name: str, value: float
) -> dict[str, Any]:
    result = base.to_observability(
        tenant_id=tenant_id, metric_name=metric_name, value=value
    )
    result["automation_metrics"] = True
    return result
