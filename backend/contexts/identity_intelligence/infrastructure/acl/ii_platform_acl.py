"""ACL: Identity Intelligence ↔ platform peers (P207-A)."""
from __future__ import annotations

from typing import Any


def to_ai_infer(*, tenant_id: str, surface: str, context: dict) -> dict[str, Any]:
    return {
        "target": "ai",
        "command": "Infer",
        "payload": {
            "tenant_id": tenant_id,
            "surface": surface,
            "context": dict(context),
        },
        "pattern": "acl",
        "via_ai_platform": True,
        "embeds_llm_sdk_forbidden": True,
        "hitl_required": True,
        "explainable_ai_required": True,
        "chatbot_only_forbidden": True,
    }


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
        "automation_governance_required": True,
        "local_policy_engine_forbidden": True,
    }


def to_authz_check(*, tenant_id: str, subject_id: str, action: str) -> dict[str, Any]:
    return {
        "target": "authorization",
        "command": "Check",
        "payload": {
            "tenant_id": tenant_id,
            "subject_id": subject_id,
            "action": action,
        },
        "local_pdp_forbidden": True,
        "duplicates_authz_pdp_forbidden": True,
    }


def to_digital_twin(*, tenant_id: str, twin_ref: str) -> dict[str, Any]:
    return {
        "target": "identity_digital_twin",
        "command": "ResolveTwin",
        "payload": {"tenant_id": tenant_id, "twin_ref": twin_ref},
        "pattern": "customer_supplier",
        "digital_twin_required": True,
        "duplicates_twin_sor_forbidden": True,
    }


def to_directory_graph(*, tenant_id: str, projection_ref: str) -> dict[str, Any]:
    return {
        "target": "directory",
        "command": "ResolveGraphProjection",
        "payload": {"tenant_id": tenant_id, "projection_ref": projection_ref},
        "pattern": "acl",
        "p205h_graph": True,
        "identity_graph_integration_required": True,
        "duplicates_directory_graph_sor_forbidden": True,
    }


def to_audit(*, tenant_id: str, action: str, resource_ref: str) -> dict[str, Any]:
    return {
        "target": "audit",
        "command": "RecordEntry",
        "payload": {
            "tenant_id": tenant_id,
            "action": action,
            "resource_ref": resource_ref,
        },
        "pattern": "partnership",
        "decision_audit_required": True,
        "explainability_trail": True,
    }


def to_lifecycle(*, tenant_id: str, subject_ref: str) -> dict[str, Any]:
    return {
        "target": "identity_lifecycle",
        "command": "ResolveLifecycleSubject",
        "payload": {"tenant_id": tenant_id, "subject_ref": subject_ref},
        "pattern": "partnership",
        "p201_lifecycle": True,
    }


def to_iga(*, tenant_id: str, subject_ref: str) -> dict[str, Any]:
    return {
        "target": "identity_governance",
        "command": "RecommendCertification",
        "payload": {"tenant_id": tenant_id, "subject_ref": subject_ref},
        "pattern": "partnership",
        "p202_iga": True,
    }


def to_pam(*, tenant_id: str, subject_ref: str) -> dict[str, Any]:
    return {
        "target": "privileged_access",
        "command": "ConsumePrivilegeRisk",
        "payload": {"tenant_id": tenant_id, "subject_ref": subject_ref},
        "pattern": "partnership",
        "p203_pam": True,
    }


def to_am(*, tenant_id: str, subject_ref: str) -> dict[str, Any]:
    return {
        "target": "authentication",
        "command": "SupportAccessDecision",
        "payload": {"tenant_id": tenant_id, "subject_ref": subject_ref},
        "pattern": "partnership",
        "p204_am": True,
    }


def to_observability(
    *, tenant_id: str, metric_name: str, value: float
) -> dict[str, Any]:
    return {
        "target": "observability",
        "command": "EmitMetric",
        "payload": {
            "tenant_id": tenant_id,
            "metric_name": metric_name,
            "value": value,
        },
        "pattern": "acl",
        "local_metrics_store_forbidden": True,
        "via_observability_platform": True,
    }
