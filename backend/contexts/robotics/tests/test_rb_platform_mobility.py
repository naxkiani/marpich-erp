"""P216-H robotics autonomous mobility / connected vehicles / drones foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_mobility_foundation import validate_rb_mobility_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_mobility as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_mobility_foundation():
    result = validate_rb_mobility_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-H"
    assert result["adr"] == 480
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_mobility_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-H"
    assert cat["fabric"] == "meos_autonomous_mobility_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["logistics_gate"] == "P216-G"
    assert cat["industrial_gate"] == "P216-F"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["connected_vehicle_platform_present_required"] is True
    assert cat["drone_intelligence_platform_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 13
    assert cat["never_replace_p216_g_logistics"] is True
    assert cat["never_direct_v2x_bypass"] is True
    assert cat["foundation_for_p216_i"] is True
    assert "GET /robotics/mobility" in mod.mobility_surface()["routes"]
    assert "MEOS Autonomous Mobility Platform SHALL coordinate" in cat["mobility_vision"]
@pytest.mark.unit
def test_rb_mobility_acl():
    from contexts.robotics.infrastructure.acl import rb_mobility_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_logistics(tenant_id="t1", logistics_ref="l1")["never_replace_p216_g_logistics"] is True
    assert acls.to_robotics_physical_ai(tenant_id="t1", physical_ai_ref="p1")["never_replace_p216_e_physical_ai"] is True
    assert acls.to_integration_platform(tenant_id="t1", connector_ref="c1")["never_direct_v2x_bypass"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["ungated_physical_autonomy_strategy_forbidden"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_strategy_forbidden"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mobility():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_mobility"]["prompt_id"] == "P216-H"
    assert svc.mobility_readiness()["passed"] is True
