"""ACL: Data Security DLP ↔ peers (P211-G)."""
from __future__ import annotations

from typing import Any


def to_discovery(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211_d_discovery": True,
        "peer_ids_only": True,
    }


def to_classification(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211_e_classification": True,
        "sensitive_data_identifiable_required": True,
        "peer_ids_only": True,
    }


def to_dspm(*, tenant_id: str, posture_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "posture_ref": posture_ref,
        "via_p211_f_dspm": True,
        "peer_ids_only": True,
    }


def to_enterprise_ai(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai": True,
        "ai_leakage_managed_required": True,
        "module_local_llm_sdk_forbidden": True,
        "peer_ids_only": True,
    }


def to_policy_engine(*, tenant_id: str, policy_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_policy_engine": True,
        "policies_enforceable_required": True,
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
        "via_p210_soar": True,
        "via_p210_siem": True,
        "automated_response_available_required": True,
        "peer_ids_only": True,
    }


def to_identity(*, tenant_id: str, identity_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "identity_ref": identity_ref,
        "via_p207": True,
        "insider_risk_visible_required": True,
        "peer_ids_only": True,
    }


def to_workflow_incident(
    *, tenant_id: str, incident_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "incident_ref": incident_ref,
        "via_workflow": True,
        "violations_investigable_required": True,
        "data_movement_monitored_required": True,
        "peer_ids_only": True,
    }
