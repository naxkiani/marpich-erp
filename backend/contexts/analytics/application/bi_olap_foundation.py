"""Analytics P213-G BI OLAP / semantic foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/411-enterprise-business-intelligence-olap.md",
    "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_OLAP.md",
    "docs/architecture/business_intelligence/BI_OLAP_CAPABILITIES.v1.yaml",
    "docs/architecture/business_intelligence/BI_OLAP_DDD_CQRS.v1.yaml",
    "docs/architecture/business_intelligence/BI_OLAP_SECURITY.v1.yaml",
    "docs/architecture/business_intelligence/BI_OLAP_VALIDATION.v1.yaml",
    "backend/contexts/analytics/domain/services/bi_platform_olap.py",
    "backend/contexts/analytics/domain/aggregates/bi_olap_aggregates.py",
    "backend/contexts/analytics/infrastructure/acl/bi_olap_acl.py",
    "backend/contexts/analytics/application/bi_olap_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/business_intelligence",
    "backend/contexts/decision_intelligence",
    "backend/contexts/reporting_platform",
    "backend/contexts/metric_governance_platform",
    "backend/contexts/visualization_platform",
    "backend/contexts/bi_core",
)


def validate_bi_olap_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.analytics.domain.aggregates.bi_olap_aggregates import (
        BiCalculationEngineRoot,
        BiKpiGovernanceRoot,
        BiMetricPlatformRoot,
        BiOlapProfileRoot,
        BiSemanticLayerRoot,
    )
    from contexts.analytics.domain.services import bi_platform_olap as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P213-G"
        and cat.get("adr") == 411
        and cat.get("sor") == "analytics"
        and cat.get("capability") == "CAP-PLT-BI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "governed semantic definition" in cat["principle"]
        and cat["enterprise_semantic_layer_present_required"] is True
        and cat["enterprise_metric_platform_present_required"] is True
        and cat["kpi_governance_present_required"] is True
        and cat["olap_platform_present_required"] is True
        and cat["business_glossary_present_required"] is True
        and cat["business_vocabulary_present_required"] is True
        and cat["semantic_query_layer_present_required"] is True
        and cat["knowledge_graph_integration_present_required"] is True
        and cat["ai_native_semantic_platform_present_required"] is True
        and cat["digital_twin_integration_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_sourcing_architecture_present_required"] is True
        and cat["microservice_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["architecture_present_required"] is True
        and cat["dimension_platform_present_required"] is True
        and cat["calculation_engine_present_required"] is True
        and cat["sibling_business_intelligence_bc_forbidden"] is True
        and cat["domain_model"]["supporting_count"] >= 8
        and cat["bounded_contexts"]["context_count"] >= 5
        and cat["metrics"]["class_count"] >= 13
        and cat["kpi_governance"]["lifecycle_step_count"] >= 8
        and cat["dimensions"]["dimension_count"] >= 14
        and cat["ai_native"]["agent_count"] >= 6
        and cat["ai_native"]["via_enterprise_ai"] is True
        and cat["knowledge_graph"]["via_p212_j"] is True
        and cat["digital_twin"]["via_p212_l"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["cqrs"]["query_count"] >= 5
        and cat["events"]["core_event_count"] >= 7
        and cat["microservices"]["service_count"] >= 8
        and cat["deployment"]["cloud_native"] is True
        and cat["cursor_outputs"]["count"] >= 20
        and "olap_semantic_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
        and "enterprise_semantic_layer_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P213-F" in cat["builds_on"]
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
            BiOlapProfileRoot.publish,
            tenant_id="t1",
            profile_ref="r1",
            complete=False,
        )
        and BiOlapProfileRoot.publish(
            tenant_id="t1", profile_ref="r2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            BiSemanticLayerRoot.publish,
            tenant_id="t1",
            layer_ref="s1",
            present=False,
        )
        and BiSemanticLayerRoot.publish(
            tenant_id="t1", layer_ref="s2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiMetricPlatformRoot.publish,
            tenant_id="t1",
            catalog_ref="m1",
            present=False,
        )
        and BiMetricPlatformRoot.publish(
            tenant_id="t1", catalog_ref="m2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiKpiGovernanceRoot.enable,
            tenant_id="t1",
            governance_ref="k1",
            present=False,
        )
        and BiKpiGovernanceRoot.enable(
            tenant_id="t1", governance_ref="k2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiCalculationEngineRoot.enable,
            tenant_id="t1",
            engine_ref="c1",
            present=False,
        )
        and BiCalculationEngineRoot.enable(
            tenant_id="t1", engine_ref="c2"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/analytics/infrastructure/acl/bi_olap_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_p212_j" in acl_text
        and "via_p212_l" in acl_text
        and "via_p213_d" in acl_text
        and "via_p213_e" in acl_text
        and "via_p213_f" in acl_text
        and "via_enterprise_ai" in acl_text
        and "via_enterprise_search" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/analytics/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/olap")' in router
        and "/olap/readiness" in router
        and "/olap/vision" in router
        and "/olap/metrics" in router
        and "/olap/semantic-layer" in router
        and "/olap/calculation-engine" in router
        and "/olap/ai" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_OLAP.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise semantic layer is missing" in law
        and "Never Enterprise metric platform is missing" in law
        and "Never KPI governance is missing" in law
        and "Never OLAP platform is missing" in law
        and "Never Business glossary is missing" in law
        and "Never Business vocabulary is missing" in law
        and "Never Semantic query layer is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never AI native semantic platform is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event sourcing architecture is missing" in law
        and "Never Microservice architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never OLAP semantic architecture is incomplete" in law
        and "Never Dimension platform is missing" in law
        and "Never Calculation engine is missing" in law
        and "Never Sibling business intelligence BC" in law
        and "MEOS Enterprise Semantic Intelligence Fabric" in law
        and "governed semantic definition" in law
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
        "prompt": "P213-G",
        "adr": 411,
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
