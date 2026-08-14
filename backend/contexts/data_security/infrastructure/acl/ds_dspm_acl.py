"""ACL: Data Security DSPM ↔ peers (P211-F)."""
from __future__ import annotations

from typing import Any


def to_discovery(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211_d_discovery": True,
        "data_assets_known_required": True,
        "peer_ids_only": True,
    }


def to_classification(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211_e_classification": True,
        "peer_ids_only": True,
    }


def to_enterprise_ai(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai": True,
        "security_posture_measurable_required": True,
        "module_local_llm_sdk_forbidden": True,
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
        "exposure_risks_visible_required": True,
        "peer_ids_only": True,
    }


def to_identity(*, tenant_id: str, identity_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "identity_ref": identity_ref,
        "via_p207": True,
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
        "continuous_assessment_available_required": True,
        "peer_ids_only": True,
    }


def to_workflow_remediation(
    *, tenant_id: str, remediation_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "remediation_ref": remediation_ref,
        "via_workflow": True,
        "remediation_not_manual_only_required": True,
        "findings_owned_required": True,
        "peer_ids_only": True,
    }


def to_policy_engine(
    *, tenant_id: str, policy_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_policy_engine": True,
        "peer_ids_only": True,
    }
