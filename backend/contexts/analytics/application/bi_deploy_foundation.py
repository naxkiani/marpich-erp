"""Analytics P213-O BI deploy foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/419-enterprise-business-intelligence-deploy.md",
    "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_DEPLOY.md",
    "docs/architecture/business_intelligence/BI_DEPLOY_CAPABILITIES.v1.yaml",
    "docs/architecture/business_intelligence/BI_DEPLOY_DDD_CQRS.v1.yaml",
    "docs/architecture/business_intelligence/BI_DEPLOY_SECURITY.v1.yaml",
    "docs/architecture/business_intelligence/BI_DEPLOY_VALIDATION.v1.yaml",
    "backend/contexts/analytics/domain/services/bi_platform_deploy.py",
    "backend/contexts/analytics/domain/aggregates/bi_deploy_aggregates.py",
    "backend/contexts/analytics/infrastructure/acl/bi_deploy_acl.py",
    "backend/contexts/analytics/application/bi_deploy_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/business_intelligence",
    "backend/contexts/decision_intelligence",
    "backend/contexts/reporting_platform",
    "backend/contexts/metric_governance_platform",
    "backend/contexts/visualization_platform",
    "backend/contexts/bi_core",
)


def validate_bi_deploy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.analytics.domain.aggregates.bi_deploy_aggregates import (
        BiDefinitionOfDoneRoot,
        BiDeployProfileRoot,
        BiDevSecOpsRoot,
        BiGitOpsPlatformRoot,
        BiKubernetesRuntimeRoot,
        BiObservabilityRoot,
    )
    from contexts.analytics.domain.services import bi_platform_deploy as catmod

    cat = catmod.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P213-O"
        and cat.get("adr") == 419
        and cat.get("sor") == "analytics"
        and cat.get("capability") == "CAP-PLT-BI-001"
        and cat.get("principle") == catmod.PRINCIPLE
        and cat.get("fabric") == catmod.FABRIC
        and "secure GitOps" in cat["principle"]
        and cat["enterprise_production_deployment_present_required"] is True
        and cat["kubernetes_runtime_present_required"] is True
        and cat["gitops_platform_present_required"] is True
        and cat["devsecops_pipeline_present_required"] is True
        and cat["observability_platform_present_required"] is True
        and cat["sre_processes_present_required"] is True
        and cat["scalability_architecture_present_required"] is True
        and cat["disaster_recovery_present_required"] is True
        and cat["definition_of_done_present_required"] is True
        and cat["cloud_native_deployment_present_required"] is True
        and cat["zero_trust_security_present_required"] is True
        and cat["continuous_governance_present_required"] is True
        and cat["architecture_present_required"] is True
        and cat["sibling_business_intelligence_bc_forbidden"] is True
        and cat["domain_model"]["supporting_count"] >= 9
        and cat["bounded_contexts"]["context_count"] >= 6
        and cat["environments"]["environment_count"] >= 11
        and cat["definition_of_done"]["criterion_count"] >= 23
        and cat["aiops"]["agent_count"] >= 9
        and cat["aiops"]["via_enterprise_ai"] is True
        and cat["devsecops"]["via_p209"] is True
        and cat["devsecops"]["via_p210"] is True
        and cat["observability"]["via_enterprise_observability"] is True
        and cat["cqrs"]["command_count"] >= 6
        and cat["events"]["core_event_count"] >= 6
        and cat["microservices"]["service_count"] >= 8
        and cat["deployment"]["cloud_native"] is True
        and cat["cursor_outputs"]["count"] >= 20
        and "bi_deploy_architecture_is_incomplete"
        in cat["quality_gates"]["reject_if"]
        and "definition_of_done_is_incomplete"
        in cat["quality_gates"]["reject_if"]
        and "P213-N" in cat["builds_on"]
        and "P209" in cat["builds_on"]
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
            BiDeployProfileRoot.publish,
            tenant_id="t1",
            profile_ref="r1",
            complete=False,
        )
        and BiDeployProfileRoot.publish(
            tenant_id="t1", profile_ref="r2"
        ).is_incomplete()
        is False
    )
    checks.append(
        not _bad(
            BiKubernetesRuntimeRoot.enable,
            tenant_id="t1",
            cluster_ref="c1",
            present=False,
        )
        and BiKubernetesRuntimeRoot.enable(
            tenant_id="t1", cluster_ref="c2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiGitOpsPlatformRoot.enable,
            tenant_id="t1",
            gitops_ref="g1",
            present=False,
        )
        and BiGitOpsPlatformRoot.enable(
            tenant_id="t1", gitops_ref="g2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiDevSecOpsRoot.enable,
            tenant_id="t1",
            pipeline_ref="p1",
            present=False,
        )
        and BiDevSecOpsRoot.enable(
            tenant_id="t1", pipeline_ref="p2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiObservabilityRoot.enable,
            tenant_id="t1",
            obs_ref="o1",
            present=False,
        )
        and BiObservabilityRoot.enable(
            tenant_id="t1", obs_ref="o2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            BiDefinitionOfDoneRoot.enable,
            tenant_id="t1",
            dod_ref="d1",
            present=False,
        )
        and BiDefinitionOfDoneRoot.enable(
            tenant_id="t1", dod_ref="d2"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/analytics/infrastructure/acl/bi_deploy_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p212" in acl_text
        and "via_p213_n" in acl_text
        and "via_enterprise_ai" in acl_text
        and "via_enterprise_observability" in acl_text
        and "module_local_llm_sdk_forbidden" in acl_text
        and "image_signing_required" in acl_text
    )

    router = (
        root / "backend/contexts/analytics/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@router.get("/deploy")' in router
        and "/deploy/readiness" in router
        and "/deploy/vision" in router
        and "/deploy/kubernetes" in router
        and "/deploy/gitops" in router
        and "/deploy/devsecops" in router
        and "/deploy/observability" in router
        and "/deploy/definition-of-done" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_BUSINESS_INTELLIGENCE_DEPLOY.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Enterprise production deployment is missing" in law
        and "Never Kubernetes runtime is missing" in law
        and "Never GitOps platform is missing" in law
        and "Never DevSecOps pipeline is missing" in law
        and "Never Observability platform is missing" in law
        and "Never SRE processes are missing" in law
        and "Never Scalability architecture is missing" in law
        and "Never Disaster recovery is missing" in law
        and "Never Definition of done is incomplete" in law
        and "Never Cloud native deployment is missing" in law
        and "Never Zero trust security is missing" in law
        and "Never Continuous governance is missing" in law
        and "Never BI deploy architecture is incomplete" in law
        and "Never Sibling business intelligence BC" in law
        and "MEOS Enterprise BI Operations Fabric" in law
        and "secure GitOps" in law
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
        "prompt": "P213-O",
        "adr": 419,
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
