"""ACL: Data Security deploy/DevSecOps ↔ peers (P211-O)."""
from __future__ import annotations

from typing import Any


def to_observability(*, tenant_id: str, service_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "service_ref": service_ref,
        "via_observability_platform": True,
        "monitoring_complete_required": True,
        "module_local_metrics_store_forbidden": True,
        "peer_ids_only": True,
    }


def to_secrets_signing(*, tenant_id: str, image_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "image_ref": image_ref,
        "via_p209": True,
        "security_scanning_present_required": True,
        "runtime_security_present_required": True,
        "signed_images_required": True,
        "peer_ids_only": True,
    }


def to_cyber_security(
    *, tenant_id: str, signal_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "signal_ref": signal_ref,
        "via_p210_siem": True,
        "via_p210_soar": True,
        "via_p210_xdr": True,
        "peer_ids_only": True,
    }


def to_gitops(*, tenant_id: str, env_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "env_ref": env_ref,
        "via_gitops": True,
        "deployment_automated_required": True,
        "peer_ids_only": True,
    }


def to_api_gateway(*, tenant_id: str, route_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "route_ref": route_ref,
        "via_api_gateway": True,
        "peer_ids_only": True,
    }


def to_enterprise_ai(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai_aiops": True,
        "peer_ids_only": True,
    }


def to_ops(*, tenant_id: str, fabric_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "fabric_ref": fabric_ref,
        "via_p211_n": True,
        "infrastructure_scalable_required": True,
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


def to_dr(*, tenant_id: str, plan_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "plan_ref": plan_ref,
        "disaster_recovery_defined_required": True,
        "peer_ids_only": True,
    }
