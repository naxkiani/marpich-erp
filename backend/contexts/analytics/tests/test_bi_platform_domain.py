"""P213-C Enterprise BI domain architecture foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_domain_foundation import (
    validate_bi_domain_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import bi_platform_domain as pdom

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_domain_foundation():
    result = validate_bi_domain_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-C"
    assert result["adr"] == 396
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_domain_catalog():
    cat = pdom.catalog()
    assert cat["prompt_id"] == "P213-C"
    assert cat["adr"] == 396
    assert cat["principle"] == pdom.PRINCIPLE
    assert cat["fabric"] == pdom.FABRIC
    assert "governed" in cat["principle"]
    assert cat["complete_ddd_bi_architecture_present_required"] is True
    assert cat["strategic_domain_model_present_required"] is True
    assert cat["bounded_contexts_present_required"] is True
    assert cat["domains_loosely_coupled_required"] is True
    assert cat["bi_ownership_clear_required"] is True
    assert cat["aggregates_defined_required"] is True
    assert cat["entities_defined_required"] is True
    assert cat["value_objects_defined_required"] is True
    assert cat["domain_services_present_required"] is True
    assert cat["events_present_required"] is True
    assert cat["integration_boundaries_clear_required"] is True
    assert cat["cqrs_alignment_present_required"] is True
    assert cat["microservice_boundaries_clear_required"] is True
    assert cat["data_mesh_alignment_present_required"] is True
    assert cat["knowledge_graph_alignment_present_required"] is True
    assert cat["digital_twin_alignment_present_required"] is True
    assert cat["enterprise_governance_alignment_present_required"] is True
    assert cat["sibling_business_intelligence_bc_forbidden"] is True
    assert cat["domain_map"]["core_domain"] == (
        "enterprise_business_intelligence_management"
    )
    assert cat["domain_map"]["supporting_count"] >= 4
    assert cat["bounded_contexts"]["context_count"] >= 5
    assert cat["aggregates"]["aggregate_count"] >= 4
    assert cat["aggregates"]["major"]["enterprise_bi_asset"]["root"] == "BIAsset"
    assert cat["events"]["core_event_count"] >= 8
    assert cat["microservices"]["service_count"] >= 6
    assert cat["domain_services"]["service_count"] >= 5
    assert cat["entities"]["entity_count"] >= 10
    assert cat["value_objects"]["count"] >= 8
    assert cat["cursor_outputs"]["count"] >= 17
    assert cat["integrations"]["data_mesh"]["via_p212_f"] is True
    assert cat["integrations"]["knowledge_graph"]["via_p212_j"] is True
    assert cat["integrations"]["digital_twin"]["via_p212_l"] is True
    assert cat["deployment"]["cloud_native"] is True
    assert "domains_are_tightly_coupled" in cat["quality_gates"]["reject_if"]
    assert (
        "complete_ddd_bi_architecture_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P213-B" in cat["builds_on"]
    assert "P212-M" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/domain" in pdom.domain_surface()["routes"]
    assert "GET /analytics/domain/readiness" in pdom.domain_surface()["routes"]


@pytest.mark.unit
def test_bi_domain_acl():
    from contexts.analytics.infrastructure.acl import bi_domain_acl as acls

    assert acls.to_data_governance(tenant_id="t1", product_ref="p1")["via_p212"] is True
    assert acls.to_data_security(tenant_id="t1", asset_ref="a1")["via_p211"] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read"
    )["via_p208"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")["via_p207"] is True
    assert acls.to_knowledge_graph(tenant_id="t1", node_ref="n1")[
        "knowledge_graph_alignment_present_required"
    ] is True
    assert acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
        "digital_twin_alignment_present_required"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_domain():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_domain"]["prompt_id"] == "P213-C"
    assert catalog["platform_domain"]["adr"] == 396
    assert catalog["sor"] == "analytics"
    summary = svc.platform_domain()
    assert summary["prompt_id"] == "P213-C"
    assert summary["principle"] == pdom.PRINCIPLE
    assert summary["fabric"] == pdom.FABRIC
    assert "P213-B" in summary["builds_on"]
    assert summary["context_count"] >= 5
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.domain_readiness()["passed"] is True
