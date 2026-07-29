"""P210-O Cyber Security QA / Validation foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.cyber_security.application.cs_qa_foundation import (
    validate_cs_qa_foundation,
)
from contexts.cyber_security.container import (
    get_cyber_security_service,
    reset_cyber_security_service,
)
from contexts.cyber_security.domain.services import cs_platform_qa as qa

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_cyber_security_service()
    yield
    reset_cyber_security_service()


@pytest.mark.unit
def test_cs_qa_foundation():
    result = validate_cs_qa_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P210-O"
    assert result["adr"] == 375
    assert result["sor"] == "cyber_security"
    assert result["series_complete"] is True
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_cs_qa_catalog():
    cat = qa.catalog()
    assert cat["prompt_id"] == "P210-O"
    assert cat["adr"] == 375
    assert cat["security_testing_automated_required"] is True
    assert cat["adversarial_validation_required"] is True
    assert cat["ai_systems_tested_required"] is True
    assert cat["compliance_verifiable_required"] is True
    assert cat["production_readiness_defined_required"] is True
    assert cat["security_controls_measurable_required"] is True
    assert cat["test_evidence_auditable_required"] is True
    assert cat["series_complete"] is True
    assert cat["architecture"]["layer_count"] >= 8
    assert cat["cursor_outputs"]["count"] >= 20
    assert "security_testing_is_manual_only" in cat["quality_gates"]["reject_if"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /cyber-security/qa" in qa.qa_surface()["routes"]
    assert "GET /cyber-security/qa/readiness" in qa.qa_surface()["routes"]


@pytest.mark.unit
def test_cs_qa_acl():
    from contexts.cyber_security.infrastructure.acl import cs_qa_acl as acls

    assert acls.to_workflow_exercise(tenant_id="t1", exercise_ref="e1")[
        "live_destructive_without_workflow_forbidden"
    ] is True
    assert acls.to_compliance(tenant_id="t1", evidence_ref="ev1")[
        "compliance_verifiable_required"
    ] is True
    assert acls.to_audit(tenant_id="t1", evidence_ref="a1")[
        "test_evidence_auditable_required"
    ] is True
    assert acls.to_gov(tenant_id="t1", model_ref="m1")[
        "ai_systems_tested_required"
    ] is True
    assert acls.to_deploy(tenant_id="t1", pipeline_ref="p1")[
        "security_testing_automated_required"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_qa():
    svc = get_cyber_security_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_qa"]["prompt_id"] == "P210-O"
    assert catalog["platform_qa"]["adr"] == 375
    summary = svc.platform_qa()
    assert summary["prompt_id"] == "P210-O"
    assert "P210-N" in summary["builds_on"]
    assert summary["series_complete"] is True
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
