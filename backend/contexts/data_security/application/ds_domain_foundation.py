"""Data Security P211-C Domain Architecture foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/378-enterprise-data-security-domain-architecture.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_DOMAIN_ARCHITECTURE.md",
    "docs/architecture/data_security/DATA_SECURITY_DOMAIN_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DOMAIN_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DOMAIN_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DOMAIN_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_domain.py",
    "backend/contexts/data_security/domain/aggregates/ds_domain_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_domain_acl.py",
    "backend/contexts/data_security/application/ds_domain_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/dspm",
    "backend/contexts/dspm_platform",
    "backend/contexts/privacy_intelligence",
    "backend/contexts/data_classification",
    "backend/contexts/data_protection_platform",
    "backend/contexts/data_lineage_platform",
)


def validate_ds_domain_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_domain_aggregates import (
        DsAggregatesDefinedRoot,
        DsContextMapRoot,
        DsDomainMapRoot,
        DsDomainsLooselyCoupledRoot,
        DsEventsPresentRoot,
        DsIntegrationBoundariesClearRoot,
        DsOwnershipClearRoot,
        DsPrivacyIntegratedRoot,
    )
    from contexts.data_security.domain.services import ds_platform_domain as pdom

    cat = pdom.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-C"
        and cat.get("adr") == 378
        and cat.get("sor") == "data_security"
        and cat["domains_loosely_coupled_required"] is True
        and cat["data_ownership_clear_required"] is True
        and cat["privacy_integrated_with_security_required"] is True
        and cat["events_present_required"] is True
        and cat["aggregates_defined_required"] is True
        and cat["integration_boundaries_clear_required"] is True
        and cat["domain_map"]["not_tightly_coupled"] is True
        and cat["ownership"]["not_unclear"] is True
        and cat["privacy_security"]["not_separated"] is True
        and cat["events"]["not_missing"] is True
        and cat["aggregates"]["not_undefined"] is True
        and cat["integrations"]["not_unclear"] is True
        and cat["bounded_contexts"]["context_count"] >= 12
        and cat["aggregates"]["aggregate_count"] >= 12
        and cat["events"]["core_event_count"] >= 12
        and cat["microservices"]["service_count"] >= 12
        and cat["cursor_outputs"]["count"] >= 12
        and "domains_are_tightly_coupled" in cat["quality_gates"]["reject_if"]
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
            DsDomainsLooselyCoupledRoot.enforce,
            tenant_id="t1",
            map_ref="m1",
            loosely_coupled=False,
        )
        and DsDomainsLooselyCoupledRoot.enforce(
            tenant_id="t1", map_ref="m2"
        ).is_tightly_coupled()
        is False
    )
    checks.append(
        not _bad(
            DsOwnershipClearRoot.bind,
            tenant_id="t1",
            ownership_ref="o1",
            clear=False,
        )
        and DsOwnershipClearRoot.bind(
            tenant_id="t1", ownership_ref="o2"
        ).is_unclear()
        is False
    )
    checks.append(
        not _bad(
            DsPrivacyIntegratedRoot.integrate,
            tenant_id="t1",
            integration_ref="p1",
            integrated=False,
        )
        and DsPrivacyIntegratedRoot.integrate(
            tenant_id="t1", integration_ref="p2"
        ).is_separated()
        is False
    )
    checks.append(
        not _bad(
            DsEventsPresentRoot.publish,
            tenant_id="t1",
            catalogue_ref="e1",
            present=False,
        )
        and DsEventsPresentRoot.publish(
            tenant_id="t1", catalogue_ref="e2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DsAggregatesDefinedRoot.define,
            tenant_id="t1",
            catalog_ref="a1",
            defined=False,
        )
        and DsAggregatesDefinedRoot.define(
            tenant_id="t1", catalog_ref="a2"
        ).is_undefined()
        is False
    )
    checks.append(
        not _bad(
            DsIntegrationBoundariesClearRoot.declare,
            tenant_id="t1",
            boundary_ref="b1",
            clear=False,
        )
        and DsIntegrationBoundariesClearRoot.declare(
            tenant_id="t1", boundary_ref="b2"
        ).is_unclear()
        is False
    )
    published = DsDomainMapRoot.publish(tenant_id="t1", map_ref="dm1")
    registered = DsContextMapRoot.register(tenant_id="t1", context_ref="c1")
    checks.append("DomainMapPublished" in published.pending_events)
    checks.append("SubdomainRegistered" in registered.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/data_security/infrastructure/acl/ds_domain_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "privacy_integrated_with_security_required" in acl_text
        and "integration_boundaries_clear_required" in acl_text
        and "via_consent" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/domain")' in router
        and "/domain/map" in router
        and "/domain/bounded-contexts" in router
        and "/domain/aggregates" in router
        and "/domain/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_DOMAIN_ARCHITECTURE.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Domains are tightly coupled" in law
        and "Never Data ownership is unclear" in law
        and "Never Privacy is separated from security" in law
        and "Never Events are missing" in law
        and "Never Aggregates are undefined" in law
        and "Never Integration boundaries are unclear" in law
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
        "prompt": "P211-C",
        "adr": 378,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "data_security",
        "capability": "CAP-PLT-DS-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
