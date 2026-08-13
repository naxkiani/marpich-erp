"""P216-P robotics hospitality / smart hotel foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_hospitality_foundation import validate_rb_hospitality_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_hospitality as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_hospitality_foundation():
    result = validate_rb_hospitality_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-P"
    assert result["adr"] == 488
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_hospitality_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-P"
    assert cat["fabric"] == "meos_hospitality_intelligence_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["retail_gate"] == "P216-O"
    assert cat["mobility_gate"] == "P216-H"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["hospitality_robotics_platform_present_required"] is True
    assert cat["smart_hotel_platform_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 15
    assert cat["never_replace_p216_o_retail"] is True
    assert cat["never_direct_payment_bypass"] is True
    assert cat["never_duplicate_hotel_pms_core_logic"] is True
    assert cat["foundation_for_p216_q"] is True
    assert "GET /robotics/hospitality" in mod.hospitality_surface()["routes"]
    assert "MEOS Hospitality Intelligence Platform SHALL unify" in cat["hospitality_vision"]
@pytest.mark.unit
def test_rb_hospitality_acl():
    from contexts.robotics.infrastructure.acl import rb_hospitality_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_retail(tenant_id="t1", retail_ref="r1")["never_replace_p216_o_retail"] is True
    assert acls.to_robotics_mobility(tenant_id="t1", mobility_ref="m1")["never_replace_p216_h_mobility"] is True
    assert acls.to_robotics_physical_ai(tenant_id="t1", physical_ai_ref="p1")["never_replace_p216_e_physical_ai"] is True
    assert acls.to_integration_platform(tenant_id="t1", connector_ref="c1")["never_direct_payment_bypass"] is True
    assert acls.to_hotel_pms(tenant_id="t1", pms_ref="pms1")["never_duplicate_hotel_pms_core_logic"] is True
    assert acls.to_booking(tenant_id="t1", booking_ref="b1")["never_duplicate_hotel_pms_core_logic"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["human_centered_hospitality_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_strategy_forbidden"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_hospitality():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_hospitality"]["prompt_id"] == "P216-P"
    assert svc.hospitality_readiness()["passed"] is True
