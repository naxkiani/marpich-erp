"""ACL: Data Security strategy ↔ peers (P211-A)."""
from __future__ import annotations

from typing import Any


def to_consent(*, tenant_id: str, subject_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "subject_ref": subject_ref,
        "via_consent": True,
        "consent_ledger_owned_by_consent": True,
        "peer_ids_only": True,
    }


def to_secrets(*, tenant_id: str, key_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "key_ref": key_ref,
        "via_p209": True,
        "crypto_owned_by_secrets": True,
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
        "data_access_governed_required": True,
        "peer_ids_only": True,
    }


def to_cyber_security(
    *, tenant_id: str, signal_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "signal_ref": signal_ref,
        "via_p210": True,
        "threat_defense_owned_by_cyber_security": True,
        "peer_ids_only": True,
    }


def to_compliance(
    *, tenant_id: str, evidence_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "evidence_ref": evidence_ref,
        "via_compliance_framework": True,
        "compliance_evidence_generatable_required": True,
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


def to_enterprise_ai(
    *, tenant_id: str, model_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai": True,
        "module_local_llm_sdk_forbidden": True,
        "ai_data_protected_required": True,
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
