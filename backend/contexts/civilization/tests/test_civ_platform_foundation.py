"""P219 civilization OS foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.civilization.application.civ_foundation_foundation import (
    validate_civ_foundation_foundation,
)
from contexts.civilization.container import get_civilization_service, reset_civilization_service
from contexts.civilization.domain.services import civ_platform_foundation as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_civilization_service()
    yield
    reset_civilization_service()


@pytest.mark.unit
def test_civ_foundation_foundation():
    result = validate_civ_foundation_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P219"
    assert result["adr"] == 553
    assert result["sor"] == "civilization"
    assert result["capability"] == "CAP-PLT-CIV-001"


@pytest.mark.unit
def test_civ_foundation_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P219"
    assert cat["fabric"] == "meos_civilization_operating_system_fabric"
    assert cat["intelligence_nexus_gate"] == "P218-Z"
    assert cat["space_gate"] == "P218"
    assert cat["bio_gate"] == "P217-Z"
    assert cat["robotics_gate"] == "P216-Z"
    assert cat["quantum_gate"] == "P215-Z"
    assert cat["ai_gate"] == "P214-Z"
    assert cat["civilization_operating_system_present_required"] is True
    assert cat["civilization_os_kernel_present_required"] is True
    assert cat["planetary_intelligence_governance_present_required"] is True
    assert cat["global_infrastructure_intelligence_present_required"] is True
    assert cat["architecture"]["layer_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 8
    assert cat["domain_model"]["entity_count"] == 7
    assert cat["agents"]["agent_count"] == 7
    assert cat["never_replace_space"] is True
    assert cat["never_replace_p218_z_intelligence_nexus"] is True
    assert cat["never_merge_p218_t_space_civilization"] is True
    assert cat["never_ungated_civilization_decision"] is True
    assert cat["never_opaque_unexplainable_civilization_decisions"] is True
    assert cat["never_skip_human_authority"] is True
    assert cat["foundation_for_p219_a"] is True
    assert "GET /civilization/foundation" in mod.foundation_surface()["routes"]
    assert "MEOS Civilization Operating System Platform SHALL unify" in cat["civilization_vision"]


@pytest.mark.unit
def test_civ_foundation_acl():
    from contexts.civilization.infrastructure.acl import civ_foundation_acl as acls

    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="m1")["module_local_llm_forbidden"] is True
    assert acls.to_quantum_supreme(tenant_id="t1", supreme_ref="z1")["never_replace_p215_z"] is True
    assert acls.to_robotics_supreme(tenant_id="t1", robotics_ref="r1")["never_replace_robotics_supreme"] is True
    assert acls.to_biotechnology(tenant_id="t1", bio_ref="b1")["never_replace_biotechnology"] is True
    assert acls.to_space(tenant_id="t1", space_ref="s1")["never_replace_space"] is True
    assert acls.to_space(tenant_id="t1", space_ref="s1")["never_merge_p218_t_space_civilization"] is True
    assert acls.to_intelligence_nexus(tenant_id="t1", nexus_ref="n1")["never_replace_p218_z_intelligence_nexus"] is True
    assert acls.to_integration(tenant_id="t1", connector_ref="c1")["external_systems_via_integration_platform_only"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_ungated_civilization_decision"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_authority"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_violate_human_sovereignty"] is True
    assert acls.to_core_platform(tenant_id="t1", core_ref="c1")["never_replace_core_platform"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_foundation():
    svc = get_civilization_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_foundation"]["prompt_id"] == "P219"
    assert catalog["platform_foundation"]["foundation_for_p219_a"] is True
    assert svc.foundation_readiness()["passed"] is True
