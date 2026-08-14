"""P218-M manufacturing intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_manufacturing_foundation import validate_sp_manufacturing_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_manufacturing as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_manufacturing_foundation():
    result = validate_sp_manufacturing_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-M"
    assert result["adr"] == 539
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"


@pytest.mark.unit
def test_sp_manufacturing_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-M"
    assert cat["fabric"] == "meos_space_manufacturing_intelligence_fabric"
    assert cat["exploration_gate"] == "P218-L"
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["stage_count"] == 10
    assert cat["in_orbit"]["capability_count"] == 8
    assert cat["industrial"]["infrastructure_count"] == 7
    assert cat["manufacturing_ai"]["model_count"] == 6
    assert cat["autonomy"]["agent_count"] == 8
    assert cat["knowledge_graph"]["entity_count"] == 10
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_l_exploration"] is True
    assert cat["never_ungated_autonomous_factory_production"] is True
    assert cat["never_skip_quality_validation"] is True
    assert cat["never_skip_industrial_safety_certification"] is True
    assert cat["never_violate_circular_space_economy_principles"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p218_n"] is True
    assert "GET /space/manufacturing" in mod.manufacturing_surface()["routes"]
    assert "autonomous space industrial ecosystem" in cat["manufacturing_mission"]


@pytest.mark.unit
def test_sp_manufacturing_acl():
    from contexts.space.infrastructure.acl import sp_manufacturing_acl as acls

    assert acls.to_exploration(tenant_id="t1", exploration_ref="e1")["never_replace_p218_l_exploration"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_autonomous_factory_production"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_quality_validation"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_skip_industrial_safety_certification"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", manufacturing_ref="m1")["module_local_manufacturing_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_manufacturing():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_manufacturing"]["prompt_id"] == "P218-M"
    assert svc.manufacturing_readiness()["passed"] is True
