"""ACL: Data Security intelligence graph ↔ peers (P211-K)."""
from __future__ import annotations

from typing import Any


def to_discovery(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211_d_discovery": True,
        "data_origin_known_required": True,
        "peer_ids_only": True,
    }


def to_classification(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211_e_classification": True,
        "metadata_complete_required": True,
        "peer_ids_only": True,
    }


def to_dlp(*, tenant_id: str, policy_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_p211_g_dlp": True,
        "data_movement_visible_required": True,
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
        "ai_reasoning_over_context_required": True,
        "module_local_llm_sdk_forbidden": True,
        "peer_ids_only": True,
    }


def to_enterprise_search(
    *, tenant_id: str, query_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "query_ref": query_ref,
        "via_enterprise_search": True,
        "relationships_queryable_required": True,
        "module_local_search_forbidden": True,
        "peer_ids_only": True,
    }


def to_integration(
    *, tenant_id: str, connector_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "connector_ref": connector_ref,
        "via_integration_platform": True,
        "impact_analysis_available_required": True,
        "vendor_sdk_embed_forbidden": True,
        "peer_ids_only": True,
    }
