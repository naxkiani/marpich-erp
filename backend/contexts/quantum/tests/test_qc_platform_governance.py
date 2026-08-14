"""P215-K Quantum governance foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.quantum.application.qc_governance_foundation import (
    validate_qc_governance_foundation,
)
from contexts.quantum.container import get_quantum_service, reset_quantum_service
from contexts.quantum.domain.services import qc_platform_governance as gov

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_quantum_service()
    yield
    reset_quantum_service()


@pytest.mark.unit
def test_qc_governance_foundation():
    result = validate_qc_governance_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P215-K"
    assert result["adr"] == 403
    assert result["sor"] == "quantum"
    assert result["capability"] == "CAP-PLT-QC-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_qc_governance_catalog():
    cat = gov.catalog()
    assert cat["prompt_id"] == "P215-K"
    assert cat["adr"] == 403
    assert cat["sor"] == "quantum"
    assert cat["capability"] == "CAP-PLT-QC-001"
    assert cat["quantum_governance_platform_complete_required"] is True
    assert cat["quantum_regulatory_intelligence_present_required"] is True
    assert cat["responsible_quantum_computing_present_required"] is True
    assert cat["quantum_ethics_framework_present_required"] is True
    assert cat["quantum_risk_management_present_required"] is True
    assert cat["quantum_compliance_automation_present_required"] is True
    assert cat["quantum_audit_intelligence_present_required"] is True
    assert cat["accountability_framework_present_required"] is True
    assert cat["knowledge_graph_integration_present_required"] is True
    assert cat["digital_twin_integration_present_required"] is True
    assert cat["cqrs_architecture_present_required"] is True
    assert cat["event_architecture_present_required"] is True
    assert cat["microservices_architecture_present_required"] is True
    assert cat["api_first_architecture_present_required"] is True
    assert cat["cloud_native_governance_present_required"] is True
    assert cat["governance_platform"]["bc_count"] >= 7
    assert cat["policy_management"]["category_count"] >= 6
    assert cat["risk_management"]["risk_type_count"] >= 6
    assert cat["microservices"]["service_count"] >= 11
    assert cat["cqrs"]["event_count"] >= 6
    assert cat["cursor_outputs"]["count"] >= 16
    assert cat["policy_management"]["via_policy_engine"] is True
    assert (
        "quantum_governance_platform_is_incomplete"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert cat["fabric"] == "meos_quantum_responsible_intelligence_fabric"
    assert cat["builds_on_p215_a_through_j"] is True
    assert "P214-H" in cat["builds_on"]
    assert "P214-Y" in cat["builds_on"]
    assert "P215-J" in cat["builds_on"]
    assert "GET /quantum/governance" in gov.governance_surface()["routes"]
    assert (
        "GET /quantum/governance/readiness"
        in gov.governance_surface()["routes"]
    )


@pytest.mark.unit
def test_qc_governance_acl():
    from contexts.quantum.infrastructure.acl import qc_governance_acl as acls

    assert acls.to_secrets(tenant_id="t1", key_ref="k1")[
        "pqc_remains_secrets"
    ] is True
    assert acls.to_cyber_security(tenant_id="t1", signal_ref="s1")[
        "via_p210"
    ] is True
    assert acls.to_data_governance(tenant_id="t1", asset_ref="a1")[
        "via_p212"
    ] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")[
        "module_local_pdp_forbidden"
    ] is True
    assert acls.to_audit(tenant_id="t1", entry_ref="e1")[
        "via_audit"
    ] is True
    assert acls.to_ai_governance(tenant_id="t1", ethics_ref="eth1")[
        "via_ai_governance"
    ] is True
    assert acls.to_workflow(tenant_id="t1", oversight_ref="o1")[
        "human_oversight_required"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="approve_usage"
    )["via_p208"] is True
    assert acls.to_responsible_ai_governance(tenant_id="t1", governance_ref="rai1")["via_p214_h"] is True
    assert acls.to_ai_ethics_civilization(tenant_id="t1", ethics_ref="civ1")["via_p214_y"] is True
    assert acls.to_foundation(tenant_id="t1", foundation_ref="f1")["via_p215_a"] is True
    assert acls.to_quantum_network(tenant_id="t1", network_ref="n1")["via_p215_j"] is True
    assert acls.to_enterprise_quantum(tenant_id="t1", governance_ref="g1")["module_local_quantum_governance_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_governance():
    svc = get_quantum_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_governance"]["prompt_id"] == "P215-K"
    assert catalog["platform_governance"]["adr"] == 403
    assert catalog["sor"] == "quantum"
    summary = svc.platform_governance()
    assert summary["prompt_id"] == "P215-K"
    assert summary["capability"] == "CAP-PLT-QC-001"
    assert "P209" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.governance_readiness()["passed"] is True
