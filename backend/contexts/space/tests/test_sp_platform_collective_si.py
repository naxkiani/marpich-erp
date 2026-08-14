"""P218-W collective super intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_collective_si_foundation import validate_sp_collective_si_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_collective_si as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_collective_si_foundation():
    result = validate_sp_collective_si_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-W"
    assert result["adr"] == 549
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"


@pytest.mark.unit
def test_sp_collective_si_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-W"
    assert cat["fabric"] == "meos_collective_intelligence_fabric"
    assert cat["human_gi_gate"] == "P218-V"
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["stage_count"] == 10
    assert cat["collective_si"]["capability_count"] == 7
    assert cat["civilization_network"]["participant_count"] == 7
    assert cat["cognitive_ecosystem"]["domain_count"] == 8
    assert cat["collective_reasoning"]["agent_count"] == 5
    assert cat["knowledge_graph"]["entity_count"] == 9
    assert cat["alignment"]["human_contribution_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 6
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_v_human_gi"] is True
    assert cat["never_replace_p218_u_human_evolution"] is True
    assert cat["never_replace_p218_t_civilization"] is True
    assert cat["never_ungated_collective_decision"] is True
    assert cat["never_skip_intelligence_alignment"] is True
    assert cat["never_violate_human_sovereignty"] is True
    assert cat["never_skip_ethical_validation"] is True
    assert cat["never_opaque_unexplainable_intelligence_decisions"] is True
    assert cat["never_skip_human_authority_preservation"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p218_x"] is True
    assert "GET /space/collective-si" in mod.collective_si_surface()["routes"]
    assert "global intelligence ecosystem where humans, AI systems" in cat["csi_mission"]


@pytest.mark.unit
def test_sp_collective_si_acl():
    from contexts.space.infrastructure.acl import sp_collective_si_acl as acls

    assert acls.to_human_gi(tenant_id="t1", human_gi_ref="g1")["never_replace_p218_v_human_gi"] is True
    assert acls.to_human_evolution(tenant_id="t1", human_evolution_ref="h1")["never_replace_p218_u_human_evolution"] is True
    assert acls.to_civilization(tenant_id="t1", civilization_ref="c1")["never_replace_p218_t_civilization"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_collective_decision"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_intelligence_alignment"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_violate_human_sovereignty"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", collective_si_ref="csi1")["module_local_collective_si_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_collective_si():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_collective_si"]["prompt_id"] == "P218-W"
    assert svc.collective_si_readiness()["passed"] is True
