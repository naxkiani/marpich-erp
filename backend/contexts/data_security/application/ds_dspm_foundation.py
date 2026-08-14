"""Data Security P211-F DSPM foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/381-enterprise-data-security-dspm.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_DSPM.md",
    "docs/architecture/data_security/DATA_SECURITY_DSPM_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DSPM_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DSPM_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DSPM_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_dspm.py",
    "backend/contexts/data_security/domain/aggregates/ds_dspm_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_dspm_acl.py",
    "backend/contexts/data_security/application/ds_dspm_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/dspm",
    "backend/contexts/dspm_platform",
    "backend/contexts/posture_management",
)


def validate_ds_dspm_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_dspm_aggregates import (
        DsAutonomousRemediationRoot,
        DsContinuousAssessmentRoot,
        DsControlAppliedRoot,
        DsKnownAssetsRoot,
        DsMeasurablePostureRoot,
        DsOwnedFindingRoot,
        DsSensitiveDetectedRoot,
        DsVisibleExposureRoot,
    )
    from contexts.data_security.domain.services import ds_platform_dspm as dspm

    cat = dspm.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-F"
        and cat.get("adr") == 381
        and cat.get("sor") == "data_security"
        and cat["data_assets_known_required"] is True
        and cat["security_posture_measurable_required"] is True
        and cat["exposure_risks_visible_required"] is True
        and cat["findings_owned_required"] is True
        and cat["remediation_not_manual_only_required"] is True
        and cat["continuous_assessment_available_required"] is True
        and cat["discovery_visibility"]["not_unknown"] is True
        and cat["posture_scoring"]["not_unmeasurable"] is True
        and cat["exposure_management"]["not_invisible"] is True
        and cat["findings"]["not_unowned"] is True
        and cat["remediation"]["not_manual_only"] is True
        and cat["continuous_assessment"]["not_unavailable"] is True
        and cat["architecture"]["layer_count"] >= 7
        and cat["architecture"]["scope_count"] >= 10
        and cat["domain"]["context_count"] >= 7
        and cat["cqrs"]["event_count"] >= 6
        and cat["cursor_outputs"]["count"] >= 14
        and "data_assets_are_unknown" in cat["quality_gates"]["reject_if"]
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
            DsKnownAssetsRoot.discover,
            tenant_id="t1",
            estate_ref="e1",
            known=False,
        )
        and DsKnownAssetsRoot.discover(
            tenant_id="t1", estate_ref="e2"
        ).is_unknown()
        is False
    )
    checks.append(
        not _bad(
            DsMeasurablePostureRoot.assess,
            tenant_id="t1",
            posture_ref="p1",
            measurable=False,
        )
        and DsMeasurablePostureRoot.assess(
            tenant_id="t1", posture_ref="p2"
        ).is_unmeasurable()
        is False
    )
    checks.append(
        not _bad(
            DsVisibleExposureRoot.detect,
            tenant_id="t1",
            exposure_ref="x1",
            visible=False,
        )
        and DsVisibleExposureRoot.detect(
            tenant_id="t1", exposure_ref="x2"
        ).is_invisible()
        is False
    )
    checks.append(
        not _bad(
            DsOwnedFindingRoot.create,
            tenant_id="t1",
            finding_ref="f1",
            owned=False,
        )
        and DsOwnedFindingRoot.create(
            tenant_id="t1", finding_ref="f2"
        ).is_unowned()
        is False
    )
    checks.append(
        not _bad(
            DsAutonomousRemediationRoot.generate,
            tenant_id="t1",
            action_ref="a1",
            autonomous_path=False,
        )
        and DsAutonomousRemediationRoot.generate(
            tenant_id="t1", action_ref="a2"
        ).is_manual_only()
        is False
    )
    checks.append(
        not _bad(
            DsContinuousAssessmentRoot.run,
            tenant_id="t1",
            assessment_ref="c1",
            available=False,
        )
        and DsContinuousAssessmentRoot.run(
            tenant_id="t1", assessment_ref="c2"
        ).is_unavailable()
        is False
    )
    control = DsControlAppliedRoot.apply(tenant_id="t1", control_ref="ctrl1")
    sens = DsSensitiveDetectedRoot.detect(tenant_id="t1", detection_ref="s1")
    checks.append("ControlApplied" in control.pending_events)
    checks.append("SensitiveDataDetected" in sens.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root / "backend/contexts/data_security/infrastructure/acl/ds_dspm_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p211_d_discovery" in acl_text
        and "via_p211_e_classification" in acl_text
        and "security_posture_measurable_required" in acl_text
        and "remediation_not_manual_only_required" in acl_text
        and "continuous_assessment_available_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/dspm")' in router
        and "/dspm/posture" in router
        and "/dspm/exposure" in router
        and "/dspm/remediation" in router
        and "/dspm/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_DSPM.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Data assets are unknown" in law
        and "Never Security posture cannot be measured" in law
        and "Never Exposure risks are invisible" in law
        and "Never Findings have no ownership" in law
        and "Never Remediation is manual only" in law
        and "Never Continuous assessment is unavailable" in law
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
        "prompt": "P211-F",
        "adr": 381,
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
