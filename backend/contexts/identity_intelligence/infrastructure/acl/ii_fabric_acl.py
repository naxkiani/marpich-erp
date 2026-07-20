"""ACL: Distributed fabric ↔ platform peers (P207-L)."""
from __future__ import annotations

from typing import Any

from contexts.identity_intelligence.infrastructure.acl import ii_platform_acl as base


def to_authz_check(*, tenant_id: str, subject_id: str, action: str) -> dict[str, Any]:
    result = base.to_authz_check(
        tenant_id=tenant_id, subject_id=subject_id, action=action
    )
    result["zero_trust_api"] = True
    result["policy_based_access"] = True
    return result


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["complete_audit_history_required"] = True
    result["decision_traceability"] = True
    return result


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    result = base.to_ai_infer(tenant_id=tenant_id, surface=surface, context=context)
    result["fabric_ai_context"] = True
    result["ai_integration_connected_required"] = True
    return result


def to_observability(
    *, tenant_id: str, metric_name: str, value: float
) -> dict[str, Any]:
    result = base.to_observability(
        tenant_id=tenant_id, metric_name=metric_name, value=value
    )
    result["service_latency_tracking"] = True
    result["event_failure_rate_tracking"] = True
    return result


def to_event_fabric(*, tenant_id: str, event_name: str, version: str) -> dict[str, Any]:
    return {
        "target": "event_bus",
        "command": "PublishIntegrationEvent",
        "payload": {
            "tenant_id": tenant_id,
            "event_name": event_name,
            "version": version,
        },
        "pattern": "acl",
        "event_versioning_required": True,
        "guaranteed_delivery_required": True,
        "replay_required": True,
    }


def to_service_mesh(*, tenant_id: str, service_name: str) -> dict[str, Any]:
    return {
        "target": "service_mesh",
        "command": "ValidateServiceIdentity",
        "payload": {"tenant_id": tenant_id, "service_name": service_name},
        "pattern": "customer_supplier",
        "mtls_required": True,
        "service_identity_required": True,
        "permissions_required": True,
    }


def to_api_gateway(*, tenant_id: str, route_ref: str) -> dict[str, Any]:
    return {
        "target": "api_gateway",
        "command": "ValidateRoutePolicy",
        "payload": {"tenant_id": tenant_id, "route_ref": route_ref},
        "pattern": "customer_supplier",
        "gateway_required": True,
        "rate_limiting_required": True,
        "threat_detection_required": True,
    }
