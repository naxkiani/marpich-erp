"""ACL: Cyber Security AI Ops ↔ peers (P210-J)."""
from __future__ import annotations

from typing import Any


def to_enterprise_ai(
    *, tenant_id: str, inference_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "inference_ref": inference_ref,
        "via_enterprise_ai_platform": True,
        "module_local_llm_sdk_forbidden": True,
        "explainable_required": True,
        "peer_ids_only": True,
    }


def to_workflow_oversight(
    *, tenant_id: str, gate_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "gate_ref": gate_ref,
        "via_workflow": True,
        "human_oversight_required": True,
        "peer_ids_only": True,
    }


def to_soar(*, tenant_id: str, playbook_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "playbook_ref": playbook_ref,
        "via_p210_f_soar": True,
        "autonomous_actions_audited_required": True,
        "peer_ids_only": True,
    }


def to_soc(*, tenant_id: str, alert_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "alert_ref": alert_ref,
        "via_p210_d_soc": True,
        "peer_ids_only": True,
    }


def to_siem(*, tenant_id: str, detection_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "detection_ref": detection_ref,
        "via_p210_e_siem": True,
        "peer_ids_only": True,
    }


def to_intel(*, tenant_id: str, intel_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "intel_ref": intel_ref,
        "via_p210_h_intel": True,
        "peer_ids_only": True,
    }


def to_asm(*, tenant_id: str, exposure_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "exposure_ref": exposure_ref,
        "via_p210_i_asm": True,
        "peer_ids_only": True,
    }


def to_knowledge_graph(
    *, tenant_id: str, graph_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "graph_ref": graph_ref,
        "via_knowledge_graph": True,
        "connected_required": True,
        "peer_ids_only": True,
    }


def to_model_lifecycle(
    *, tenant_id: str, model_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai_platform": True,
        "model_lifecycle_management_required": True,
        "peer_ids_only": True,
    }


def to_audit(
    *, tenant_id: str, action: str, resource_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "action": action,
        "resource_ref": resource_ref,
        "via_audit_platform": True,
        "autonomous_actions_audited_required": True,
        "immutable": True,
        "peer_ids_only": True,
    }
