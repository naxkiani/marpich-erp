"""P213-I BI advanced foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_advanced_foundation import (
    validate_bi_advanced_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import bi_platform_advanced as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_advanced_foundation():
    result = validate_bi_advanced_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-I"
    assert result["adr"] == 413
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_advanced_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P213-I"
    assert cat["adr"] == 413
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "scientific business intelligence" in cat["principle"]
    assert cat["enterprise_advanced_analytics_platform_present_required"] is True
    assert cat["statistical_intelligence_platform_present_required"] is True
    assert cat["enterprise_experimentation_platform_present_required"] is True
    assert cat["pattern_discovery_platform_present_required"] is True
    assert cat["root_cause_analytics_present_required"] is True
    assert cat["insight_management_present_required"] is True
    assert cat["ai_assisted_analytics_present_required"] is True
    assert cat["sibling_business_intelligence_bc_forbidden"] is True
    assert cat["domain_model"]["core_domain"] == (
        "enterprise_advanced_analytics_management"
    )
    assert cat["domain_model"]["aggregate"]["name"] == "AdvancedAnalyticsAggregate"
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["workbench"]["type_count"] >= 7
    assert len(cat["statistical"]["capabilities"]) >= 13
    assert cat["ai_native"]["agent_count"] >= 7
    assert cat["events"]["core_event_count"] >= 6
    assert cat["microservices"]["service_count"] >= 8
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "root_cause_analytics_is_missing" in cat["quality_gates"]["reject_if"]
    )
    assert "P213-H" in cat["builds_on"]
    assert "P212-J" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/advanced" in mod.advanced_surface()["routes"]
    assert "GET /analytics/advanced/experiments" in mod.advanced_surface()["routes"]


@pytest.mark.unit
def test_bi_advanced_acl():
    from contexts.analytics.infrastructure.acl import bi_advanced_acl as acls

    assert acls.to_semantic(tenant_id="t1", metric_ref="m1")[
        "via_p213_g"
    ] is True
    assert acls.to_self_service(tenant_id="t1", workspace_ref="w1")[
        "via_p213_h"
    ] is True
    assert acls.to_knowledge_graph(tenant_id="t1", node_ref="n1")[
        "via_p212_j"
    ] is True
    assert acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
        "via_p212_l"
    ] is True
    assert acls.to_warehouse(tenant_id="t1", warehouse_ref="wh1")[
        "via_p213_e"
    ] is True
    assert acls.to_lakehouse(tenant_id="t1", lakehouse_ref="lh1")[
        "via_p213_f"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read"
    )["row_level_security"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_advanced():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_advanced"]["prompt_id"] == "P213-I"
    assert catalog["platform_advanced"]["adr"] == 413
    assert catalog["sor"] == "analytics"
    summary = svc.platform_advanced()
    assert summary["prompt_id"] == "P213-I"
    assert summary["principle"] == mod.PRINCIPLE
    assert summary["fabric"] == mod.FABRIC
    assert "P213-H" in summary["builds_on"]
    assert summary["context_count"] >= 6
    assert summary["workbench_type_count"] >= 7
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.advanced_readiness()["passed"] is True
    assert svc.advanced_ai()["agent_count"] >= 7
    assert len(svc.advanced_statistical()["capabilities"]) >= 13
