"""ACL: AI Security ↔ peers (P214-I)."""
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
        "tool_authorization": True,
        "peer_ids_only": True,
    }


def to_cryptographic_trust(
    *, tenant_id: str, secret_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "secret_ref": secret_ref,
        "via_p209": True,
        "model_signing": True,
        "peer_ids_only": True,
    }


def to_cyber_security(*, tenant_id: str, control_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "control_ref": control_ref,
        "via_p210": True,
        "siem_soar": True,
        "ai_soc_alignment": True,
        "peer_ids_only": True,
    }


def to_data_security(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211": True,
        "data_protection": True,
        "peer_ids_only": True,
    }


def to_genai(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_p214_e": True,
        "llm_firewall": True,
        "peer_ids_only": True,
    }


def to_agents(*, tenant_id: str, agent_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "agent_ref": agent_ref,
        "via_p214_f": True,
        "agent_zero_trust": True,
        "peer_ids_only": True,
    }


def to_knowledge(*, tenant_id: str, knowledge_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "knowledge_ref": knowledge_ref,
        "via_p214_g": True,
        "security_knowledge_graph": True,
        "peer_ids_only": True,
    }


def to_governance(*, tenant_id: str, policy_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_p214_h": True,
        "prompt_governance": True,
        "peer_ids_only": True,
    }


def to_policy_engine(*, tenant_id: str, policy_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_policy_engine": True,
        "peer_ids_only": True,
    }


def to_ops_deploy(*, tenant_id: str, release_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "release_ref": release_ref,
        "via_p213_o": True,
        "peer_ids_only": True,
    }


def to_enterprise_ai(*, tenant_id: str, security_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "security_ref": security_ref,
        "via_enterprise_ai": True,
        "module_local_ai_security_forbidden": True,
        "peer_ids_only": True,
    }


def to_api_gateway(*, tenant_id: str, route_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "route_ref": route_ref,
        "via_api_gateway": True,
        "peer_ids_only": True,
    }
