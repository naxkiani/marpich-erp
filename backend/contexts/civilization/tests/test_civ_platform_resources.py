"""P219-G planetary resource intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.civilization.application.civ_resources_foundation import (
    validate_civ_resources_foundation,
)
from contexts.civilization.container import get_civilization_service, reset_civilization_service
from contexts.civilization.domain.services import civ_platform_resources as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_civilization_service()
    yield
    reset_civilization_service()


@pytest.mark.unit
def test_civ_resources_foundation():
    result = validate_civ_resources_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P219-G"
    assert result["adr"] == 560
    assert result["sor"] == "civilization"
    assert result["capability"] == "CAP-PLT-CIV-001"


@pytest.mark.unit
def test_civ_resources_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P219-G"
    assert cat["fabric"] == "meos_civilization_os_planetary_resource_intelligence_framework"
    assert cat["foundation_gate"] == "P219"
    assert cat["mission_gate"] == "P219-A"
    assert cat["strategy_gate"] == "P219-B"
    assert cat["domain_gate"] == "P219-C"
    assert cat["planetary_gate"] == "P219-D"
    assert cat["ai_os_gate"] == "P219-E"
    assert cat["simulation_gate"] == "P219-F"
    assert cat["intelligence_nexus_gate"] == "P218-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["architecture"]["layer_count"] == 6
    assert cat["architecture"]["evolution_stage_count"] == 5
    assert cat["architecture"]["managed_domain_count"] == 6
    assert cat["energy"]["agent_count"] == 4
    assert cat["water"]["agent_count"] == 4
    assert cat["food"]["agent_count"] == 4
    assert cat["agents"]["agent_count"] == 12
    assert cat["optimization"]["cycle_step_count"] == 6
    assert cat["digital_twin"]["twin_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 4
    assert cat["aggregates"]["aggregate_count"] == 5
    assert cat["events"]["core_event_count"] == 11
    assert cat["cqrs"]["command_count"] == 6
    assert cat["knowledge_graph"]["node_count"] == 10
    assert cat["knowledge_graph"]["edge_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["never_replace_p219_foundation"] is True
    assert cat["never_replace_p219_f_simulation"] is True
    assert cat["never_ungated_resource_allocation_execution"] is True
    assert cat["never_bypass_circular_economy_safeguards"] is True
    assert cat["never_opaque_unexplainable_resource_decisions"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p219_h"] is True
    assert "GET /civilization/resources" in mod.resources_surface()["routes"]
    assert "sustainable human development and long-term planetary resilience" in cat["primary_capability"]


@pytest.mark.unit
def test_civ_resources_acl():
    from contexts.civilization.infrastructure.acl import civ_resources_acl as acls

    assert acls.to_civilization_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p219_foundation"] is True
    assert acls.to_civilization_mission(tenant_id="t1", mission_ref="m1")["never_replace_p219_a_mission"] is True
    assert acls.to_civilization_strategy(tenant_id="t1", strategy_ref="s1")["never_replace_p219_b_strategy"] is True
    assert acls.to_civilization_domain(tenant_id="t1", domain_ref="d1")["never_replace_p219_c_domain"] is True
    assert acls.to_civilization_planetary(tenant_id="t1", planetary_ref="p1")["never_replace_p219_d_planetary"] is True
    assert acls.to_civilization_ai_os(tenant_id="t1", aios_ref="a1")["never_replace_p219_e_ai_os"] is True
    assert acls.to_civilization_simulation(tenant_id="t1", simulation_ref="s1")["never_replace_p219_f_simulation"] is True
    assert acls.to_intelligence_nexus(tenant_id="t1", nexus_ref="n1")["never_replace_p218_z_intelligence_nexus"] is True
    assert acls.to_space(tenant_id="t1", space_ref="s1")["never_replace_space"] is True
    assert acls.to_biotechnology(tenant_id="t1", bio_ref="b1")["never_replace_biotechnology"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["never_replace_ai_platform"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_ungated_resource_allocation_execution"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_bypass_circular_economy_safeguards"] is True
    assert acls.to_enterprise_civilization(tenant_id="t1", resource_ref="r1")["never_replace_p219_f_simulation"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_resources():
    svc = get_civilization_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_resources"]["prompt_id"] == "P219-G"
    assert catalog["platform_resources"]["foundation_for_p219_h"] is True
    assert svc.resources_readiness()["passed"] is True
