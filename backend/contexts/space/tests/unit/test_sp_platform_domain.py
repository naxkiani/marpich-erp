"""P218-C space DDD domain architecture foundation tests."""
from __future__ import annotations
from pathlib import Path
import pytest
from contexts.space.application.sp_domain_foundation import validate_sp_domain_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_domain as mod
REPO_ROOT = Path(__file__).resolve().parents[5]
@pytest.fixture(autouse=True)
def _reset():
    reset_space_service(); yield; reset_space_service()
@pytest.mark.unit
def test_sp_domain_foundation():
    result = validate_sp_domain_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-C"
    assert result["adr"] == 529
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"
@pytest.mark.unit
def test_sp_domain_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-C"
    assert cat["fabric"] == "meos_space_intelligence_domain_architecture_framework"
    assert cat["foundation_gate"] == "P218"
    assert cat["mission_gate"] == "P218-A"
    assert cat["strategy_gate"] == "P218-B"
    assert cat["bio_gate"] == "P217-Z"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["space_core_domain_present_required"] is True
    assert cat["bounded_context_map_present_required"] is True
    assert cat["aggregates_present_required"] is True
    assert cat["knowledge_graph_mapping_present_required"] is True
    assert cat["digital_twin_mapping_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["aggregates"]["aggregate_count"] == 8
    assert cat["domain_services"]["service_count"] == 12
    assert cat["repositories"]["repository_count"] == 9
    assert cat["microservices"]["service_count"] == 8
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_foundation"] is True
    assert cat["never_replace_p218_a_mission"] is True
    assert cat["never_replace_p218_b_strategy"] is True
    assert cat["never_cross_context_aggregate_mutation"] is True
    assert cat["module_local_llm_forbidden"] is True
    assert cat["foundation_for_p218_d"] is True
    assert "GET /space/domain" in mod.domain_surface()["routes"]
    assert "intelligent space mission discovery" in cat["primary_capability"]
@pytest.mark.unit
def test_sp_domain_acl():
    from contexts.space.infrastructure.acl import sp_domain_acl as acls
    assert acls.to_space_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p218_foundation"] is True
    assert acls.to_space_mission(tenant_id="t1", mission_ref="m1")["never_replace_p218_a_mission"] is True
    assert acls.to_space_strategy(tenant_id="t1", strategy_ref="s1")["never_replace_p218_b_strategy"] is True
    assert acls.to_biotechnology(tenant_id="t1", bio_ref="b1")["never_replace_biotechnology"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["never_replace_ai_platform"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["module_local_llm_forbidden"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_skip_space_cybersecurity_strategy"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_opaque_mission_critical_strategy"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True
    assert acls.to_enterprise_space(tenant_id="t1", domain_ref="d1")["never_cross_context_aggregate_mutation"] is True
@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_domain():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_domain"]["prompt_id"] == "P218-C"
    assert svc.domain_readiness()["passed"] is True
