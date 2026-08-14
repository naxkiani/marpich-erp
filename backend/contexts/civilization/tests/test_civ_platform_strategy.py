"""P219-B civilization strategic architecture foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.civilization.application.civ_strategy_foundation import (
    validate_civ_strategy_foundation,
)
from contexts.civilization.container import get_civilization_service, reset_civilization_service
from contexts.civilization.domain.services import civ_platform_strategy as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_civilization_service()
    yield
    reset_civilization_service()


@pytest.mark.unit
def test_civ_strategy_foundation():
    result = validate_civ_strategy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P219-B"
    assert result["adr"] == 555
    assert result["sor"] == "civilization"
    assert result["capability"] == "CAP-PLT-CIV-001"


@pytest.mark.unit
def test_civ_strategy_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P219-B"
    assert cat["fabric"] == "meos_civilization_os_strategic_architecture_framework"
    assert cat["foundation_gate"] == "P219"
    assert cat["mission_gate"] == "P219-A"
    assert cat["intelligence_nexus_gate"] == "P218-Z"
    assert cat["space_gate"] == "P218"
    assert cat["architecture_layers"]["layer_count"] == 5
    assert cat["capability_model"]["domain_count"] == 8
    assert cat["operating_model"]["layer_count"] == 4
    assert cat["service_framework"]["category_count"] == 5
    assert cat["operating_framework"]["cycle_step_count"] == 7
    assert cat["governance"]["domain_count"] == 6
    assert cat["digital_twin"]["representation_count"] == 7
    assert cat["bounded_contexts"]["context_count"] == 6
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 8
    assert cat["never_replace_p219_foundation"] is True
    assert cat["never_replace_p219_a_mission"] is True
    assert cat["never_replace_space"] is True
    assert cat["never_replace_p218_z_intelligence_nexus"] is True
    assert cat["never_opaque_unexplainable_civilization_architecture_decisions"] is True
    assert cat["never_ungated_civilization_decision_architecture"] is True
    assert cat["foundation_for_p219_c"] is True
    assert "GET /civilization/strategy" in mod.strategy_surface()["routes"]
    assert "unified enterprise framework where" in cat["architecture_vision"]


@pytest.mark.unit
def test_civ_strategy_acl():
    from contexts.civilization.infrastructure.acl import civ_strategy_acl as acls

    assert acls.to_civilization_foundation(tenant_id="t1", foundation_ref="f1")["never_replace_p219_foundation"] is True
    assert acls.to_civilization_mission(tenant_id="t1", mission_ref="m1")["never_replace_p219_a_mission"] is True
    assert acls.to_intelligence_nexus(tenant_id="t1", nexus_ref="n1")["never_replace_p218_z_intelligence_nexus"] is True
    assert acls.to_space(tenant_id="t1", space_ref="s1")["never_replace_space"] is True
    assert acls.to_biotechnology(tenant_id="t1", bio_ref="b1")["never_replace_biotechnology"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_p216_z"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["never_replace_ai_platform"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_opaque_unexplainable_civilization_architecture_decisions"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_ungated_civilization_decision_architecture"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_violate_human_sovereignty_architecture"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_strategy():
    svc = get_civilization_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_strategy"]["prompt_id"] == "P219-B"
    assert catalog["platform_strategy"]["foundation_for_p219_c"] is True
    assert svc.strategy_readiness()["passed"] is True
