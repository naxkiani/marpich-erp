"""ACL: BI ops / CQRS-events-APIs ↔ peers (P213-N)."""
from __future__ import annotations

from typing import Any


def to_identity(*, tenant_id: str, identity_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "identity_ref": identity_ref,
        "via_p207": True,
        "oauth2": True,
        "oidc": True,
        "jwt": True,
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
        "fine_grained_authorization": True,
        "peer_ids_only": True,
    }


def to_cryptographic_trust(*, tenant_id: str, trust_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "trust_ref": trust_ref,
        "via_p209": True,
        "mtls": True,
        "spiffe_spire": True,
        "peer_ids_only": True,
    }


def to_cyber_security(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p210": True,
        "zero_trust": True,
        "peer_ids_only": True,
    }


def to_data_security(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211": True,
        "api_auditing": True,
        "peer_ids_only": True,
    }


def to_data_governance(*, tenant_id: str, product_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "product_ref": product_ref,
        "via_p212": True,
        "continuous_governance": True,
        "peer_ids_only": True,
    }


def to_ai_native(*, tenant_id: str, decision_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "decision_ref": decision_ref,
        "via_p213_m": True,
        "peer_ids_only": True,
    }


def to_decision_graph(*, tenant_id: str, decision_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "decision_ref": decision_ref,
        "via_p213_l": True,
        "peer_ids_only": True,
    }


def to_prescriptive(*, tenant_id: str, recommendation_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "recommendation_ref": recommendation_ref,
        "via_p213_k": True,
        "peer_ids_only": True,
    }


def to_predictive(*, tenant_id: str, forecast_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "forecast_ref": forecast_ref,
        "via_p213_j": True,
        "peer_ids_only": True,
    }


def to_enterprise_event_fabric(
    *, tenant_id: str, event_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "event_ref": event_ref,
        "via_enterprise_event_fabric": True,
        "module_local_event_bus_forbidden": True,
        "outbox_required": True,
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
        "rate_limiting": True,
        "peer_ids_only": True,
    }


def to_observability(*, tenant_id: str, span_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "span_ref": span_ref,
        "via_platform_observability": True,
        "opentelemetry": True,
        "module_local_metrics_store_forbidden": True,
        "peer_ids_only": True,
    }
