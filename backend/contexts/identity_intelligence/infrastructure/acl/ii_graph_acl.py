"""ACL: Knowledge Graph Intelligence ↔ peers (P207-K)."""
from __future__ import annotations

from typing import Any

from contexts.identity_intelligence.infrastructure.acl import ii_platform_acl as base


def to_directory_graph(*, tenant_id: str, projection_ref: str) -> dict[str, Any]:
    result = base.to_directory_graph(
        tenant_id=tenant_id, projection_ref=projection_ref
    )
    result["orchestrate_only"] = True
    result["duplicates_directory_graph_sor_forbidden"] = True
    result["graph_storage_peer"] = "directory"
    result["p205h_graph"] = True
    return result


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    result = base.to_ai_infer(tenant_id=tenant_id, surface=surface, context=context)
    result["graph_reasoning"] = True
    result["explainable_required"] = True
    result["embeds_llm_sdk_forbidden"] = True
    return result


def to_search(*, tenant_id: str, query: str) -> dict[str, Any]:
    return {
        "target": "search",
        "command": "SemanticQuery",
        "payload": {"tenant_id": tenant_id, "query": query},
        "pattern": "acl",
        "semantic_search": True,
        "via_search_platform": True,
    }


def to_digital_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    result = base.to_digital_twin(tenant_id=tenant_id, twin_ref=twin_ref)
    result["future_simulation_graph"] = True
    result["via_p207f"] = True
    return result


def to_risk_calculate(
    *, tenant_id: str, subject_ref: str, graph_context: dict
) -> dict[str, Any]:
    return {
        "target": "identity_intelligence.risk",
        "command": "CalculateIdentityRisk",
        "payload": {
            "tenant_id": tenant_id,
            "subject_ref": subject_ref,
            "graph_context": dict(graph_context),
        },
        "pattern": "internal",
        "via_p207g": True,
        "ii_integration_strong": True,
    }


def to_authz_check(*, tenant_id: str, subject_id: str, action: str) -> dict[str, Any]:
    result = base.to_authz_check(
        tenant_id=tenant_id, subject_id=subject_id, action=action
    )
    result["verify_every_query"] = True
    result["bypasses_authorization_pdp_forbidden"] = True
    return result


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["decision_tracking"] = True
    result["explainability_trail"] = True
    return result


def to_agent_task(*, tenant_id: str, agent_kind: str, graph_ref: str) -> dict[str, Any]:
    return {
        "target": "identity_intelligence.agents",
        "command": "CreateAgentTask",
        "payload": {
            "tenant_id": tenant_id,
            "agent_kind": agent_kind,
            "graph_ref": graph_ref,
        },
        "pattern": "internal",
        "via_p207e": True,
        "explainable_required": True,
    }
