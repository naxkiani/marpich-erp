"""P218-B space strategic architecture foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.space.application.sp_strategy_foundation import validate_sp_strategy_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_strategy as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_space_service(); yield; reset_space_service()
@pytest.mark.unit
def test_sp_strategy_foundation():
    result = validate_sp_strategy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-B"
    assert result["adr"] == 528
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"
@pytest.mark.unit
def test_sp_strategy_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-B"
    assert cat["fabric"] == "meos_space_intelligence_strategic_architecture_framework"
    assert cat["foundation_gate"] == "P218"
    assert cat["mission_gate"] == "P218-A"
    assert cat["bio_gate"] == "P217-Z"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["space_strategic_architecture_present_required"] is True
    assert cat["capability_model_present_required"] is True
    assert cat["operating_framework_present_required"] is True
    assert cat["platform_model_present_required"] is True
    assert cat["service_model_present_required"] is True
    assert cat["maturity_model_present_required"] is True
    assert cat["transformation_roadmap_present_required"] is True
    assert cat["space_operating_framework_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["architecture_layers"]["layer_count"] == 5
    assert cat["capability_model"]["group_count"] == 6
    assert cat["capability_model"]["l1_count"] == 20
    assert cat["operating_framework"]["component_count"] == 10
    assert cat["operating_framework"]["framework_layer_count"] == 6
    assert cat["service_model"]["service_count"] == 16
    assert cat["maturity_model"]["level_count"] == 6
    assert cat["never_replace_p218_foundation"] is True
    assert cat["never_replace_p218_a_mission"] is True
    assert cat["never_opaque_mission_critical_strategy"] is True
    assert cat["never_ungated_autonomous_mission_strategy"] is True
    assert cat["foundation_for_p218_c"] is True
    assert "GET /space/strategy" in mod.strategy_surface()["routes"]
    assert "MEOS Space Intelligence Architecture SHALL" in cat["architecture_vision"]
@pytest.mark.unit
def test_sp_strategy_acl():
    from contexts.space.infrastructure.acl import sp_strategy_acl as acls
    assert acls.to_space_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p218_foundation"] is True
    assert acls.to_space_mission(tenant_id="t1", mission_ref="m1")["never_replace_p218_a_mission"] is True
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
async def test_service_catalog_includes_platform_strategy():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_strategy"]["prompt_id"] == "P218-B"
    assert svc.strategy_readiness()["passed"] is True
