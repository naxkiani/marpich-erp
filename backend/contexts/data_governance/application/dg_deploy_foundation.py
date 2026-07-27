"""Data Governance P212-N Deploy foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_ARTIFACTS = [
    "docs/adr/406-enterprise-data-governance-deploy.md",
    "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_DEPLOY.md",
    "docs/architecture/data_governance/DATA_GOVERNANCE_DEPLOY_CAPABILITIES.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_DEPLOY_DDD_CQRS.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_DEPLOY_SECURITY.v1.yaml",
    "docs/architecture/data_governance/DATA_GOVERNANCE_DEPLOY_VALIDATION.v1.yaml",
    "backend/contexts/data_governance/domain/services/dg_platform_deploy.py",
    "backend/contexts/data_governance/domain/aggregates/dg_deploy_aggregates.py",
    "backend/contexts/data_governance/infrastructure/acl/dg_deploy_acl.py",
    "backend/contexts/data_governance/application/dg_deploy_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/data_governance_deploy",
    "backend/contexts/dg_k8s_platform",
    "backend/contexts/governance_observability_platform",
    "backend/contexts/data_mesh",
    "backend/contexts/data_marketplace",
    "backend/contexts/metadata_governance_platform",
)


def validate_dg_deploy_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.data_governance.domain.aggregates.dg_deploy_aggregates import (
        DgDeployAiopsRoot,
        DgDeployCloudNativeRoot,
        DgDeployCqrsOpsRoot,
        DgDeployDevSecOpsRoot,
        DgDeployGitOpsRoot,
        DgDeployHaRoot,
        DgDeployIacRoot,
        DgDeployKubernetesRoot,
        DgDeployMultiRegionRoot,
        DgDeployObservabilityRoot,
        DgDeployReliabilityRoot,
        DgDeployScalabilityRoot,
        DgDeploySecurityRoot,
        DgDeployServiceMeshRoot,
    )
    from contexts.data_governance.domain.services import (
        dg_platform_deploy as deploy,
    )

    cat = deploy.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P212-N"
        and cat.get("adr") == 406
        and cat.get("sor") == "data_governance"
        and cat.get("capability") == "CAP-PLT-DG-001"
        and cat["cloud_native_deployment_architecture_present_required"] is True
        and cat["kubernetes_platform_architecture_present_required"] is True
        and cat["devsecops_platform_present_required"] is True
        and cat["gitops_architecture_present_required"] is True
        and cat["infrastructure_as_code_present_required"] is True
        and cat["service_mesh_architecture_present_required"] is True
        and cat["scalability_architecture_present_required"] is True
        and cat["high_availability_architecture_present_required"] is True
        and cat["observability_platform_present_required"] is True
        and cat["aiops_operations_present_required"] is True
        and cat["security_integration_present_required"] is True
        and cat["multi_region_architecture_present_required"] is True
        and cat["cqrs_operational_integration_present_required"] is True
        and cat["enterprise_reliability_present_required"] is True
        and cat["cloud_native"]["not_missing"] is True
        and cat["kubernetes"]["not_missing"] is True
        and cat["devsecops"]["not_missing"] is True
        and cat["gitops"]["not_missing"] is True
        and cat["infrastructure_as_code"]["not_missing"] is True
        and cat["service_mesh"]["not_missing"] is True
        and cat["scalability"]["not_missing"] is True
        and cat["high_availability"]["not_missing"] is True
        and cat["observability"]["not_missing"] is True
        and cat["aiops"]["not_missing"] is True
        and cat["security_integration"]["not_missing"] is True
        and cat["multi_region"]["not_missing"] is True
        and cat["cqrs_operational_integration"]["not_missing"] is True
        and cat["enterprise_reliability"]["not_missing"] is True
        and cat["cloud_native"]["layer_count"] >= 6
        and cat["devsecops"]["pipeline_stage_count"] >= 10
        and cat["aiops"]["agent_count"] >= 5
        and cat["cqrs_operational_integration"]["event_count"] >= 5
        and cat["cursor_outputs"]["count"] >= 20
        and cat["observability"]["via_platform_observability"] is True
        and cat["cqrs_operational_integration"]["via_p212_m"] is True
        and cat["api_first"]["via_api_gateway"] is True
        and (
            "cloud_native_deployment_architecture_is_missing"
            in cat["quality_gates"]["reject_if"]
        )
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
            DgDeployCloudNativeRoot.publish,
            tenant_id="t1",
            cloud_ref="r0",
            present=False,
        )
        and DgDeployCloudNativeRoot.publish(
            tenant_id="t1", cloud_ref="ok0"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDeployKubernetesRoot.enable,
            tenant_id="t1",
            k8s_ref="r1",
            present=False,
        )
        and DgDeployKubernetesRoot.enable(
            tenant_id="t1", k8s_ref="ok1"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDeployDevSecOpsRoot.enable,
            tenant_id="t1",
            pipeline_ref="r2",
            present=False,
        )
        and DgDeployDevSecOpsRoot.enable(
            tenant_id="t1", pipeline_ref="ok2"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDeployGitOpsRoot.enable,
            tenant_id="t1",
            gitops_ref="r3",
            present=False,
        )
        and DgDeployGitOpsRoot.enable(
            tenant_id="t1", gitops_ref="ok3"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDeployIacRoot.enable,
            tenant_id="t1",
            iac_ref="r4",
            present=False,
        )
        and DgDeployIacRoot.enable(
            tenant_id="t1", iac_ref="ok4"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDeployServiceMeshRoot.enable,
            tenant_id="t1",
            mesh_ref="r5",
            present=False,
        )
        and DgDeployServiceMeshRoot.enable(
            tenant_id="t1", mesh_ref="ok5"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDeployScalabilityRoot.confirm,
            tenant_id="t1",
            scale_ref="r6",
            present=False,
        )
        and DgDeployScalabilityRoot.confirm(
            tenant_id="t1", scale_ref="ok6"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDeployHaRoot.confirm,
            tenant_id="t1",
            ha_ref="r7",
            present=False,
        )
        and DgDeployHaRoot.confirm(
            tenant_id="t1", ha_ref="ok7"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDeployObservabilityRoot.enable,
            tenant_id="t1",
            obs_ref="r8",
            present=False,
        )
        and DgDeployObservabilityRoot.enable(
            tenant_id="t1", obs_ref="ok8"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDeployAiopsRoot.enable,
            tenant_id="t1",
            aiops_ref="r9",
            present=False,
        )
        and DgDeployAiopsRoot.enable(
            tenant_id="t1", aiops_ref="ok9"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDeploySecurityRoot.integrate,
            tenant_id="t1",
            security_ref="r10",
            present=False,
        )
        and DgDeploySecurityRoot.integrate(
            tenant_id="t1", security_ref="ok10"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDeployMultiRegionRoot.confirm,
            tenant_id="t1",
            region_ref="r11",
            present=False,
        )
        and DgDeployMultiRegionRoot.confirm(
            tenant_id="t1", region_ref="ok11"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDeployCqrsOpsRoot.integrate,
            tenant_id="t1",
            cqrs_ops_ref="r12",
            present=False,
        )
        and DgDeployCqrsOpsRoot.integrate(
            tenant_id="t1", cqrs_ops_ref="ok12"
        ).is_missing()
        is False
    )
    checks.append(
        not _bad(
            DgDeployReliabilityRoot.confirm,
            tenant_id="t1",
            reliability_ref="r13",
            present=False,
        )
        and DgDeployReliabilityRoot.confirm(
            tenant_id="t1", reliability_ref="ok13"
        ).is_missing()
        is False
    )
    aggregates_ok = all(checks)

    acl_path = (
        root
        / "backend/contexts/data_governance/infrastructure/acl/dg_deploy_acl.py"
    )
    acl_text = acl_path.read_text(encoding="utf-8") if acl_path.exists() else ""
    acl_ok = (
        acl_path.exists()
        and "via_platform_observability" in acl_text
        and "via_enterprise_event_bus" in acl_text
        and "via_api_gateway" in acl_text
        and "via_p207" in acl_text
        and "via_p208" in acl_text
        and "via_p209" in acl_text
        and "via_p210" in acl_text
        and "via_p211" in acl_text
        and "via_p212_m" in acl_text
        and "module_local_observability_stack_forbidden" in acl_text
        and "cqrs_operational_integration_present_required" in acl_text
    )

    router = (
        root / "backend/contexts/data_governance/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@data_governance_router.get("/deploy")' in router
        and "/deploy/kubernetes" in router
        and "/deploy/devsecops" in router
        and "/deploy/observability" in router
        and "/deploy/readiness" in router
    )

    law = (
        root / "docs/architecture/ENTERPRISE_DATA_GOVERNANCE_DEPLOY.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never Cloud native deployment architecture is missing" in law
        and "Never Kubernetes platform architecture is missing" in law
        and "Never DevSecOps platform is missing" in law
        and "Never GitOps architecture is missing" in law
        and "Never Infrastructure as code is missing" in law
        and "Never Service mesh architecture is missing" in law
        and "Never Scalability architecture is missing" in law
        and "Never High availability architecture is missing" in law
        and "Never Observability platform is missing" in law
        and "Never AIOps operations is missing" in law
        and "Never Security integration is missing" in law
        and "Never Multi region architecture is missing" in law
        and "Never CQRS operational integration is missing" in law
        and "Never Enterprise reliability is missing" in law
        and "Never Sibling data governance deploy BC" in law
        and (
            "Enterprise intelligence platforms require continuous"
            in law
        )
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
        "prompt": "P212-N",
        "adr": 406,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "data_governance",
        "capability": "CAP-PLT-DG-001",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
