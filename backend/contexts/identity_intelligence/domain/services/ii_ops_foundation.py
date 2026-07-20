"""Identity Intelligence P207-N DevSecOps/Ops foundation validator."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/329-enterprise-identity-intelligence-devsecops-kubernetes-observability.md",
    "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_DEVSECOPS_OBSERVABILITY.md",
    "docs/architecture/identity/intelligence/II_OPS_CAPABILITIES.v1.yaml",
    "docs/architecture/identity/intelligence/II_OPS_DDD_CQRS.v1.yaml",
    "docs/architecture/identity/intelligence/II_OPS_SECURITY.v1.yaml",
    "docs/architecture/identity/intelligence/II_OPS_VALIDATION.v1.yaml",
    "backend/contexts/identity_intelligence/domain/services/ii_platform_ops.py",
    "backend/contexts/identity_intelligence/domain/aggregates/ii_ops_aggregates.py",
    "backend/contexts/identity_intelligence/infrastructure/acl/ii_ops_acl.py",
    "backend/contexts/identity_intelligence/domain/services/ii_ops_foundation.py",
]

FORBIDDEN_SIBLINGS = (
    "backend/contexts/identity_intelligence_ops",
    "backend/contexts/identity_devsecops_platform",
    "backend/contexts/identity_k8s_platform",
)


def validate_ii_ops_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = any((root / path).exists() for path in FORBIDDEN_SIBLINGS)

    from contexts.identity_intelligence.domain.aggregates.ii_ops_aggregates import (
        DevSecOpsPipelineRunRoot,
        DisasterRecoveryTestRoot,
        GitOpsDeploymentSyncRoot,
        HighAvailabilityPlanRoot,
        KubernetesClusterBlueprintRoot,
        ObservabilityBaselineRoot,
        ScalabilityPolicyRoot,
    )
    from contexts.identity_intelligence.domain.services import ii_platform_ops as ops
    from contexts.identity_intelligence.infrastructure.acl import ii_ops_acl as acls

    cat = ops.catalog()
    catalog_ok = (
        cat.get("prompt_id") == "P207-N"
        and cat.get("adr") == 329
        and cat.get("sor") == "identity_intelligence"
        and cat["automated_deployment_required"] is True
        and cat["capabilities"]["not_manual_deployment"] is True
        and cat["capabilities"]["not_undefined_kubernetes"] is True
        and cat["capabilities"]["not_separated_security"] is True
        and cat["capabilities"]["not_incomplete_observability"] is True
        and cat["capabilities"]["not_missing_scaling"] is True
        and cat["capabilities"]["not_untested_dr"] is True
        and cat["kubernetes_platform"]["not_undefined"] is True
        and cat["devsecops_pipeline"]["not_manual"] is True
        and cat["devsecops_pipeline"]["not_separated"] is True
        and cat["scalability"]["not_missing"] is True
        and cat["disaster_recovery"]["not_untested"] is True
        and cat["observability"]["not_incomplete"] is True
        and cat["high_availability"]["availability_target"] == "99.99%"
        and cat["ddd"]["aggregate_count"] >= 7
        and cat["integrations"]["ops_integration_complete"] is True
        and "deployment_manual" in cat["quality_gates"]["reject_if"]
        and cat["production_readiness"]["verdict"] == "ENTERPRISE_GRADE"
    )

    try:
        KubernetesClusterBlueprintRoot.provision(
            tenant_id="t1",
            cluster_ref="c1",
            defined=False,
        )
        undef_k8s = True
    except ValueError:
        undef_k8s = False

    cluster = KubernetesClusterBlueprintRoot.provision(
        tenant_id="t1", cluster_ref="c2"
    )
    cluster_ok = (
        not undef_k8s
        and cluster.is_undefined() is False
        and "ClusterProvisioned" in cluster.pending_events
    )

    try:
        DevSecOpsPipelineRunRoot.run(
            tenant_id="t1",
            run_ref="r1",
            automated=False,
        )
        manual = True
    except ValueError:
        manual = False

    try:
        DevSecOpsPipelineRunRoot.run(
            tenant_id="t1",
            run_ref="r2",
            security_integrated=False,
        )
        sep_sec = True
    except ValueError:
        sep_sec = False

    pipeline = DevSecOpsPipelineRunRoot.run(tenant_id="t1", run_ref="r3")
    pipeline_ok = (
        not manual
        and not sep_sec
        and pipeline.is_manual() is False
        and pipeline.security_separated() is False
        and "PipelineCompleted" in pipeline.pending_events
    )

    gitops = GitOpsDeploymentSyncRoot.sync(tenant_id="t1", sync_ref="g1")
    gitops_ok = gitops.gitops_enabled is True

    try:
        ScalabilityPolicyRoot.define(
            tenant_id="t1",
            policy_ref="s1",
            strategy_defined=False,
        )
        no_scale = True
    except ValueError:
        no_scale = False

    scale = ScalabilityPolicyRoot.define(tenant_id="t1", policy_ref="s2")
    scale_ok = not no_scale and scale.strategy_missing() is False

    ha = HighAvailabilityPlanRoot.establish(tenant_id="t1", plan_ref="h1")
    ha_ok = ha.availability_target == "99.99%"

    try:
        DisasterRecoveryTestRoot.execute(
            tenant_id="t1",
            test_ref="d1",
            tested=False,
        )
        no_dr = True
    except ValueError:
        no_dr = False

    dr = DisasterRecoveryTestRoot.execute(tenant_id="t1", test_ref="d2")
    dr_ok = (
        not no_dr
        and dr.not_tested() is False
        and "FailoverTestPassed" in dr.pending_events
    )

    try:
        ObservabilityBaselineRoot.collect(
            tenant_id="t1",
            baseline_ref="o1",
            complete=False,
        )
        inc_obs = True
    except ValueError:
        inc_obs = False

    obs = ObservabilityBaselineRoot.collect(tenant_id="t1", baseline_ref="o2")
    obs_ok = (
        not inc_obs
        and obs.is_incomplete() is False
        and "ObservabilityBaselineCollected" in obs.pending_events
    )

    aggregates_ok = (
        cluster_ok
        and pipeline_ok
        and gitops_ok
        and scale_ok
        and ha_ok
        and dr_ok
        and obs_ok
    )

    acl_ok = (
        acls.to_observability(tenant_id="t1", metric_name="latency", value=1.0)[
            "observability_complete_required"
        ]
        is True
        and acls.to_api_gateway(tenant_id="t1", route_ref="/ops")["cloud_native_entry"]
        is True
        and acls.to_service_mesh(
            tenant_id="t1", service_name="identity-intelligence-service"
        )["mtls_required"]
        is True
        and acls.to_secrets(tenant_id="t1", secret_ref="k8s-tls")[
            "secret_management_required"
        ]
        is True
        and acls.to_security_ops(tenant_id="t1", incident_ref="inc1")[
            "devsecops_integrated"
        ]
        is True
        and acls.to_audit(
            tenant_id="t1", action="ii.ops.deploy", resource_ref="r3"
        )["pipeline_audit_trail"]
        is True
    )

    router = (
        root / "backend/contexts/identity_intelligence/presentation/router.py"
    ).read_text(encoding="utf-8")
    router_ok = (
        '@identity_intelligence_router.get("/ops"' in router
        and "/ops/kubernetes" in router
        and "/ops/devsecops" in router
        and "/ops/observability" in router
        and "/ops/disaster-recovery" in router
        and "/ops/readiness" in router
    )

    law = (
        root
        / "docs/architecture/ENTERPRISE_IDENTITY_INTELLIGENCE_DEVSECOPS_OBSERVABILITY.md"
    ).read_text(encoding="utf-8")
    doc_ok = (
        "Never deployment is manual" in law
        and "Never Kubernetes architecture is undefined" in law
        and "Never security is separated from DevOps" in law
        and "Never observability is incomplete" in law
        and "Never scaling strategy is missing" in law
        and "Never disaster recovery is not tested" in law
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
        "prompt": "P207-N",
        "adr": 329,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "catalog": catalog_ok,
        "aggregates": aggregates_ok,
        "acl": acl_ok,
        "router": router_ok,
        "documentation": doc_ok,
        "sor": "identity_intelligence",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
