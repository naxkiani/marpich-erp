"""P212-O Data Governance QA foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.data_governance.application.dg_qa_foundation import (
    validate_dg_qa_foundation,
)
from contexts.data_governance.container import (
    get_data_governance_service,
    reset_data_governance_service,
)
from contexts.data_governance.domain.services import dg_platform_qa as qa

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_data_governance_service()
    yield
    reset_data_governance_service()


@pytest.mark.unit
def test_dg_qa_foundation():
    result = validate_dg_qa_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P212-O"
    assert result["adr"] == 407
    assert result["sor"] == "data_governance"
    assert result["capability"] == "CAP-PLT-DG-001"
    assert result["series_complete"] is True
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_dg_qa_catalog():
    cat = qa.catalog()
    assert cat["prompt_id"] == "P212-O"
    assert cat["adr"] == 407
    assert cat["sor"] == "data_governance"
    assert cat["capability"] == "CAP-PLT-DG-001"
    assert cat["complete_enterprise_testing_architecture_present_required"] is True
    assert cat["governance_validation_platform_present_required"] is True
    assert cat["compliance_automation_present_required"] is True
    assert cat["security_assurance_present_required"] is True
    assert cat["definition_of_done_engine_present_required"] is True
    assert cat["ai_quality_intelligence_present_required"] is True
    assert cat["knowledge_graph_integration_present_required"] is True
    assert cat["digital_twin_integration_present_required"] is True
    assert cat["cqrs_architecture_present_required"] is True
    assert cat["event_sourcing_architecture_present_required"] is True
    assert cat["microservices_architecture_present_required"] is True
    assert cat["api_first_architecture_present_required"] is True
    assert cat["continuous_governance_present_required"] is True
    assert cat["testing_architecture"]["layer_count"] >= 6
    assert cat["governance_validation"]["bc_count"] >= 5
    assert cat["ai_quality_intelligence"]["agent_count"] >= 5
    assert cat["event_sourcing"]["event_count"] >= 6
    assert cat["microservices"]["service_count"] >= 7
    assert cat["cursor_outputs"]["count"] >= 19
    assert cat["compliance_automation"]["via_compliance_framework"] is True
    assert cat["knowledge_graph_integration"]["via_p212_j"] is True
    assert cat["digital_twin_integration"]["via_p212_l"] is True
    assert cat["deployment_validation"]["via_p212_n"] is True
    assert cat["api_first"]["via_api_gateway"] is True
    assert (
        "complete_enterprise_testing_architecture_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert cat["production_readiness"]["checklist"]["p212_series_complete"] is True
    assert "GET /data-governance/qa" in qa.qa_surface()["routes"]
    assert "GET /data-governance/qa/readiness" in qa.qa_surface()["routes"]


@pytest.mark.unit
def test_dg_qa_acl():
    from contexts.data_governance.infrastructure.acl import dg_qa_acl as acls

    assert acls.to_compliance(tenant_id="t1", control_ref="c1")[
        "via_compliance_framework"
    ] is True
    assert acls.to_audit(tenant_id="t1", evidence_ref="e1")[
        "via_audit_platform"
    ] is True
    assert acls.to_graph(tenant_id="t1", entity_ref="g1")["via_p212_j"] is True
    assert acls.to_twin(tenant_id="t1", twin_ref="tw1")["via_p212_l"] is True
    assert acls.to_deploy(tenant_id="t1", deploy_ref="d1")["via_p212_n"] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="validate"
    )["via_p208"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "via_enterprise_ai"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_qa():
    svc = get_data_governance_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_qa"]["prompt_id"] == "P212-O"
    assert catalog["platform_qa"]["adr"] == 407
    assert catalog["sor"] == "data_governance"
    summary = svc.platform_qa()
    assert summary["prompt_id"] == "P212-O"
    assert summary["capability"] == "CAP-PLT-DG-001"
    assert "P212-N" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert summary["production_readiness"]["checklist"]["p212_series_complete"] is True
    assert svc.qa_readiness()["passed"] is True
