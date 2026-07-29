"""ACL: Data Security AI autonomous protection ↔ peers (P211-L)."""
from __future__ import annotations

from typing import Any


def to_enterprise_ai(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai": True,
        "ai_decisions_explainable_required": True,
        "data_risks_predictable_required": True,
        "module_local_llm_sdk_forbidden": True,
        "peer_ids_only": True,
    }


def to_workflow_oversight(
    *, tenant_id: str, action_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "action_ref": action_ref,
        "via_workflow": True,
        "human_oversight_possible_required": True,
        "autonomous_actions_controlled_required": True,
        "peer_ids_only": True,
    }


def to_policy_engine(*, tenant_id: str, policy_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_policy_engine": True,
        "ai_security_governance_present_required": True,
        "peer_ids_only": True,
    }


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


def to_protection(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211_j_protection": True,
        "peer_ids_only": True,
    }


def to_intelligence(*, tenant_id: str, graph_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "graph_ref": graph_ref,
        "via_p211_k_intelligence": True,
        "learning_loop_present_required": True,
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
