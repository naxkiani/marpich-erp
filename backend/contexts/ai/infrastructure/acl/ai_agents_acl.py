"""ACL: AI Agents ↔ peers (P214-F)."""
from __future__ import annotations

from typing import Any


def to_identity(*, tenant_id: str, identity_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "identity_ref": identity_ref,
        "via_p207": True,
        "agent_identity": True,
        "peer_ids_only": True,
    }


def to_authorization(
    *, tenant_id: str, principal_ref: str, action: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "principal_ref": principal_ref,
        "action": action,
        "via_p208": True,
        "tool_authorization": True,
        "least_privilege": True,
        "peer_ids_only": True,
    }


def to_cryptographic_trust(
    *, tenant_id: str, secret_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "secret_ref": secret_ref,
        "via_p209": True,
        "digital_certificate": True,
        "peer_ids_only": True,
    }


def to_cyber_security(*, tenant_id: str, control_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "control_ref": control_ref,
        "via_p210": True,
        "agent_zero_trust": True,
        "peer_ids_only": True,
    }


def to_data_security(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211": True,
        "memory_security": True,
        "peer_ids_only": True,
    }


def to_data_governance(
    *, tenant_id: str, product_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "product_ref": product_ref,
        "via_p212": True,
        "knowledge_retrieval": True,
        "peer_ids_only": True,
    }


def to_knowledge_graph(*, tenant_id: str, graph_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "graph_ref": graph_ref,
        "via_p213_l": True,
        "semantic_reasoning": True,
        "peer_ids_only": True,
    }


def to_ops_deploy(*, tenant_id: str, release_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "release_ref": release_ref,
        "via_p213_o": True,
        "agent_runtime_deploy": True,
        "peer_ids_only": True,
    }


def to_foundation(*, tenant_id: str, profile_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "profile_ref": profile_ref,
        "via_p214_a": True,
        "peer_ids_only": True,
    }


def to_domain(*, tenant_id: str, context_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "context_ref": context_ref,
        "via_p214_c": True,
        "peer_ids_only": True,
    }


def to_mlops(*, tenant_id: str, registry_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "registry_ref": registry_ref,
        "via_p214_d": True,
        "peer_ids_only": True,
    }


def to_genai(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_p214_e": True,
        "llm_reasoning": True,
        "peer_ids_only": True,
    }


def to_workflow(*, tenant_id: str, workflow_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "workflow_ref": workflow_ref,
        "via_workflow_engine": True,
        "human_approval": True,
        "peer_ids_only": True,
    }


def to_enterprise_ai(*, tenant_id: str, agent_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "agent_ref": agent_ref,
        "via_enterprise_ai": True,
        "module_local_agent_runtime_forbidden": True,
        "peer_ids_only": True,
    }


def to_api_gateway(*, tenant_id: str, route_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "route_ref": route_ref,
        "via_api_gateway": True,
        "peer_ids_only": True,
    }
