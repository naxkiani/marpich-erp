"""P216-Y robotics ultimate / future intelligence foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_ultimate_foundation import validate_rb_ultimate_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_ultimate as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_ultimate_foundation():
    result = validate_rb_ultimate_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-Y"
    assert result["adr"] == 497
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_ultimate_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-Y"
    assert cat["fabric"] == "meos_ultimate_robotics_intelligence_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["entertainment_gate"] == "P216-X"
    assert cat["personal_gate"] == "P216-W"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["future_robotics_architecture_present_required"] is True
    assert cat["human_machine_symbiosis_platform_present_required"] is True
    assert cat["human_governance_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 10
    assert cat["events"]["core_event_count"] == 7
    assert cat["never_replace_p216_x_entertainment"] is True
    assert cat["never_replace_identity_platform"] is True
    assert cat["human_control_preservation_required"] is True
    assert cat["safety_by_design_required"] is True
    assert cat["human_override_authority_required"] is True
    assert cat["foundation_for_p216_z"] is True
    assert "GET /robotics/ultimate" in mod.ultimate_surface()["routes"]
    assert "MEOS Ultimate Robotics Intelligence Platform SHALL unify" in cat["ultimate_vision"]
@pytest.mark.unit
def test_rb_ultimate_acl():
    from contexts.robotics.infrastructure.acl import rb_ultimate_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_entertainment(tenant_id="t1", entertainment_ref="e1")["never_replace_p216_x_entertainment"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_replace_identity_platform"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_human_interface(tenant_id="t1", human_interface_ref="h1")["via_human_interface_api"] is True
    assert acls.to_ai_agent_ecosystem(tenant_id="t1", agent_ref="a1")["via_ai_agent_api"] is True
    assert acls.to_smart_infrastructure(tenant_id="t1", infrastructure_ref="si1")["via_smart_infrastructure_api"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["human_override_authority_required"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["safety_by_design_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["human_override_authority_required"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ultimate():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_ultimate"]["prompt_id"] == "P216-Y"
    assert svc.ultimate_readiness()["passed"] is True
