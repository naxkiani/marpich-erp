"""P218-I space navigation foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.space.application.sp_navigation_foundation import validate_sp_navigation_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_navigation as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_space_service(); yield; reset_space_service()
@pytest.mark.unit
def test_sp_navigation_foundation():
    result = validate_sp_navigation_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-I"
    assert result["adr"] == 535
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"
@pytest.mark.unit
def test_sp_navigation_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-I"
    assert cat["fabric"] == "meos_space_navigation_intelligence_fabric"
    assert cat["foundation_gate"] == "P218"
    assert cat["mission_gate"] == "P218-A"
    assert cat["strategy_gate"] == "P218-B"
    assert cat["domain_gate"] == "P218-C"
    assert cat["infrastructure_gate"] == "P218-D"
    assert cat["space_ai_gate"] == "P218-E"
    assert cat["satellite_gate"] == "P218-F"
    assert cat["orbital_gate"] == "P218-G"
    assert cat["communications_gate"] == "P218-H"
    assert cat["bio_gate"] == "P217-Z"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["space_navigation_platform_present_required"] is True
    assert cat["gnss_intelligence_present_required"] is True
    assert cat["autonomous_navigation_present_required"] is True
    assert cat["trajectory_optimization_present_required"] is True
    assert cat["guidance_and_control_present_required"] is True
    assert cat["navigation_ai_present_required"] is True
    assert cat["navigation_digital_twin_present_required"] is True
    assert cat["architecture"]["layer_count"] == 5
    assert cat["gnss"]["capability_count"] == 8
    assert cat["navigation_ai"]["model_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_h_communications"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["no_module_local_gnss_receiver_stack"] is True
    assert cat["never_opaque_unexplainable_decisions"] is True
    assert cat["never_ungated_guidance_command"] is True
    assert cat["never_skip_gnss_spoofing_detection"] is True
    assert cat["foundation_for_p218_j"] is True
    assert "GET /space/navigation" in mod.navigation_surface()["routes"]
    assert "unified navigation intelligence platform" in cat["nav_mission"]
@pytest.mark.unit
def test_sp_navigation_acl():
    from contexts.space.infrastructure.acl import sp_navigation_acl as acls
    assert acls.to_space_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p218_foundation"] is True
    assert acls.to_communications(tenant_id="t1", communications_ref="c1")["never_replace_p218_h_communications"] is True
    assert acls.to_orbital(tenant_id="t1", orbital_ref="o1")["never_replace_p218_g_orbital"] is True
    assert acls.to_satellite(tenant_id="t1", satellite_ref="s1")["never_replace_p218_f_satellite"] is True
    assert acls.to_space_ai(tenant_id="t1", space_ai_ref="e1")["never_replace_p218_e_space_ai"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_integration(tenant_id="t1", integration_ref="i1")["no_module_local_gnss_receiver_stack"] is True
    assert acls.to_integration(tenant_id="t1", integration_ref="i1")["never_skip_gnss_spoofing_detection"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_biotechnology(tenant_id="t1", bio_ref="b1")["never_replace_biotechnology"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_ungated_guidance_command"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_navigation():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_navigation"]["prompt_id"] == "P218-I"
    assert svc.navigation_readiness()["passed"] is True
