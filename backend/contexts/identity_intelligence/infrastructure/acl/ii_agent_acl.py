"""ACL: Identity AI Agent Platform ↔ peers (P207-E)."""
from __future__ import annotations

from typing import Any

from contexts.identity_intelligence.infrastructure.acl import ii_platform_acl as base


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    result = base.to_ai_infer(tenant_id=tenant_id, surface=surface, context=context)
    result["agent_runtime"] = True
    result["embeds_llm_sdk_forbidden"] = True
    result["explainable_required"] = True
    result["hitl_required"] = True
    return result


def to_authz_check(*, tenant_id: str, subject_id: str, action: str) -> dict[str, Any]:
    result = base.to_authz_check(
        tenant_id=tenant_id, subject_id=subject_id, action=action
    )
    result["agent_authorization_required"] = True
    result["tool_access_control"] = True
    result["permissionless_forbidden"] = True
    return result


def to_workflow_approval(
    *, tenant_id: str, recommendation_ref: str
) -> dict[str, Any]:
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


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["ai_actions_audited_required"] = True
    result["decision_logging"] = True
    return result


def to_search_rag(*, tenant_id: str, query: str) -> dict[str, Any]:
    return {
        "target": "search",
        "command": "SemanticQuery",
        "payload": {"tenant_id": tenant_id, "query": query},
        "pattern": "acl",
        "knowledge_sources_controlled": True,
        "uncontrolled_rag_forbidden": True,
    }


def to_directory_graph(*, tenant_id: str, projection_ref: str) -> dict[str, Any]:
    result = base.to_directory_graph(
        tenant_id=tenant_id, projection_ref=projection_ref
    )
    result["agent_graph_tool"] = True
    return result


def to_policy_evaluate(
    *, tenant_id: str, policy_key: str, context: dict
) -> dict[str, Any]:
    result = base.to_policy_evaluate(
        tenant_id=tenant_id, policy_key=policy_key, context=context
    )
    result["agent_guardrails"] = True
    return result
