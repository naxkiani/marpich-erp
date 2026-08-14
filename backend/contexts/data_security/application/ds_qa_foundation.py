"""Data Security P211-P QA/governance/DoD foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/391-enterprise-data-security-qa.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_QA.md",
    "docs/architecture/data_security/DATA_SECURITY_QA_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_QA_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_QA_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_QA_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_qa.py",
    "backend/contexts/data_security/domain/aggregates/ds_qa_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_qa_acl.py",
    "backend/contexts/data_security/application/ds_qa_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_security_qa",
    "backend/contexts/ds_assurance_platform",
    "backend/contexts/data_security_compliance_validation",
)


def validate_ds_qa_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_qa_aggregates import (
        DsAutomatedTestingRoot,
        DsAvailableComplianceEvidenceRoot,
        DsClearGovernanceOwnershipRoot,
        DsDefinedProductionReadinessRoot,
        DsFindingCreatedRoot,
        DsPresentSecurityValidationRoot,
        DsReleaseApprovedRoot,
        DsTrackableRisksRoot,
    )
    from contexts.data_security.domain.services import ds_platform_qa as qa

    cat = qa.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-P"
        and cat.get("adr") == 391
        and cat.get("sor") == "data_security"
        and cat["testing_automated_required"] is True
        and cat["compliance_evidence_available_required"] is True
        and cat["security_validation_present_required"] is True
        and cat["governance_ownership_clear_required"] is True
        and cat["risks_trackable_required"] is True
        and cat["production_readiness_defined_required"] is True
        and cat["automated_testing"]["not_manual_only"] is True
        and cat["compliance_evidence"]["not_unavailable"] is True
        and cat["security_validation"]["not_missing"] is True
        and cat["governance_ownership"]["not_unclear"] is True
        and cat["risk_tracking"]["not_untrackable"] is True
        and cat["production_readiness"]["not_undefined"] is True
        and cat["architecture"]["layer_count"] >= 6
        and cat["domain"]["context_count"] >= 7
        and cat["cqrs"]["event_count"] >= 7
        and cat["cursor_outputs"]["count"] >= 16
        and cat["series_finalizes_p211"] is True
        and "testing_is_manual_only" in cat["quality_gates"]["reject_if"]
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
            DsAutomatedTestingRoot.execute,
            tenant_id="t1",
            plan_ref="p1",
            automated=False,
        )
        and DsAutomatedTestingRoot.execute(
            tenant_id="t1", plan_ref="p2"
        ).is_manual_only()
        is False
    )
    checks.append(
        not _bad(
            DsAvailableComplianceEvidenceRoot.collect,
            tenant_id="t1",
            evidence_ref="e1",
            available=False,
        )
        and DsAvailableComplianceEvidenceRoot.collect(
            tenant_id="t1", evidence_ref="e2"
        ).is_unavailable()
        is False
    )
    checks.append(
        not _bad(
            DsPresentSecurityValidationRoot.validate,
            tenant_id="t1",
            validation_ref="v1",
            present=False,
        )
        and DsPresentSecurityValidationRoot.validate(
            tenant_id="t1", validation_ref="v2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DsClearGovernanceOwnershipRoot.assign,
            tenant_id="t1",
            control_ref="c1",
            clear=False,
        )
        and DsClearGovernanceOwnershipRoot.assign(
            tenant_id="t1", control_ref="c2"
        ).is_unclear()
        is False
    )
    checks.append(
        not _bad(
            DsTrackableRisksRoot.track,
            tenant_id="t1",
            risk_ref="r1",
            trackable=False,
        )
        and DsTrackableRisksRoot.track(
            tenant_id="t1", risk_ref="r2"
        ).cannot_be_tracked()
        is False
    )
    checks.append(
        not _bad(
            DsDefinedProductionReadinessRoot.certify,
            tenant_id="t1",
            readiness_ref="pr1",
            defined=False,
        )
        and DsDefinedProductionReadinessRoot.certify(
            tenant_id="t1", readiness_ref="pr2"
        ).is_undefined()
        is False
    )
    finding = DsFindingCreatedRoot.open(tenant_id="t1", finding_ref="f1")
    release = DsReleaseApprovedRoot.approve(
        tenant_id="t1", release_ref="rel1"
    )
    checks.append("FindingCreated" in finding.pending_events)
    checks.append("ReleaseApproved" in release.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/data_security/infrastructure/acl/ds_qa_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_audit_platform" in acl_text
        and "testing_automated_required" in acl_text
        and "compliance_evidence_available_required" in acl_text
        and "governance_ownership_clear_required" in acl_text
        and "risks_trackable_required" in acl_text
        and "via_p211_o_devsecops" in acl_text
        and "via_consent_acl_only" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/qa")' in router
        and "/qa/testing" in router
        and "/qa/definition-of-done" in router
        and "/qa/quality-gates" in router
        and "/qa/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_QA.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Testing is manual only" in law
        and "Never Compliance evidence is unavailable" in law
        and "Never Security validation is missing" in law
        and "Never Governance ownership is unclear" in law
        and "Never Risks cannot be tracked" in law
        and "Never Production readiness is undefined" in law
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
        "prompt": "P211-P",
        "adr": 391,
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
        "series_finalizes_p211": True,
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
