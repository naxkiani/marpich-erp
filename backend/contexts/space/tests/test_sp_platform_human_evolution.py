"""P218-U human evolution intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_human_evolution_foundation import validate_sp_human_evolution_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_human_evolution as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_human_evolution_foundation():
    result = validate_sp_human_evolution_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-U"
    assert result["adr"] == 547
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"


@pytest.mark.unit
def test_sp_human_evolution_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-U"
    assert cat["fabric"] == "meos_human_evolution_intelligence_fabric"
    assert cat["civilization_gate"] == "P218-T"
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["stage_count"] == 10
    assert cat["augmentation"]["capability_count"] == 5
    assert cat["symbiosis"]["domain_count"] == 7
    assert cat["cognitive"]["ai_component_count"] == 5
    assert cat["neural"]["security_principle_count"] == 4
    assert cat["evolution_ai"]["model_count"] == 5
    assert cat["knowledge_graph"]["entity_count"] == 9
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_t_civilization"] is True
    assert cat["never_ungated_augmentation_approval"] is True
    assert cat["never_skip_human_consent"] is True
    assert cat["never_skip_ethical_augmentation_review"] is True
    assert cat["never_violate_human_sovereignty"] is True
    assert cat["never_opaque_unexplainable_evolution_decisions"] is True
    assert cat["never_skip_neural_data_privacy"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p218_v"] is True
    assert "GET /space/human-evolution" in mod.human_evolution_surface()["routes"]
    assert "intelligent platform that enables humanity to safely extend" in cat["evolution_mission"]


@pytest.mark.unit
def test_sp_human_evolution_acl():
    from contexts.space.infrastructure.acl import sp_human_evolution_acl as acls

    assert acls.to_civilization(tenant_id="t1", civilization_ref="c1")["never_replace_p218_t_civilization"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_augmentation_approval"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_human_consent"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_violate_human_sovereignty"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", human_evolution_ref="h1")["module_local_human_evolution_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_human_evolution():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_human_evolution"]["prompt_id"] == "P218-U"
    assert svc.human_evolution_readiness()["passed"] is True
