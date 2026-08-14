"""P216-Z robotics supreme control plane / intelligence nexus foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_supreme_foundation import validate_rb_supreme_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_supreme as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_supreme_foundation():
    result = validate_rb_supreme_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-Z"
    assert result["adr"] == 498
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_supreme_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-Z"
    assert cat["fabric"] == "meos_robotics_supreme_intelligence_nexus"
    assert cat["foundation_gate"] == "P216"
    assert cat["ultimate_gate"] == "P216-Y"
    assert cat["entertainment_gate"] == "P216-X"
    assert cat["physical_ai_gate"] == "P216-E"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["meos_robotics_supreme_control_plane_present_required"] is True
    assert cat["universal_robotics_network_present_required"] is True
    assert cat["human_authority_framework_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 10
    assert cat["events"]["core_event_count"] == 7
    assert cat["never_replace_p216_y_ultimate"] is True
    assert cat["never_replace_identity_platform"] is True
    assert cat["human_authority_framework_required"] is True
    assert cat["safety_by_design_required"] is True
    assert cat["human_override_authority_required"] is True
    assert cat["completes_p216_master_series"] is True
    assert cat["foundation_for_p217"] is True
    assert "GET /robotics/supreme" in mod.supreme_surface()["routes"]
    assert "MEOS Robotics Supreme Intelligence Nexus SHALL unify" in cat["supreme_vision"]
@pytest.mark.unit
def test_rb_supreme_acl():
    from contexts.robotics.infrastructure.acl import rb_supreme_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_ultimate(tenant_id="t1", ultimate_ref="u1")["never_replace_p216_y_ultimate"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_replace_identity_platform"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_meos_data(tenant_id="t1", data_ref="d1")["via_meos_data_api"] is True
    assert acls.to_meos_digital_twin(tenant_id="t1", twin_ref="t1")["via_meos_digital_twin_api"] is True
    assert acls.to_meos_knowledge_graph(tenant_id="t1", kg_ref="k1")["via_meos_kg_api"] is True
    assert acls.to_meos_autonomous_agent(tenant_id="t1", agent_ref="a1")["via_meos_agent_api"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["human_authority_framework_required"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["safety_by_design_required"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["human_override_authority_required"] is True
    assert acls.to_enterprise_robotics(tenant_id="t1", supreme_ref="s1")["completes_p216_master_series"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_supreme():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_supreme"]["prompt_id"] == "P216-Z"
    assert svc.supreme_readiness()["passed"] is True
