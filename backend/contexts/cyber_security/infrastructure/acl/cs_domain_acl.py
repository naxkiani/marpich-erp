"""ACL: Cyber Security domain architecture ↔ peers (P210-C)."""
from __future__ import annotations

from typing import Any


def to_security_incident(*, tenant_id: str, detection_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "detection_ref": detection_ref,
        "via_security_incident": True,
        "ir_lifecycle_owned_by_security_incident": True,
        "logical_context": "incident_response_handoff",
        "peer_ids_only": True,
    }


def to_identity_intelligence(*, tenant_id: str, signal_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "signal_ref": signal_ref,
        "via_p207": True,
        "peer_ids_only": True,
    }


def to_authorization(*, tenant_id: str, principal_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "principal_ref": principal_ref,
        "via_p208": True,
        "peer_ids_only": True,
    }


def to_secrets(*, tenant_id: str, trust_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "trust_ref": trust_ref,
        "via_p209": True,
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


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "action": action,
        "resource_ref": resource_ref,
        "via_audit_platform": True,
        "immutable": True,
        "peer_ids_only": True,
    }
