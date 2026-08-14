"""Cyber Security P210-N Deploy / DevSecOps foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/374-enterprise-cyber-security-deploy-devsecops.md",
    "docs/architecture/ENTERPRISE_CYBER_SECURITY_DEPLOY.md",
    "docs/architecture/cyber_security/CYBER_DEPLOY_CAPABILITIES.v1.yaml",
    "docs/architecture/cyber_security/CYBER_DEPLOY_DDD_CQRS.v1.yaml",
    "docs/architecture/cyber_security/CYBER_DEPLOY_SECURITY.v1.yaml",
    "docs/architecture/cyber_security/CYBER_DEPLOY_VALIDATION.v1.yaml",
    "backend/contexts/cyber_security/domain/services/cs_platform_deploy.py",
    "backend/contexts/cyber_security/domain/aggregates/cs_deploy_aggregates.py",
    "backend/contexts/cyber_security/infrastructure/acl/cs_deploy_acl.py",
    "backend/contexts/cyber_security/application/cs_deploy_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/deploy_platform",
    "backend/contexts/devsecops",
    "backend/contexts/k8s_platform",
    "backend/contexts/cyber_observability",
    "backend/contexts/cyber_ops",
)


def validate_cs_deploy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.cyber_security.domain.aggregates.cs_deploy_aggregates import (
        CsDeployAutoScalingRoot,
        CsDeployAutomatedPipelineRoot,
        CsDeployDisasterRecoveryRoot,
        CsDeployK8sSecurityRoot,
        CsDeployObservabilityRoot,
        CsDeployPipelineValidationRoot,
        CsDeployReproducibleInfraRoot,
        CsDeploySecurityControlsRoot,
    )
    from contexts.cyber_security.domain.services import cs_platform_deploy as deploy

    cat = deploy.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P210-N"
        and cat.get("adr") == 374
        and cat.get("sor") == "cyber_security"
        and cat["deployment_automated_required"] is True
        and cat["kubernetes_security_complete_required"] is True
        and cat["infrastructure_reproducible_required"] is True
        and cat["observability_required"] is True
        and cat["auto_scaling_required"] is True
        and cat["disaster_recovery_defined_required"] is True
        and cat["security_controls_integrated_required"] is True
        and cat["pipeline_validation_required"] is True
        and cat["module_local_observability_stack_forbidden"] is True
        and cat["devsecops"]["not_manual_only"] is True
        and cat["kubernetes"]["not_incomplete"] is True
        and cat["iac"]["not_non_reproducible"] is True
        and cat["observability"]["not_missing"] is True
        and cat["scalability"]["not_manual_only"] is True
        and cat["resilience"]["not_undefined"] is True
        and cat["security_observability"]["not_unintegrated"] is True
        and cat["devsecops"]["not_lacking_validation"] is True
        and cat["architecture"]["layer_count"] >= 10
        and cat["cqrs"]["event_count"] >= 8
        and cat["cursor_outputs"]["count"] >= 20
        and "deployment_is_not_automated" in cat["quality_gates"]["reject_if"]
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
            CsDeployAutomatedPipelineRoot.start,
            tenant_id="t1",
            pipeline_ref="p1",
            automated=False,
        )
        and CsDeployAutomatedPipelineRoot.start(
            tenant_id="t1", pipeline_ref="p2"
        ).is_manual_only()
        is False
    )
    checks.append(
        not _bad(
            CsDeployK8sSecurityRoot.harden,
            tenant_id="t1",
            cluster_ref="c1",
            security_complete=False,
        )
        and CsDeployK8sSecurityRoot.harden(
            tenant_id="t1", cluster_ref="c2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            CsDeployReproducibleInfraRoot.provision,
            tenant_id="t1",
            stack_ref="s1",
            reproducible=False,
        )
        and CsDeployReproducibleInfraRoot.provision(
            tenant_id="t1", stack_ref="s2"
        ).is_non_reproducible()
        is False
    )
    checks.append(
        not _bad(
            CsDeployObservabilityRoot.attach,
            tenant_id="t1",
            service_ref="svc1",
            observability_present=False,
        )
        and CsDeployObservabilityRoot.attach(
            tenant_id="t1", service_ref="svc2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            CsDeployAutoScalingRoot.enable,
            tenant_id="t1",
            service_ref="svc3",
            auto_scaling=False,
        )
        and CsDeployAutoScalingRoot.enable(
            tenant_id="t1", service_ref="svc4"
        ).is_manual_only()
        is False
    )
    checks.append(
        not _bad(
            CsDeployDisasterRecoveryRoot.declare,
            tenant_id="t1",
            plan_ref="dr1",
            defined=False,
        )
        and CsDeployDisasterRecoveryRoot.declare(
            tenant_id="t1", plan_ref="dr2"
        ).is_undefined()
        is False
    )
    checks.append(
        not _bad(
            CsDeploySecurityControlsRoot.integrate,
            tenant_id="t1",
            control_ref="ctrl1",
            integrated=False,
        )
        and CsDeploySecurityControlsRoot.integrate(
            tenant_id="t1", control_ref="ctrl2"
        ).is_unintegrated()
        is False
    )
    checks.append(
        not _bad(
            CsDeployPipelineValidationRoot.validate,
            tenant_id="t1",
            pipeline_ref="pipe1",
            validated=False,
        )
        and CsDeployPipelineValidationRoot.validate(
            tenant_id="t1", pipeline_ref="pipe2"
        ).lacks_validation()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = root / "backend/contexts/cyber_security/infrastructure/acl/cs_deploy_acl.py"
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_enterprise_observability" in acl_text
        and "via_p209" in acl_text
        and "via_workflow" in acl_text
        and "security_controls_integrated_required" in acl_text
        and "observability_required" in acl_text
    )

    router = (
        root / "backend/contexts/cyber_security/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@cyber_security_router.get("/deploy")' in router
        and "/deploy/kubernetes" in router
        and "/deploy/devsecops" in router
        and "/deploy/observability" in router
        and "/deploy/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_CYBER_SECURITY_DEPLOY.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Deployment is not automated" in law
        and "Never Kubernetes security is incomplete" in law
        and "Never Infrastructure cannot be reproduced" in law
        and "Never Observability is missing" in law
        and "Never Scaling is manual" in law
        and "Never Disaster recovery is undefined" in law
        and "Never Security controls are not integrated" in law
        and "Never DevSecOps pipeline lacks validation" in law
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
        "prompt": "P210-N",
        "adr": 374,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "cyber_security",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
