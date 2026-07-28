"""ACL: AI domain architecture ↔ peers (P214-C)."""
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
        "peer_ids_only": True,
    }


def to_cryptographic_trust(
    *, tenant_id: str, secret_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "secret_ref": secret_ref,
        "via_p209": True,
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


def to_data_governance(
    *, tenant_id: str, product_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "product_ref": product_ref,
        "via_p212": True,
        "ai_data_domain": True,
        "peer_ids_only": True,
    }


def to_graph(*, tenant_id: str, entity_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "entity_ref": entity_ref,
        "via_p212_j": True,
        "via_p213_l": True,
        "knowledge_domain": True,
        "peer_ids_only": True,
    }


def to_analytics(*, tenant_id: str, insight_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "insight_ref": insight_ref,
        "via_p213": True,
        "peer_ids_only": True,
    }


def to_foundation(*, tenant_id: str, profile_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "profile_ref": profile_ref,
        "via_p214_a": True,
        "peer_ids_only": True,
    }


def to_mission(*, tenant_id: str, mission_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "mission_ref": mission_ref,
        "via_p214_b": True,
        "peer_ids_only": True,
    }


def to_enterprise_ai(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai": True,
        "module_local_llm_sdk_forbidden": True,
        "peer_ids_only": True,
    }


def to_api_gateway(*, tenant_id: str, route_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "route_ref": route_ref,
        "via_api_gateway": True,
        "peer_ids_only": True,
    }
