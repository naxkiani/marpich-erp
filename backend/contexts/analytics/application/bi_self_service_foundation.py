"""Analytics P213-H BI self-service foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/412-enterprise-business-intelligence-self-service.md",
    "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_SELF_SERVICE.md",
    "docs/architecture/business_intelligence/BI_SELF_SERVICE_CAPABILITIES.v1.yaml",
    "docs/architecture/business_intelligence/BI_SELF_SERVICE_DDD_CQRS.v1.yaml",
    "docs/architecture/business_intelligence/BI_SELF_SERVICE_SECURITY.v1.yaml",
    "docs/architecture/business_intelligence/BI_SELF_SERVICE_VALIDATION.v1.yaml",
    "backend/contexts/analytics/domain/services/bi_platform_self_service.py",
    "backend/contexts/analytics/domain/aggregates/bi_self_service_aggregates.py",
    "backend/contexts/analytics/infrastructure/acl/bi_self_service_acl.py",
    "backend/contexts/analytics/application/bi_self_service_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/business_intelligence",
    "backend/contexts/decision_intelligence",
    "backend/contexts/reporting_platform",
    "backend/contexts/metric_governance_platform",
    "backend/contexts/visualization_platform",
    "backend/contexts/bi_core",
)


def validate_bi_self_service_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.analytics.domain.aggregates.bi_self_service_aggregates import (
        BiAiAssistantRoot,
        BiAnalyticsWorkspaceRoot,
        BiCollaborativeAnalyticsRoot,
        BiNoCodeAnalyticsRoot,
        BiSelfServiceProfileRoot,
    )
    from contexts.analytics.domain.services import (
        bi_platform_self_service as catmod,
    )

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P213-H"
        and cat.get("adr") == 412
        and cat.get("sor") == "analytics"
        and cat.get("capability") == "CAP-PLT-BI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "without compromising governance" in cat["principle"]
        and cat["enterprise_self_service_bi_platform_present_required"] is True
        and cat["citizen_analytics_platform_present_required"] is True
        and cat["no_code_analytics_platform_present_required"] is True
        and cat["low_code_analytics_platform_present_required"] is True
        and cat["natural_language_analytics_present_required"] is True
        and cat["ai_analytics_assistant_present_required"] is True
        and cat["collaborative_analytics_present_required"] is True
        and cat["semantic_layer_integration_present_required"] is True
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
        and cat["analytics_workspace_present_required"] is True
        and cat["ad_hoc_analytics_present_required"] is True
        and cat["sibling_business_intelligence_bc_forbidden"] is True
        and cat["domain_model"]["supporting_count"] >= 8
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["workspaces"]["type_count"] >= 7
        and cat["no_code_low_code"]["sql_knowledge_required"] is False
        and cat["ai_native"]["agent_count"] >= 7
        and cat["ai_native"]["via_enterprise_ai"] is True
        and cat["semantic_integration"]["via_p213_g"] is True
        and cat["knowledge_graph"]["via_p212_j"] is True
        and cat["digital_twin"]["via_p212_l"] is True
        and cat["discovery"]["via_p212_i"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["cqrs"]["query_count"] >= 5
        and cat["events"]["core_event_count"] >= 6
        and cat["microservices"]["service_count"] >= 8
        and cat["deployment"]["cloud_native"] is True
        and cat["cursor_outputs"]["count"] >= 20
        and "self_service_bi_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
        and "ai_analytics_assistant_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P213-G" in cat["builds_on"]
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
            BiSelfServiceProfileRoot.publish,
            tenant_id="t1",
            profile_ref="r1",
            complete=False,
        )
        and BiSelfServiceProfileRoot.publish(
            tenant_id="t1", profile_ref="r2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            BiAnalyticsWorkspaceRoot.create,
            tenant_id="t1",
            workspace_ref="w1",
            present=False,
        )
        and BiAnalyticsWorkspaceRoot.create(
            tenant_id="t1", workspace_ref="w2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiNoCodeAnalyticsRoot.enable,
            tenant_id="t1",
            builder_ref="b1",
            present=False,
        )
        and BiNoCodeAnalyticsRoot.enable(
            tenant_id="t1", builder_ref="b2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiAiAssistantRoot.enable,
            tenant_id="t1",
            assistant_ref="a1",
            present=False,
        )
        and BiAiAssistantRoot.enable(
            tenant_id="t1", assistant_ref="a2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiCollaborativeAnalyticsRoot.enable,
            tenant_id="t1",
            collab_ref="c1",
            present=False,
        )
        and BiCollaborativeAnalyticsRoot.enable(
            tenant_id="t1", collab_ref="c2"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/analytics/infrastructure/acl/bi_self_service_acl.py"
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
        and "via_p213_d" in acl_text
        and "via_p213_g" in acl_text
        and "via_enterprise_ai" in acl_text
        and "via_enterprise_search" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
        and "row_level_security" in acl_text
    )

    router = (
        root / "backend/contexts/analytics/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/self-service")' in router
        and "/self-service/readiness" in router
        and "/self-service/vision" in router
        and "/self-service/workspaces" in router
        and "/self-service/ai" in router
        and "/self-service/natural-language" in router
        and "/self-service/no-code" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_SELF_SERVICE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise self-service BI platform is missing" in law
        and "Never Citizen analytics platform is missing" in law
        and "Never No-code analytics platform is missing" in law
        and "Never Low-code analytics platform is missing" in law
        and "Never Natural language analytics is missing" in law
        and "Never AI analytics assistant is missing" in law
        and "Never Collaborative analytics is missing" in law
        and "Never Semantic layer integration is missing" in law
        and "Never Knowledge graph integration is missing" in law
        and "Never Digital twin integration is missing" in law
        and "Never CQRS architecture is missing" in law
        and "Never Event sourcing architecture is missing" in law
        and "Never Microservice architecture is missing" in law
        and "Never API first architecture is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Enterprise governance is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Self-service BI architecture is incomplete" in law
        and "Never Analytics workspace is missing" in law
        and "Never Ad-hoc analytics is missing" in law
        and "Never Sibling business intelligence BC" in law
        and "MEOS Enterprise Analytics Experience Fabric" in law
        and "without compromising governance" in law
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
        "prompt": "P213-H",
        "adr": 412,
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
