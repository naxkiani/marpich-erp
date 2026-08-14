"""ACL: Cyber Security SOAR ↔ peers (P210-F)."""
from __future__ import annotations

from typing import Any


def to_workflow_approval(
    *, tenant_id: str, gate_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "gate_ref": gate_ref,
        "via_workflow": True,
        "human_approval_required": True,
        "local_approval_engine_forbidden": True,
        "peer_ids_only": True,
    }


def to_integration_connector(
    *, tenant_id: str, connector_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "connector_ref": connector_ref,
        "via_integration_platform": True,
        "tightly_coupled_forbidden": True,
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


def to_ai_explainable(
    *, tenant_id: str, advisory_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "advisory_ref": advisory_ref,
        "via_ai_platform": True,
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
        "automation_auditable_required": True,
        "immutable": True,
        "peer_ids_only": True,
    }


def to_evidence(
    *, tenant_id: str, evidence_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "evidence_ref": evidence_ref,
        "preservation_required": True,
        "peer_ids_only": True,
    }
