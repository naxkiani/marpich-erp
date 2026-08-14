"""P218-A space mission / vision / strategy foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.space.application.sp_mission_foundation import validate_sp_mission_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_mission as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_space_service(); yield; reset_space_service()
@pytest.mark.unit
def test_sp_mission_foundation():
    result = validate_sp_mission_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-A"
    assert result["adr"] == 527
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"
@pytest.mark.unit
def test_sp_mission_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-A"
    assert cat["fabric"] == "meos_space_intelligence_strategic_framework"
    assert cat["foundation_gate"] == "P218"
    assert cat["bio_gate"] == "P217-Z"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["space_mission_framework_present_required"] is True
    assert cat["space_vision_framework_present_required"] is True
    assert cat["strategic_space_scope_present_required"] is True
    assert cat["space_capability_framework_present_required"] is True
    assert cat["value_streams_framework_present_required"] is True
    assert cat["maturity_model_present_required"] is True
    assert cat["governance_framework_present_required"] is True
    assert cat["meos_integration_strategy_present_required"] is True
    assert cat["future_evolution_roadmap_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["objectives"]["objective_count"] >= 7
    assert cat["drivers"]["driver_count"] >= 10
    assert cat["capability_framework"]["l1_count"] >= 20
    assert cat["value_streams"]["stream_count"] >= 10
    assert cat["never_replace_p218_foundation"] is True
    assert cat["never_replace_biotechnology"] is True
    assert cat["never_opaque_mission_critical_strategy"] is True
    assert cat["never_ungated_autonomous_mission_strategy"] is True
    assert cat["foundation_for_p218_b"] is True
    assert "GET /space/mission" in mod.mission_surface()["routes"]
    assert "unified enterprise platform" in cat["mission_statement"]
@pytest.mark.unit
def test_sp_mission_acl():
    from contexts.space.infrastructure.acl import sp_mission_acl as acls
    assert acls.to_space_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p218_foundation"] is True
    assert acls.to_biotechnology(tenant_id="t1", bio_ref="b1")["never_replace_biotechnology"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["never_replace_ai_platform"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_skip_space_cybersecurity_strategy"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_opaque_mission_critical_strategy"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_ungated_autonomous_mission_strategy"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mission():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_mission"]["prompt_id"] == "P218-A"
    assert svc.mission_readiness()["passed"] is True
