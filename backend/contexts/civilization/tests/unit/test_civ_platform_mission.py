"""P219-A civilization mission / vision / strategy foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.civilization.application.civ_mission_foundation import (
    validate_civ_mission_foundation,
)
from contexts.civilization.container import get_civilization_service, reset_civilization_service
from contexts.civilization.domain.services import civ_platform_mission as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_civilization_service()
    yield
    reset_civilization_service()


@pytest.mark.unit
def test_civ_mission_foundation():
    result = validate_civ_mission_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P219-A"
    assert result["adr"] == 554
    assert result["sor"] == "civilization"
    assert result["capability"] == "CAP-PLT-CIV-001"


@pytest.mark.unit
def test_civ_mission_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P219-A"
    assert cat["fabric"] == "meos_civilization_os_strategic_framework"
    assert cat["foundation_gate"] == "P219"
    assert cat["intelligence_nexus_gate"] == "P218-Z"
    assert cat["space_gate"] == "P218"
    assert cat["bio_gate"] == "P217-Z"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["civilization_os_mission_framework_present_required"] is True
    assert cat["civilization_os_vision_framework_present_required"] is True
    assert cat["strategic_civilization_scope_present_required"] is True
    assert cat["civilization_os_capability_framework_present_required"] is True
    assert cat["strategic_pillars_framework_present_required"] is True
    assert cat["maturity_model_present_required"] is True
    assert cat["governance_framework_present_required"] is True
    assert cat["meos_integration_strategy_present_required"] is True
    assert cat["future_evolution_roadmap_present_required"] is True
    assert cat["bounded_contexts"]["context_count"] >= 7
    assert cat["objectives"]["objective_count"] >= 7
    assert cat["strategic_scope"]["domain_count"] == 7
    assert cat["capability_framework"]["group_count"] == 8
    assert cat["value_streams"]["stream_count"] >= 10
    assert cat["value_streams"]["pillars"]["pillar_count"] == 6
    assert cat["maturity_model"]["level_count"] == 5
    assert cat["never_replace_p219_foundation"] is True
    assert cat["never_replace_space"] is True
    assert cat["never_replace_p218_z_intelligence_nexus"] is True
    assert cat["never_opaque_unexplainable_civilization_strategy"] is True
    assert cat["never_ungated_civilization_decision_strategy"] is True
    assert cat["foundation_for_p219_b"] is True
    assert "GET /civilization/mission" in mod.mission_surface()["routes"]
    assert "unified intelligent operating foundation" in cat["mission_statement"]


@pytest.mark.unit
def test_civ_mission_acl():
    from contexts.civilization.infrastructure.acl import civ_mission_acl as acls

    assert acls.to_civilization_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p219_foundation"] is True
    assert acls.to_intelligence_nexus(tenant_id="t1", nexus_ref="n1")["never_replace_p218_z_intelligence_nexus"] is True
    assert acls.to_space(tenant_id="t1", space_ref="s1")["never_replace_space"] is True
    assert acls.to_space(tenant_id="t1", space_ref="s1")["never_merge_p218_t_space_civilization"] is True
    assert acls.to_biotechnology(tenant_id="t1", bio_ref="b1")["never_replace_biotechnology"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["never_replace_ai_platform"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_skip_ethical_civilization_governance_strategy"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_opaque_unexplainable_civilization_strategy"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_ungated_civilization_decision_strategy"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_violate_human_sovereignty_strategy"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mission():
    svc = get_civilization_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_mission"]["prompt_id"] == "P219-A"
    assert catalog["platform_mission"]["foundation_for_p219_b"] is True
    assert svc.mission_readiness()["passed"] is True
