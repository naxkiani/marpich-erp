"""ACL: Cyber Security QA / Validation ↔ peers (P210-O)."""
from __future__ import annotations

from typing import Any


def to_workflow_exercise(
    *, tenant_id: str, exercise_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "exercise_ref": exercise_ref,
        "via_workflow": True,
        "adversarial_validation_required": True,
        "live_destructive_without_workflow_forbidden": True,
        "peer_ids_only": True,
    }


def to_compliance(
    *, tenant_id: str, evidence_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "evidence_ref": evidence_ref,
        "via_compliance_framework": True,
        "compliance_verifiable_required": True,
        "peer_ids_only": True,
    }


def to_audit(
    *, tenant_id: str, evidence_ref: str
) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "evidence_ref": evidence_ref,
        "via_audit_platform": True,
        "test_evidence_auditable_required": True,
        "immutable": True,
        "peer_ids_only": True,
    }


def to_gov(*, tenant_id: str, model_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "model_ref": model_ref,
        "via_p210_m_gov": True,
        "ai_systems_tested_required": True,
        "peer_ids_only": True,
    }


def to_deploy(*, tenant_id: str, pipeline_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "pipeline_ref": pipeline_ref,
        "via_p210_n_deploy": True,
        "security_testing_automated_required": True,
        "peer_ids_only": True,
    }


def to_siem(*, tenant_id: str, detection_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "detection_ref": detection_ref,
        "via_p210_e_siem": True,
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


def to_graph(*, tenant_id: str, graph_ref: str) -> dict[str, Any]:
    return {
        "tenant_id": tenant_id,
        "graph_ref": graph_ref,
        "via_p210_k": True,
        "peer_ids_only": True,
    }
