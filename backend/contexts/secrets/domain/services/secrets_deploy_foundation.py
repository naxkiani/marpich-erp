"""Secrets P209-N Deploy / DevSecOps / K8s / Observability foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/359-enterprise-secrets-deploy.md",
    "docs/architecture/ENTERPRISE_SECRETS_DEPLOY.md",
    "docs/architecture/secrets/SECRETS_DEPLOY_CAPABILITIES.v1.yaml",
    "docs/architecture/secrets/SECRETS_DEPLOY_DDD_CQRS.v1.yaml",
    "docs/architecture/secrets/SECRETS_DEPLOY_SECURITY.v1.yaml",
    "docs/architecture/secrets/SECRETS_DEPLOY_VALIDATION.v1.yaml",
    "backend/contexts/secrets/domain/services/secrets_platform_deploy.py",
    "backend/contexts/secrets/domain/aggregates/secrets_deploy_aggregates.py",
    "backend/contexts/secrets/infrastructure/acl/secrets_deploy_acl.py",
    "backend/contexts/secrets/domain/services/secrets_deploy_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/deploy_platform",
    "backend/contexts/secrets_sre_platform",
    "backend/contexts/secrets_k8s_platform",
    "backend/contexts/crypto_ops_platform",
    "backend/contexts/ops_platform",
    "backend/contexts/governance_platform",
    "backend/contexts/vault",
    "backend/contexts/pki_platform",
    "backend/contexts/kms_platform",
    "backend/contexts/hsm_platform",
)


def validate_secrets_deploy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.secrets.domain.aggregates.secrets_deploy_aggregates import (
        SecretsDeployAutomatedRoot,
        SecretsDeployCicdSecurityRoot,
        SecretsDeployDrAvailableRoot,
        SecretsDeployIacManagedRoot,
        SecretsDeployK8sSecurityRoot,
        SecretsDeployObservabilityRoot,
        SecretsDeployScalingDefinedRoot,
        SecretsDeployZeroTrustOpsRoot,
    )
    from contexts.secrets.domain.services import secrets_platform_deploy as deploy
    from contexts.secrets.infrastructure.acl import secrets_deploy_acl as acls

    cat = deploy.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P209-N"
        and cat.get("adr") == 359
        and cat.get("sor") == "secrets"
        and cat["deployment_automated_required"] is True
        and cat["kubernetes_security_complete_required"] is True
        and cat["observability_present_required"] is True
        and cat["cicd_security_validation_required"] is True
        and cat["scaling_strategy_defined_required"] is True
        and cat["disaster_recovery_available_required"] is True
        and cat["infrastructure_changes_managed_required"] is True
        and cat["architecture"]["not_manual"] is True
        and cat["kubernetes"]["not_incomplete"] is True
        and cat["observability"]["not_missing"] is True
        and cat["devsecops"]["not_lacking_security"] is True
        and cat["scalability"]["not_undefined"] is True
        and cat["disaster_recovery"]["not_unavailable"] is True
        and cat["iac"]["not_unmanaged"] is True
        and cat["cqrs"]["event_count"] >= 16
        and cat["cursor_outputs"]["count"] >= 20
        and "deployment_is_manual" in cat["quality_gates"]["reject_if"]
        and "disaster_recovery_unavailable" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        SecretsDeployAutomatedRoot.enable(
            tenant_id="t1", deploy_ref="d1", automated=False
        )
        auto_bad = True
    except ValueError:
        auto_bad = False

    auto = SecretsDeployAutomatedRoot.enable(
        tenant_id="t1", deploy_ref="pki-service"
    )
    auto_ok = not auto_bad and auto.is_manual() is False

    try:
        SecretsDeployK8sSecurityRoot.verify(
            tenant_id="t1", cluster_ref="c1", complete=False
        )
        k8s_bad = True
    except ValueError:
        k8s_bad = False

    k8s = SecretsDeployK8sSecurityRoot.verify(
        tenant_id="t1", cluster_ref="secrets-prod"
    )
    k8s_ok = not k8s_bad and k8s.is_incomplete() is False

    try:
        SecretsDeployObservabilityRoot.enable(
            tenant_id="t1", service_ref="s1", present=False
        )
        obs_bad = True
    except ValueError:
        obs_bad = False

    obs = SecretsDeployObservabilityRoot.enable(
        tenant_id="t1", service_ref="kms-service"
    )
    obs_ok = not obs_bad and obs.is_missing() is False

    try:
        SecretsDeployCicdSecurityRoot.validate(
            tenant_id="t1", pipeline_ref="p1", secured=False
        )
        cicd_bad = True
    except ValueError:
        cicd_bad = False

    cicd = SecretsDeployCicdSecurityRoot.validate(
        tenant_id="t1", pipeline_ref="secrets-release"
    )
    cicd_ok = not cicd_bad and cicd.lacks_security() is False

    try:
        SecretsDeployScalingDefinedRoot.define(
            tenant_id="t1", strategy_ref="sc1", defined=False
        )
        scale_bad = True
    except ValueError:
        scale_bad = False

    scale = SecretsDeployScalingDefinedRoot.define(
        tenant_id="t1", strategy_ref="hpa-global"
    )
    scale_ok = not scale_bad and scale.is_undefined() is False

    try:
        SecretsDeployDrAvailableRoot.enable(
            tenant_id="t1", plan_ref="dr1", available=False
        )
        dr_bad = True
    except ValueError:
        dr_bad = False

    dr = SecretsDeployDrAvailableRoot.enable(
        tenant_id="t1", plan_ref="secrets-dr"
    )
    dr_ok = not dr_bad and dr.is_unavailable() is False

    try:
        SecretsDeployIacManagedRoot.manage(
            tenant_id="t1", change_ref="ch1", managed=False
        )
        iac_bad = True
    except ValueError:
        iac_bad = False

    iac = SecretsDeployIacManagedRoot.manage(
        tenant_id="t1", change_ref="tf-k8s"
    )
    iac_ok = not iac_bad and iac.is_unmanaged() is False

    zt = SecretsDeployZeroTrustOpsRoot.enforce(
        tenant_id="t1", env_ref="production"
    )
    zt_ok = "ZeroTrustOpsEnforced" in zt.pending_events

    aggregates_ok = (
        auto_ok
        and k8s_ok
        and obs_ok
        and cicd_ok
        and scale_ok
        and dr_ok
        and iac_ok
        and zt_ok
    )

    acl_ok = (
        acls.to_observability(tenant_id="t1", service_ref="vault-service")[
            "observability_present_required"
        ]
        is True
        and acls.to_workflow_deploy_approval(
            tenant_id="t1", deploy_ref="d1"
        )["iac_managed_required"]
        is True
        and acls.to_authorization_deploy(
            tenant_id="t1", principal_ref="u1", action="secrets.deploy.write"
        )["zero_trust_operations"]
        is True
        and acls.to_signing_sbom(tenant_id="t1", artifact_ref="img1")[
            "cicd_security_validation_required"
        ]
        is True
        and acls.to_audit(
            tenant_id="t1", action="secrets.deploy.release", resource_ref="r1"
        )["deployment_automated_required"]
        is True
    )

    router = (
        root / "backend/contexts/secrets/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '/deploy"' in router
        and "/deploy/kubernetes" in router
        and "/deploy/devsecops" in router
        and "/deploy/observability" in router
        and "/deploy/disaster-recovery" in router
        and "/deploy/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_SECRETS_DEPLOY.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never deployment is manual" in law
        and "Never Kubernetes security is incomplete" in law
        and "Never observability is missing" in law
        and "Never CI/CD lacks security validation" in law
        and "Never scaling strategy is undefined" in law
        and "Never disaster recovery is unavailable" in law
        and "Never infrastructure changes are unmanaged" in law
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
        "prompt": "P209-N",
        "adr": 359,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "secrets",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
