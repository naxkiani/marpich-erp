"""ACL: Data Governance deploy ↔ peers (P212-N)."""
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


def to_secrets(*, tenant_id: str, key_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "key_ref": key_ref,
        "via_p209": True,
        "peer_ids_only": True,
    }


def to_cyber_security(*, tenant_id: str, posture_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "posture_ref": posture_ref,
        "via_p210": True,
        "peer_ids_only": True,
    }


def to_data_security(*, tenant_id: str, classification_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "classification_ref": classification_ref,
        "via_p211": True,
        "peer_ids_only": True,
    }


def to_observability(*, tenant_id: str, signal_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "signal_ref": signal_ref,
        "via_platform_observability": True,
        "module_local_observability_stack_forbidden": True,
        "peer_ids_only": True,
    }


def to_event_bus(*, tenant_id: str, topic_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "topic_ref": topic_ref,
        "via_enterprise_event_bus": True,
        "module_local_broker_forbidden": True,
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


def to_ops(*, tenant_id: str, ops_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "ops_ref": ops_ref,
        "via_p212_m": True,
        "cqrs_operational_integration_present_required": True,
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
