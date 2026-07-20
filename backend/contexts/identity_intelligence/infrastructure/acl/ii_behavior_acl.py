"""ACL: Behavioral Identity Analytics ↔ peers (P207-H)."""
from __future__ import annotations

from typing import Any

from contexts.identity_intelligence.infrastructure.acl import ii_platform_acl as base


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    result = base.to_ai_infer(tenant_id=tenant_id, surface=surface, context=context)
    result["behavior_modeling"] = True
    result["ai_models_governed_required"] = True
    result["embeds_llm_sdk_forbidden"] = True
    result["explainable_detection_required"] = True
    return result


def to_risk_calculate(
    *, tenant_id: str, subject_ref: str, behavior_signal: dict
) -> dict[str, Any]:
    return {
        "target": "identity_intelligence.risk",
        "command": "CalculateIdentityRisk",
        "payload": {
            "tenant_id": tenant_id,
            "subject_ref": subject_ref,
            "behavior_signal": dict(behavior_signal),
        },
        "pattern": "internal",
        "via_p207g": True,
        "risk_intelligence_integration_required": True,
        "integration_absent_forbidden": True,
    }


def to_directory_graph(*, tenant_id: str, projection_ref: str) -> dict[str, Any]:
    result = base.to_directory_graph(
        tenant_id=tenant_id, projection_ref=projection_ref
    )
    result["relationship_anomaly_detection"] = True
    result["hidden_pattern_discovery"] = True
    return result


def to_digital_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    result = base.to_digital_twin(tenant_id=tenant_id, twin_ref=twin_ref)
    result["behavior_simulation"] = True
    result["via_p207f"] = True
    return result


def to_authz_check(*, tenant_id: str, subject_id: str, action: str) -> dict[str, Any]:
    result = base.to_authz_check(
        tenant_id=tenant_id, subject_id=subject_id, action=action
    )
    result["trust_signal_consumer"] = True
    result["does_not_replace_pdp"] = True
    result["bypasses_authorization_pdp_forbidden"] = True
    return result


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["behavior_decision_trail"] = True
    result["privacy_access_logged"] = True
    return result


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
        "ai_governed": True,
    }


def to_ai_governance(
    *, tenant_id: str, model_ref: str
) -> dict[str, Any]:
    return {
        "target": "ai_governance",
        "command": "EvaluateModel",
        "payload": {"tenant_id": tenant_id, "model_ref": model_ref},
        "pattern": "customer_supplier",
        "ai_models_governed_required": True,
        "ungoverned_forbidden": True,
        "bias_monitoring": True,
    }
