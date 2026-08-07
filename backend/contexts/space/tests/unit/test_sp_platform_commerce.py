"""P218-R commerce intelligence foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.space.application.sp_commerce_foundation import validate_sp_commerce_foundation
from contexts.space.container import get_space_service, reset_space_service
from contexts.space.domain.services import sp_platform_commerce as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_space_service()
    yield
    reset_space_service()


@pytest.mark.unit
def test_sp_commerce_foundation():
    result = validate_sp_commerce_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["prompt"] == "P218-R"
    assert result["adr"] == 544
    assert result["sor"] == "space"
    assert result["capability"] == "CAP-PLT-SP-001"


@pytest.mark.unit
def test_sp_commerce_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P218-R"
    assert cat["fabric"] == "meos_space_commerce_intelligence_fabric"
    assert cat["sustainability_gate"] == "P218-Q"
    assert cat["architecture"]["layer_count"] == 5
    assert cat["lifecycle"]["stage_count"] == 10
    assert cat["marketplace"]["domain_count"] == 7
    assert cat["operations"]["capability_count"] == 6
    assert cat["economy"]["model_count"] == 5
    assert cat["investment"]["agent_count"] == 4
    assert cat["commerce_ai"]["model_count"] == 5
    assert cat["knowledge_graph"]["entity_count"] == 10
    assert cat["bounded_contexts"]["context_count"] == 7
    assert cat["microservices"]["service_count"] == 10
    assert cat["events"]["core_event_count"] == 10
    assert cat["never_replace_p218_q_sustainability"] is True
    assert cat["never_ungated_commercial_transaction"] is True
    assert cat["never_skip_marketplace_identity_verification"] is True
    assert cat["never_skip_contract_compliance_validation"] is True
    assert cat["never_opaque_unexplainable_commerce_decisions"] is True
    assert cat["never_duplicate_financial_kernel"] is True
    assert cat["space_ai_via_p214z_acl_only"] is True
    assert cat["no_module_local_llm"] is True
    assert cat["foundation_for_p218_s"] is True
    assert "GET /space/commerce" in mod.commerce_surface()["routes"]
    assert "intelligent commercial ecosystem enabling companies" in cat["commerce_mission"]


@pytest.mark.unit
def test_sp_commerce_acl():
    from contexts.space.infrastructure.acl import sp_commerce_acl as acls

    assert acls.to_sustainability(tenant_id="t1", sustainability_ref="s1")["never_replace_p218_q_sustainability"] is True
    assert acls.to_financial_kernel(tenant_id="t1", financial_ref="f1")["never_duplicate_financial_kernel"] is True
    assert acls.to_policy_engine(tenant_id="t1", policy_ref="p1")["never_ungated_commercial_transaction"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["never_skip_marketplace_identity_verification"] is True
    assert acls.to_master_ai(tenant_id="t1", master_ai_ref="a1")["space_ai_via_p214z_acl_only"] is True
    assert acls.to_enterprise_space(tenant_id="t1", commerce_ref="c1")["module_local_commerce_forbidden"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_commerce():
    svc = get_space_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_commerce"]["prompt_id"] == "P218-R"
    assert svc.commerce_readiness()["passed"] is True
