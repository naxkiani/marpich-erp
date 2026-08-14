"""P217-K biotechnology drug discovery foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_drug_discovery_foundation import validate_drug_discovery_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_drug_discovery as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_drug_discovery_foundation():
    result = validate_drug_discovery_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-K"
    assert result["adr"] == 510
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_drug_discovery_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-K"
    assert cat["fabric"] == "meos_drug_intelligence_fabric"
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
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["drug_discovery_platform_present_required"] is True
    assert cat["ai_drug_design_present_required"] is True
    assert cat["molecular_discovery_present_required"] is True
    assert cat["pharmaceutical_intelligence_present_required"] is True
    assert cat["architecture"]["layer_count"] == 6
    assert cat["ai_drug_design"]["component_count"] == 4
    assert cat["molecular_discovery"]["capability_count"] == 4
    assert cat["computational_drug"]["engine_count"] == 4
    assert cat["drug_agents"]["agent_count"] == 6
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 8
    assert cat["never_replace_p217_j_clinical_research"] is True
    assert cat["never_replace_hospital_emr"] is True
    assert cat["bio_ai_via_p214z_acl_only"] is True
    assert cat["drug_twins_via_p217g_acl_only"] is True
    assert cat["quantum_molecular_via_p215z_acl_only"] is True
    assert cat["lab_execution_via_p216z_acl_only"] is True
    assert cat["clinical_translation_via_p217j_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["never_unvalidated_therapeutic_candidate_release"] is True
    assert cat["never_skip_human_scientific_oversight"] is True
    assert cat["foundation_for_p217_l"] is True
    assert "GET /biotechnology/drug-discovery" in mod.drug_discovery_surface()["routes"]
    assert "autonomous drug innovation" in cat["drug_discovery_vision"]
@pytest.mark.unit
def test_drug_discovery_acl():
    from contexts.biotechnology.infrastructure.acl import bio_drug_discovery_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_clinical_research(tenant_id="t1", clinical_research_ref="cr1")["never_replace_p217_j_clinical_research"] is True
    assert acls.to_biotechnology_simulation(tenant_id="t1", simulation_ref="s1")["drug_twins_via_p217g_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["bio_ai_via_p214z_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="q1")["quantum_molecular_via_p215z_acl_only"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["lab_execution_via_p216z_acl_only"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_unvalidated_therapeutic_candidate_release"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_scientific_oversight"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_laboratory(tenant_id="t1", laboratory_ref="l1")["never_replace_laboratory_lims"] is True
    assert acls.to_pharmacy(tenant_id="t1", pharmacy_ref="ph1")["never_replace_pharmacy"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_drug_discovery():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_drug_discovery"]["prompt_id"] == "P217-K"
    assert svc.drug_discovery_readiness()["passed"] is True
