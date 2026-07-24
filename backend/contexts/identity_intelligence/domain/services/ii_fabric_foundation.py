"""Identity Intelligence P207-L distributed fabric foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/327-enterprise-identity-intelligence-cqrs-events-apis-microservices.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_DISTRIBUTED_FABRIC.md",
    "docs/architecture/identity/intelligence/II_FABRIC_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_FABRIC_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_FABRIC_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_FABRIC_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_fabric.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_fabric_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_fabric_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_fabric_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/identity_intelligence_runtime",
    "backend/contexts/identity_event_platform",
    "backend/contexts/identity_microservices_bc",
)


def validate_ii_fabric_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_fabric_aggregates import (
        ApiSecurityPolicyRoot,
        CommandCatalogRoot,
        EventContractCatalogRoot,
        EventStreamingTopologyRoot,
        ProductionReadinessAssessmentRoot,
        QueryCatalogRoot,
        ServiceBoundaryMapRoot,
    )
    from contexts.identity_intelligence.domain.services import ii_platform_fabric as fabric
    from contexts.identity_intelligence.infrastructure.acl import ii_fabric_acl as acls

    cat = fabric.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-L"
        and cat.get("adr") == 327
        and cat.get("sor") == "identity_intelligence"
        and cat["shared_database_forbidden"] is True
        and cat["secure_api_required"] is True
        and cat["capabilities"]["service_boundaries_required"] is True
        and cat["capabilities"]["cqrs_required"] is True
        and cat["capabilities"]["event_store_required"] is True
        and cat["capabilities"]["secure_apis_required"] is True
        and cat["capabilities"]["audit_history_required"] is True
        and cat["capabilities"]["ai_integration_connected_required"] is True
        and cat["microservice_architecture"]["shared_database_forbidden"] is True
        and cat["service_boundaries"]["not_unclear"] is True
        and cat["cqrs_design"]["cqrs_boundaries_clear"] is True
        and cat["event_catalog"]["defined"] is True
        and cat["api_security"]["apis_secure"] is True
        and cat["ai_native_integration"]["not_disconnected"] is True
        and cat["ddd"]["logical_count"] >= 9
        and cat["ddd"]["aggregate_count"] >= 7
        and cat["integrations"]["distributed_runtime_complete"] is True
        and "services_share_databases" in cat["quality_gates"]["reject_if"]
        and "apis_lack_security" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness_assessment"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        ServiceBoundaryMapRoot.define(
            tenant_id="t1",
            map_ref="m1",
            shared_database=True,
        )
        shared_db = True
    except ValueError:
        shared_db = False

    boundaries = ServiceBoundaryMapRoot.define(tenant_id="t1", map_ref="m2")
    boundaries_ok = (
        not shared_db
        and boundaries.shares_database() is False
        and "ServiceBoundaryDefined" in boundaries.pending_events
    )

    try:
        CommandCatalogRoot.register(
            tenant_id="t1",
            catalog_ref="c1",
            cqrs_clear=False,
        )
        unclear = True
    except ValueError:
        unclear = False

    commands = CommandCatalogRoot.register(tenant_id="t1", catalog_ref="c2")
    commands_ok = (
        not unclear
        and commands.boundaries_unclear() is False
        and "CommandCatalogRegistered" in commands.pending_events
    )

    queries = QueryCatalogRoot.register(tenant_id="t1", catalog_ref="q1")
    queries_ok = "QueryCatalogRegistered" in queries.pending_events

    try:
        EventContractCatalogRoot.register(
            tenant_id="t1",
            catalog_ref="e1",
            versioned=False,
        )
        undef = True
    except ValueError:
        undef = False

    events = EventContractCatalogRoot.register(tenant_id="t1", catalog_ref="e2")
    events_ok = (
        not undef
        and events.undefined() is False
        and "EventCatalogRegistered" in events.pending_events
    )

    try:
        ApiSecurityPolicyRoot.enforce(
            tenant_id="t1",
            policy_ref="a1",
            mtls_enabled=False,
        )
        insecure = True
    except ValueError:
        insecure = False

    api = ApiSecurityPolicyRoot.enforce(tenant_id="t1", policy_ref="a2")
    api_ok = (
        not insecure
        and api.insecure() is False
        and "ApiSecurityEnforced" in api.pending_events
    )

    stream = EventStreamingTopologyRoot.design(tenant_id="t1", topology_ref="t1")
    stream_ok = "EventStreamingDesigned" in stream.pending_events

    try:
        ProductionReadinessAssessmentRoot.assess(
            tenant_id="t1",
            assessment_ref="r1",
            audit_complete=False,
        )
        no_audit = True
    except ValueError:
        no_audit = False

    try:
        ProductionReadinessAssessmentRoot.assess(
            tenant_id="t1",
            assessment_ref="r2",
            ai_connected=False,
        )
        no_ai = True
    except ValueError:
        no_ai = False

    readiness = ProductionReadinessAssessmentRoot.assess(
        tenant_id="t1",
        assessment_ref="r3",
    )
    readiness_ok = (
        not no_audit
        and not no_ai
        and readiness.audit_incomplete() is False
        and readiness.ai_disconnected() is False
        and "ProductionReadinessAssessed" in readiness.pending_events
    )

    aggregates_ok = (
        boundaries_ok
        and commands_ok
        and queries_ok
        and events_ok
        and api_ok
        and stream_ok
        and readiness_ok
    )

    acl_ok = (
        acls.to_authz_check(
            tenant_id="t1", subject_id="u1", action="identity_intelligence.read"
        )["policy_based_access"]
        is True
        and acls.to_audit(
            tenant_id="t1", action="ii.fabric.release", resource_ref="r3"
        )["complete_audit_history_required"]
        is True
        and acls.to_ai_infer(tenant_id="t1", surface="fabric", context={})[
            "ai_integration_connected_required"
        ]
        is True
        and acls.to_observability(
            tenant_id="t1", metric_name="latency", value=12.0
        )["service_latency_tracking"]
        is True
        and acls.to_event_fabric(
            tenant_id="t1", event_name="IdentityAnalyzed", version="v1"
        )["event_versioning_required"]
        is True
        and acls.to_service_mesh(
            tenant_id="t1", service_name="identity-risk-service"
        )["mtls_required"]
        is True
        and acls.to_api_gateway(
            tenant_id="t1", route_ref="/fabric/apis"
        )["gateway_required"]
        is True
    )

    router = (
        root / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@identity_intelligence_router.get("/fabric"' in router
        and "/fabric/cqrs" in router
        and "/fabric/events" in router
        and "/fabric/api-security" in router
        and "/fabric/kubernetes" in router
        and "/fabric/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_DISTRIBUTED_FABRIC.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never services share databases" in law
        and "Never undefined events" in law
        and "Never APIs lack security" in law
        and "Never CQRS boundaries are unclear" in law
        and "Never audit history is incomplete" in law
        and "Never AI integration is disconnected" in law
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
        "prompt": "P207-L",
        "adr": 327,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "identity_intelligence",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
