"""P216-W robotics personal / home intelligence foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_personal_foundation import validate_rb_personal_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_personal as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_personal_foundation():
    result = validate_rb_personal_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-W"
    assert result["adr"] == 495
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_personal_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-W"
    assert cat["fabric"] == "meos_personal_intelligence_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["science_gate"] == "P216-V"
    assert cat["healthcare_gate"] == "P216-I"
    assert cat["education_gate"] == "P216-Q"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["personal_robotics_platform_present_required"] is True
    assert cat["ai_companion_platform_present_required"] is True
    assert cat["privacy_sovereignty_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 10
    assert cat["events"]["core_event_count"] == 7
    assert cat["never_replace_p216_v_science"] is True
    assert cat["never_replace_identity_platform"] is True
    assert cat["personal_data_sovereignty_required"] is True
    assert cat["human_control_by_design_required"] is True
    assert cat["consent_management_required"] is True
    assert cat["foundation_for_p216_x"] is True
    assert "GET /robotics/personal" in mod.personal_surface()["routes"]
    assert "MEOS Personal Intelligence Platform SHALL unify" in cat["personal_vision"]
@pytest.mark.unit
def test_rb_personal_acl():
    from contexts.robotics.infrastructure.acl import rb_personal_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_science(tenant_id="t1", science_ref="s1")["never_replace_p216_v_science"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_replace_identity_platform"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_iot(tenant_id="t1", iot_ref="iot1")["via_iot_api"] is True
    assert acls.to_smart_home(tenant_id="t1", home_ref="h1")["via_smart_home_api"] is True
    assert acls.to_wearable(tenant_id="t1", wearable_ref="w1")["via_wearable_api"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["personal_data_sovereignty_required"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["consent_management_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["human_control_by_design_required"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_personal():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_personal"]["prompt_id"] == "P216-W"
    assert svc.personal_readiness()["passed"] is True
