"""P217-M biotechnology bio supply chain foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_bio_supply_chain_foundation import validate_bio_supply_chain_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_bio_supply_chain as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_bio_supply_chain_foundation():
    result = validate_bio_supply_chain_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-M"
    assert result["adr"] == 512
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_bio_supply_chain_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-M"
    assert cat["fabric"] == "meos_bio_supply_chain_intelligence_fabric"
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
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["bio_supply_chain_platform_present_required"] is True
    assert cat["bio_logistics_present_required"] is True
    assert cat["cold_chain_intelligence_present_required"] is True
    assert cat["inventory_intelligence_present_required"] is True
    assert cat["architecture"]["layer_count"] == 6
    assert cat["bio_logistics"]["capability_count"] == 4
    assert cat["cold_chain"]["domain_count"] == 4
    assert cat["bio_inventory"]["category_count"] == 4
    assert cat["supply_ai"]["engine_count"] == 4
    assert cat["supply_agents"]["agent_count"] == 6
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 8
    assert cat["never_replace_p217_l_bio_manufacturing"] is True
    assert cat["never_replace_hospital_emr"] is True
    assert cat["never_replace_inventory"] is True
    assert cat["bio_ai_via_p214z_acl_only"] is True
    assert cat["supply_twins_via_p217g_acl_only"] is True
    assert cat["manufacturing_via_p217l_acl_only"] is True
    assert cat["product_intelligence_via_p217k_acl_only"] is True
    assert cat["robotics_via_p216z_acl_only"] is True
    assert cat["quantum_optimization_via_p215z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["never_skip_cold_chain_integrity"] is True
    assert cat["never_skip_human_logistics_oversight"] is True
    assert cat["never_untraceable_biological_material_movement"] is True
    assert cat["foundation_for_p217_n"] is True
    assert "GET /biotechnology/bio-supply-chain" in mod.bio_supply_chain_surface()["routes"]
    assert "self-optimizing biological supply" in cat["bio_supply_vision"]
@pytest.mark.unit
def test_bio_supply_chain_acl():
    from contexts.biotechnology.infrastructure.acl import bio_bio_supply_chain_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_bio_manufacturing(tenant_id="t1", manufacturing_ref="m1")["never_replace_p217_l_bio_manufacturing"] is True
    assert acls.to_biotechnology_simulation(tenant_id="t1", simulation_ref="s1")["supply_twins_via_p217g_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["bio_ai_via_p214z_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="q1")["quantum_optimization_via_p215z_acl_only"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["robotics_via_p216z_acl_only"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_cold_chain_integrity"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_logistics_oversight"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_untraceable_biological_material_movement"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_laboratory(tenant_id="t1", laboratory_ref="l1")["never_replace_laboratory_lims"] is True
    assert acls.to_pharmacy(tenant_id="t1", pharmacy_ref="ph1")["never_replace_pharmacy"] is True
    assert acls.to_inventory(tenant_id="t1", inventory_ref="inv1")["never_replace_inventory"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_bio_supply_chain():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_bio_supply_chain"]["prompt_id"] == "P217-M"
    assert svc.bio_supply_chain_readiness()["passed"] is True
