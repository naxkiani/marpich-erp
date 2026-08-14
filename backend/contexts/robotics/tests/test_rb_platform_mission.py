"""P216-A robotics mission / vision / strategy foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_mission_foundation import validate_rb_mission_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_mission as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_mission_foundation():
    result = validate_rb_mission_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-A"
    assert result["adr"] == 473
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_mission_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-A"
    assert cat["fabric"] == "meos_cyber_physical_strategic_intelligence_framework"
    assert cat["foundation_gate"] == "P216"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["robotics_mission_framework_present_required"] is True
    assert cat["robotics_vision_framework_present_required"] is True
    assert cat["strategic_cyber_physical_scope_present_required"] is True
    assert cat["capability_map_present_required"] is True
    assert cat["operating_model_present_required"] is True
    assert cat["evolution_roadmap_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["objectives"]["objective_count"] >= 5
    assert cat["never_replace_p216_foundation"] is True
    assert cat["ungated_physical_autonomy_strategy_forbidden"] is True
    assert cat["foundation_for_p216_b"] is True
    assert "GET /robotics/mission" in mod.mission_surface()["routes"]
    assert "MEOS Enterprise Robotics Platform SHALL" in cat["mission_statement"]
@pytest.mark.unit
def test_rb_mission_acl():
    from contexts.robotics.infrastructure.acl import rb_mission_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["never_replace_ai_platform"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["ungated_physical_autonomy_strategy_forbidden"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_strategy_forbidden"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mission():
    svc = get_robotics_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_mission"]["prompt_id"] == "P216-A"; assert svc.mission_readiness()["passed"] is True
