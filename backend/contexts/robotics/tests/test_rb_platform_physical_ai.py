"""P216-E robotics Physical AI foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_physical_ai_foundation import validate_rb_physical_ai_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_physical_ai as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_physical_ai_foundation():
    result = validate_rb_physical_ai_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-E"
    assert result["adr"] == 477
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_physical_ai_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-E"
    assert cat["fabric"] == "meos_physical_ai_intelligence_fabric"
    assert cat["foundation_gate"] == "P216"
    assert cat["runtime_gate"] == "P216-D"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["physical_ai_engine_present_required"] is True
    assert cat["robot_perception_platform_present_required"] is True
    assert cat["cognitive_robotics_platform_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["domain_model"]["entity_count"] == 10
    assert cat["never_replace_p216_d_runtime"] is True
    assert cat["physical_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["never_opaque_unexplainable_decisions"] is True
    assert cat["foundation_for_p216_f"] is True
    assert "GET /robotics/physical-ai" in mod.physical_ai_surface()["routes"]
    assert "Physical AI enables robots to perceive" in cat["physical_ai_vision"]
@pytest.mark.unit
def test_rb_physical_ai_acl():
    from contexts.robotics.infrastructure.acl import rb_physical_ai_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_runtime(tenant_id="t1", runtime_ref="r1")["never_replace_p216_d_runtime"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["physical_ai_via_p214z_acl_only"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["no_module_local_llm"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["ungated_physical_autonomy_strategy_forbidden"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_strategy_forbidden"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_opaque_unexplainable_decisions"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_physical_ai():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_physical_ai"]["prompt_id"] == "P216-E"
    assert svc.physical_ai_readiness()["passed"] is True
