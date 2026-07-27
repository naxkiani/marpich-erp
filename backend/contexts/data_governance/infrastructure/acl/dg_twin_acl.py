"""ACL: Data Governance digital twin ↔ peers (P212-L)."""
from __future__ import annotations

from typing import Any


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


def to_cyber_security(*, tenant_id: str, signal_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "signal_ref": signal_ref,
        "via_p210": True,
        "peer_ids_only": True,
    }


def to_data_security(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211": True,
        "peer_ids_only": True,
    }


def to_quality(*, tenant_id: str, quality_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "quality_ref": quality_ref,
        "via_p212_e": True,
        "peer_ids_only": True,
    }


def to_mesh(*, tenant_id: str, product_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "product_ref": product_ref,
        "via_p212_f": True,
        "data_mesh_integration_present_required": True,
        "peer_ids_only": True,
    }


def to_policies(*, tenant_id: str, policy_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_p212_h": True,
        "policy_simulation_present_required": True,
        "peer_ids_only": True,
    }


def to_graph(*, tenant_id: str, entity_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "entity_ref": entity_ref,
        "via_p212_j": True,
        "knowledge_graph_integration_present_required": True,
        "peer_ids_only": True,
    }


def to_ai_readiness(*, tenant_id: str, dataset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "dataset_ref": dataset_ref,
        "via_p212_k": True,
        "ai_governance_integration_present_required": True,
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
        "peer_ids_only": True,
    }
