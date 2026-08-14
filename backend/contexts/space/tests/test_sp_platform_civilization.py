"""P218-T civilization intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_civilization_foundation import validate_sp_civilization_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_civilization as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_civilization_foundation():
    result = validate_sp_civilization_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-T"
    assert result["adr"] == 546
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"


@pytest.mark.unit
def test_sp_civilization_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-T"
    assert cat["fabric"] == "meos_space_civilization_intelligence_fabric"
    assert cat["education_gate"] == "P218-S"
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["stage_count"] == 10
    assert cat["society"]["domain_count"] == 5
    assert cat["governance_platform"]["agent_count"] == 5
    assert cat["future_architecture"]["architecture_domain_count"] == 6
    assert cat["civilization_ai"]["model_count"] == 5
    assert cat["knowledge_graph"]["entity_count"] == 9
    assert cat["ethics"]["domain_count"] == 5
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_s_education"] is True
    assert cat["never_ungated_governance_decision"] is True
    assert cat["never_skip_ethical_ai_review"] is True
    assert cat["never_skip_human_rights_protection"] is True
    assert cat["never_opaque_unexplainable_civilization_decisions"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p218_u"] is True
    assert "GET /space/civilization" in mod.civilization_surface()["routes"]
    assert "intelligent civilization operating platform capable of modeling" in cat["civilization_mission"]


@pytest.mark.unit
def test_sp_civilization_acl():
    from contexts.space.infrastructure.acl import sp_civilization_acl as acls

    assert acls.to_education(tenant_id="t1", education_ref="e1")["never_replace_p218_s_education"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_governance_decision"] is True
    assert acls.to_workflow(tenant_id="t1", workflow_ref="w1")["never_skip_ethical_ai_review"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_skip_human_rights_protection"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", civilization_ref="c1")["module_local_civilization_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_civilization():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_civilization"]["prompt_id"] == "P218-T"
    assert svc.civilization_readiness()["passed"] is True
