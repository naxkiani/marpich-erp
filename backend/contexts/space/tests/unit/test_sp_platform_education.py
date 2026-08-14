"""P218-S education intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_education_foundation import validate_sp_education_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_education as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_education_foundation():
    result = validate_sp_education_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-S"
    assert result["adr"] == 545
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"


@pytest.mark.unit
def test_sp_education_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-S"
    assert cat["fabric"] == "meos_space_education_intelligence_fabric"
    assert cat["commerce_gate"] == "P218-R"
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["stage_count"] == 10
    assert cat["learning"]["domain_count"] == 10
    assert cat["training"]["technology_count"] == 5
    assert cat["simulation"]["domain_count"] == 6
    assert cat["workforce"]["agent_count"] == 5
    assert cat["education_ai"]["model_count"] == 5
    assert cat["knowledge_graph"]["entity_count"] == 9
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_r_commerce"] is True
    assert cat["never_ungated_certification_issuance"] is True
    assert cat["never_skip_credential_verification"] is True
    assert cat["never_skip_research_ethics_review"] is True
    assert cat["never_opaque_unexplainable_education_decisions"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p218_t"] is True
    assert "GET /space/education" in mod.education_surface()["routes"]
    assert "intelligent global space education ecosystem capable of training" in cat["education_mission"]


@pytest.mark.unit
def test_sp_education_acl():
    from contexts.space.infrastructure.acl import sp_education_acl as acls

    assert acls.to_commerce(tenant_id="t1", commerce_ref="c1")["never_replace_p218_r_commerce"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_certification_issuance"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_skip_credential_verification"] is True
    assert acls.to_scientific(tenant_id="t1", scientific_ref="s1")["never_skip_research_ethics_review"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", education_ref="e1")["module_local_education_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_education():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_education"]["prompt_id"] == "P218-S"
    assert svc.education_readiness()["passed"] is True
