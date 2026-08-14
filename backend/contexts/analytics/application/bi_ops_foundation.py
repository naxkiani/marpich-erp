"""Analytics P213-N BI CQRS/Events/APIs/Microservices foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/418-enterprise-business-intelligence-ops.md",
    "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_OPS.md",
    "docs/architecture/business_intelligence/BI_OPS_CAPABILITIES.v1.yaml",
    "docs/architecture/business_intelligence/BI_OPS_DDD_CQRS.v1.yaml",
    "docs/architecture/business_intelligence/BI_OPS_SECURITY.v1.yaml",
    "docs/architecture/business_intelligence/BI_OPS_VALIDATION.v1.yaml",
    "backend/contexts/analytics/domain/services/bi_platform_ops.py",
    "backend/contexts/analytics/domain/aggregates/bi_ops_aggregates.py",
    "backend/contexts/analytics/infrastructure/acl/bi_ops_acl.py",
    "backend/contexts/analytics/application/bi_ops_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/business_intelligence",
    "backend/contexts/decision_intelligence",
    "backend/contexts/reporting_platform",
    "backend/contexts/metric_governance_platform",
    "backend/contexts/visualization_platform",
    "backend/contexts/bi_core",
)


def validate_bi_ops_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.analytics.domain.aggregates.bi_ops_aggregates import (
        BiApiManagementRoot,
        BiCqrsPlatformRoot,
        BiEventSourcingRoot,
        BiEventStreamingRoot,
        BiIntegrationPlatformRoot,
        BiMicroservicesPlatformRoot,
        BiOpsProfileRoot,
    )
    from contexts.analytics.domain.services import bi_platform_ops as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P213-N"
        and cat.get("adr") == 418
        and cat.get("sor") == "analytics"
        and cat.get("capability") == "CAP-PLT-BI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "durable enterprise event" in cat["principle"]
        and cat["cqrs_architecture_present_required"] is True
        and cat["event_sourcing_platform_present_required"] is True
        and cat["event_streaming_platform_present_required"] is True
        and cat["api_management_platform_present_required"] is True
        and cat["enterprise_integration_platform_present_required"] is True
        and cat["microservices_platform_present_required"] is True
        and cat["read_model_architecture_present_required"] is True
        and cat["api_first_design_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["observability_present_required"] is True
        and cat["high_availability_present_required"] is True
        and cat["disaster_recovery_present_required"] is True
        and cat["continuous_governance_present_required"] is True
        and cat["architecture_present_required"] is True
        and cat["sibling_business_intelligence_bc_forbidden"] is True
        and cat["via_enterprise_event_fabric"] is True
        and cat["via_api_gateway"] is True
        and cat["module_local_event_bus_forbidden"] is True
        and cat["module_local_gateway_forbidden"] is True
        and cat["domain_model"]["supporting_count"] >= 8
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["cqrs"]["command_count"] >= 6
        and cat["cqrs"]["query_count"] >= 6
        and cat["events"]["core_event_count"] >= 10
        and cat["microservices"]["service_count"] >= 10
        and cat["read_models"]["type_count"] >= 8
        and cat["event_sourcing"]["via_enterprise_event_fabric"] is True
        and cat["deployment"]["cloud_native"] is True
        and cat["cursor_outputs"]["count"] >= 20
        and "cqrs_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
        and "event_sourcing_platform_is_missing"
        in cat["quality_gates"]["reject_if"]
        and "P213-M" in cat["builds_on"]
        and "ADR-417" in cat["builds_on"]
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
            BiOpsProfileRoot.publish,
            tenant_id="t1",
            profile_ref="r1",
            complete=False,
        )
        and BiOpsProfileRoot.publish(
            tenant_id="t1", profile_ref="r2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            BiCqrsPlatformRoot.enable,
            tenant_id="t1",
            cqrs_ref="c1",
            present=False,
        )
        and BiCqrsPlatformRoot.enable(
            tenant_id="t1", cqrs_ref="c2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiEventSourcingRoot.enable,
            tenant_id="t1",
            store_ref="s1",
            present=False,
        )
        and BiEventSourcingRoot.enable(
            tenant_id="t1", store_ref="s2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiEventStreamingRoot.enable,
            tenant_id="t1",
            stream_ref="st1",
            present=False,
        )
        and BiEventStreamingRoot.enable(
            tenant_id="t1", stream_ref="st2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiApiManagementRoot.enable,
            tenant_id="t1",
            api_ref="a1",
            present=False,
        )
        and BiApiManagementRoot.enable(
            tenant_id="t1", api_ref="a2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiMicroservicesPlatformRoot.enable,
            tenant_id="t1",
            service_ref="ms1",
            present=False,
        )
        and BiMicroservicesPlatformRoot.enable(
            tenant_id="t1", service_ref="ms2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiIntegrationPlatformRoot.enable,
            tenant_id="t1",
            integration_ref="i1",
            present=False,
        )
        and BiIntegrationPlatformRoot.enable(
            tenant_id="t1", integration_ref="i2"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/analytics/infrastructure/acl/bi_ops_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_p213_m" in acl_text
        and "via_enterprise_event_fabric" in acl_text
        and "module_local_event_bus_forbidden" in acl_text
        and "via_api_gateway" in acl_text
        and "module_local_gateway_forbidden" in acl_text
        and "via_platform_observability" in acl_text
        and "via_enterprise_ai" in acl_text
    )

    router = (
        root / "backend/contexts/analytics/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/ops")' in router
        and "/ops/readiness" in router
        and "/ops/vision" in router
        and "/ops/cqrs" in router
        and "/ops/event-sourcing" in router
        and "/ops/streaming" in router
        and "/ops/apis" in router
        and "/ops/microservices" in router
        and "/ops/observability" in router
        and "/ops/resilience" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_OPS.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never CQRS architecture is incomplete" in law
        and "Never Event sourcing platform is missing" in law
        and "Never Event streaming platform is missing" in law
        and "Never API management platform is missing" in law
        and "Never Enterprise integration platform is missing" in law
        and "Never Microservices platform is missing" in law
        and "Never Read model architecture is missing" in law
        and "Never API first design is missing" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Observability is missing" in law
        and "Never High availability is missing" in law
        and "Never Disaster recovery is missing" in law
        and "Never Continuous governance is missing" in law
        and "Never BI CQRS architecture is incomplete" in law
        and "Never Sibling business intelligence BC" in law
        and "MEOS Enterprise Analytics Integration Fabric" in law
        and "durable enterprise event" in law
        and "Module-local event bus" in law
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
        "prompt": "P213-N",
        "adr": 418,
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
