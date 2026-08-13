"""P216-O robotics retail / autonomous commerce foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_retail_foundation import validate_rb_retail_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_retail as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_retail_foundation():
    result = validate_rb_retail_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-O"
    assert result["adr"] == 487
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_retail_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-O"
    assert cat["fabric"] == "meos_autonomous_commerce_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["public_safety_gate"] == "P216-L"
    assert cat["logistics_gate"] == "P216-G"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["retail_robotics_platform_present_required"] is True
    assert cat["autonomous_commerce_platform_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 13
    assert cat["never_replace_p216_l_public_safety"] is True
    assert cat["never_direct_payment_bypass"] is True
    assert cat["never_duplicate_pos_sales_crm_core_logic"] is True
    assert cat["foundation_for_p216_p"] is True
    assert "GET /robotics/retail" in mod.retail_surface()["routes"]
    assert "MEOS Autonomous Commerce Platform SHALL unify" in cat["retail_vision"]
@pytest.mark.unit
def test_rb_retail_acl():
    from contexts.robotics.infrastructure.acl import rb_retail_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_public_safety(tenant_id="t1", public_safety_ref="p1")["never_replace_p216_l_public_safety"] is True
    assert acls.to_robotics_logistics(tenant_id="t1", logistics_ref="l1")["never_replace_p216_g_logistics"] is True
    assert acls.to_robotics_physical_ai(tenant_id="t1", physical_ai_ref="p1")["never_replace_p216_e_physical_ai"] is True
    assert acls.to_integration_platform(tenant_id="t1", connector_ref="c1")["never_direct_payment_bypass"] is True
    assert acls.to_pos(tenant_id="t1", pos_ref="pos1")["never_duplicate_pos_sales_crm_core_logic"] is True
    assert acls.to_crm(tenant_id="t1", crm_ref="crm1")["never_duplicate_pos_sales_crm_core_logic"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["privacy_by_design_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_strategy_forbidden"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_retail():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_retail"]["prompt_id"] == "P216-O"
    assert svc.retail_readiness()["passed"] is True
