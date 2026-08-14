"""P217-G biotechnology simulation foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.biotechnology.application.bio_simulation_foundation import validate_simulation_foundation
from contexts.biotechnology.container import get_biotechnology_service, reset_biotechnology_service
from contexts.biotechnology.domain.services import bio_platform_simulation as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_biotechnology_service(); yield; reset_biotechnology_service()
@pytest.mark.unit
def test_simulation_foundation():
    result = validate_simulation_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P217-G"
    assert result["adr"] == 506
    assert result["sor"] == "biotechnology"
    assert result["capability"] == "CAP-PLT-BIO-001"
@pytest.mark.unit
def test_simulation_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P217-G"
    assert cat["fabric"] == "meos_biological_simulation_intelligence_fabric"
    assert cat["foundation_gate"] == "P217"
    assert cat["mission_gate"] == "P217-A"
    assert cat["strategy_gate"] == "P217-B"
    assert cat["domain_gate"] == "P217-C"
    assert cat["infrastructure_gate"] == "P217-D"
    assert cat["bio_ai_gate"] == "P217-E"
    assert cat["synthetic_gate"] == "P217-F"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["bio_simulation_platform_present_required"] is True
    assert cat["digital_twin_architecture_present_required"] is True
    assert cat["computational_simulation_engine_present_required"] is True
    assert cat["life_modeling_framework_present_required"] is True
    assert cat["architecture"]["layer_count"] == 6
    assert cat["digital_twins"]["domain_count"] == 5
    assert cat["simulation_engine"]["component_count"] == 5
    assert cat["life_modeling"]["level_count"] == 5
    assert cat["simulation_intelligence"]["capability_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 8
    assert cat["never_replace_p217_f_synthetic"] is True
    assert cat["bio_ai_via_p214z_acl_only"] is True
    assert cat["quantum_simulation_via_p215z_acl_only"] is True
    assert cat["physical_validation_via_p216z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["never_unvalidated_simulation_claims"] is True
    assert cat["foundation_for_p217_h"] is True
    assert "GET /biotechnology/simulation" in mod.simulation_surface()["routes"]
    assert "intelligent digital representation" in cat["simulation_vision"]
@pytest.mark.unit
def test_simulation_acl():
    from contexts.biotechnology.infrastructure.acl import bio_simulation_acl as acls
    assert acls.to_biotechnology_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p217_foundation"] is True
    assert acls.to_biotechnology_synthetic(tenant_id="t1", synthetic_ref="s1")["never_replace_p217_f_synthetic"] is True
    assert acls.to_biotechnology_bio_ai(tenant_id="t1", bio_ai_ref="b1")["never_replace_p217_e_bio_ai"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["bio_ai_via_p214z_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["quantum_simulation_via_p215z_acl_only"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["physical_validation_via_p216z_acl_only"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_unvalidated_simulation_claims"] is True
    assert acls.to_hospital(tenant_id="t1", hospital_ref="h1")["never_replace_hospital_emr"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_simulation():
    svc = get_biotechnology_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_simulation"]["prompt_id"] == "P217-G"
    assert svc.simulation_readiness()["passed"] is True
