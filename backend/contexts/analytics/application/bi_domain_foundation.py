"""Analytics P213-C BI Domain Architecture foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/396-enterprise-business-intelligence-domain-architecture.md",
    "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_DOMAIN_ARCHITECTURE.md",
    "docs/architecture/business_intelligence/BI_DOMAIN_CAPABILITIES.v1.yaml",
    "docs/architecture/business_intelligence/BI_DOMAIN_DDD_CQRS.v1.yaml",
    "docs/architecture/business_intelligence/BI_DOMAIN_SECURITY.v1.yaml",
    "docs/architecture/business_intelligence/BI_DOMAIN_VALIDATION.v1.yaml",
    "backend/contexts/analytics/domain/services/bi_platform_domain.py",
    "backend/contexts/analytics/domain/aggregates/bi_domain_aggregates.py",
    "backend/contexts/analytics/infrastructure/acl/bi_domain_acl.py",
    "backend/contexts/analytics/application/bi_domain_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/business_intelligence",
    "backend/contexts/decision_intelligence",
    "backend/contexts/reporting_platform",
    "backend/contexts/metric_governance_platform",
    "backend/contexts/visualization_platform",
    "backend/contexts/bi_core",
)


def validate_bi_domain_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.analytics.domain.aggregates.bi_domain_aggregates import (
        BiAggregatesDefinedRoot,
        BiContextMapRoot,
        BiCqrsAlignedRoot,
        BiDataMeshAlignedRoot,
        BiDigitalTwinAlignedRoot,
        BiDomainMapRoot,
        BiDomainsLooselyCoupledRoot,
        BiEventsPresentRoot,
        BiGovernanceAlignedRoot,
        BiIntegrationBoundariesClearRoot,
        BiKnowledgeGraphAlignedRoot,
        BiMicroserviceBoundariesClearRoot,
        BiOwnershipClearRoot,
    )
    from contexts.analytics.domain.services import bi_platform_domain as pdom

    cat = pdom.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P213-C"
        and cat.get("adr") == 396
        and cat.get("sor") == "analytics"
        and cat.get("capability") == "CAP-PLT-BI-001"
        and cat.get("principle") == pdom.PRINCIPLE
        and cat.get("fabric") == pdom.FABRIC
        and "governed" in cat["principle"]
        and cat["domain_map"]["core_domain"]
        == "enterprise_business_intelligence_management"
        and cat["domain_map"]["supporting_count"] >= 4
        and cat["complete_ddd_bi_architecture_present_required"] is True
        and cat["strategic_domain_model_present_required"] is True
        and cat["bounded_contexts_present_required"] is True
        and cat["domains_loosely_coupled_required"] is True
        and cat["bi_ownership_clear_required"] is True
        and cat["aggregates_defined_required"] is True
        and cat["entities_defined_required"] is True
        and cat["value_objects_defined_required"] is True
        and cat["domain_services_present_required"] is True
        and cat["events_present_required"] is True
        and cat["integration_boundaries_clear_required"] is True
        and cat["cqrs_alignment_present_required"] is True
        and cat["microservice_boundaries_clear_required"] is True
        and cat["data_mesh_alignment_present_required"] is True
        and cat["knowledge_graph_alignment_present_required"] is True
        and cat["digital_twin_alignment_present_required"] is True
        and cat["enterprise_governance_alignment_present_required"] is True
        and cat["sibling_business_intelligence_bc_forbidden"] is True
        and cat["domain_map"]["not_tightly_coupled"] is True
        and cat["ownership"]["not_unclear"] is True
        and cat["events"]["not_missing"] is True
        and cat["aggregates"]["not_undefined"] is True
        and cat["integrations"]["not_unclear"] is True
        and cat["integrations"]["data_mesh"]["via_p212_f"] is True
        and cat["integrations"]["knowledge_graph"]["via_p212_j"] is True
        and cat["integrations"]["digital_twin"]["via_p212_l"] is True
        and cat["integrations"]["governance"]["via_p207"] is True
        and cat["cqrs"]["not_missing"] is True
        and cat["cqrs"]["command_count"] >= 5
        and cat["cqrs"]["query_count"] >= 5
        and cat["microservices"]["not_unclear"] is True
        and cat["bounded_contexts"]["context_count"] >= 5
        and cat["aggregates"]["aggregate_count"] >= 4
        and cat["events"]["core_event_count"] >= 8
        and cat["microservices"]["service_count"] >= 6
        and cat["domain_services"]["service_count"] >= 5
        and cat["entities"]["entity_count"] >= 10
        and cat["value_objects"]["count"] >= 8
        and cat["cursor_outputs"]["count"] >= 17
        and cat["deployment"]["cloud_native"] is True
        and "domains_are_tightly_coupled" in cat["quality_gates"]["reject_if"]
        and (
            "complete_ddd_bi_architecture_is_missing"
            in cat["quality_gates"]["reject_if"]
        )
        and (
            "strategic_domain_model_is_missing"
            in cat["quality_gates"]["reject_if"]
        )
        and "P213-A" in cat["builds_on"]
        and "P213-B" in cat["builds_on"]
        and "P212-F" in cat["builds_on"]
        and "P212-J" in cat["builds_on"]
        and "P212-L" in cat["builds_on"]
        and "P212-M" in cat["builds_on"]
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
            BiDomainsLooselyCoupledRoot.enforce,
            tenant_id="t1",
            map_ref="m1",
            loosely_coupled=False,
        )
        and BiDomainsLooselyCoupledRoot.enforce(
            tenant_id="t1", map_ref="m2"
        ).is_tightly_coupled()
        is False
    )
    checks.append(
        not _bad(
            BiOwnershipClearRoot.bind,
            tenant_id="t1",
            ownership_ref="o1",
            clear=False,
        )
        and BiOwnershipClearRoot.bind(
            tenant_id="t1", ownership_ref="o2"
        ).is_unclear()
        is False
    )
    checks.append(
        not _bad(
            BiAggregatesDefinedRoot.define,
            tenant_id="t1",
            catalog_ref="a1",
            defined=False,
        )
        and BiAggregatesDefinedRoot.define(
            tenant_id="t1", catalog_ref="a2"
        ).is_undefined()
        is False
    )
    checks.append(
        not _bad(
            BiEventsPresentRoot.publish,
            tenant_id="t1",
            catalogue_ref="e1",
            present=False,
        )
        and BiEventsPresentRoot.publish(
            tenant_id="t1", catalogue_ref="e2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiIntegrationBoundariesClearRoot.declare,
            tenant_id="t1",
            boundary_ref="b1",
            clear=False,
        )
        and BiIntegrationBoundariesClearRoot.declare(
            tenant_id="t1", boundary_ref="b2"
        ).is_unclear()
        is False
    )
    checks.append(
        not _bad(
            BiCqrsAlignedRoot.align,
            tenant_id="t1",
            cqrs_ref="c1",
            present=False,
        )
        and BiCqrsAlignedRoot.align(
            tenant_id="t1", cqrs_ref="c2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiMicroserviceBoundariesClearRoot.declare,
            tenant_id="t1",
            boundary_ref="ms1",
            clear=False,
        )
        and BiMicroserviceBoundariesClearRoot.declare(
            tenant_id="t1", boundary_ref="ms2"
        ).is_unclear()
        is False
    )
    checks.append(
        not _bad(
            BiDataMeshAlignedRoot.align,
            tenant_id="t1",
            mesh_ref="dm1",
            present=False,
        )
        and BiDataMeshAlignedRoot.align(
            tenant_id="t1", mesh_ref="dm2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiKnowledgeGraphAlignedRoot.align,
            tenant_id="t1",
            graph_ref="kg1",
            present=False,
        )
        and BiKnowledgeGraphAlignedRoot.align(
            tenant_id="t1", graph_ref="kg2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiDigitalTwinAlignedRoot.align,
            tenant_id="t1",
            twin_ref="tw1",
            present=False,
        )
        and BiDigitalTwinAlignedRoot.align(
            tenant_id="t1", twin_ref="tw2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiGovernanceAlignedRoot.align,
            tenant_id="t1",
            gov_ref="g1",
            present=False,
        )
        and BiGovernanceAlignedRoot.align(
            tenant_id="t1", gov_ref="g2"
        ).is_missing()
        is False
    )
    published = BiDomainMapRoot.publish(tenant_id="t1", map_ref="dm1")
    registered = BiContextMapRoot.register(tenant_id="t1", context_ref="c1")
    checks.append("DomainMapPublished" in published.pending_events)
    checks.append("SubdomainRegistered" in registered.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/analytics/infrastructure/acl/bi_domain_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p212" in acl_text
        and "via_p212_j" in acl_text
        and "via_p212_l" in acl_text
        and "via_p211" in acl_text
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_enterprise_ai" in acl_text
        and "data_mesh_alignment_present_required" in acl_text
        and "knowledge_graph_alignment_present_required" in acl_text
        and "digital_twin_alignment_present_required" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/analytics/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/domain")' in router
        and "/domain/map" in router
        and "/domain/bounded-contexts" in router
        and "/domain/aggregates" in router
        and "/domain/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_DOMAIN_ARCHITECTURE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Complete DDD BI architecture is missing" in law
        and "Never Strategic domain model is missing" in law
        and "Never Bounded contexts are missing" in law
        and "Never Domains are tightly coupled" in law
        and "Never BI ownership is unclear" in law
        and "Never Aggregates are undefined" in law
        and "Never Entities are undefined" in law
        and "Never Value objects are undefined" in law
        and "Never Events are missing" in law
        and "Never Domain services are missing" in law
        and "Never Integration boundaries are unclear" in law
        and "Never CQRS alignment is missing" in law
        and "Never Microservice boundaries are unclear" in law
        and "Never Data mesh alignment is missing" in law
        and "Never Knowledge graph alignment is missing" in law
        and "Never Digital twin alignment is missing" in law
        and "Never Enterprise governance alignment is missing" in law
        and "Never Sibling business intelligence BC" in law
        and "MEOS Enterprise BI Domain Fabric" in law
        and (
            "Raw enterprise data SHALL be transformed into governed"
            in law
        )
        and "Only validated intelligence assets can be published" in law
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
        "prompt": "P213-C",
        "adr": 396,
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
