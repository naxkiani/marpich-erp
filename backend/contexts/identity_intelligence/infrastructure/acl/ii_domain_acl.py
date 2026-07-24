"""ACL: Identity Intelligence Domain ↔ peers (P207-C)."""
from __future__ import annotations

from typing import Any

from contexts.identity_intelligence.infrastructure.acl import ii_platform_acl as base


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    result = base.to_ai_infer(tenant_id=tenant_id, surface=surface, context=context)
    result["domain_reasoning"] = True
    result["chatbot_only_forbidden"] = True
    return result


def to_authz_check(*, tenant_id: str, subject_id: str, action: str) -> dict[str, Any]:
    result = base.to_authz_check(
        tenant_id=tenant_id, subject_id=subject_id, action=action
    )
    result["domain_does_not_own_pdp"] = True
    return result


def to_directory_graph(*, tenant_id: str, projection_ref: str) -> dict[str, Any]:
    result = base.to_directory_graph(
        tenant_id=tenant_id, projection_ref=projection_ref
    )
    result["domain_graph_via_acl"] = True
    return result


def to_digital_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    result = base.to_digital_twin(tenant_id=tenant_id, twin_ref=twin_ref)
    result["domain_twin_orchestration_only"] = True
    return result


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["domain_event_audit"] = True
    return result


def to_lifecycle(*, tenant_id: str, subject_ref: str) -> dict[str, Any]:
    result = base.to_lifecycle(tenant_id=tenant_id, subject_ref=subject_ref)
    result["context_map_partnership"] = True
    return result


def to_iga(*, tenant_id: str, subject_ref: str) -> dict[str, Any]:
    result = base.to_iga(tenant_id=tenant_id, subject_ref=subject_ref)
    result["context_map_partnership"] = True
    return result


def to_policy_evaluate(
    *, tenant_id: str, policy_key: str, context: dict
) -> dict[str, Any]:
    result = base.to_policy_evaluate(
        tenant_id=tenant_id, policy_key=policy_key, context=context
    )
    result["domain_invariant_enforcement"] = True
    return result
