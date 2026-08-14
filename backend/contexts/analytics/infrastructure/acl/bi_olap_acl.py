"""ACL: BI olap / semantic ↔ peers (P213-G)."""
from __future__ import annotations

from typing import Any


def to_identity(*, tenant_id: str, identity_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "identity_ref": identity_ref,
        "via_p207": True,
        "metric_level_authorization": True,
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
        "attribute_based_access_control": True,
        "fine_grained_access_control": True,
        "peer_ids_only": True,
    }


def to_data_security(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211": True,
        "data_masking": True,
        "classification_awareness": True,
        "peer_ids_only": True,
    }


def to_data_governance(
    *, tenant_id: str, product_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "product_ref": product_ref,
        "via_p212": True,
        "policy_based_calculations": True,
        "peer_ids_only": True,
    }


def to_knowledge_graph(*, tenant_id: str, node_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "node_ref": node_ref,
        "via_p212_j": True,
        "knowledge_graph_integration_present_required": True,
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


def to_warehouse(*, tenant_id: str, warehouse_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "warehouse_ref": warehouse_ref,
        "via_p213_e": True,
        "peer_ids_only": True,
    }


def to_lakehouse(*, tenant_id: str, lakehouse_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "lakehouse_ref": lakehouse_ref,
        "via_p213_f": True,
        "peer_ids_only": True,
    }


def to_reporting(*, tenant_id: str, report_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "report_ref": report_ref,
        "via_p213_d": True,
        "peer_ids_only": True,
    }


def to_enterprise_ai(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai": True,
        "module_local_llm_sdk_forbidden": True,
        "ai_native_semantic_platform_present_required": True,
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


def to_enterprise_search(*, tenant_id: str, query_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "query_ref": query_ref,
        "via_enterprise_search": True,
        "semantic_query_layer_present_required": True,
        "peer_ids_only": True,
    }
