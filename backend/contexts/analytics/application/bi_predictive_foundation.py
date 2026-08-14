"""Analytics P213-J BI predictive foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/414-enterprise-business-intelligence-predictive.md",
    "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_PREDICTIVE.md",
    "docs/architecture/business_intelligence/BI_PREDICTIVE_CAPABILITIES.v1.yaml",
    "docs/architecture/business_intelligence/BI_PREDICTIVE_DDD_CQRS.v1.yaml",
    "docs/architecture/business_intelligence/BI_PREDICTIVE_SECURITY.v1.yaml",
    "docs/architecture/business_intelligence/BI_PREDICTIVE_VALIDATION.v1.yaml",
    "backend/contexts/analytics/domain/services/bi_platform_predictive.py",
    "backend/contexts/analytics/domain/aggregates/bi_predictive_aggregates.py",
    "backend/contexts/analytics/infrastructure/acl/bi_predictive_acl.py",
    "backend/contexts/analytics/application/bi_predictive_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/business_intelligence",
    "backend/contexts/decision_intelligence",
    "backend/contexts/reporting_platform",
    "backend/contexts/metric_governance_platform",
    "backend/contexts/visualization_platform",
    "backend/contexts/bi_core",
)


def validate_bi_predictive_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.analytics.domain.aggregates.bi_predictive_aggregates import (
        BiExplainableAiRoot,
        BiForecastManagementRoot,
        BiPredictiveModelingRoot,
        BiPredictiveProfileRoot,
        BiScenarioPredictionRoot,
        BiTimeSeriesIntelligenceRoot,
    )
    from contexts.analytics.domain.services import (
        bi_platform_predictive as catmod,
    )

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P213-J"
        and cat.get("adr") == 414
        and cat.get("sor") == "analytics"
        and cat.get("capability") == "CAP-PLT-BI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "anticipate future business conditions" in cat["principle"]
        and cat["enterprise_predictive_analytics_platform_present_required"]
        is True
        and cat["enterprise_forecasting_platform_present_required"] is True
        and cat["predictive_modeling_platform_present_required"] is True
        and cat["scenario_prediction_platform_present_required"] is True
        and cat["time_series_intelligence_present_required"] is True
        and cat["explainable_ai_platform_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_sourcing_architecture_present_required"] is True
        and cat["microservice_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["enterprise_governance_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["architecture_present_required"] is True
        and cat["sibling_business_intelligence_bc_forbidden"] is True
        and cat["domain_model"]["supporting_count"] >= 8
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["forecast_management"]["lifecycle_step_count"] >= 8
        and cat["predictive_models"]["type_count"] >= 10
        and cat["time_series"]["capability_count"] >= 7
        and cat["ai_native"]["agent_count"] >= 8
        and cat["ai_native"]["via_enterprise_ai"] is True
        and cat["explainability"]["xai_required"] is True
        and cat["semantic_integration"]["via_p213_g"] is True
        and cat["advanced_integration"]["via_p213_i"] is True
        and cat["knowledge_graph"]["via_p212_j"] is True
        and cat["digital_twin"]["via_p212_l"] is True
        and cat["cqrs"]["command_count"] >= 5
        and cat["cqrs"]["query_count"] >= 5
        and cat["events"]["core_event_count"] >= 7
        and cat["microservices"]["service_count"] >= 8
        and cat["deployment"]["cloud_native"] is True
        and cat["cursor_outputs"]["count"] >= 20
        and "predictive_analytics_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
        and "explainable_ai_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P213-I" in cat["builds_on"]
        and "P212-J" in cat["builds_on"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    def _bad(fn, **kwargs):
        try:
            fn(**kwargs)
            return True
        except ValueError:
            return False

    checks = []
    checks.append(
        not _bad(
            BiPredictiveProfileRoot.publish,
            tenant_id="t1",
            profile_ref="r1",
            complete=False,
        )
        and BiPredictiveProfileRoot.publish(
            tenant_id="t1", profile_ref="r2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            BiForecastManagementRoot.enable,
            tenant_id="t1",
            forecast_ref="f1",
            present=False,
        )
        and BiForecastManagementRoot.enable(
            tenant_id="t1", forecast_ref="f2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiPredictiveModelingRoot.enable,
            tenant_id="t1",
            model_ref="m1",
            present=False,
        )
        and BiPredictiveModelingRoot.enable(
            tenant_id="t1", model_ref="m2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiScenarioPredictionRoot.enable,
            tenant_id="t1",
            scenario_ref="s1",
            present=False,
        )
        and BiScenarioPredictionRoot.enable(
            tenant_id="t1", scenario_ref="s2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiTimeSeriesIntelligenceRoot.enable,
            tenant_id="t1",
            series_ref="ts1",
            present=False,
        )
        and BiTimeSeriesIntelligenceRoot.enable(
            tenant_id="t1", series_ref="ts2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiExplainableAiRoot.enable,
            tenant_id="t1",
            xai_ref="x1",
            present=False,
        )
        and BiExplainableAiRoot.enable(
            tenant_id="t1", xai_ref="x2"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/analytics/infrastructure/acl/bi_predictive_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_p212_i" in acl_text
        and "via_p212_j" in acl_text
        and "via_p212_l" in acl_text
        and "via_p213_e" in acl_text
        and "via_p213_f" in acl_text
        and "via_p213_g" in acl_text
        and "via_p213_i" in acl_text
        and "via_enterprise_ai" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
        and "row_level_security" in acl_text
    )

    router = (
        root / "backend/contexts/analytics/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/predictive")' in router
        and "/predictive/readiness" in router
        and "/predictive/vision" in router
        and "/predictive/forecast-management" in router
        and "/predictive/models" in router
        and "/predictive/scenarios" in router
        and "/predictive/ai" in router
        and "/predictive/explainability" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_PREDICTIVE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise predictive analytics platform is missing" in law
        and "Never Enterprise forecasting platform is missing" in law
        and "Never Predictive modeling platform is missing" in law
        and "Never Scenario prediction platform is missing" in law
        and "Never Time series intelligence is missing" in law
        and "Never Explainable AI platform is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event sourcing architecture is missing" in law
        and "Never Microservice architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Enterprise governance is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Predictive analytics architecture is incomplete" in law
        and "Never Sibling business intelligence BC" in law
        and "MEOS Enterprise Predictive Intelligence Fabric" in law
        and "anticipate future business conditions" in law
    )

    passed = (
        not missing
        and not sibling
        and catalog_ok
        and aggregates_ok
        and acl_ok
        and router_ok
        and doc_ok
    )
    return {
        "prompt": "P213-J",
        "adr": 414,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "analytics",
        "capability": "CAP-PLT-BI-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
