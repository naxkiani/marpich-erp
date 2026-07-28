"""P213-J BI predictive foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_predictive_foundation import (
    validate_bi_predictive_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import bi_platform_predictive as mod

REPO_ROOT = Path(__file__).resolve().parents[4]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_predictive_foundation():
    result = validate_bi_predictive_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-J"
    assert result["adr"] == 414
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_predictive_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P213-J"
    assert cat["adr"] == 414
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "anticipate future business conditions" in cat["principle"]
    assert cat["enterprise_predictive_analytics_platform_present_required"] is True
    assert cat["enterprise_forecasting_platform_present_required"] is True
    assert cat["predictive_modeling_platform_present_required"] is True
    assert cat["scenario_prediction_platform_present_required"] is True
    assert cat["time_series_intelligence_present_required"] is True
    assert cat["explainable_ai_platform_present_required"] is True
    assert cat["sibling_business_intelligence_bc_forbidden"] is True
    assert cat["domain_model"]["core_domain"] == (
        "enterprise_predictive_intelligence_management"
    )
    assert cat["domain_model"]["aggregate"]["name"] == (
        "PredictiveAnalyticsAggregate"
    )
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["forecast_management"]["lifecycle_step_count"] >= 8
    assert cat["predictive_models"]["type_count"] >= 10
    assert cat["time_series"]["capability_count"] >= 7
    assert cat["ai_native"]["agent_count"] >= 8
    assert cat["events"]["core_event_count"] >= 7
    assert cat["microservices"]["service_count"] >= 8
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "explainable_ai_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
    )
    assert "P213-I" in cat["builds_on"]
    assert "P212-J" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/predictive" in mod.predictive_surface()["routes"]
    assert (
        "GET /analytics/predictive/explainability"
        in mod.predictive_surface()["routes"]
    )


@pytest.mark.unit
def test_bi_predictive_acl():
    from contexts.analytics.infrastructure.acl import bi_predictive_acl as acls

    assert acls.to_semantic(tenant_id="t1", metric_ref="m1")[
        "via_p213_g"
    ] is True
    assert acls.to_advanced(tenant_id="t1", analysis_ref="a1")[
        "via_p213_i"
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
async def test_service_catalog_includes_platform_predictive():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_predictive"]["prompt_id"] == "P213-J"
    assert catalog["platform_predictive"]["adr"] == 414
    assert catalog["sor"] == "analytics"
    summary = svc.platform_predictive()
    assert summary["prompt_id"] == "P213-J"
    assert summary["principle"] == mod.PRINCIPLE
    assert summary["fabric"] == mod.FABRIC
    assert "P213-I" in summary["builds_on"]
    assert summary["context_count"] >= 6
    assert summary["forecast_lifecycle_step_count"] >= 8
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.predictive_readiness()["passed"] is True
    assert svc.predictive_ai()["agent_count"] >= 8
    assert svc.predictive_explainability()["xai_required"] is True
