"""Data Security P211-O deploy/DevSecOps foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/390-enterprise-data-security-deploy.md",
    "docs/architecture/ENTERPRISE_DATA_SECURITY_DEPLOY.md",
    "docs/architecture/data_security/DATA_SECURITY_DEPLOY_CAPABILITIES.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DEPLOY_DDD_CQRS.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DEPLOY_SECURITY.v1.yaml",
    "docs/architecture/data_security/DATA_SECURITY_DEPLOY_VALIDATION.v1.yaml",
    "backend/contexts/data_security/domain/services/ds_platform_deploy.py",
    "backend/contexts/data_security/domain/aggregates/ds_deploy_aggregates.py",
    "backend/contexts/data_security/infrastructure/acl/ds_deploy_acl.py",
    "backend/contexts/data_security/application/ds_deploy_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_security_deploy",
    "backend/contexts/ds_kubernetes_platform",
    "backend/contexts/data_security_observability",
)


def validate_ds_deploy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_security.domain.aggregates.ds_deploy_aggregates import (
        DsAnomalyDetectedRoot,
        DsAutomatedDeploymentRoot,
        DsCompleteMonitoringRoot,
        DsComplianceEvidenceRoot,
        DsDefinedDisasterRecoveryRoot,
        DsPresentRuntimeSecurityRoot,
        DsScalableInfrastructureRoot,
        DsSecurityScanningRoot,
    )
    from contexts.data_security.domain.services import (
        ds_platform_deploy as deploy,
    )

    cat = deploy.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P211-O"
        and cat.get("adr") == 390
        and cat.get("sor") == "data_security"
        and cat["deployment_automated_required"] is True
        and cat["security_scanning_present_required"] is True
        and cat["infrastructure_scalable_required"] is True
        and cat["monitoring_complete_required"] is True
        and cat["disaster_recovery_defined_required"] is True
        and cat["runtime_security_present_required"] is True
        and cat["automated_deployment"]["not_manual"] is True
        and cat["security_scanning"]["not_missing"] is True
        and cat["infrastructure_scale"]["not_unscalable"] is True
        and cat["monitoring_completeness"]["not_incomplete"] is True
        and cat["disaster_recovery"]["not_undefined"] is True
        and cat["runtime_security"]["not_absent"] is True
        and cat["architecture"]["layer_count"] >= 8
        and cat["domain"]["context_count"] >= 7
        and cat["kubernetes"]["cluster_count"] >= 4
        and cat["cqrs"]["event_count"] >= 8
        and cat["cursor_outputs"]["count"] >= 16
        and "deployment_is_manual" in cat["quality_gates"]["reject_if"]
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
            DsAutomatedDeploymentRoot.promote,
            tenant_id="t1",
            release_ref="r1",
            automated=False,
        )
        and DsAutomatedDeploymentRoot.promote(
            tenant_id="t1", release_ref="r2"
        ).is_manual()
        is False
    )
    checks.append(
        not _bad(
            DsSecurityScanningRoot.enforce,
            tenant_id="t1",
            scan_ref="s1",
            present=False,
        )
        and DsSecurityScanningRoot.enforce(
            tenant_id="t1", scan_ref="s2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DsScalableInfrastructureRoot.scale,
            tenant_id="t1",
            workload_ref="w1",
            scalable=False,
        )
        and DsScalableInfrastructureRoot.scale(
            tenant_id="t1", workload_ref="w2"
        ).cannot_scale()
        is False
    )
    checks.append(
        not _bad(
            DsCompleteMonitoringRoot.enable,
            tenant_id="t1",
            monitor_ref="m1",
            complete=False,
        )
        and DsCompleteMonitoringRoot.enable(
            tenant_id="t1", monitor_ref="m2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            DsDefinedDisasterRecoveryRoot.define,
            tenant_id="t1",
            dr_ref="d1",
            defined=False,
        )
        and DsDefinedDisasterRecoveryRoot.define(
            tenant_id="t1", dr_ref="d2"
        ).is_undefined()
        is False
    )
    checks.append(
        not _bad(
            DsPresentRuntimeSecurityRoot.enforce,
            tenant_id="t1",
            policy_ref="p1",
            present=False,
        )
        and DsPresentRuntimeSecurityRoot.enforce(
            tenant_id="t1", policy_ref="p2"
        ).is_absent()
        is False
    )
    evidence = DsComplianceEvidenceRoot.collect(
        tenant_id="t1", evidence_ref="e1"
    )
    anomaly = DsAnomalyDetectedRoot.detect(
        tenant_id="t1", anomaly_ref="a1"
    )
    checks.append("ComplianceEvidenceCollected" in evidence.pending_events)
    checks.append("AnomalyDetected" in anomaly.pending_events)
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_security/infrastructure/acl/ds_deploy_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_observability_platform" in acl_text
        and "deployment_automated_required" in acl_text
        and "security_scanning_present_required" in acl_text
        and "disaster_recovery_defined_required" in acl_text
        and "via_p210_siem" in acl_text
        and "via_p209" in acl_text
        and "module_local_metrics_store_forbidden" in acl_text
    )

    router = (
        root / "backend/contexts/data_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_security_router.get("/deploy")' in router
        and "/deploy/devsecops" in router
        and "/deploy/observability" in router
        and "/deploy/dr" in router
        and "/deploy/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_SECURITY_DEPLOY.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Deployment is manual" in law
        and "Never Security scanning is missing" in law
        and "Never Infrastructure cannot scale" in law
        and "Never Monitoring is incomplete" in law
        and "Never Disaster recovery is undefined" in law
        and "Never Runtime security is absent" in law
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
        "prompt": "P211-O",
        "adr": 390,
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
