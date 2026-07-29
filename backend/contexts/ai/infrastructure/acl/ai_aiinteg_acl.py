"""ACL: AI Integration ↔ peers (P214-M)."""
from __future__ import annotations

from typing import Any


def to_identity(*, tenant_id: str, identity_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "identity_ref": identity_ref,
        "via_p207": True,
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
        "api_authorization": True,
        "peer_ids_only": True,
    }


def to_cryptographic_trust(
    *, tenant_id: str, secret_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "secret_ref": secret_ref,
        "via_p209": True,
        "mtls": True,
        "peer_ids_only": True,
    }


def to_cyber_security(*, tenant_id: str, control_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "control_ref": control_ref,
        "via_p210": True,
        "peer_ids_only": True,
    }


def to_data_security(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211": True,
        "peer_ids_only": True,
    }


def to_ops_deploy(*, tenant_id: str, release_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "release_ref": release_ref,
        "via_p213_o": True,
        "peer_ids_only": True,
    }


def to_api_gateway(*, tenant_id: str, route_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "route_ref": route_ref,
        "via_api_gateway": True,
        "platform_owns_edge": True,
        "peer_ids_only": True,
    }


def to_event_fabric(*, tenant_id: str, channel_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "channel_ref": channel_ref,
        "via_event_fabric": True,
        "platform_owns_bus": True,
        "peer_ids_only": True,
    }


def to_workflow(*, tenant_id: str, workflow_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "workflow_ref": workflow_ref,
        "via_workflow_engine": True,
        "peer_ids_only": True,
    }


def to_observability(*, tenant_id: str, signal_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "signal_ref": signal_ref,
        "via_observability": True,
        "peer_ids_only": True,
    }


def to_mlops(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_p214_d": True,
        "peer_ids_only": True,
    }


def to_genai(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_p214_e": True,
        "peer_ids_only": True,
    }


def to_agents(*, tenant_id: str, agent_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "agent_ref": agent_ref,
        "via_p214_f": True,
        "agent_communication": True,
        "peer_ids_only": True,
    }


def to_knowledge(*, tenant_id: str, knowledge_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "knowledge_ref": knowledge_ref,
        "via_p214_g": True,
        "integration_graph": True,
        "peer_ids_only": True,
    }


def to_governance(*, tenant_id: str, policy_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_p214_h": True,
        "peer_ids_only": True,
    }


def to_aisec(*, tenant_id: str, security_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "security_ref": security_ref,
        "via_p214_i": True,
        "peer_ids_only": True,
    }


def to_aiops(*, tenant_id: str, ops_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "ops_ref": ops_ref,
        "via_p214_j": True,
        "routing_intelligence": True,
        "peer_ids_only": True,
    }


def to_aidata(*, tenant_id: str, dataset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "dataset_ref": dataset_ref,
        "via_p214_k": True,
        "peer_ids_only": True,
    }


def to_modelintel(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_p214_l": True,
        "serving_gateway": True,
        "peer_ids_only": True,
    }


def to_enterprise_ai(*, tenant_id: str, integ_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "integ_ref": integ_ref,
        "via_enterprise_ai": True,
        "module_local_ai_gateway_forbidden": True,
        "peer_ids_only": True,
    }
