"""P217-L biotechnology bio manufacturing foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_bio_manufacturing_foundation import validate_bio_manufacturing_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_bio_manufacturing as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_manufacturing_foundation():
    result = validate_bio_manufacturing_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-L"
    assert result["adr"] == 511
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_bio_manufacturing_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-L"
    assert cat["fabric"] == "meos_bio_manufacturing_intelligence_fabric"
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
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["biomedical_manufacturing_platform_present_required"] is True
    assert cat["smart_bio_factory_present_required"] is True
    assert cat["bio_production_automation_present_required"] is True
    assert cat["manufacturing_ai_present_required"] is True
    assert cat["architecture"]["layer_count"] == 6
    assert cat["bio_pos"]["component_count"] == 4
    assert cat["biopharma"]["domain_count"] == 4
    assert cat["automation"]["domain_count"] == 4
    assert cat["manufacturing_ai"]["engine_count"] == 4
    assert cat["manufacturing_agents"]["agent_count"] == 6
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 8
    assert cat["never_replace_p217_k_drug_discovery"] is True
    assert cat["never_replace_hospital_emr"] is True
    assert cat["bio_ai_via_p214z_acl_only"] is True
    assert cat["manufacturing_twins_via_p217g_acl_only"] is True
    assert cat["product_intelligence_via_p217k_acl_only"] is True
    assert cat["robotics_via_p216z_acl_only"] is True
    assert cat["quantum_optimization_via_p215z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["never_skip_gmp_compliance"] is True
    assert cat["never_skip_human_manufacturing_oversight"] is True
    assert cat["never_autonomous_release_without_quality_approval"] is True
    assert cat["foundation_for_p217_m"] is True
    assert "GET /biotechnology/bio-manufacturing" in mod.bio_manufacturing_surface()["routes"]
    assert "Smart Bio Factory" in cat["bio_manufacturing_vision"]
@pytest.mark.unit
def test_bio_manufacturing_acl():
    from contexts.biotechnology.infrastructure.acl import bio_bio_manufacturing_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_drug_discovery(tenant_id="t1", drug_discovery_ref="dd1")["never_replace_p217_k_drug_discovery"] is True
    assert acls.to_biotechnology_simulation(tenant_id="t1", simulation_ref="s1")["manufacturing_twins_via_p217g_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["bio_ai_via_p214z_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="q1")["quantum_optimization_via_p215z_acl_only"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["robotics_via_p216z_acl_only"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_gmp_compliance"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_manufacturing_oversight"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_autonomous_release_without_quality_approval"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_laboratory(tenant_id="t1", laboratory_ref="l1")["never_replace_laboratory_lims"] is True
    assert acls.to_pharmacy(tenant_id="t1", pharmacy_ref="ph1")["never_replace_pharmacy"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_bio_manufacturing():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_bio_manufacturing"]["prompt_id"] == "P217-L"
    assert svc.bio_manufacturing_readiness()["passed"] is True
