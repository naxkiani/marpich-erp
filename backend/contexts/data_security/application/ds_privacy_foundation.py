"""Data Security P211-I Privacy intelligence foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/384-enterprise-data-security-privacy.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_PRIVACY.md",
    "docs/architecture/data_security/DATA_SECURITY_PRIVACY_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_PRIVACY_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_PRIVACY_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_PRIVACY_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_privacy.py",
    "backend/contexts/data_security/domain/aggregates/ds_privacy_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_privacy_acl.py",
    "backend/contexts/data_security/application/ds_privacy_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/privacy_intelligence",
    "backend/contexts/data_privacy_platform",
    "backend/contexts/personal_data_platform",
)


def validate_ds_privacy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_privacy_aggregates import (
        DsAssessmentCompletedRoot,
        DsConsentWithdrawnRoot,
        DsDiscoverablePersonalDataRoot,
        DsManagedAiPrivacyRoot,
        DsMappedObligationsRoot,
        DsMeasurablePrivacyRiskRoot,
        DsTrackableConsentRoot,
        DsVisibleProcessingRoot,
    )
    from contexts.data_security.domain.services import (
        ds_platform_privacy as privacy,
    )

    cat = privacy.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-I"
        and cat.get("adr") == 384
        and cat.get("sor") == "data_security"
        and cat["personal_data_discoverable_required"] is True
        and cat["consent_trackable_required"] is True
        and cat["privacy_risks_measurable_required"] is True
        and cat["processing_visible_required"] is True
        and cat["regulatory_obligations_mapped_required"] is True
        and cat["ai_privacy_risks_managed_required"] is True
        and cat["consent_ledger_remains_consent"] is True
        and cat["personal_data"]["not_undiscoverable"] is True
        and cat["consent"]["not_untrackable"] is True
        and cat["privacy_risk"]["not_unmeasurable"] is True
        and cat["processing"]["not_invisible"] is True
        and cat["obligations"]["not_unmapped"] is True
        and cat["ai_privacy"]["not_unmanaged"] is True
        and cat["consent"]["ledger_owner"] == "consent"
        and cat["architecture"]["layer_count"] >= 7
        and cat["domain"]["context_count"] >= 7
        and cat["cqrs"]["event_count"] >= 6
        and cat["cursor_outputs"]["count"] >= 16
        and "personal_data_cannot_be_discovered"
        in cat["quality_gates"]["reject_if"]
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
            DsDiscoverablePersonalDataRoot.discover,
            tenant_id="t1",
            asset_ref="a1",
            discoverable=False,
        )
        and DsDiscoverablePersonalDataRoot.discover(
            tenant_id="t1", asset_ref="a2"
        ).is_undiscoverable()
        is False
    )
    checks.append(
        not _bad(
            DsTrackableConsentRoot.track,
            tenant_id="t1",
            consent_ref="c1",
            trackable=False,
        )
        and DsTrackableConsentRoot.track(
            tenant_id="t1", consent_ref="c2"
        ).is_untrackable()
        is False
    )
    checks.append(
        not _bad(
            DsMeasurablePrivacyRiskRoot.measure,
            tenant_id="t1",
            risk_ref="r1",
            measurable=False,
        )
        and DsMeasurablePrivacyRiskRoot.measure(
            tenant_id="t1", risk_ref="r2"
        ).is_unmeasurable()
        is False
    )
    checks.append(
        not _bad(
            DsVisibleProcessingRoot.register,
            tenant_id="t1",
            activity_ref="p1",
            visible=False,
        )
        and DsVisibleProcessingRoot.register(
            tenant_id="t1", activity_ref="p2"
        ).is_invisible()
        is False
    )
    checks.append(
        not _bad(
            DsMappedObligationsRoot.map,
            tenant_id="t1",
            obligation_ref="o1",
            mapped=False,
        )
        and DsMappedObligationsRoot.map(
            tenant_id="t1", obligation_ref="o2"
        ).is_unmapped()
        is False
    )
    checks.append(
        not _bad(
            DsManagedAiPrivacyRoot.govern,
            tenant_id="t1",
            ai_ref="ai1",
            managed=False,
        )
        and DsManagedAiPrivacyRoot.govern(
            tenant_id="t1", ai_ref="ai2"
        ).is_unmanaged()
        is False
    )
    withdrawn = DsConsentWithdrawnRoot.withdraw(
        tenant_id="t1", consent_ref="cw1"
    )
    assessed = DsAssessmentCompletedRoot.complete(
        tenant_id="t1", assessment_ref="as1"
    )
    checks.append("ConsentWithdrawn" in withdrawn.pending_events)
    checks.append("AssessmentCompleted" in assessed.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_security/infrastructure/acl/ds_privacy_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_consent_bc" in acl_text
        and "absorb_consent_ledger_forbidden" in acl_text
        and "personal_data_discoverable_required" in acl_text
        and "ai_privacy_risks_managed_required" in acl_text
        and "regulatory_obligations_mapped_required" in acl_text
        and "via_p211_h_access" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/privacy")' in router
        and "/privacy/consent" in router
        and "/privacy/dsar" in router
        and "/privacy/dpia" in router
        and "/privacy/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_PRIVACY.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Personal data cannot be discovered" in law
        and "Never Consent cannot be tracked" in law
        and "Never Privacy risks cannot be measured" in law
        and "Never Data processing is invisible" in law
        and "Never Regulatory obligations are unmapped" in law
        and "Never AI privacy risks are unmanaged" in law
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
        "prompt": "P211-I",
        "adr": 384,
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
