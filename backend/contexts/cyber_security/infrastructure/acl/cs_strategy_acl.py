"""ACL: Cyber Security strategy ↔ peers (P210-A)."""
from __future__ import annotations

from typing import Any


def to_security_incident(*, tenant_id: str, detection_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "detection_ref": detection_ref,
        "via_security_incident": True,
        "ir_lifecycle_owned_by_security_incident": True,
        "peer_ids_only": True,
    }


def to_integration_connector(
    *, tenant_id: str, connector_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "connector_ref": connector_ref,
        "via_integration_platform": True,
        "vendor_sdk_embed_forbidden": True,
        "peer_ids_only": True,
    }


def to_authorization(
    *, tenant_id: str, principal_ref: str, action: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "principal_ref": principal_ref,
        "action": action,
        "via_authorization": True,
        "zero_trust": True,
        "peer_ids_only": True,
    }


def to_workflow_automation(
    *, tenant_id: str, playbook_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "playbook_ref": playbook_ref,
        "via_workflow": True,
        "manual_only_forbidden": True,
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
        "immutable": True,
        "peer_ids_only": True,
    }


def to_ai_security(
    *, tenant_id: str, surface_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "surface_ref": surface_ref,
        "via_ai_platform": True,
        "ai_security_required": True,
        "advisor_not_authority": True,
        "peer_ids_only": True,
    }


def to_observability_signal(
    *, tenant_id: str, signal_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "signal_ref": signal_ref,
        "observability_is_not_cyber_sor": True,
        "peer_ids_only": True,
    }


def to_secrets_crypto_trust(
    *, tenant_id: str, trust_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "trust_ref": trust_ref,
        "via_secrets": True,
        "crypto_owned_by_secrets": True,
        "peer_ids_only": True,
    }
