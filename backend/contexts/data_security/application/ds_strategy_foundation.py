"""Data Security P211-A Strategy foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/376-enterprise-data-security-strategy.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_STRATEGY.md",
    "docs/architecture/data_security/DATA_SECURITY_STRATEGY_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_STRATEGY_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_STRATEGY_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_STRATEGY_VALIDATION.v1.yaml",
    "docs/architecture/data_security/P211_MASTER_SERIES_ROADMAP.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_strategy.py",
    "backend/contexts/data_security/domain/aggregates/ds_strategy_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_strategy_acl.py",
    "backend/contexts/data_security/application/ds_strategy_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/dspm",
    "backend/contexts/dspm_platform",
    "backend/contexts/privacy_intelligence",
    "backend/contexts/data_classification",
    "backend/contexts/data_protection_platform",
    "backend/contexts/data_lineage_platform",
    "backend/contexts/data_privacy_platform",
)


def validate_ds_strategy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_strategy_aggregates import (
        DsAvailableLineageRoot,
        DsClassifiableDataRoot,
        DsComplianceEvidenceRoot,
        DsDiscoverableAssetRoot,
        DsGovernedAccessRoot,
        DsMeasurablePrivacyRiskRoot,
        DsProtectedAiDataRoot,
        DsStrategyProfileRoot,
    )
    from contexts.data_security.domain.services import (
        ds_platform_strategy as strat,
    )

    cat = strat.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-A"
        and cat.get("adr") == 376
        and cat.get("sor") == "data_security"
        and cat.get("capability") == "CAP-PLT-DS-001"
        and cat["data_assets_discoverable_required"] is True
        and cat["sensitive_data_classifiable_required"] is True
        and cat["privacy_risks_measurable_required"] is True
        and cat["data_access_governed_required"] is True
        and cat["ai_data_protected_required"] is True
        and cat["data_lineage_available_required"] is True
        and cat["compliance_evidence_generatable_required"] is True
        and cat["inventory"]["not_undiscoverable"] is True
        and cat["classification"]["not_unclassifiable"] is True
        and cat["privacy"]["not_unmeasurable"] is True
        and cat["zero_trust_data"]["not_ungoverned"] is True
        and cat["ai_data_security"]["not_unprotected"] is True
        and cat["lineage"]["not_unavailable"] is True
        and cat["compliance"]["not_ungeneratable"] is True
        and cat["architecture"]["layer_count"] >= 8
        and cat["inventory"]["asset_count"] >= 10
        and cat["cqrs"]["event_count"] >= 7
        and cat["cursor_outputs"]["count"] >= 20
        and "data_assets_cannot_be_discovered" in cat["quality_gates"]["reject_if"]
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
            DsDiscoverableAssetRoot.register,
            tenant_id="t1",
            asset_ref="a1",
            discoverable=False,
        )
        and DsDiscoverableAssetRoot.register(
            tenant_id="t1", asset_ref="a2"
        ).is_undiscoverable()
        is False
    )
    checks.append(
        not _bad(
            DsClassifiableDataRoot.classify,
            tenant_id="t1",
            asset_ref="a3",
            classifiable=False,
        )
        and DsClassifiableDataRoot.classify(
            tenant_id="t1", asset_ref="a4"
        ).is_unclassifiable()
        is False
    )
    checks.append(
        not _bad(
            DsMeasurablePrivacyRiskRoot.assess,
            tenant_id="t1",
            risk_ref="r1",
            measurable=False,
        )
        and DsMeasurablePrivacyRiskRoot.assess(
            tenant_id="t1", risk_ref="r2"
        ).is_unmeasurable()
        is False
    )
    checks.append(
        not _bad(
            DsGovernedAccessRoot.govern,
            tenant_id="t1",
            policy_ref="p1",
            governed=False,
        )
        and DsGovernedAccessRoot.govern(
            tenant_id="t1", policy_ref="p2"
        ).is_ungoverned()
        is False
    )
    checks.append(
        not _bad(
            DsProtectedAiDataRoot.protect,
            tenant_id="t1",
            dataset_ref="d1",
            protected=False,
        )
        and DsProtectedAiDataRoot.protect(
            tenant_id="t1", dataset_ref="d2"
        ).is_unprotected()
        is False
    )
    checks.append(
        not _bad(
            DsAvailableLineageRoot.declare,
            tenant_id="t1",
            lineage_ref="l1",
            available=False,
        )
        and DsAvailableLineageRoot.declare(
            tenant_id="t1", lineage_ref="l2"
        ).is_unavailable()
        is False
    )
    checks.append(
        not _bad(
            DsComplianceEvidenceRoot.generate,
            tenant_id="t1",
            evidence_ref="e1",
            generatable=False,
        )
        and DsComplianceEvidenceRoot.generate(
            tenant_id="t1", evidence_ref="e2"
        ).is_ungeneratable()
        is False
    )
    published = DsStrategyProfileRoot.publish(
        tenant_id="t1", strategy_ref="s1"
    )
    checks.append("DataSecurityStrategyPublished" in published.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/data_security/infrastructure/acl/ds_strategy_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_consent" in acl_text
        and "via_p209" in acl_text
        and "via_p208" in acl_text
        and "via_p210" in acl_text
        and "compliance_evidence_generatable_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/strategy")' in router
        and "/strategy/inventory" in router
        and "/strategy/classification" in router
        and "/strategy/privacy" in router
        and "/strategy/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_STRATEGY.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Data assets cannot be discovered" in law
        and "Never Sensitive data cannot be classified" in law
        and "Never Privacy risks cannot be measured" in law
        and "Never Data access cannot be governed" in law
        and "Never AI data cannot be protected" in law
        and "Never Data lineage is unavailable" in law
        and "Never Compliance evidence cannot be generated" in law
    )

    registry = (root / "backend/contexts/registry.py").read_text(encoding="utf-8")
    registry_ok = 'id="data_security"' in registry and "DATA_SECURITY" in registry

    startup = (
        root / "backend/core/presentation/api/startup_registry.py"
    ).read_text(encoding="utf-8")
    startup_ok = "contexts.data_security.presentation.router" in startup

    passed = (
        not missing
        and not sibling
        and catalog_ok
        and aggregates_ok
        and acl_ok
        and router_ok
        and doc_ok
        and registry_ok
        and startup_ok
    )
    return {
        "prompt": "P211-A",
        "adr": 376,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "registry": registry_ok,
        "startup": startup_ok,
        "sor": "data_security",
        "capability": "CAP-PLT-DS-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
