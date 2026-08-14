"""ACL: BI strategy ↔ peers (P213-A)."""
from __future__ import annotations

from typing import Any


def to_data_governance(*, tenant_id: str, product_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "product_ref": product_ref,
        "via_p212": True,
        "data_mesh_alignment_present_required": True,
        "peer_ids_only": True,
    }


def to_graph(*, tenant_id: str, entity_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "entity_ref": entity_ref,
        "via_p212_j": True,
        "knowledge_graph_integration_present_required": True,
        "peer_ids_only": True,
    }


def to_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "twin_ref": twin_ref,
        "via_p212_l": True,
        "digital_twin_integration_present_required": True,
        "peer_ids_only": True,
    }


def to_data_security(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211": True,
        "peer_ids_only": True,
    }


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
        "module_local_gateway_forbidden": True,
        "peer_ids_only": True,
    }
