"""P219-L civilization innovation intelligence platform foundation tests (unit path)."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.civilization.application.civ_innovation_foundation import (
    validate_civ_innovation_foundation,
)
from contexts.civilization.container import get_civilization_service, reset_civilization_service
from contexts.civilization.domain.services import civ_platform_innovation as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_civilization_service()
    yield
    reset_civilization_service()


@pytest.mark.unit
def test_civ_innovation_foundation():
    result = validate_civ_innovation_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P219-L"
    assert result["adr"] == 565
    assert result["sor"] == "civilization"
    assert result["capability"] == "CAP-PLT-CIV-001"


@pytest.mark.unit
def test_civ_innovation_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P219-L"
    assert cat["fabric"] == "meos_civilization_os_civilization_innovation_intelligence_framework"
    assert cat["foundation_gate"] == "P219"
    assert cat["mission_gate"] == "P219-A"
    assert cat["strategy_gate"] == "P219-B"
    assert cat["domain_gate"] == "P219-C"
    assert cat["planetary_gate"] == "P219-D"
    assert cat["ai_os_gate"] == "P219-E"
    assert cat["simulation_gate"] == "P219-F"
    assert cat["resources_gate"] == "P219-G"
    assert cat["economy_gate"] == "P219-H"
    assert cat["knowledge_gate"] == "P219-I"
    assert cat["human_gate"] == "P219-J"
    assert cat["governance_gate"] == "P219-K"
    assert cat["intelligence_nexus_gate"] == "P218-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["architecture"]["evolution_stage_count"] == 6
    assert cat["architecture"]["layer_count"] == 6
    assert cat["architecture"]["network_domain_count"] == 8
    assert cat["architecture"]["research_lifecycle_step_count"] == 8
    assert cat["architecture"]["technology_domain_count"] == 10
    assert cat["architecture"]["portfolio_type_count"] == 5
    assert cat["agents"]["agent_count"] == 5
    assert cat["knowledge_graph"]["entity_count"] == 10
    assert cat["knowledge_graph"]["relationship_count"] == 8
    assert cat["digital_twin"]["twin_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 4
    assert cat["aggregates"]["aggregate_count"] == 5
    assert cat["events"]["core_event_count"] == 14
    assert cat["cqrs"]["command_count"] == 6
    assert cat["cqrs"]["query_count"] == 6
    assert cat["microservices"]["service_count"] == 10
    assert cat["never_replace_p219_foundation"] is True
    assert cat["never_replace_p219_k_governance"] is True
    assert cat["never_ungated_innovation_commercialization"] is True
    assert cat["never_skip_responsible_innovation_governance"] is True
    assert cat["never_opaque_unexplainable_innovation_decisions"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p219_m"] is True
    assert "GET /civilization/innovation" in mod.innovation_surface()["routes"]
    assert "discovering, connecting, evaluating and accelerating scientific" in cat["primary_capability"]


@pytest.mark.unit
def test_civ_innovation_acl():
    from contexts.civilization.infrastructure.acl import civ_innovation_acl as acls

    assert acls.to_civilization_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p219_foundation"] is True
    assert acls.to_civilization_mission(tenant_id="t1", mission_ref="m1")["never_replace_p219_a_mission"] is True
    assert acls.to_civilization_strategy(tenant_id="t1", strategy_ref="s1")["never_replace_p219_b_strategy"] is True
    assert acls.to_civilization_domain(tenant_id="t1", domain_ref="d1")["never_replace_p219_c_domain"] is True
    assert acls.to_civilization_planetary(tenant_id="t1", planetary_ref="p1")["never_replace_p219_d_planetary"] is True
    assert acls.to_civilization_ai_os(tenant_id="t1", aios_ref="a1")["never_replace_p219_e_ai_os"] is True
    assert acls.to_civilization_simulation(tenant_id="t1", simulation_ref="s1")["never_replace_p219_f_simulation"] is True
    assert acls.to_civilization_resources(tenant_id="t1", resource_ref="r1")["never_replace_p219_g_resources"] is True
    assert acls.to_civilization_economy(tenant_id="t1", economy_ref="e1")["never_replace_p219_h_economy"] is True
    assert acls.to_civilization_knowledge(tenant_id="t1", knowledge_ref="k1")["never_replace_p219_i_knowledge"] is True
    assert acls.to_civilization_human(tenant_id="t1", human_ref="h1")["never_replace_p219_j_human"] is True
    assert acls.to_civilization_governance(tenant_id="t1", governance_ref="g1")["never_replace_p219_k_governance"] is True
    assert acls.to_civilization_governance(tenant_id="t1", governance_ref="g1")["never_ungated_innovation_commercialization"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_replace_policy_engine"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_replace_workflow"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_ungated_innovation_commercialization"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_replace_audit"] is True
    assert acls.to_intelligence_nexus(tenant_id="t1", nexus_ref="n1")["never_replace_p218_z_intelligence_nexus"] is True
    assert acls.to_space(tenant_id="t1", space_ref="s1")["never_replace_space"] is True
    assert acls.to_biotechnology(tenant_id="t1", bio_ref="b1")["never_replace_biotechnology"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["never_replace_ai_platform"] is True
    assert acls.to_enterprise_civilization(tenant_id="t1", innovation_ref="i1")["never_replace_p219_k_governance"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_innovation():
    svc = get_civilization_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_innovation"]["prompt_id"] == "P219-L"
    assert catalog["platform_innovation"]["foundation_for_p219_m"] is True
    assert svc.innovation_readiness()["passed"] is True
