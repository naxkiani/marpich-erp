"""ACL: Cyber Security Knowledge Graph ↔ peers (P210-K)."""
from __future__ import annotations

from typing import Any


def to_enterprise_ai(
    *, tenant_id: str, reasoning_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "reasoning_ref": reasoning_ref,
        "via_enterprise_ai_platform": True,
        "ai_reasoning_available_required": True,
        "peer_ids_only": True,
    }


def to_soc(*, tenant_id: str, graph_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "graph_ref": graph_ref,
        "via_p210_d_soc": True,
        "peer_ids_only": True,
    }


def to_siem(*, tenant_id: str, entity_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "entity_ref": entity_ref,
        "via_p210_e_siem": True,
        "peer_ids_only": True,
    }


def to_soar(*, tenant_id: str, playbook_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "playbook_ref": playbook_ref,
        "via_p210_f_soar": True,
        "peer_ids_only": True,
    }


def to_xdr(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p210_g_xdr": True,
        "peer_ids_only": True,
    }


def to_intel(*, tenant_id: str, threat_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "threat_ref": threat_ref,
        "via_p210_h_intel": True,
        "peer_ids_only": True,
    }


def to_asm(*, tenant_id: str, exposure_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "exposure_ref": exposure_ref,
        "via_p210_i_asm": True,
        "peer_ids_only": True,
    }


def to_ai_ops(*, tenant_id: str, agent_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "agent_ref": agent_ref,
        "via_p210_j_ai_ops": True,
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
        "graph_governance_required": True,
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
