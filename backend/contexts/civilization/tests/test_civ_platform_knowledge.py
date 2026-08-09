"""P219-I civilization knowledge civilization platform foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.civilization.application.civ_knowledge_foundation import (
    validate_civ_knowledge_foundation,
)
from contexts.civilization.container import get_civilization_service, reset_civilization_service
from contexts.civilization.domain.services import civ_platform_knowledge as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_civilization_service()
    yield
    reset_civilization_service()


@pytest.mark.unit
def test_civ_knowledge_foundation():
    result = validate_civ_knowledge_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P219-I"
    assert result["adr"] == 562
    assert result["sor"] == "civilization"
    assert result["capability"] == "CAP-PLT-CIV-001"


@pytest.mark.unit
def test_civ_knowledge_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P219-I"
    assert cat["fabric"] == "meos_civilization_os_knowledge_civilization_framework"
    assert cat["foundation_gate"] == "P219"
    assert cat["mission_gate"] == "P219-A"
    assert cat["strategy_gate"] == "P219-B"
    assert cat["domain_gate"] == "P219-C"
    assert cat["planetary_gate"] == "P219-D"
    assert cat["ai_os_gate"] == "P219-E"
    assert cat["simulation_gate"] == "P219-F"
    assert cat["resources_gate"] == "P219-G"
    assert cat["economy_gate"] == "P219-H"
    assert cat["intelligence_nexus_gate"] == "P218-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["architecture"]["evolution_stage_count"] == 6
    assert cat["architecture"]["knowledge_domain_count"] == 10
    assert cat["architecture"]["ukg_layer_count"] == 4
    assert cat["architecture"]["entity_type_count"] == 11
    assert cat["architecture"]["relationship_count"] == 9
    assert cat["scientific"]["domain_count"] == 8
    assert cat["scientific"]["agent_count"] == 4
    assert cat["learning"]["agent_count"] == 4
    assert cat["agents"]["agent_count"] == 8
    assert cat["collective"]["component_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 4
    assert cat["aggregates"]["aggregate_count"] == 5
    assert cat["events"]["core_event_count"] == 13
    assert cat["cqrs"]["command_count"] == 6
    assert cat["cqrs"]["query_count"] == 5
    assert cat["microservices"]["service_count"] == 10
    assert cat["never_replace_p219_foundation"] is True
    assert cat["never_replace_p219_h_economy"] is True
    assert cat["never_replace_enterprise_search"] is True
    assert cat["never_replace_document_exchange"] is True
    assert cat["never_ungated_knowledge_publication"] is True
    assert cat["never_bypass_trusted_knowledge_validation"] is True
    assert cat["never_opaque_unexplainable_knowledge_decisions"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p219_j"] is True
    assert "GET /civilization/knowledge" in mod.knowledge_surface()["routes"]
    assert "preserving, connecting, understanding and expanding humanity's collective" in cat["primary_capability"]


@pytest.mark.unit
def test_civ_knowledge_acl():
    from contexts.civilization.infrastructure.acl import civ_knowledge_acl as acls

    assert acls.to_civilization_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p219_foundation"] is True
    assert acls.to_civilization_mission(tenant_id="t1", mission_ref="m1")["never_replace_p219_a_mission"] is True
    assert acls.to_civilization_strategy(tenant_id="t1", strategy_ref="s1")["never_replace_p219_b_strategy"] is True
    assert acls.to_civilization_domain(tenant_id="t1", domain_ref="d1")["never_replace_p219_c_domain"] is True
    assert acls.to_civilization_planetary(tenant_id="t1", planetary_ref="p1")["never_replace_p219_d_planetary"] is True
    assert acls.to_civilization_ai_os(tenant_id="t1", aios_ref="a1")["never_replace_p219_e_ai_os"] is True
    assert acls.to_civilization_simulation(tenant_id="t1", simulation_ref="s1")["never_replace_p219_f_simulation"] is True
    assert acls.to_civilization_resources(tenant_id="t1", resource_ref="r1")["never_replace_p219_g_resources"] is True
    assert acls.to_civilization_economy(tenant_id="t1", economy_ref="e1")["never_replace_p219_h_economy"] is True
    assert acls.to_enterprise_search(tenant_id="t1", search_ref="s1")["never_replace_enterprise_search"] is True
    assert acls.to_document_exchange(tenant_id="t1", document_ref="d1")["never_replace_document_exchange"] is True
    assert acls.to_intelligence_nexus(tenant_id="t1", nexus_ref="n1")["never_replace_p218_z_intelligence_nexus"] is True
    assert acls.to_space(tenant_id="t1", space_ref="s1")["never_replace_space"] is True
    assert acls.to_biotechnology(tenant_id="t1", bio_ref="b1")["never_replace_biotechnology"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["never_replace_ai_platform"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_ungated_knowledge_publication"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_bypass_trusted_knowledge_validation"] is True
    assert acls.to_enterprise_civilization(tenant_id="t1", knowledge_ref="k1")["never_replace_enterprise_search"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_knowledge():
    svc = get_civilization_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_knowledge"]["prompt_id"] == "P219-I"
    assert catalog["platform_knowledge"]["foundation_for_p219_j"] is True
    assert svc.knowledge_readiness()["passed"] is True
