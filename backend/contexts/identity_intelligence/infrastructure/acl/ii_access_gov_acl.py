"""ACL: AI Governance & Access Optimization ↔ peers (P207-J)."""
from __future__ import annotations

from typing import Any

from contexts.identity_intelligence.infrastructure.acl import ii_platform_acl as base


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    result = base.to_ai_infer(tenant_id=tenant_id, surface=surface, context=context)
    result["governance_recommendation"] = True
    result["explainable_required"] = True
    result["embeds_llm_sdk_forbidden"] = True
    return result


def to_risk_calculate(
    *, tenant_id: str, subject_ref: str, access_context: dict
) -> dict[str, Any]:
    return {
        "target": "identity_intelligence.risk",
        "command": "CalculateIdentityRisk",
        "payload": {
            "tenant_id": tenant_id,
            "subject_ref": subject_ref,
            "access_context": dict(access_context),
        },
        "pattern": "internal",
        "via_p207g": True,
        "risk_intelligence_connected_required": True,
        "disconnected_forbidden": True,
    }


def to_digital_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    result = base.to_digital_twin(tenant_id=tenant_id, twin_ref=twin_ref)
    result["governance_simulation"] = True
    result["via_p207f"] = True
    return result


def to_directory_graph(*, tenant_id: str, projection_ref: str) -> dict[str, Any]:
    result = base.to_directory_graph(
        tenant_id=tenant_id, projection_ref=projection_ref
    )
    result["toxic_access_detection"] = True
    result["access_relationship_discovery"] = True
    return result


def to_iga(*, tenant_id: str, subject_ref: str) -> dict[str, Any]:
    result = base.to_iga(tenant_id=tenant_id, subject_ref=subject_ref)
    result["orchestrate_only"] = True
    result["duplicates_p202_iga_sor_forbidden"] = True
    result["continuous_certification_intelligence"] = True
    return result


def to_workflow_approval(*, tenant_id: str, recommendation_ref: str) -> dict[str, Any]:
    return {
        "target": "workflow",
        "command": "StartApproval",
        "payload": {
            "tenant_id": tenant_id,
            "recommendation_ref": recommendation_ref,
        },
        "pattern": "customer_supplier",
        "human_governance_required": True,
        "local_approval_engine_forbidden": True,
    }


def to_policy_evaluate(
    *, tenant_id: str, policy_key: str, context: dict
) -> dict[str, Any]:
    result = base.to_policy_evaluate(
        tenant_id=tenant_id, policy_key=policy_key, context=context
    )
    result["policy_intelligence"] = True
    result["local_policy_engine_forbidden"] = True
    return result


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["compliance_evidence_required"] = True
    result["decision_logging"] = True
    return result


def to_authz_check(*, tenant_id: str, subject_id: str, action: str) -> dict[str, Any]:
    result = base.to_authz_check(
        tenant_id=tenant_id, subject_id=subject_id, action=action
    )
    result["access_validation"] = True
    result["bypasses_authorization_pdp_forbidden"] = True
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
        "explainable_required": True,
    }
