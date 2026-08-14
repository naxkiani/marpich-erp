"""ACL: Cyber Security Deploy / DevSecOps ↔ peers (P210-N)."""
from __future__ import annotations

from typing import Any


def to_enterprise_observability(
    *, tenant_id: str, service_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "service_ref": service_ref,
        "via_enterprise_observability": True,
        "observability_required": True,
        "module_local_observability_stack_forbidden": True,
        "peer_ids_only": True,
    }


def to_workflow_promotion(
    *, tenant_id: str, env_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "env_ref": env_ref,
        "via_workflow": True,
        "deployment_approval_required": True,
        "peer_ids_only": True,
    }


def to_p209_secrets(
    *, tenant_id: str, secret_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "secret_ref": secret_ref,
        "via_p209": True,
        "image_signing_required": True,
        "peer_ids_only": True,
    }


def to_policy_engine(
    *, tenant_id: str, policy_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_policy_engine": True,
        "policy_as_code": True,
        "peer_ids_only": True,
    }


def to_siem(*, tenant_id: str, event_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "event_ref": event_ref,
        "via_p210_e_siem": True,
        "security_controls_integrated_required": True,
        "peer_ids_only": True,
    }


def to_soar(*, tenant_id: str, playbook_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "playbook_ref": playbook_ref,
        "via_p210_f_soar": True,
        "peer_ids_only": True,
    }


def to_xdr(*, tenant_id: str, detection_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "detection_ref": detection_ref,
        "via_p210_g_xdr": True,
        "peer_ids_only": True,
    }


def to_ai_ops(*, tenant_id: str, signal_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "signal_ref": signal_ref,
        "via_p210_j_ai_ops": True,
        "peer_ids_only": True,
    }


def to_gov(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_p210_m_gov": True,
        "peer_ids_only": True,
    }
