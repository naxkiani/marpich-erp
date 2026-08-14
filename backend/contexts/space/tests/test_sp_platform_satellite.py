"""P218-F satellite intelligence foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.space.application.sp_satellite_foundation import validate_sp_satellite_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_satellite as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_space_service(); yield; reset_space_service()
@pytest.mark.unit
def test_sp_satellite_foundation():
    result = validate_sp_satellite_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-F"
    assert result["adr"] == 532
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"
@pytest.mark.unit
def test_sp_satellite_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-F"
    assert cat["fabric"] == "meos_satellite_intelligence_fabric"
    assert cat["foundation_gate"] == "P218"
    assert cat["mission_gate"] == "P218-A"
    assert cat["strategy_gate"] == "P218-B"
    assert cat["domain_gate"] == "P218-C"
    assert cat["infrastructure_gate"] == "P218-D"
    assert cat["space_ai_gate"] == "P218-E"
    assert cat["bio_gate"] == "P217-Z"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["satellite_intelligence_platform_present_required"] is True
    assert cat["constellation_management_present_required"] is True
    assert cat["orbital_asset_operations_present_required"] is True
    assert cat["satellite_lifecycle_present_required"] is True
    assert cat["payload_intelligence_present_required"] is True
    assert cat["satellite_ai_present_required"] is True
    assert cat["satellite_digital_twin_present_required"] is True
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["phase_count"] == 10
    assert cat["constellation"]["capability_count"] == 10
    assert cat["satellite_ai"]["model_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 11
    assert cat["never_replace_p218_e_space_ai"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["no_module_local_telemetry_stack"] is True
    assert cat["never_opaque_unexplainable_decisions"] is True
    assert cat["never_ungated_autonomous_mission_strategy"] is True
    assert cat["never_ungated_satellite_command_uplink"] is True
    assert cat["foundation_for_p218_g"] is True
    assert "GET /space/satellite" in mod.satellite_surface()["routes"]
    assert "thousands of satellites" in cat["satellite_mission"]
@pytest.mark.unit
def test_sp_satellite_acl():
    from contexts.space.infrastructure.acl import sp_satellite_acl as acls
    assert acls.to_space_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p218_foundation"] is True
    assert acls.to_space_ai(tenant_id="t1", space_ai_ref="e1")["never_replace_p218_e_space_ai"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_integration(tenant_id="t1", integration_ref="i1")["no_module_local_telemetry_stack"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_biotechnology(tenant_id="t1", bio_ref="b1")["never_replace_biotechnology"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_ungated_satellite_command_uplink"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_satellite():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_satellite"]["prompt_id"] == "P218-F"
    assert svc.satellite_readiness()["passed"] is True
