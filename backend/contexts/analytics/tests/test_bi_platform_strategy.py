"""P213-A Enterprise BI strategy foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_strategy_foundation import (
    validate_bi_strategy_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import bi_platform_strategy as strat

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_strategy_foundation():
    result = validate_bi_strategy_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-A"
    assert result["adr"] == 394
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_strategy_catalog():
    cat = strat.catalog()
    assert cat["prompt_id"] == "P213-A"
    assert cat["adr"] == 394
    assert cat["sor"] == "analytics"
    assert cat["capability"] == "CAP-PLT-BI-001"
    assert "trusted data" in cat["principle"]
    assert cat["core_domain"] == "enterprise_decision_intelligence_management"
    assert cat["aggregate"] == "EnterpriseInsightAggregate"
    assert cat["architecture"]["layer_count"] >= 6
    assert cat["domains"]["supporting_count"] >= 8
    assert cat["bounded_contexts"]["context_count"] >= 5
    assert cat["microservices"]["service_count"] >= 6
    assert cat["cqrs"]["event_count"] >= 8
    assert cat["ai_native"]["agent_count"] >= 5
    assert cat["knowledge_graph_integration"]["via_p212_j"] is True
    assert cat["digital_twin_integration"]["via_p212_l"] is True
    assert cat["api_first"]["via_api_gateway"] is True
    assert cat["decision_intelligence_foundation_present_required"] is True
    assert (
        "enterprise_bi_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
    )
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/strategy" in strat.strategy_surface()["routes"]


@pytest.mark.unit
def test_bi_strategy_acl():
    from contexts.analytics.infrastructure.acl import bi_strategy_acl as acls

    assert acls.to_data_governance(tenant_id="t1", product_ref="p1")[
        "via_p212"
    ] is True
    assert acls.to_graph(tenant_id="t1", entity_ref="e1")["via_p212_j"] is True
    assert acls.to_twin(tenant_id="t1", twin_ref="tw1")["via_p212_l"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "via_enterprise_ai"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="read_insight"
    )["via_p208"] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_strategy():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_strategy"]["prompt_id"] == "P213-A"
    assert catalog["platform_strategy"]["adr"] == 394
    assert catalog["sor"] == "analytics"
    summary = svc.platform_strategy()
    assert summary["prompt_id"] == "P213-A"
    assert summary["capability"] == "CAP-PLT-BI-001"
    assert "P212" in summary["builds_on"]
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.strategy_readiness()["passed"] is True
