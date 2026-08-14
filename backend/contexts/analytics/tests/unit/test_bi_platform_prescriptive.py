"""P213-K BI prescriptive foundation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from contexts.analytics.application.bi_prescriptive_foundation import (
    validate_bi_prescriptive_foundation,
)
from contexts.analytics.container import (
    get_analytics_service,
    reset_analytics_service,
)
from contexts.analytics.domain.services import bi_platform_prescriptive as mod

REPO_ROOT = Path(__file__).resolve().parents[5]


@pytest.fixture(autouse=True)
def _reset():
    reset_analytics_service()
    yield
    reset_analytics_service()


@pytest.mark.unit
def test_bi_prescriptive_foundation():
    result = validate_bi_prescriptive_foundation(repo_root=REPO_ROOT)
    assert result["passed"] is True, result
    assert result["verdict"] == "ENTERPRISE_GRADE"
    assert result["prompt"] == "P213-K"
    assert result["adr"] == 415
    assert result["sor"] == "analytics"
    assert result["capability"] == "CAP-PLT-BI-001"
    assert result["forbidden_sibling_present"] is False


@pytest.mark.unit
def test_bi_prescriptive_catalog():
    cat = mod.catalog()
    assert cat["prompt_id"] == "P213-K"
    assert cat["adr"] == 415
    assert cat["principle"] == mod.PRINCIPLE
    assert cat["fabric"] == mod.FABRIC
    assert "optimal enterprise action" in cat["principle"]
    assert cat["enterprise_prescriptive_analytics_platform_present_required"] is True
    assert cat["enterprise_optimization_platform_present_required"] is True
    assert cat["recommendation_engine_present_required"] is True
    assert cat["constraint_management_platform_present_required"] is True
    assert cat["objective_function_platform_present_required"] is True
    assert cat["ai_decision_optimization_present_required"] is True
    assert cat["explainable_optimization_present_required"] is True
    assert cat["sibling_business_intelligence_bc_forbidden"] is True
    assert cat["domain_model"]["core_domain"] == (
        "enterprise_decision_optimization_management"
    )
    assert cat["domain_model"]["aggregate"]["name"] == (
        "DecisionOptimizationAggregate"
    )
    assert cat["bounded_contexts"]["context_count"] >= 6
    assert cat["optimization_platform"]["lifecycle_step_count"] >= 11
    assert cat["optimization_engine"]["algorithm_count"] >= 11
    assert cat["recommendations"]["domain_count"] >= 14
    assert cat["ai_native"]["agent_count"] >= 8
    assert cat["events"]["core_event_count"] >= 7
    assert cat["microservices"]["service_count"] >= 8
    assert cat["cursor_outputs"]["count"] >= 20
    assert (
        "recommendation_engine_is_missing" in cat["quality_gates"]["reject_if"]
    )
    assert "P213-J" in cat["builds_on"]
    assert "P212-J" in cat["builds_on"]
    assert cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert "GET /analytics/prescriptive" in mod.prescriptive_surface()["routes"]
    assert (
        "GET /analytics/prescriptive/constraints"
        in mod.prescriptive_surface()["routes"]
    )


@pytest.mark.unit
def test_bi_prescriptive_acl():
    from contexts.analytics.infrastructure.acl import bi_prescriptive_acl as acls

    assert acls.to_semantic(tenant_id="t1", metric_ref="m1")[
        "via_p213_g"
    ] is True
    assert acls.to_advanced(tenant_id="t1", analysis_ref="a1")[
        "via_p213_i"
    ] is True
    assert acls.to_predictive(tenant_id="t1", forecast_ref="f1")[
        "via_p213_j"
    ] is True
    assert acls.to_knowledge_graph(tenant_id="t1", node_ref="n1")[
        "via_p212_j"
    ] is True
    assert acls.to_digital_twin(tenant_id="t1", twin_ref="tw1")[
        "via_p212_l"
    ] is True
    assert acls.to_authorization(
        tenant_id="t1", principal_ref="u1", action="approve"
    )["segregation_of_duties"] is True
    assert acls.to_enterprise_ai(tenant_id="t1", model_ref="m1")[
        "module_local_llm_sdk_forbidden"
    ] is True
    assert acls.to_data_governance(tenant_id="t1", product_ref="p1")[
        "optimization_approval_workflow"
    ] is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_service_catalog_includes_platform_prescriptive():
    svc = get_analytics_service()
    catalog = (await svc.list_catalog()).unwrap()
    assert catalog["platform_prescriptive"]["prompt_id"] == "P213-K"
    assert catalog["platform_prescriptive"]["adr"] == 415
    assert catalog["sor"] == "analytics"
    summary = svc.platform_prescriptive()
    assert summary["prompt_id"] == "P213-K"
    assert summary["principle"] == mod.PRINCIPLE
    assert summary["fabric"] == mod.FABRIC
    assert "P213-J" in summary["builds_on"]
    assert summary["context_count"] >= 6
    assert summary["optimization_lifecycle_step_count"] >= 11
    assert summary["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    assert svc.prescriptive_readiness()["passed"] is True
    assert svc.prescriptive_ai()["agent_count"] >= 8
    assert svc.prescriptive_explainability()["xai_required"] is True
