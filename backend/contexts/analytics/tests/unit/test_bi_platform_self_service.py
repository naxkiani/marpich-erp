"""P213-H BI self-service foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_self_service_foundation import (
    validate_bi_self_service_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import bi_platform_self_service as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_self_service_foundation():
    result = validate_bi_self_service_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-H"
    assert result["adr"] == 412
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_self_service_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P213-H"
    assert cat["adr"] == 412
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "without compromising governance" in cat["principle"]
    assert cat["enterprise_self_service_bi_platform_present_required"] is True
    assert cat["no_code_analytics_platform_present_required"] is True
    assert cat["ai_analytics_assistant_present_required"] is True
    assert cat["semantic_layer_integration_present_required"] is True
    assert cat["analytics_workspace_present_required"] is True
    assert cat["sibling_business_intelligence_bc_forbidden"] is True
    assert cat["domain_model"]["core_domain"] == (
        "enterprise_self_service_analytics_management"
    )
    assert cat["domain_model"]["aggregate"]["name"] == (
        "SelfServiceAnalyticsWorkspaceAggregate"
    )
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["workspaces"]["type_count"] >= 7
    assert cat["no_code_low_code"]["sql_knowledge_required"] is False
    assert cat["ai_native"]["agent_count"] >= 7
    assert cat["events"]["core_event_count"] >= 6
    assert cat["microservices"]["service_count"] >= 8
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "ai_analytics_assistant_is_missing" in cat["quality_gates"]["reject_if"]
    )
    assert "P213-G" in cat["builds_on"]
    assert "P212-I" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/self-service" in mod.self_service_surface()["routes"]
    assert (
        "GET /analytics/self-service/natural-language"
        in mod.self_service_surface()["routes"]
    )


@pytest.mark.unit
def test_bi_self_service_acl():
    from contexts.analytics.infrastructure.acl import bi_self_service_acl as acls

    assert acls.to_semantic(tenant_id="t1", metric_ref="m1")[
        "via_p213_g"
    ] is True
    assert acls.to_knowledge_graph(tenant_id="t1", node_ref="n1")[
        "via_p212_j"
    ] is True
    assert acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
        "via_p212_l"
    ] is True
    assert acls.to_metadata(tenant_id="t1", asset_ref="a1")[
        "via_p212_i"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read"
    )["row_level_security"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_enterprise_search(tenant_id="t1", query_ref="q1")[
        "via_enterprise_search"
    ] is True
    assert acls.to_reporting(tenant_id="t1", report_ref="r1")[
        "via_p213_d"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_self_service():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_self_service"]["prompt_id"] == "P213-H"
    assert catalog["platform_self_service"]["adr"] == 412
    assert catalog["sor"] == "analytics"
    summary = svc.platform_self_service()
    assert summary["prompt_id"] == "P213-H"
    assert summary["principle"] == mod.PRINCIPLE
    assert summary["fabric"] == mod.FABRIC
    assert "P213-G" in summary["builds_on"]
    assert summary["context_count"] >= 6
    assert summary["workspace_type_count"] >= 7
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.self_service_readiness()["passed"] is True
    assert svc.self_service_ai()["agent_count"] >= 7
    assert svc.self_service_no_code()["sql_knowledge_required"] is False
