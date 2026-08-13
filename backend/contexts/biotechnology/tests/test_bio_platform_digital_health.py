"""P217-H biotechnology digital health foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_digital_health_foundation import validate_digital_health_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_digital_health as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_digital_health_foundation():
    result = validate_digital_health_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-H"
    assert result["adr"] == 507
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_digital_health_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-H"
    assert cat["fabric"] == "meos_digital_health_intelligence_fabric"
    assert cat["foundation_gate"] == "P217"
    assert cat["mission_gate"] == "P217-A"
    assert cat["strategy_gate"] == "P217-B"
    assert cat["domain_gate"] == "P217-C"
    assert cat["infrastructure_gate"] == "P217-D"
    assert cat["bio_ai_gate"] == "P217-E"
    assert cat["synthetic_gate"] == "P217-F"
    assert cat["simulation_gate"] == "P217-G"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["digital_health_platform_present_required"] is True
    assert cat["healthcare_ai_present_required"] is True
    assert cat["predictive_medicine_present_required"] is True
    assert cat["patient_intelligence_present_required"] is True
    assert cat["architecture"]["layer_count"] == 6
    assert cat["healthcare_ai"]["component_count"] == 5
    assert cat["predictive_medicine"]["capability_count"] == 4
    assert cat["patient_intelligence"]["component_count"] == 4
    assert cat["health_digital_twin"]["type_count"] == 3
    assert cat["health_agents"]["agent_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 8
    assert cat["never_replace_p217_g_simulation"] is True
    assert cat["never_replace_hospital_emr"] is True
    assert cat["bio_ai_via_p214z_acl_only"] is True
    assert cat["health_twins_via_p217g_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["never_autonomous_clinical_action_without_physician"] is True
    assert cat["foundation_for_p217_i"] is True
    assert "GET /biotechnology/digital-health" in mod.digital_health_surface()["routes"]
    assert "proactive, predictive and personalized" in cat["digital_health_vision"]
@pytest.mark.unit
def test_digital_health_acl():
    from contexts.biotechnology.infrastructure.acl import bio_digital_health_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_simulation(tenant_id="t1", simulation_ref="s1")["never_replace_p217_g_simulation"] is True
    assert acls.to_biotechnology_simulation(tenant_id="t1", simulation_ref="s1")["health_twins_via_p217g_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["bio_ai_via_p214z_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_autonomous_clinical_action_without_physician"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_laboratory(tenant_id="t1", laboratory_ref="l1")["never_replace_laboratory_lims"] is True
    assert acls.to_pharmacy(tenant_id="t1", pharmacy_ref="p1")["never_replace_pharmacy"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_digital_health():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_digital_health"]["prompt_id"] == "P217-H"
    assert svc.digital_health_readiness()["passed"] is True
