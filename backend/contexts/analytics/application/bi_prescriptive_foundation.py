"""Analytics P213-K BI prescriptive foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/415-enterprise-business-intelligence-prescriptive.md",
    "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_PRESCRIPTIVE.md",
    "docs/architecture/business_intelligence/BI_PRESCRIPTIVE_CAPABILITIES.v1.yaml",
    "docs/architecture/business_intelligence/BI_PRESCRIPTIVE_DDD_CQRS.v1.yaml",
    "docs/architecture/business_intelligence/BI_PRESCRIPTIVE_SECURITY.v1.yaml",
    "docs/architecture/business_intelligence/BI_PRESCRIPTIVE_VALIDATION.v1.yaml",
    "backend/contexts/analytics/domain/services/bi_platform_prescriptive.py",
    "backend/contexts/analytics/domain/aggregates/bi_prescriptive_aggregates.py",
    "backend/contexts/analytics/infrastructure/acl/bi_prescriptive_acl.py",
    "backend/contexts/analytics/application/bi_prescriptive_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/business_intelligence",
    "backend/contexts/decision_intelligence",
    "backend/contexts/reporting_platform",
    "backend/contexts/metric_governance_platform",
    "backend/contexts/visualization_platform",
    "backend/contexts/bi_core",
)


def validate_bi_prescriptive_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.analytics.domain.aggregates.bi_prescriptive_aggregates import (
        BiConstraintManagementRoot,
        BiExplainableOptimizationRoot,
        BiObjectiveFunctionRoot,
        BiOptimizationPlatformRoot,
        BiPrescriptiveProfileRoot,
        BiRecommendationEngineRoot,
    )
    from contexts.analytics.domain.services import (
        bi_platform_prescriptive as catmod,
    )

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P213-K"
        and cat.get("adr") == 415
        and cat.get("sor") == "analytics"
        and cat.get("capability") == "CAP-PLT-BI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "optimal enterprise action" in cat["principle"]
        and cat["enterprise_prescriptive_analytics_platform_present_required"]
        is True
        and cat["enterprise_optimization_platform_present_required"] is True
        and cat["recommendation_engine_present_required"] is True
        and cat["constraint_management_platform_present_required"] is True
        and cat["objective_function_platform_present_required"] is True
        and cat["ai_decision_optimization_present_required"] is True
        and cat["explainable_optimization_present_required"] is True
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
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["optimization_platform"]["lifecycle_step_count"] >= 11
        and cat["optimization_engine"]["algorithm_count"] >= 11
        and cat["recommendations"]["domain_count"] >= 14
        and cat["ai_native"]["agent_count"] >= 8
        and cat["ai_native"]["via_enterprise_ai"] is True
        and cat["explainability"]["xai_required"] is True
        and cat["semantic_integration"]["via_p213_g"] is True
        and cat["advanced_integration"]["via_p213_i"] is True
        and cat["predictive_integration"]["via_p213_j"] is True
        and cat["knowledge_graph"]["via_p212_j"] is True
        and cat["digital_twin"]["via_p212_l"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["cqrs"]["query_count"] >= 6
        and cat["events"]["core_event_count"] >= 7
        and cat["microservices"]["service_count"] >= 8
        and cat["deployment"]["cloud_native"] is True
        and cat["cursor_outputs"]["count"] >= 20
        and "prescriptive_analytics_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
        and "recommendation_engine_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P213-J" in cat["builds_on"]
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
            BiPrescriptiveProfileRoot.publish,
            tenant_id="t1",
            profile_ref="r1",
            complete=False,
        )
        and BiPrescriptiveProfileRoot.publish(
            tenant_id="t1", profile_ref="r2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            BiOptimizationPlatformRoot.enable,
            tenant_id="t1",
            opt_ref="o1",
            present=False,
        )
        and BiOptimizationPlatformRoot.enable(
            tenant_id="t1", opt_ref="o2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiRecommendationEngineRoot.enable,
            tenant_id="t1",
            rec_ref="rec1",
            present=False,
        )
        and BiRecommendationEngineRoot.enable(
            tenant_id="t1", rec_ref="rec2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiConstraintManagementRoot.enable,
            tenant_id="t1",
            constraint_ref="c1",
            present=False,
        )
        and BiConstraintManagementRoot.enable(
            tenant_id="t1", constraint_ref="c2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiObjectiveFunctionRoot.enable,
            tenant_id="t1",
            objective_ref="obj1",
            present=False,
        )
        and BiObjectiveFunctionRoot.enable(
            tenant_id="t1", objective_ref="obj2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiExplainableOptimizationRoot.enable,
            tenant_id="t1",
            xai_ref="x1",
            present=False,
        )
        and BiExplainableOptimizationRoot.enable(
            tenant_id="t1", xai_ref="x2"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/analytics/infrastructure/acl/bi_prescriptive_acl.py"
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
        and "via_p213_g" in acl_text
        and "via_p213_i" in acl_text
        and "via_p213_j" in acl_text
        and "via_enterprise_ai" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
        and "row_level_security" in acl_text
    )

    router = (
        root / "backend/contexts/analytics/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/prescriptive")' in router
        and "/prescriptive/readiness" in router
        and "/prescriptive/vision" in router
        and "/prescriptive/optimization" in router
        and "/prescriptive/recommendations" in router
        and "/prescriptive/constraints" in router
        and "/prescriptive/ai" in router
        and "/prescriptive/explainability" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_PRESCRIPTIVE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise prescriptive analytics platform is missing" in law
        and "Never Enterprise optimization platform is missing" in law
        and "Never Recommendation engine is missing" in law
        and "Never Constraint management platform is missing" in law
        and "Never Objective function platform is missing" in law
        and "Never AI decision optimization is missing" in law
        and "Never Explainable optimization is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event sourcing architecture is missing" in law
        and "Never Microservice architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Enterprise governance is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Prescriptive analytics architecture is incomplete" in law
        and "Never Sibling business intelligence BC" in law
        and "MEOS Enterprise Decision Optimization Fabric" in law
        and "optimal enterprise action" in law
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
        "prompt": "P213-K",
        "adr": 415,
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
