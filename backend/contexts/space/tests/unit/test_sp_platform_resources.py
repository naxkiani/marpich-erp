"""P218-N resource intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_resources_foundation import validate_sp_resources_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_resources as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_resources_foundation():
    result = validate_sp_resources_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-N"
    assert result["adr"] == 540
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"


@pytest.mark.unit
def test_sp_resources_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-N"
    assert cat["fabric"] == "meos_space_resource_intelligence_fabric"
    assert cat["manufacturing_gate"] == "P218-M"
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["stage_count"] == 10
    assert cat["isru"]["capability_count"] == 7
    assert cat["asteroid"]["target_count"] == 4
    assert cat["resource_ai"]["model_count"] == 5
    assert cat["autonomy"]["agent_count"] == 7
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_m_manufacturing"] is True
    assert cat["never_ungated_resource_extraction_authorization"] is True
    assert cat["never_skip_resource_environmental_assessment"] is True
    assert cat["never_skip_planetary_protection_for_extraction"] is True
    assert cat["never_violate_circular_resource_economy_principles"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p218_o"] is True
    assert "GET /space/resources" in mod.resources_surface()["routes"]
    assert "intelligent planetary-scale resource platform" in cat["resources_mission"]


@pytest.mark.unit
def test_sp_resources_acl():
    from contexts.space.infrastructure.acl import sp_resources_acl as acls

    assert acls.to_manufacturing(tenant_id="t1", manufacturing_ref="m1")["never_replace_p218_m_manufacturing"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_resource_extraction_authorization"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_resource_environmental_assessment"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_skip_planetary_protection_for_extraction"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", resources_ref="r1")["module_local_resources_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_resources():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_resources"]["prompt_id"] == "P218-N"
    assert svc.resources_readiness()["passed"] is True
