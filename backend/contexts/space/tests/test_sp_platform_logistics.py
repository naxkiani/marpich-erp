"""P218-O logistics intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_logistics_foundation import validate_sp_logistics_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_logistics as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_logistics_foundation():
    result = validate_sp_logistics_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-O"
    assert result["adr"] == 541
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"


@pytest.mark.unit
def test_sp_logistics_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-O"
    assert cat["fabric"] == "meos_space_logistics_intelligence_fabric"
    assert cat["resources_gate"] == "P218-N"
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["stage_count"] == 10
    assert cat["cargo"]["capability_count"] == 8
    assert cat["supply_chain"]["capability_count"] == 12
    assert cat["logistics_ai"]["model_count"] == 6
    assert cat["knowledge_graph"]["entity_count"] == 10
    assert cat["bounded_contexts"]["context_count"] == 8
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_n_resources"] is True
    assert cat["never_ungated_cargo_launch_authorization"] is True
    assert cat["never_skip_cargo_authentication"] is True
    assert cat["never_skip_supply_chain_security_controls"] is True
    assert cat["never_ungated_emergency_route_activation"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p218_p"] is True
    assert "GET /space/logistics" in mod.logistics_surface()["routes"]
    assert "autonomous logistics intelligence ecosystem" in cat["logistics_mission"]


@pytest.mark.unit
def test_sp_logistics_acl():
    from contexts.space.infrastructure.acl import sp_logistics_acl as acls

    assert acls.to_resources(tenant_id="t1", resources_ref="r1")["never_replace_p218_n_resources"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_cargo_launch_authorization"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_cargo_authentication"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_skip_supply_chain_security_controls"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", logistics_ref="l1")["module_local_logistics_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_logistics():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_logistics"]["prompt_id"] == "P218-O"
    assert svc.logistics_readiness()["passed"] is True
