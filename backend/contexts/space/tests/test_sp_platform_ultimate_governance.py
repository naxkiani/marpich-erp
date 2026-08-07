"""P218-Y ultimate intelligence governance foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_ultimate_governance_foundation import (
    validate_sp_ultimate_governance_foundation,
)
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_ultimate_governance as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_ultimate_governance_foundation():
    result = validate_sp_ultimate_governance_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-Y"
    assert result["adr"] == 551
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"


@pytest.mark.unit
def test_sp_ultimate_governance_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-Y"
    assert cat["fabric"] == "meos_ultimate_intelligence_governance_fabric"
    assert cat["singularity_gate"] == "P218-X"
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["stage_count"] == 10
    assert cat["ultimate_governance"]["capability_count"] == 7
    assert cat["alignment"]["agent_count"] == 5
    assert cat["trust"]["trust_model_count"] == 5
    assert cat["ethics"]["domain_count"] == 7
    assert cat["safety"]["agent_count"] == 5
    assert cat["knowledge_graph"]["entity_count"] == 9
    assert cat["operating_model"]["layer_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 6
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_x_singularity"] is True
    assert cat["never_replace_p218_w_collective_si"] is True
    assert cat["never_replace_p218_v_human_gi"] is True
    assert cat["never_replace_p218_u_human_evolution"] is True
    assert cat["never_replace_p218_t_civilization"] is True
    assert cat["never_ungated_governance_decision"] is True
    assert cat["never_skip_intelligence_alignment"] is True
    assert cat["never_violate_human_sovereignty"] is True
    assert cat["never_skip_ethical_validation"] is True
    assert cat["never_opaque_unexplainable_intelligence_decisions"] is True
    assert cat["never_skip_human_authority_preservation"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p218_z"] is True
    assert "GET /space/ultimate-governance" in mod.ultimate_governance_surface()["routes"]
    assert "civilization-scale governance platform capable of ensuring" in cat["ug_mission"]


@pytest.mark.unit
def test_sp_ultimate_governance_acl():
    from contexts.space.infrastructure.acl import sp_ultimate_governance_acl as acls

    assert acls.to_singularity(tenant_id="t1", singularity_ref="s1")["never_replace_p218_x_singularity"] is True
    assert acls.to_collective_si(tenant_id="t1", collective_si_ref="csi1")["never_replace_p218_w_collective_si"] is True
    assert acls.to_human_gi(tenant_id="t1", human_gi_ref="g1")["never_replace_p218_v_human_gi"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_governance_decision"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_ethical_validation"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_violate_human_sovereignty"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", ultimate_governance_ref="ug1")["module_local_ultimate_governance_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_ultimate_governance():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_ultimate_governance"]["prompt_id"] == "P218-Y"
    assert svc.ultimate_governance_readiness()["passed"] is True
