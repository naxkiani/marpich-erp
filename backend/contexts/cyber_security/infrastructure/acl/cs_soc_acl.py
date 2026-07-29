"""ACL: Cyber Security SOC ↔ peers (P210-D)."""
from __future__ import annotations

from typing import Any


def to_security_incident_handoff(
    *, tenant_id: str, alert_ref: str, severity: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "alert_ref": alert_ref,
        "severity": severity,
        "event_name": "security.attack.detected",
        "via_security_incident": True,
        "ir_lifecycle_owned_by_security_incident": True,
        "peer_ids_only": True,
    }


def to_workflow_playbook(
    *, tenant_id: str, playbook_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "playbook_ref": playbook_ref,
        "via_workflow": True,
        "manual_only_forbidden": True,
        "peer_ids_only": True,
    }


def to_ai_assistance(*, tenant_id: str, surface_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "surface_ref": surface_ref,
        "via_ai_platform": True,
        "ai_assistance_required": True,
        "advisor_not_authority": True,
        "peer_ids_only": True,
    }


def to_knowledge_graph(*, tenant_id: str, node_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "node_ref": node_ref,
        "via_knowledge_graph": True,
        "does_not_own_kg_sor": True,
        "peer_ids_only": True,
    }


def to_digital_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "twin_ref": twin_ref,
        "via_digital_twin": True,
        "does_not_own_twin_sor": True,
        "peer_ids_only": True,
    }


def to_integration(*, tenant_id: str, connector_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "connector_ref": connector_ref,
        "via_integration_platform": True,
        "vendor_sdk_embed_forbidden": True,
        "peer_ids_only": True,
    }


def to_authorization(*, tenant_id: str, principal_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "principal_ref": principal_ref,
        "via_authorization": True,
        "zero_trust": True,
        "peer_ids_only": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "action": action,
        "resource_ref": resource_ref,
        "via_audit_platform": True,
        "immutable": True,
        "peer_ids_only": True,
    }
