"""ACL: Data Security CQRS/events/ops ↔ peers (P211-N)."""
from __future__ import annotations

from typing import Any


def to_event_bus(*, tenant_id: str, event_name: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "event_name": event_name,
        "via_enterprise_event_bus": True,
        "events_immutable_required": True,
        "outbox_required": True,
        "mutate_envelope_forbidden": True,
        "peer_ids_only": True,
    }


def to_api_gateway(*, tenant_id: str, route_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "route_ref": route_ref,
        "via_api_gateway": True,
        "apis_managed_required": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, decision_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "decision_ref": decision_ref,
        "via_audit_platform": True,
        "security_decisions_traceable_required": True,
        "audit_history_complete_required": True,
        "peer_ids_only": True,
    }


def to_secrets_mesh(*, tenant_id: str, service_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "service_ref": service_ref,
        "via_p209": True,
        "mtls_via_p209": True,
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


def to_cyber_security(
    *, tenant_id: str, signal_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "signal_ref": signal_ref,
        "via_p210": True,
        "peer_ids_only": True,
    }


def to_intelligence(*, tenant_id: str, graph_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "graph_ref": graph_ref,
        "via_p211_k": True,
        "services_loosely_coupled_required": True,
        "peer_ids_only": True,
    }


def to_ai_security(*, tenant_id: str, decision_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "decision_ref": decision_ref,
        "via_p211_l": True,
        "peer_ids_only": True,
    }


def to_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "twin_ref": twin_ref,
        "via_p211_m": True,
        "scaling_possible_required": True,
        "peer_ids_only": True,
    }
