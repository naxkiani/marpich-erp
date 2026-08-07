"""P218-L exploration intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_exploration_foundation import validate_sp_exploration_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_exploration as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_exploration_foundation():
    result = validate_sp_exploration_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-L"
    assert result["adr"] == 538
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"


@pytest.mark.unit
def test_sp_exploration_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-L"
    assert cat["fabric"] == "meos_space_exploration_intelligence_fabric"
    assert cat["scientific_gate"] == "P218-K"
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["stage_count"] == 10
    assert cat["lunar"]["capability_count"] == 10
    assert cat["mars"]["mission_type_count"] == 6
    assert cat["exploration_ai"]["model_count"] == 6
    assert cat["autonomy"]["agent_count"] == 8
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_k_scientific"] is True
    assert cat["never_ungated_planetary_landing_authorization"] is True
    assert cat["never_skip_planetary_protection_compliance"] is True
    assert cat["never_ungated_surface_hazard_response"] is True
    assert cat["never_skip_crew_safety_validation"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p218_m"] is True
    assert "GET /space/exploration" in mod.exploration_surface()["routes"]
    assert "autonomous, resilient and continuously learning" in cat["exploration_mission"]


@pytest.mark.unit
def test_sp_exploration_acl():
    from contexts.space.infrastructure.acl import sp_exploration_acl as acls

    assert acls.to_scientific(tenant_id="t1", scientific_ref="s1")["never_replace_p218_k_scientific"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_planetary_landing_authorization"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_planetary_protection_compliance"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_skip_crew_safety_validation"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", exploration_ref="e1")["module_local_exploration_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_exploration():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_exploration"]["prompt_id"] == "P218-L"
    assert svc.exploration_readiness()["passed"] is True
