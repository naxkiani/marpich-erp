"""ACL: Identity Intelligence Mission ↔ peers (P207-B)."""
from __future__ import annotations

from typing import Any

from contexts.identity_intelligence.infrastructure.acl import ii_platform_acl as base


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    result = base.to_ai_infer(tenant_id=tenant_id, surface=surface, context=context)
    result["mission_governance"] = True
    result["chatbot_only_forbidden"] = True
    return result


def to_policy_evaluate(
    *, tenant_id: str, policy_key: str, context: dict
) -> dict[str, Any]:
    result = base.to_policy_evaluate(
        tenant_id=tenant_id, policy_key=policy_key, context=context
    )
    result["scope_boundary_enforcement"] = True
    return result


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["mission_charter_audit"] = True
    return result


def to_directory(*, tenant_id: str, note: str = "consume_not_replace") -> dict[str, Any]:
    return {
        "target": "directory",
        "command": "ConsumeDirectoryIntelligence",
        "payload": {"tenant_id": tenant_id, "note": note},
        "pattern": "acl",
        "does_not_replace_p205": True,
        "p205_directory": True,
    }


def to_iga(*, tenant_id: str, subject_ref: str) -> dict[str, Any]:
    result = base.to_iga(tenant_id=tenant_id, subject_ref=subject_ref)
    result["does_not_replace_p202"] = True
    return result


def to_am(*, tenant_id: str, subject_ref: str) -> dict[str, Any]:
    result = base.to_am(tenant_id=tenant_id, subject_ref=subject_ref)
    result["does_not_replace_p204"] = True
    return result


def to_pam(*, tenant_id: str, subject_ref: str) -> dict[str, Any]:
    result = base.to_pam(tenant_id=tenant_id, subject_ref=subject_ref)
    result["does_not_replace_p203"] = True
    return result


def to_digital_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    result = base.to_digital_twin(tenant_id=tenant_id, twin_ref=twin_ref)
    result["does_not_replace_twin_sor"] = True
    return result
