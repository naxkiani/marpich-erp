"""ACL: Cyber Security XDR/EDR/NDR ↔ peers (P210-G)."""
from __future__ import annotations

from typing import Any


def to_soar_playbook(
    *, tenant_id: str, playbook_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "playbook_ref": playbook_ref,
        "via_p210_f_soar": True,
        "orchestration_not_local": True,
        "peer_ids_only": True,
    }


def to_workflow_approval(
    *, tenant_id: str, gate_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "gate_ref": gate_ref,
        "via_workflow": True,
        "response_safeguards_required": True,
        "local_approval_engine_forbidden": True,
        "peer_ids_only": True,
    }


def to_integration_sensor(
    *, tenant_id: str, sensor_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "sensor_ref": sensor_ref,
        "via_integration_platform": True,
        "vendor_sdk_embed_forbidden": True,
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


def to_soc(*, tenant_id: str, alert_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "alert_ref": alert_ref,
        "via_p210_d_soc": True,
        "peer_ids_only": True,
    }


def to_ai_analytics(
    *, tenant_id: str, analytics_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "analytics_ref": analytics_ref,
        "via_ai_platform": True,
        "ai_analytics_required": True,
        "explainable_required": True,
        "advisor_not_authority": True,
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


def to_observability(
    *, tenant_id: str, telemetry_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "telemetry_ref": telemetry_ref,
        "via_observability": True,
        "endpoint_telemetry_complete_required": True,
        "peer_ids_only": True,
    }


def to_secrets_agent_integrity(
    *, tenant_id: str, agent_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "agent_ref": agent_ref,
        "via_secrets_p209": True,
        "agent_integrity_verifiable_required": True,
        "code_signing": True,
        "peer_ids_only": True,
    }
