"""P218-Q sustainability intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_sustainability_foundation import validate_sp_sustainability_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_sustainability as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_sustainability_foundation():
    result = validate_sp_sustainability_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-Q"
    assert result["adr"] == 543
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"


@pytest.mark.unit
def test_sp_sustainability_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-Q"
    assert cat["fabric"] == "meos_space_sustainability_intelligence_fabric"
    assert cat["security_gate"] == "P218-P"
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["stage_count"] == 10
    assert cat["orbital_environment"]["capability_count"] == 6
    assert cat["debris"]["domain_count"] == 6
    assert cat["sustainability_ai"]["model_count"] == 6
    assert cat["autonomy"]["agent_count"] == 5
    assert cat["knowledge_graph"]["entity_count"] == 9
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_p_security"] is True
    assert cat["never_ungated_debris_cleanup_mission"] is True
    assert cat["never_skip_planetary_protection_compliance"] is True
    assert cat["never_skip_environmental_impact_assessment"] is True
    assert cat["never_opaque_unexplainable_sustainability_decisions"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p218_r"] is True
    assert "GET /space/sustainability" in mod.sustainability_surface()["routes"]
    assert "intelligent sustainability platform capable of monitoring" in cat["sustainability_mission"]


@pytest.mark.unit
def test_sp_sustainability_acl():
    from contexts.space.infrastructure.acl import sp_sustainability_acl as acls

    assert acls.to_security(tenant_id="t1", security_ref="s1")["never_replace_p218_p_security"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_debris_cleanup_mission"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_planetary_protection_compliance"] is True
    assert acls.to_exploration(tenant_id="t1", exploration_ref="e1")["never_skip_planetary_protection_compliance"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", sustainability_ref="sus1")["module_local_sustainability_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_sustainability():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_sustainability"]["prompt_id"] == "P218-Q"
    assert svc.sustainability_readiness()["passed"] is True
