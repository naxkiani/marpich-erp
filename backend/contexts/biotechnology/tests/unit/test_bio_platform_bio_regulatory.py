"""P217-N biotechnology bio regulatory foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_bio_regulatory_foundation import validate_bio_regulatory_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_bio_regulatory as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_regulatory_foundation():
    result = validate_bio_regulatory_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-N"
    assert result["adr"] == 513
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_bio_regulatory_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-N"
    assert cat["fabric"] == "meos_bio_regulatory_intelligence_fabric"
    assert cat["foundation_gate"] == "P217"
    assert cat["mission_gate"] == "P217-A"
    assert cat["strategy_gate"] == "P217-B"
    assert cat["domain_gate"] == "P217-C"
    assert cat["infrastructure_gate"] == "P217-D"
    assert cat["bio_ai_gate"] == "P217-E"
    assert cat["synthetic_gate"] == "P217-F"
    assert cat["simulation_gate"] == "P217-G"
    assert cat["digital_health_gate"] == "P217-H"
    assert cat["precision_medicine_gate"] == "P217-I"
    assert cat["clinical_research_gate"] == "P217-J"
    assert cat["drug_discovery_gate"] == "P217-K"
    assert cat["bio_manufacturing_gate"] == "P217-L"
    assert cat["bio_supply_chain_gate"] == "P217-M"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["bio_regulatory_platform_present_required"] is True
    assert cat["regulatory_ai_present_required"] is True
    assert cat["biomedical_compliance_present_required"] is True
    assert cat["life_science_governance_present_required"] is True
    assert cat["architecture"]["layer_count"] == 6
    assert cat["regulatory_ai"]["component_count"] == 4
    assert cat["biomedical_compliance"]["domain_count"] == 4
    assert cat["compliance_ops"]["capability_count"] == 4
    assert cat["regulatory_agents"]["agent_count"] == 6
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 8
    assert cat["never_replace_p217_m_bio_supply_chain"] is True
    assert cat["never_replace_hospital_emr"] is True
    assert cat["never_replace_compliance_platform"] is True
    assert cat["bio_ai_via_p214z_acl_only"] is True
    assert cat["regulatory_twins_via_p217g_acl_only"] is True
    assert cat["manufacturing_compliance_via_p217l_acl_only"] is True
    assert cat["distribution_compliance_via_p217m_acl_only"] is True
    assert cat["drug_regulatory_via_p217k_acl_only"] is True
    assert cat["robotics_via_p216z_acl_only"] is True
    assert cat["quantum_optimization_via_p215z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["never_skip_human_regulatory_oversight"] is True
    assert cat["never_autonomous_regulatory_submission_without_approval"] is True
    assert cat["never_skip_explainable_regulatory_ai"] is True
    assert cat["foundation_for_p217_o"] is True
    assert "GET /biotechnology/bio-regulatory" in mod.bio_regulatory_surface()["routes"]
    assert "autonomous regulatory intelligence" in cat["bio_regulatory_vision"]
@pytest.mark.unit
def test_bio_regulatory_acl():
    from contexts.biotechnology.infrastructure.acl import bio_bio_regulatory_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_bio_supply_chain(tenant_id="t1", supply_ref="s1")["never_replace_p217_m_bio_supply_chain"] is True
    assert acls.to_biotechnology_simulation(tenant_id="t1", simulation_ref="s1")["regulatory_twins_via_p217g_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["bio_ai_via_p214z_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="q1")["quantum_optimization_via_p215z_acl_only"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["robotics_via_p216z_acl_only"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_regulatory_oversight"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_autonomous_regulatory_submission_without_approval"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_explainable_regulatory_ai"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_laboratory(tenant_id="t1", laboratory_ref="l1")["never_replace_laboratory_lims"] is True
    assert acls.to_pharmacy(tenant_id="t1", pharmacy_ref="ph1")["never_replace_pharmacy"] is True
    assert acls.to_compliance(tenant_id="t1", compliance_ref="c1")["never_replace_compliance_platform"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_bio_regulatory():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_bio_regulatory"]["prompt_id"] == "P217-N"
    assert svc.bio_regulatory_readiness()["passed"] is True
