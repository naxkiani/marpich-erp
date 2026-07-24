"""ACL: Secrets Deploy / DevSecOps / K8s / Observability ↔ peers (P209-N)."""
from __future__ import annotations

from typing import Any

from contexts.secrets.infrastructure.acl import secrets_acl as base


def to_observability(*, tenant_id: str, service_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "service_ref": service_ref,
        "via_observability_platform": True,
        "observability_present_required": True,
        "otel": True,
        "peer_ids_only": True,
    }


def to_workflow_deploy_approval(
    *, tenant_id: str, deploy_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "deploy_ref": deploy_ref,
        "via_workflow": True,
        "deployment_approval_required": True,
        "iac_managed_required": True,
        "peer_ids_only": True,
    }


def to_authorization_deploy(
    *, tenant_id: str, principal_ref: str, action: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "principal_ref": principal_ref,
        "action": action,
        "via_authorization": True,
        "zero_trust_operations": True,
        "peer_ids_only": True,
    }


def to_signing_sbom(*, tenant_id: str, artifact_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "artifact_ref": artifact_ref,
        "via_signing": True,
        "sbom_required": True,
        "cicd_security_validation_required": True,
        "peer_ids_only": True,
    }


def to_ai_ops_infer(
    *, tenant_id: str, surface: str, context: dict
) -> dict[str, Any]:
    result = base.to_ai_infer(
        tenant_id=tenant_id, surface=surface, context=context
    )
    result["via_ai_platform"] = True
    result["advisor_not_authority"] = True
    return result


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["deployment_automated_required"] = True
    result["infrastructure_changes_managed_required"] = True
    return result


def acl_catalog() -> dict[str, Any]:
    return {
        "targets": [
            "observability",
            "workflow",
            "authorization",
            "signing",
            "ai",
            "audit",
        ],
        "deployment_automated_required": True,
        "observability_present_required": True,
        "cicd_security_validation_required": True,
        "via_observability_platform": True,
        "via_signing": True,
    }
