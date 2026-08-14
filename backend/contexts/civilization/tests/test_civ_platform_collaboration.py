"""P219-P civilization collaboration intelligence platform foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.civilization.application.civ_collaboration_foundation import (
    validate_civ_collaboration_foundation,
)
from contexts.civilization.container import get_civilization_service, reset_civilization_service
from contexts.civilization.domain.services import civ_platform_collaboration as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_civilization_service()
    yield
    reset_civilization_service()


@pytest.mark.unit
def test_civ_collaboration_foundation():
    result = validate_civ_collaboration_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P219-P"
    assert result["adr"] == 569
    assert result["sor"] == "civilization"
    assert result["capability"] == "CAP-PLT-CIV-001"


@pytest.mark.unit
def test_civ_collaboration_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P219-P"
    assert cat["fabric"] == "meos_civilization_os_civilization_collaboration_intelligence_framework"
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
    assert cat["innovation_gate"] == "P219-L"
    assert cat["security_gate"] == "P219-M"
    assert cat["sustainability_gate"] == "P219-N"
    assert cat["prosperity_gate"] == "P219-O"
    assert cat["intelligence_nexus_gate"] == "P218-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["architecture"]["evolution_stage_count"] == 6
    assert cat["architecture"]["layer_count"] == 6
    assert cat["architecture"]["participant_count"] == 8
    assert cat["architecture"]["network_domain_count"] == 9
    assert cat["architecture"]["problem_domain_count"] == 10
    assert cat["architecture"]["problem_solving_lifecycle_step_count"] == 8
    assert cat["architecture"]["coordination_level_count"] == 9
    assert cat["agents"]["agent_count"] == 5
    assert cat["knowledge_graph"]["entity_count"] == 10
    assert cat["knowledge_graph"]["relationship_count"] == 8
    assert cat["digital_twin"]["twin_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 4
    assert cat["aggregates"]["aggregate_count"] == 5
    assert cat["events"]["core_event_count"] == 13
    assert cat["cqrs"]["command_count"] == 6
    assert cat["cqrs"]["query_count"] == 6
    assert cat["microservices"]["service_count"] == 10
    assert cat["never_replace_p219_foundation"] is True
    assert cat["never_replace_p219_o_prosperity"] is True
    assert cat["never_replace_p219_i_knowledge"] is True
    assert cat["never_replace_p219_k_governance"] is True
    assert cat["never_ungated_collaborative_decision_execution"] is True
    assert cat["never_treat_consensus_score_as_binding_policy"] is True
    assert cat["never_bypass_collective_consent_safeguards"] is True
    assert cat["never_opaque_unexplainable_collaboration_decisions"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p219_q"] is True
    assert "GET /civilization/collaboration" in mod.collaboration_surface()["routes"]
    assert "enabling humans, AI, institutions and autonomous systems to solve global" in cat["primary_capability"]


@pytest.mark.unit
def test_civ_collaboration_acl():
    from contexts.civilization.infrastructure.acl import civ_collaboration_acl as acls

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
    assert acls.to_civilization_innovation(tenant_id="t1", innovation_ref="i1")["never_replace_p219_l_innovation"] is True
    assert acls.to_civilization_security(tenant_id="t1", security_ref="sec1")["never_replace_p219_m_security"] is True
    assert acls.to_civilization_sustainability(tenant_id="t1", sustainability_ref="s1")["never_replace_p219_n_sustainability"] is True
    assert acls.to_civilization_prosperity(tenant_id="t1", prosperity_ref="p1")["never_replace_p219_o_prosperity"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_violate_human_sovereignty_collaboration"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_replace_policy_engine"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_treat_consensus_score_as_binding_policy"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_replace_workflow"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_ungated_collaborative_decision_execution"] is True
    assert acls.to_audit(tenant_id="t1", audit_ref="a1")["never_replace_audit"] is True
    assert acls.to_intelligence_nexus(tenant_id="t1", nexus_ref="n1")["never_replace_p218_z_intelligence_nexus"] is True
    assert acls.to_space(tenant_id="t1", space_ref="s1")["never_replace_space"] is True
    assert acls.to_biotechnology(tenant_id="t1", bio_ref="b1")["never_replace_biotechnology"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["never_replace_ai_platform"] is True
    assert acls.to_enterprise_civilization(tenant_id="t1", collaboration_ref="c1")["never_bypass_collective_consent_safeguards"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_collaboration():
    svc = get_civilization_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_collaboration"]["prompt_id"] == "P219-P"
    assert catalog["platform_collaboration"]["foundation_for_p219_q"] is True
    assert svc.collaboration_readiness()["passed"] is True
