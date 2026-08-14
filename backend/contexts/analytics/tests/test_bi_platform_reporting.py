"""P213-D BI reporting foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_reporting_foundation import (
    validate_bi_reporting_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import bi_platform_reporting as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_reporting_foundation():
    result = validate_bi_reporting_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-D"
    assert result["adr"] == 408
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_reporting_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P213-D"
    assert cat["adr"] == 408
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "explain why" in cat["principle"]
    assert cat["enterprise_reporting_platform_present_required"] is True
    assert cat["dashboard_architecture_present_required"] is True
    assert cat["visualization_platform_present_required"] is True
    assert cat["self_service_bi_capability_present_required"] is True
    assert cat["ai_reporting_intelligence_present_required"] is True
    assert cat["real_time_analytics_experience_present_required"] is True
    assert cat["knowledge_graph_visualization_present_required"] is True
    assert cat["digital_twin_visualization_present_required"] is True
    assert cat["sibling_business_intelligence_bc_forbidden"] is True
    assert cat["domain_model"]["core_domain"] == (
        "enterprise_intelligence_experience_management"
    )
    assert cat["domain_model"]["aggregate"]["name"] == (
        "EnterpriseVisualizationExperienceAggregate"
    )
    assert cat["bounded_contexts"]["context_count"] >= 5
    assert cat["architecture"]["layers"]["layer_count"] >= 5
    assert cat["dashboards"]["category_count"] >= 4
    assert cat["visualizations"]["type_count"] >= 8
    assert cat["ai_reporting"]["agent_count"] >= 5
    assert cat["events"]["core_event_count"] >= 5
    assert cat["microservices"]["service_count"] >= 6
    assert cat["cursor_outputs"]["count"] >= 19
    assert "dashboard_architecture_is_missing" in cat["quality_gates"]["reject_if"]
    assert "P213-C" in cat["builds_on"]
    assert "P212-O" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/reporting" in mod.reporting_surface()["routes"]
    assert "GET /analytics/reporting/ai" in mod.reporting_surface()["routes"]


@pytest.mark.unit
def test_bi_reporting_acl():
    from contexts.analytics.infrastructure.acl import bi_reporting_acl as acls

    assert acls.to_data_governance(tenant_id="t1", product_ref="p1")[
        "via_p212"
    ] is True
    assert acls.to_data_security(tenant_id="t1", asset_ref="a1")[
        "data_masking"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read"
    )["via_p208"] is True
    assert acls.to_identity(tenant_id="t1", identity_ref="i1")[
        "via_p207"
    ] is True
    assert acls.to_knowledge_graph(tenant_id="t1", node_ref="n1")[
        "knowledge_graph_visualization_present_required"
    ] is True
    assert acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
        "digital_twin_visualization_present_required"
    ] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_api_gateway(tenant_id="t1", route_ref="r1")[
        "via_api_gateway"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_reporting():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_reporting"]["prompt_id"] == "P213-D"
    assert catalog["platform_reporting"]["adr"] == 408
    assert catalog["sor"] == "analytics"
    summary = svc.platform_reporting()
    assert summary["prompt_id"] == "P213-D"
    assert summary["principle"] == mod.PRINCIPLE
    assert summary["fabric"] == mod.FABRIC
    assert "P213-C" in summary["builds_on"]
    assert summary["context_count"] >= 5
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.reporting_readiness()["passed"] is True
    assert svc.reporting_ai()["agent_count"] >= 5
    assert svc.reporting_dashboards()["category_count"] >= 4
