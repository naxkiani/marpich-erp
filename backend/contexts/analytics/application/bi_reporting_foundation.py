"""Analytics P213-D BI reporting foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/408-enterprise-business-intelligence-reporting.md",
    "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_REPORTING.md",
    "docs/architecture/business_intelligence/BI_REPORTING_CAPABILITIES.v1.yaml",
    "docs/architecture/business_intelligence/BI_REPORTING_DDD_CQRS.v1.yaml",
    "docs/architecture/business_intelligence/BI_REPORTING_SECURITY.v1.yaml",
    "docs/architecture/business_intelligence/BI_REPORTING_VALIDATION.v1.yaml",
    "backend/contexts/analytics/domain/services/bi_platform_reporting.py",
    "backend/contexts/analytics/domain/aggregates/bi_reporting_aggregates.py",
    "backend/contexts/analytics/infrastructure/acl/bi_reporting_acl.py",
    "backend/contexts/analytics/application/bi_reporting_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/business_intelligence",
    "backend/contexts/decision_intelligence",
    "backend/contexts/reporting_platform",
    "backend/contexts/metric_governance_platform",
    "backend/contexts/visualization_platform",
    "backend/contexts/bi_core",
)


def validate_bi_reporting_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.analytics.domain.aggregates.bi_reporting_aggregates import (
        BiAiReportingRoot,
        BiDashboardArchitectureRoot,
        BiReportingProfileRoot,
        BiSelfServiceBiRoot,
        BiVisualizationPlatformRoot,
    )
    from contexts.analytics.domain.services import bi_platform_reporting as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P213-D"
        and cat.get("adr") == 408
        and cat.get("sor") == "analytics"
        and cat.get("capability") == "CAP-PLT-BI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "explain why" in cat["principle"]
        and cat["enterprise_reporting_platform_present_required"] is True
        and cat["dashboard_architecture_present_required"] is True
        and cat["visualization_platform_present_required"] is True
        and cat["self_service_bi_capability_present_required"] is True
        and cat["ai_reporting_intelligence_present_required"] is True
        and cat["real_time_analytics_experience_present_required"] is True
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_driven_design_present_required"] is True
        and cat["microservice_architecture_present_required"] is True
        and cat["api_first_architecture_present_required"] is True
        and cat["security_governance_present_required"] is True
        and cat["enterprise_scalability_present_required"] is True
        and cat["architecture_present_required"] is True
        and cat["knowledge_graph_visualization_present_required"] is True
        and cat["digital_twin_visualization_present_required"] is True
        and cat["sibling_business_intelligence_bc_forbidden"] is True
        and cat["domain_model"]["supporting_count"] >= 6
        and cat["bounded_contexts"]["context_count"] >= 5
        and cat["architecture"]["layers"]["layer_count"] >= 5
        and cat["architecture"]["capability_count"] >= 5
        and cat["dashboards"]["category_count"] >= 4
        and cat["visualizations"]["type_count"] >= 8
        and cat["ai_reporting"]["agent_count"] >= 5
        and cat["ai_reporting"]["via_enterprise_ai"] is True
        and cat["knowledge_graph"]["via_p212_j"] is True
        and cat["digital_twin"]["via_p212_l"] is True
        and cat["cqrs"]["command_count"] >= 5
        and cat["cqrs"]["query_count"] >= 4
        and cat["events"]["core_event_count"] >= 5
        and cat["microservices"]["service_count"] >= 6
        and cat["deployment"]["cloud_native"] is True
        and cat["cursor_outputs"]["count"] >= 19
        and "reporting_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
        and "dashboard_architecture_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P213-C" in cat["builds_on"]
        and "P212-J" in cat["builds_on"]
        and "P212-L" in cat["builds_on"]
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
            BiReportingProfileRoot.publish,
            tenant_id="t1",
            profile_ref="r1",
            complete=False,
        )
        and BiReportingProfileRoot.publish(
            tenant_id="t1", profile_ref="r2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            BiDashboardArchitectureRoot.publish,
            tenant_id="t1",
            dashboard_ref="d1",
            present=False,
        )
        and BiDashboardArchitectureRoot.publish(
            tenant_id="t1", dashboard_ref="d2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiVisualizationPlatformRoot.register,
            tenant_id="t1",
            viz_ref="v1",
            present=False,
        )
        and BiVisualizationPlatformRoot.register(
            tenant_id="t1", viz_ref="v2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiSelfServiceBiRoot.enable,
            tenant_id="t1",
            layer_ref="s1",
            present=False,
        )
        and BiSelfServiceBiRoot.enable(
            tenant_id="t1", layer_ref="s2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiAiReportingRoot.enable,
            tenant_id="t1",
            ai_ref="a1",
            present=False,
        )
        and BiAiReportingRoot.enable(
            tenant_id="t1", ai_ref="a2"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/analytics/infrastructure/acl/bi_reporting_acl.py"
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
        and "via_enterprise_ai" in acl_text
        and "via_api_gateway" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/analytics/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/reporting")' in router
        and "/reporting/readiness" in router
        and "/reporting/vision" in router
        and "/reporting/dashboards" in router
        and "/reporting/ai" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_REPORTING.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise reporting platform is missing" in law
        and "Never Dashboard architecture is missing" in law
        and "Never Visualization platform is missing" in law
        and "Never Self-service BI capability is missing" in law
        and "Never AI reporting intelligence is missing" in law
        and "Never Real-time analytics experience is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event driven design is missing" in law
        and "Never Microservice architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Security governance is missing" in law
        and "Never Enterprise scalability is missing" in law
        and "Never Reporting architecture is incomplete" in law
        and "Never Knowledge graph visualization is missing" in law
        and "Never Digital twin visualization is missing" in law
        and "Never Sibling business intelligence BC" in law
        and "MEOS Enterprise Intelligence Experience Fabric" in law
        and "explain why it happened" in law
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
        "prompt": "P213-D",
        "adr": 408,
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
