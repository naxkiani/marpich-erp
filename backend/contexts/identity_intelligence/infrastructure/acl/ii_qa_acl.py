"""ACL: QA & Governance ↔ platform peers (P207-O)."""
from __future__ import annotations

from typing import Any

from contexts.identity_intelligence.infrastructure.acl import ii_platform_acl as base


def to_compliance(
    *, tenant_id: str, pack_ref: str, frameworks: list[str]
) -> dict[str, Any]:
    return {
        "target": "compliance",
        "command": "CollectEvidence",
        "payload": {
            "tenant_id": tenant_id,
            "pack_ref": pack_ref,
            "frameworks": list(frameworks),
        },
        "pattern": "acl",
        "local_compliance_store_forbidden": True,
        "via_compliance_platform": True,
        "evidence_required": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    result = base.to_audit(
        tenant_id=tenant_id, action=action, resource_ref=resource_ref
    )
    result["qa_governance_audit"] = True
    result["traceability_required"] = True
    return result


def to_policy_evaluate(
    *, tenant_id: str, policy_key: str, context: dict
) -> dict[str, Any]:
    return {
        "target": "policy",
        "command": "EvaluatePolicy",
        "payload": {
            "tenant_id": tenant_id,
            "policy_key": policy_key,
            "context": dict(context),
        },
        "pattern": "customer_supplier",
        "policy_validation": True,
        "local_policy_engine_forbidden": True,
    }


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    result = base.to_ai_infer(tenant_id=tenant_id, surface=surface, context=context)
    result["ai_validation"] = True
    result["hitl_required"] = True
    result["embeds_llm_sdk_forbidden"] = True
    return result


def to_observability(
    *, tenant_id: str, metric_name: str, value: float
) -> dict[str, Any]:
    result = base.to_observability(
        tenant_id=tenant_id, metric_name=metric_name, value=value
    )
    result["continuous_assurance_metrics"] = True
    return result


def to_ops_readiness(*, tenant_id: str, review_ref: str) -> dict[str, Any]:
    return {
        "target": "identity_intelligence.ops",
        "command": "ResolveOpsReadiness",
        "payload": {"tenant_id": tenant_id, "review_ref": review_ref},
        "pattern": "internal",
        "via_p207n": True,
        "production_readiness_evidence": True,
    }
