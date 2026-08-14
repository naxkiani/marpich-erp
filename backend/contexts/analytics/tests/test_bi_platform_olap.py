"""P213-G BI OLAP / semantic foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_olap_foundation import (
    validate_bi_olap_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import bi_platform_olap as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_olap_foundation():
    result = validate_bi_olap_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-G"
    assert result["adr"] == 411
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_olap_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P213-G"
    assert cat["adr"] == 411
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "governed semantic definition" in cat["principle"]
    assert cat["enterprise_semantic_layer_present_required"] is True
    assert cat["enterprise_metric_platform_present_required"] is True
    assert cat["kpi_governance_present_required"] is True
    assert cat["olap_platform_present_required"] is True
    assert cat["calculation_engine_present_required"] is True
    assert cat["sibling_business_intelligence_bc_forbidden"] is True
    assert cat["domain_model"]["core_domain"] == (
        "enterprise_semantic_intelligence_management"
    )
    assert cat["domain_model"]["aggregate"]["name"] == "SemanticModelAggregate"
    assert cat["bounded_contexts"]["context_count"] >= 5
    assert cat["metrics"]["class_count"] >= 13
    assert cat["kpi_governance"]["lifecycle_step_count"] >= 8
    assert cat["dimensions"]["dimension_count"] >= 14
    assert cat["ai_native"]["agent_count"] >= 6
    assert cat["events"]["core_event_count"] >= 7
    assert cat["microservices"]["service_count"] >= 8
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "enterprise_semantic_layer_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P213-F" in cat["builds_on"]
    assert "P212-J" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/olap" in mod.olap_surface()["routes"]
    assert "GET /analytics/olap/ai" in mod.olap_surface()["routes"]


@pytest.mark.unit
def test_bi_olap_acl():
    from contexts.analytics.infrastructure.acl import bi_olap_acl as acls

    assert acls.to_knowledge_graph(tenant_id="t1", node_ref="n1")[
        "via_p212_j"
    ] is True
    assert acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
        "via_p212_l"
    ] is True
    assert acls.to_warehouse(tenant_id="t1", warehouse_ref="w1")[
        "via_p213_e"
    ] is True
    assert acls.to_lakehouse(tenant_id="t1", lakehouse_ref="lh1")[
        "via_p213_f"
    ] is True
    assert acls.to_reporting(tenant_id="t1", report_ref="r1")[
        "via_p213_d"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read"
    )["attribute_based_access_control"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_enterprise_search(tenant_id="t1", query_ref="q1")[
        "via_enterprise_search"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_olap():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_olap"]["prompt_id"] == "P213-G"
    assert catalog["platform_olap"]["adr"] == 411
    assert catalog["sor"] == "analytics"
    summary = svc.platform_olap()
    assert summary["prompt_id"] == "P213-G"
    assert summary["principle"] == mod.PRINCIPLE
    assert summary["fabric"] == mod.FABRIC
    assert "P213-F" in summary["builds_on"]
    assert summary["context_count"] >= 5
    assert summary["metric_class_count"] >= 13
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.olap_readiness()["passed"] is True
    assert svc.olap_ai()["agent_count"] >= 6
    assert svc.olap_kpi_governance()["lifecycle_step_count"] >= 8
