"""ACL: Data Security privacy intelligence ↔ peers (P211-I)."""
from __future__ import annotations

from typing import Any


def to_consent(*, tenant_id: str, consent_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "consent_ref": consent_ref,
        "via_consent_bc": True,
        "consent_trackable_required": True,
        "ledger_owner": "consent",
        "peer_ids_only": True,
        "absorb_consent_ledger_forbidden": True,
    }


def to_discovery(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211_d_discovery": True,
        "personal_data_discoverable_required": True,
        "peer_ids_only": True,
    }


def to_classification(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211_e_classification": True,
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


def to_enterprise_ai(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai": True,
        "ai_privacy_risks_managed_required": True,
        "privacy_risks_measurable_required": True,
        "module_local_llm_sdk_forbidden": True,
        "peer_ids_only": True,
    }


def to_workflow_assessment(
    *, tenant_id: str, assessment_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "assessment_ref": assessment_ref,
        "via_workflow": True,
        "processing_visible_required": True,
        "peer_ids_only": True,
    }


def to_compliance(
    *, tenant_id: str, obligation_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "obligation_ref": obligation_ref,
        "via_compliance": True,
        "regulatory_obligations_mapped_required": True,
        "peer_ids_only": True,
    }


def to_policy_engine(*, tenant_id: str, policy_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_policy_engine": True,
        "peer_ids_only": True,
    }
