"""P216-D robotics EROS / runtime / fleet control foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_runtime_foundation import validate_rb_runtime_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_runtime as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_runtime_foundation():
    result = validate_rb_runtime_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-D"
    assert result["adr"] == 476
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_runtime_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-D"
    assert cat["fabric"] == "meos_robotics_operating_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["mission_gate"] == "P216-A"
    assert cat["strategy_gate"] == "P216-B"
    assert cat["domain_gate"] == "P216-C"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["robotics_os_architecture_present_required"] is True
    assert cat["robot_runtime_platform_present_required"] is True
    assert cat["fleet_control_plane_present_required"] is True
    assert cat["os_architecture"]["layer_count"] == 6
    assert cat["runtime_platform"]["component_count"] == 5
    assert cat["microservices"]["service_count"] == 10
    assert cat["never_replace_p216_foundation"] is True
    assert cat["never_replace_p216_c_domain"] is True
    assert cat["never_direct_hardware_bypass_of_hal"] is True
    assert cat["module_local_observability_store_forbidden"] is True
    assert cat["foundation_for_p216_e"] is True
    assert "GET /robotics/runtime" in mod.runtime_surface()["routes"]
    assert "EROS SHALL become the operating intelligence layer" in cat["eros_vision"]
@pytest.mark.unit
def test_rb_runtime_acl():
    from contexts.robotics.infrastructure.acl import rb_runtime_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_mission(tenant_id="t1", mission_ref="m1")["never_replace_p216_a_mission"] is True
    assert acls.to_robotics_strategy(tenant_id="t1", strategy_ref="s1")["never_replace_p216_b_strategy"] is True
    assert acls.to_robotics_domain(tenant_id="t1", domain_ref="d1")["never_replace_p216_c_domain"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["never_replace_ai_platform"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["ungated_physical_autonomy_strategy_forbidden"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_strategy_forbidden"] is True
    assert acls.to_observability(tenant_id="t1", observability_ref="o1")["module_local_observability_store_forbidden"] is True
    assert acls.to_enterprise_robotics(tenant_id="t1", runtime_ref="r1")["never_direct_hardware_bypass_of_hal"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_runtime():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_runtime"]["prompt_id"] == "P216-D"
    assert svc.runtime_readiness()["passed"] is True
