"""ACL: Data Security protection ↔ peers (P211-J)."""
from __future__ import annotations

from typing import Any


def to_secrets(*, tenant_id: str, key_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "key_ref": key_ref,
        "via_p209": True,
        "key_integration_available_required": True,
        "kms_owner": "secrets",
        "peer_key_refs_only": True,
        "module_local_kms_forbidden": True,
        "peer_ids_only": True,
    }


def to_discovery(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211_d_discovery": True,
        "sensitive_data_protected_required": True,
        "peer_ids_only": True,
    }


def to_classification(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211_e_classification": True,
        "encryption_policies_defined_required": True,
        "peer_ids_only": True,
    }


def to_dspm(*, tenant_id: str, posture_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "posture_ref": posture_ref,
        "via_p211_f_dspm": True,
        "peer_ids_only": True,
    }


def to_dlp(*, tenant_id: str, policy_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_p211_g_dlp": True,
        "peer_ids_only": True,
    }


def to_access(*, tenant_id: str, entitlement_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "entitlement_ref": entitlement_ref,
        "via_p211_h_access": True,
        "peer_ids_only": True,
    }


def to_privacy(*, tenant_id: str, control_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "control_ref": control_ref,
        "via_p211_i_privacy": True,
        "privacy_controls_complete_required": True,
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
        "protection_decisions_auditable_required": True,
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


def to_enterprise_ai(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai": True,
        "module_local_llm_sdk_forbidden": True,
        "peer_ids_only": True,
    }


def to_policy_engine(*, tenant_id: str, policy_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_policy_engine": True,
        "encryption_policies_defined_required": True,
        "peer_ids_only": True,
    }


def to_workflow(*, tenant_id: str, approval_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "approval_ref": approval_ref,
        "via_workflow": True,
        "token_lifecycle_present_required": True,
        "peer_ids_only": True,
    }
