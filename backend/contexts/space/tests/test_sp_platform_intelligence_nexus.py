"""P218-Z final intelligence nexus foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_intelligence_nexus_foundation import (
    validate_sp_intelligence_nexus_foundation,
)
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_intelligence_nexus as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_intelligence_nexus_foundation():
    result = validate_sp_intelligence_nexus_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-Z"
    assert result["adr"] == 552
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"
    assert result["series_complete"] is True


@pytest.mark.unit
def test_sp_intelligence_nexus_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-Z"
    assert cat["fabric"] == "meos_final_intelligence_nexus_fabric"
    assert cat["ultimate_governance_gate"] == "P218-Y"
    assert cat["architecture"]["layer_count"] == 6
    assert cat["lifecycle"]["stage_count"] == 10
    assert cat["nexus_core"]["capability_count"] == 7
    assert cat["control_plane"]["domain_count"] == 7
    assert cat["autonomous"]["domain_count"] == 7
    assert cat["orchestration"]["agent_ecosystem_count"] == 8
    assert cat["decision_engine"]["model_count"] == 6
    assert cat["knowledge_graph"]["entity_count"] == 11
    assert cat["digital_twin"]["representation_count"] == 8
    assert cat["agent_ecosystem"]["agent_count"] == 8
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_y_ultimate_governance"] is True
    assert cat["never_replace_p218_x_singularity"] is True
    assert cat["never_replace_p218_w_collective_si"] is True
    assert cat["never_replace_p218_v_human_gi"] is True
    assert cat["never_replace_p218_u_human_evolution"] is True
    assert cat["never_replace_p218_t_civilization"] is True
    assert cat["never_ungated_supreme_decision"] is True
    assert cat["never_skip_intelligence_alignment"] is True
    assert cat["never_violate_human_sovereignty"] is True
    assert cat["never_skip_ethical_validation"] is True
    assert cat["never_opaque_unexplainable_intelligence_decisions"] is True
    assert cat["never_skip_human_authority_preservation"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["series_complete"] is True
    assert cat["meos_final_intelligence_nexus_complete"] is True
    assert "GET /space/intelligence-nexus" in mod.intelligence_nexus_surface()["routes"]
    assert "final intelligence coordination architecture capable of integrating" in cat["nexus_mission"]


@pytest.mark.unit
def test_sp_intelligence_nexus_acl():
    from contexts.space.infrastructure.acl import sp_intelligence_nexus_acl as acls

    assert acls.to_ultimate_governance(tenant_id="t1", ultimate_governance_ref="ug1")["never_replace_p218_y_ultimate_governance"] is True
    assert acls.to_singularity(tenant_id="t1", singularity_ref="s1")["never_replace_p218_x_singularity"] is True
    assert acls.to_collective_si(tenant_id="t1", collective_si_ref="csi1")["never_replace_p218_w_collective_si"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_supreme_decision"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_authority_preservation"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_violate_human_sovereignty"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", intelligence_nexus_ref="n1")["series_complete"] is True
    assert acls.to_enterprise_space(tenant_id="t1", intelligence_nexus_ref="n1")["module_local_intelligence_nexus_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_intelligence_nexus():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_intelligence_nexus"]["prompt_id"] == "P218-Z"
    assert catalog["platform_intelligence_nexus"]["series_complete"] is True
    assert svc.intelligence_nexus_readiness()["passed"] is True
