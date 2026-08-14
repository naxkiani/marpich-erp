"""P216 robotics / cyber-physical foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_foundation_foundation import validate_rb_foundation_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_foundation as mod
REPO_ROOT = Path(__file__).resolve().parents[4]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_foundation_foundation():
    result = validate_rb_foundation_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216"
    assert result["adr"] == 472
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_foundation_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216"
    assert cat["fabric"] == "meos_cyber_physical_intelligence_fabric"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["enterprise_robotics_platform_present_required"] is True
    assert cat["autonomous_machine_platform_present_required"] is True
    assert cat["physical_ai_engine_present_required"] is True
    assert cat["robot_fleet_intelligence_present_required"] is True
    assert cat["edge_intelligence_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["microservices"]["service_count"] >= 10
    assert cat["never_replace_core_platform"] is True
    assert cat["ungated_physical_autonomy_forbidden"] is True
    assert cat["opaque_safety_decisions_forbidden"] is True
    assert "GET /robotics/foundation" in mod.foundation_surface()["routes"]
@pytest.mark.unit
def test_rb_foundation_acl():
    from contexts.robotics.infrastructure.acl import rb_foundation_acl as acls
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["module_local_llm_forbidden"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["ungated_physical_autonomy_forbidden"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_decisions_forbidden"] is True
    assert acls.to_integration(tenant_id="t1", connector_ref="c1")["iiot_via_integration_platform_only"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="core1")["never_replace_core_platform"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_foundation():
    svc = get_robotics_service(); catalog = (await svc.list_catalog()).unwrap(); assert catalog["platform_foundation"]["prompt_id"] == "P216"; assert svc.foundation_readiness()["passed"] is True
