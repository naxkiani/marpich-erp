"""ACL: DevSecOps & Observability ↔ platform peers (P207-N)."""
from __future__ import annotations

from typing import Any

from contexts.identity_intelligence.infrastructure.acl import ii_platform_acl as base


def to_observability(
    *, tenant_id: str, metric_name: str, value: float
) -> dict[str, Any]:
    result = base.to_observability(
        tenant_id=tenant_id, metric_name=metric_name, value=value
    )
    result["metrics_logs_traces"] = True
    result["observability_complete_required"] = True
    return result


def to_api_gateway(*, tenant_id: str, route_ref: str) -> dict[str, Any]:
    return {
        "target": "api_gateway",
        "command": "ValidateIngressPolicy",
        "payload": {"tenant_id": tenant_id, "route_ref": route_ref},
        "pattern": "customer_supplier",
        "cloud_native_entry": True,
    }


def to_service_mesh(*, tenant_id: str, service_name: str) -> dict[str, Any]:
    return {
        "target": "service_mesh",
        "command": "ValidateServiceIdentity",
        "payload": {"tenant_id": tenant_id, "service_name": service_name},
        "pattern": "customer_supplier",
        "mtls_required": True,
        "service_identity_required": True,
    }


def to_secrets(*, tenant_id: str, secret_ref: str) -> dict[str, Any]:
    return {
        "target": "secrets",
        "command": "ResolveSecret",
        "payload": {"tenant_id": tenant_id, "secret_ref": secret_ref},
        "pattern": "acl",
        "secret_management_required": True,
        "zero_trust_infrastructure": True,
    }


def to_security_ops(*, tenant_id: str, incident_ref: str) -> dict[str, Any]:
    return {
        "target": "security_operations",
        "command": "EscalateIncident",
        "payload": {"tenant_id": tenant_id, "incident_ref": incident_ref},
        "pattern": "acl",
        "siem_integration": True,
        "devsecops_integrated": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["deployment_audit"] = True
    result["pipeline_audit_trail"] = True
    return result
