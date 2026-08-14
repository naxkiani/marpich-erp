"""ACL: Data Security QA/governance/DoD ↔ peers (P211-P)."""
from __future__ import annotations

from typing import Any


def to_audit(*, tenant_id: str, evidence_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "evidence_ref": evidence_ref,
        "via_audit_platform": True,
        "compliance_evidence_available_required": True,
        "peer_ids_only": True,
    }


def to_compliance(*, tenant_id: str, control_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "control_ref": control_ref,
        "via_compliance_acl": True,
        "security_validation_present_required": True,
        "peer_ids_only": True,
    }


def to_consent(*, tenant_id: str, processing_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "processing_ref": processing_ref,
        "via_consent_acl_only": True,
        "ledger_owned_by": "consent",
        "peer_ids_only": True,
    }


def to_devsecops(*, tenant_id: str, pipeline_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "pipeline_ref": pipeline_ref,
        "via_p211_o_devsecops": True,
        "testing_automated_required": True,
        "peer_ids_only": True,
    }


def to_governance(*, tenant_id: str, control_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "control_ref": control_ref,
        "governance_ownership_clear_required": True,
        "peer_ids_only": True,
    }


def to_risk(*, tenant_id: str, risk_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "risk_ref": risk_ref,
        "risks_trackable_required": True,
        "peer_ids_only": True,
    }


def to_identity(*, tenant_id: str, identity_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "identity_ref": identity_ref,
        "via_p207": True,
        "peer_ids_only": True,
    }


def to_authorization(
    *, tenant_id: str, principal_ref: str, action: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "principal_ref": principal_ref,
        "action": action,
        "via_p208": True,
        "peer_ids_only": True,
    }


def to_secrets(*, tenant_id: str, key_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "key_ref": key_ref,
        "via_p209": True,
        "peer_ids_only": True,
    }


def to_cyber_security(
    *, tenant_id: str, signal_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "signal_ref": signal_ref,
        "via_p210": True,
        "peer_ids_only": True,
    }


def to_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "twin_ref": twin_ref,
        "via_p211_m": True,
        "production_readiness_defined_required": True,
        "peer_ids_only": True,
    }
