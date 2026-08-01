"""P216-G robotics autonomous logistics / warehouse foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_logistics_foundation import validate_rb_logistics_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_logistics as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_logistics_foundation():
    result = validate_rb_logistics_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-G"
    assert result["adr"] == 479
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_logistics_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-G"
    assert cat["fabric"] == "meos_autonomous_logistics_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["industrial_gate"] == "P216-F"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["autonomous_warehouse_platform_present_required"] is True
    assert cat["supply_chain_robotics_platform_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 11
    assert cat["domain_model"]["entity_count"] == 15
    assert cat["never_replace_p216_f_industrial"] is True
    assert cat["never_duplicate_wms_tms_core_logic"] is True
    assert cat["foundation_for_p216_h"] is True
    assert "GET /robotics/logistics" in mod.logistics_surface()["routes"]
    assert "MEOS Autonomous Logistics Platform SHALL unify" in cat["logistics_vision"]
@pytest.mark.unit
def test_rb_logistics_acl():
    from contexts.robotics.infrastructure.acl import rb_logistics_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_industrial(tenant_id="t1", industrial_ref="i1")["never_replace_p216_f_industrial"] is True
    assert acls.to_robotics_physical_ai(tenant_id="t1", physical_ai_ref="p1")["never_replace_p216_e_physical_ai"] is True
    assert acls.to_wms(tenant_id="t1", wms_ref="w1")["never_duplicate_wms_tms_core_logic"] is True
    assert acls.to_tms(tenant_id="t1", tms_ref="t1")["never_duplicate_wms_tms_core_logic"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["ungated_physical_autonomy_strategy_forbidden"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_strategy_forbidden"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_logistics():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_logistics"]["prompt_id"] == "P216-G"
    assert svc.logistics_readiness()["passed"] is True
