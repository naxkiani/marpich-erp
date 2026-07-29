"""ACL: Cyber Security Ops Fabric ↔ peers (P210-L)."""
from __future__ import annotations

from typing import Any


def to_event_bus(
    *, tenant_id: str, event_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "event_ref": event_ref,
        "via_enterprise_event_bus": True,
        "events_immutable_required": True,
        "event_governance_required": True,
        "outbox_required": True,
        "peer_ids_only": True,
    }


def to_api_gateway(
    *, tenant_id: str, route_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "route_ref": route_ref,
        "via_api_gateway": True,
        "apis_security_controls_required": True,
        "peer_ids_only": True,
    }


def to_observability(
    *, tenant_id: str, signal_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "signal_ref": signal_ref,
        "via_observability": True,
        "observability_required": True,
        "peer_ids_only": True,
    }


def to_enterprise_ai(
    *, tenant_id: str, stream_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "stream_ref": stream_ref,
        "via_enterprise_ai_platform": True,
        "ai_integration_possible_required": True,
        "peer_ids_only": True,
    }


def to_authorization(
    *, tenant_id: str, principal_ref: str, action: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "principal_ref": principal_ref,
        "action": action,
        "via_authorization": True,
        "least_privilege": True,
        "peer_ids_only": True,
    }


def to_audit(
    *, tenant_id: str, action: str, resource_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "action": action,
        "resource_ref": resource_ref,
        "via_audit_platform": True,
        "immutable": True,
        "peer_ids_only": True,
    }


def to_graph(*, tenant_id: str, graph_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "graph_ref": graph_ref,
        "via_p210_k": True,
        "peer_ids_only": True,
    }
