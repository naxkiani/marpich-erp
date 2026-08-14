"""ACL: Cyber Security AI Governance ↔ peers (P210-M)."""
from __future__ import annotations

from typing import Any


def to_enterprise_ai(
    *, tenant_id: str, model_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_enterprise_ai_platform": True,
        "module_local_llm_sdk_forbidden": True,
        "ai_models_inventoried_required": True,
        "peer_ids_only": True,
    }


def to_policy_engine(
    *, tenant_id: str, policy_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "policy_ref": policy_ref,
        "via_policy_engine": True,
        "policies_enforceable_required": True,
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
    *, tenant_id: str, decision_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "decision_ref": decision_ref,
        "via_audit_platform": True,
        "ai_decisions_auditable_required": True,
        "immutable": True,
        "peer_ids_only": True,
    }


def to_authorization(
    *, tenant_id: str, agent_ref: str, action: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "agent_ref": agent_ref,
        "action": action,
        "via_authorization": True,
        "ai_agents_governed_required": True,
        "peer_ids_only": True,
    }


def to_ai_ops(*, tenant_id: str, agent_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "agent_ref": agent_ref,
        "via_p210_j_ai_ops": True,
        "peer_ids_only": True,
    }


def to_graph(*, tenant_id: str, graph_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "graph_ref": graph_ref,
        "via_p210_k": True,
        "peer_ids_only": True,
    }
