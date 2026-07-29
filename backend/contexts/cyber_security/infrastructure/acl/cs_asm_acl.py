"""ACL: Cyber Security ASM/CTEM ↔ peers (P210-I)."""
from __future__ import annotations

from typing import Any


def to_soar_remediation(
    *, tenant_id: str, playbook_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "playbook_ref": playbook_ref,
        "via_p210_f_soar": True,
        "remediation_validated_required": True,
        "peer_ids_only": True,
    }


def to_workflow_approval(
    *, tenant_id: str, gate_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "gate_ref": gate_ref,
        "via_workflow": True,
        "human_approval_required": True,
        "peer_ids_only": True,
    }


def to_threat_intel(
    *, tenant_id: str, vuln_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "vuln_ref": vuln_ref,
        "via_p210_h_intel": True,
        "peer_ids_only": True,
    }


def to_siem(*, tenant_id: str, exposure_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "exposure_ref": exposure_ref,
        "via_p210_e_siem": True,
        "peer_ids_only": True,
    }


def to_xdr(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p210_g_xdr": True,
        "peer_ids_only": True,
    }


def to_soc(*, tenant_id: str, risk_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "risk_ref": risk_ref,
        "via_p210_d_soc": True,
        "peer_ids_only": True,
    }


def to_integration_discovery(
    *, tenant_id: str, connector_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "connector_ref": connector_ref,
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
        "business_context_required": True,
        "peer_ids_only": True,
    }


def to_cmdb(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_cmdb_refs": True,
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
