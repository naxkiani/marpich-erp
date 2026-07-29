"""ACL: Cyber Security Threat Intelligence ↔ peers (P210-H)."""
from __future__ import annotations

from typing import Any


def to_soc(*, tenant_id: str, hunt_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "hunt_ref": hunt_ref,
        "via_p210_d_soc": True,
        "peer_ids_only": True,
    }


def to_siem(*, tenant_id: str, detection_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "detection_ref": detection_ref,
        "via_p210_e_siem": True,
        "detection_engineering_connected": True,
        "peer_ids_only": True,
    }


def to_soar(*, tenant_id: str, playbook_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "playbook_ref": playbook_ref,
        "via_p210_f_soar": True,
        "peer_ids_only": True,
    }


def to_xdr(*, tenant_id: str, ioc_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "ioc_ref": ioc_ref,
        "via_p210_g_xdr": True,
        "peer_ids_only": True,
    }


def to_integration_feed(
    *, tenant_id: str, feed_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "feed_ref": feed_ref,
        "via_integration_platform": True,
        "vendor_sdk_embed_forbidden": True,
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


def to_knowledge_graph(
    *, tenant_id: str, graph_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "graph_ref": graph_ref,
        "via_knowledge_graph": True,
        "integration_required": True,
        "peer_ids_only": True,
    }


def to_stix_taxii(
    *, tenant_id: str, channel_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "channel_ref": channel_ref,
        "standards_based": True,
        "stix_taxii": True,
        "peer_ids_only": True,
    }


def to_security_incident(
    *, tenant_id: str, incident_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "incident_ref": incident_ref,
        "via_security_incident": True,
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
