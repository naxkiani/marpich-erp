"""ACL: BI decision knowledge graph ↔ peers (P213-L)."""
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
        "graph_authorization": True,
        "node_level_security": True,
        "relationship_security": True,
        "attribute_based_access_control": True,
        "row_level_security": True,
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
        "policy_driven_graph_governance": True,
        "peer_ids_only": True,
    }


def to_knowledge_graph(*, tenant_id: str, node_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "node_ref": node_ref,
        "via_p212_j": True,
        "knowledge_graph_federation_present_required": True,
        "cross_domain_graph_federation": True,
        "peer_ids_only": True,
    }


def to_digital_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "twin_ref": twin_ref,
        "via_p212_l": True,
        "digital_twin_integration_present_required": True,
        "peer_ids_only": True,
    }


def to_semantic(*, tenant_id: str, metric_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "metric_ref": metric_ref,
        "via_p213_g": True,
        "certified_metrics_only": True,
        "peer_ids_only": True,
    }


def to_predictive(*, tenant_id: str, forecast_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "forecast_ref": forecast_ref,
        "via_p213_j": True,
        "peer_ids_only": True,
    }


def to_prescriptive(*, tenant_id: str, recommendation_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "recommendation_ref": recommendation_ref,
        "via_p213_k": True,
        "peer_ids_only": True,
    }


def to_enterprise_ai(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai": True,
        "module_local_llm_sdk_forbidden": True,
        "ai_reasoning_present_required": True,
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
