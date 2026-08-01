"""P216-C robotics DDD domain architecture foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.robotics.application.rb_domain_foundation import validate_rb_domain_foundation
from contexts.robotics.container import get_robotics_service, reset_robotics_service
from contexts.robotics.domain.services import rb_platform_domain as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_robotics_service(); yield; reset_robotics_service()
@pytest.mark.unit
def test_rb_domain_foundation():
    result = validate_rb_domain_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P216-C"
    assert result["adr"] == 475
    assert result["sor"] == "robotics"
    assert result["capability"] == "CAP-PLT-RB-001"
@pytest.mark.unit
def test_rb_domain_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P216-C"
    assert cat["fabric"] == "meos_robotics_domain_architecture_framework"
    assert cat["foundation_gate"] == "P216"
    assert cat["mission_gate"] == "P216-A"
    assert cat["strategy_gate"] == "P216-B"
    assert cat["supreme_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["robotics_core_domain_present_required"] is True
    assert cat["bounded_context_map_present_required"] is True
    assert cat["aggregates_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 9
    assert cat["aggregates"]["aggregate_count"] == 9
    assert cat["domain_services"]["service_count"] == 7
    assert cat["repositories"]["repository_count"] == 6
    assert cat["microservices"]["service_count"] == 9
    assert cat["never_replace_p216_foundation"] is True
    assert cat["never_replace_p216_a_mission"] is True
    assert cat["never_replace_p216_b_strategy"] is True
    assert cat["never_cross_context_aggregate_mutation"] is True
    assert cat["foundation_for_p216_d"] is True
    assert "GET /robotics/domain" in mod.domain_surface()["routes"]
    assert "autonomous cyber-physical systems" in cat["primary_capability"]
@pytest.mark.unit
def test_rb_domain_acl():
    from contexts.robotics.infrastructure.acl import rb_domain_acl as acls
    assert acls.to_robotics_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p216_foundation"] is True
    assert acls.to_robotics_mission(tenant_id="t1", mission_ref="m1")["never_replace_p216_a_mission"] is True
    assert acls.to_robotics_strategy(tenant_id="t1", strategy_ref="s1")["never_replace_p216_b_strategy"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["never_replace_ai_platform"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["ungated_physical_autonomy_strategy_forbidden"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["opaque_safety_strategy_forbidden"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
    assert acls.to_enterprise_robotics(tenant_id="t1", domain_ref="d1")["never_cross_context_aggregate_mutation"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_domain():
    svc = get_robotics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_domain"]["prompt_id"] == "P216-C"
    assert svc.domain_readiness()["passed"] is True
