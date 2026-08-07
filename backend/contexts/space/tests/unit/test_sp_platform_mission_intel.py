"""P218-J mission intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_mission_intel_foundation import validate_sp_mission_intel_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_mission_intel as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_mission_intel_foundation():
    result = validate_sp_mission_intel_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-J"
    assert result["adr"] == 536
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"


@pytest.mark.unit
def test_sp_mission_intel_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-J"
    assert cat["fabric"] == "meos_mission_intelligence_fabric"
    assert cat["navigation_gate"] == "P218-I"
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["stage_count"] == 15
    assert cat["planning"]["domain_count"] == 10
    assert cat["mission_ai"]["model_count"] == 6
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 13
    assert cat["never_replace_p218_a_mission"] is True
    assert cat["never_replace_p218_i_navigation"] is True
    assert cat["never_ungated_mission_launch_authorization"] is True
    assert cat["never_skip_mission_readiness_review"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p218_k"] is True
    assert "GET /space/mission-intel" in mod.mission_intel_surface()["routes"]
    assert "unified enterprise platform capable of planning, executing, monitoring" in cat["mission_intel_mission"]


@pytest.mark.unit
def test_sp_mission_intel_acl():
    from contexts.space.infrastructure.acl import sp_mission_intel_acl as acls

    assert acls.to_space_mission(tenant_id="t1", mission_ref="m1")["never_replace_p218_a_mission"] is True
    assert acls.to_navigation(tenant_id="t1", navigation_ref="n1")["never_replace_p218_i_navigation"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_mission_launch_authorization"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_mission_readiness_review"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", mission_intel_ref="mi1")["module_local_mission_intel_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_mission_intel():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_mission_intel"]["prompt_id"] == "P218-J"
    assert svc.mission_intel_readiness()["passed"] is True
