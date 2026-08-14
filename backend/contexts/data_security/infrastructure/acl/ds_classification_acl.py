"""ACL: Data Security classification / labeling ↔ peers (P211-E)."""
from __future__ import annotations

from typing import Any


def to_discovery(*, tenant_id: str, asset_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "asset_ref": asset_ref,
        "via_p211_d_discovery": True,
        "data_classifiable_required": True,
        "peer_ids_only": True,
    }


def to_enterprise_ai(
    *, tenant_id: str, model_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai": True,
        "ai_decisions_explainable_required": True,
        "module_local_llm_sdk_forbidden": True,
        "peer_ids_only": True,
    }


def to_policy_engine(
    *, tenant_id: str, policy_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_policy_engine": True,
        "classification_policies_present_required": True,
        "peer_ids_only": True,
    }


def to_workflow_review(
    *, tenant_id: str, review_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "review_ref": review_ref,
        "via_workflow": True,
        "classification_lifecycle_defined_required": True,
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
        "labels_managed_required": True,
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
        "sensitive_detection_available_required": True,
        "peer_ids_only": True,
    }
