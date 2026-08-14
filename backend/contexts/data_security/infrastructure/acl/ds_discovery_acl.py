"""ACL: Data Security discovery / inventory ↔ peers (P211-D)."""
from __future__ import annotations

from typing import Any


def to_integration_connector(
    *, tenant_id: str, connector_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "connector_ref": connector_ref,
        "via_integration_platform": True,
        "vendor_sdk_embed_forbidden": True,
        "data_assets_discoverable_required": True,
        "peer_ids_only": True,
    }


def to_enterprise_ai(
    *, tenant_id: str, model_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai": True,
        "ai_discovery_required": True,
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
        "ownership_determinable_required": True,
        "peer_ids_only": True,
    }


def to_secrets(*, tenant_id: str, secret_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "secret_ref": secret_ref,
        "via_p209": True,
        "connector_secrets_owned_by_secrets": True,
        "peer_ids_only": True,
    }


def to_cyber_security(
    *, tenant_id: str, signal_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "signal_ref": signal_ref,
        "via_p210": True,
        "shadow_data_visible_required": True,
        "peer_ids_only": True,
    }


def to_identity_intelligence(
    *, tenant_id: str, identity_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "identity_ref": identity_ref,
        "via_p207": True,
        "peer_ids_only": True,
    }


def to_search(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_enterprise_search": True,
        "index_via_events_only": True,
        "peer_ids_only": True,
    }
