"""P218-K scientific intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_scientific_foundation import validate_sp_scientific_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_scientific as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_scientific_foundation():
    result = validate_sp_scientific_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-K"
    assert result["adr"] == 537
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"


@pytest.mark.unit
def test_sp_scientific_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-K"
    assert cat["fabric"] == "meos_scientific_intelligence_fabric"
    assert cat["mission_intel_gate"] == "P218-J"
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["stage_count"] == 10
    assert cat["research"]["domain_count"] == 10
    assert cat["discovery"]["ai_capability_count"] == 8
    assert cat["scientific_ai"]["model_count"] == 8
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_j_mission_intel"] is True
    assert cat["never_ungated_autonomous_experiment_execution"] is True
    assert cat["never_skip_scientific_ethics_review"] is True
    assert cat["never_skip_peer_review_gate"] is True
    assert cat["never_skip_reproducibility_validation"] is True
    assert cat["never_violate_fair_data_principles"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p218_l"] is True
    assert "GET /space/scientific" in mod.scientific_surface()["routes"]
    assert "autonomously generating hypotheses" in cat["scientific_mission"]


@pytest.mark.unit
def test_sp_scientific_acl():
    from contexts.space.infrastructure.acl import sp_scientific_acl as acls

    assert acls.to_mission_intel(tenant_id="t1", mission_intel_ref="mi1")["never_replace_p218_j_mission_intel"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_autonomous_experiment_execution"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_scientific_ethics_review"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_skip_peer_review_gate"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", scientific_ref="s1")["module_local_scientific_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_scientific():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_scientific"]["prompt_id"] == "P218-K"
    assert svc.scientific_readiness()["passed"] is True
