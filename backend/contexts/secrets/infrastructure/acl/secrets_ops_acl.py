"""ACL: Secrets Ops / CQRS fabric ↔ peers (P209-L)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_event_fabric(*, tenant_id: str, event_name: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "event_name": event_name,
        "via_event_fabric": True,
        "outbox_required": True,
        "events_present_required": True,
        "peer_ids_only": True,
    }


def to_api_gateway(*, tenant_id: str, route: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "route": route,
        "via_api_gateway": True,
        "api_security_required": True,
        "zero_trust_api": True,
        "peer_ids_only": True,
    }


def to_authorization_ops(
    *, tenant_id: str, principal_ref: str, action: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "principal_ref": principal_ref,
        "action": action,
        "via_authorization": True,
        "api_security_required": True,
        "peer_ids_only": True,
    }


def to_observability(*, tenant_id: str, service_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "service_ref": service_ref,
        "via_observability": True,
        "observability_complete_required": True,
        "otel": True,
        "peer_ids_only": True,
    }


def to_ai_ops_infer(
    *, tenant_id: str, surface: str, context: dict
) -> dict[str, Any]:
    result = base.to_ai_infer(
        tenant_id=tenant_id, surface=surface, context=context
    )
    result["via_ai_platform"] = True
    result["advisor_not_authority"] = True
    return result


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["crypto_operations_auditable_required"] = True
    result["events_present_required"] = True
    return result


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": [
            "event_fabric",
            "api_gateway",
            "authorization",
            "observability",
            "ai",
            "audit",
        ],
        "no_shared_databases_required": True,
        "api_security_required": True,
        "via_event_fabric": True,
        "via_observability": True,
    }
