"""P217-J biotechnology clinical research foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_clinical_research_foundation import validate_clinical_research_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_clinical_research as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_clinical_research_foundation():
    result = validate_clinical_research_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-J"
    assert result["adr"] == 509
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_clinical_research_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-J"
    assert cat["fabric"] == "meos_clinical_innovation_intelligence_fabric"
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
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["clinical_research_platform_present_required"] is True
    assert cat["ai_clinical_trials_present_required"] is True
    assert cat["scientific_discovery_intelligence_present_required"] is True
    assert cat["research_automation_present_required"] is True
    assert cat["architecture"]["layer_count"] == 6
    assert cat["ai_clinical_trials"]["component_count"] == 5
    assert cat["scientific_discovery"]["capability_count"] == 4
    assert cat["research_automation"]["domain_count"] == 4
    assert cat["research_agents"]["agent_count"] == 6
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 8
    assert cat["never_replace_p217_i_precision_medicine"] is True
    assert cat["never_replace_hospital_emr"] is True
    assert cat["bio_ai_via_p214z_acl_only"] is True
    assert cat["trial_simulation_via_p217g_acl_only"] is True
    assert cat["lab_automation_via_p216z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["never_autonomous_clinical_trial_without_ethics_approval"] is True
    assert cat["never_skip_human_researcher_oversight"] is True
    assert cat["foundation_for_p217_k"] is True
    assert "GET /biotechnology/clinical-research" in mod.clinical_research_surface()["routes"]
    assert "AI accelerated discovery" in cat["clinical_research_vision"]
@pytest.mark.unit
def test_clinical_research_acl():
    from contexts.biotechnology.infrastructure.acl import bio_clinical_research_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_precision_medicine(tenant_id="t1", precision_ref="p1")["never_replace_p217_i_precision_medicine"] is True
    assert acls.to_biotechnology_simulation(tenant_id="t1", simulation_ref="s1")["trial_simulation_via_p217g_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["bio_ai_via_p214z_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["lab_automation_via_p216z_acl_only"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_autonomous_clinical_trial_without_ethics_approval"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_researcher_oversight"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_laboratory(tenant_id="t1", laboratory_ref="l1")["never_replace_laboratory_lims"] is True
    assert acls.to_pharmacy(tenant_id="t1", pharmacy_ref="ph1")["never_replace_pharmacy"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_clinical_research():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_clinical_research"]["prompt_id"] == "P217-J"
    assert svc.clinical_research_readiness()["passed"] is True
