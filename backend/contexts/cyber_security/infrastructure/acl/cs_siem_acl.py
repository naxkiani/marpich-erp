"""ACL: Cyber Security SIEM ↔ peers (P210-E)."""
from __future__ import annotations

from typing import Any


def to_soc(*, tenant_id: str, alert_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "alert_ref": alert_ref,
        "via_p210_d_soc": True,
        "peer_ids_only": True,
    }


def to_soar_playbook(
    *, tenant_id: str, playbook_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "playbook_ref": playbook_ref,
        "via_p210_f_soar": True,
        "peer_ids_only": True,
    }


def to_xdr(*, tenant_id: str, signal_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "signal_ref": signal_ref,
        "via_p210_g_xdr": True,
        "peer_ids_only": True,
    }


def to_integration_collector(
    *, tenant_id: str, collector_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "collector_ref": collector_ref,
        "via_integration_platform": True,
        "vendor_sdk_embed_forbidden": True,
        "peer_ids_only": True,
    }


def to_observability(
    *, tenant_id: str, telemetry_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "telemetry_ref": telemetry_ref,
        "via_observability": True,
        "telemetry_integrity_validation_required": True,
        "peer_ids_only": True,
    }


def to_ai_intelligence(
    *, tenant_id: str, intelligence_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "intelligence_ref": intelligence_ref,
        "via_ai_platform": True,
        "ai_intelligence_required": True,
        "explainable_required": True,
        "advisor_not_authority": True,
        "peer_ids_only": True,
    }


def to_security_incident(
    *, tenant_id: str, incident_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "incident_ref": incident_ref,
        "via_security_incident": True,
        "ir_lifecycle_owned_by_security_incident": True,
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
