"""EIFTP Ops Deployment / DevSecOps / Observability (P200-B11) foundation validator."""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]

REQUIRED_ARTIFACTS = [
    "docs/adr/225-enterprise-identity-federation-deployment-observability-devsecops.md",
    "docs/architecture/ENTERPRISE_IDENTITY_FEDERATION_DEPLOYMENT_OBSERVABILITY_DEVSECOPS.md",
    "docs/architecture/identity/eiftp/OPS_ARCHITECTURE.v1.yaml",
    "docs/architecture/identity/eiftp/OPS_SRE_CATALOG.v1.yaml",
    "docs/architecture/identity/eiftp/OPS_SURFACE.v1.yaml",
    "docs/deployment/IDENTITY_FEDERATION_DR_GUIDE.md",
    "infrastructure/kubernetes/helm/marpich-iam/Chart.yaml",
    "infrastructure/argocd/marpich-iam-application.yaml",
    "infrastructure/fluxcd/marpich-iam-helmrelease.yaml",
    ".github/workflows/identity-federation-enterprise.yml",
    "infrastructure/observability/prometheus/alerts/identity-federation.yml",
    "backend/shared/infrastructure/observability/telemetry.py",
    "backend/contexts/identity_federation/domain/services/federation_ops_platform.py",
    "backend/contexts/identity_federation/infrastructure/observability/federation_ops_metrics.py",
    "backend/contexts/identity_federation/application/commands/ops_commands.py",
    "backend/contexts/identity_federation/application/queries/ops_queries.py",
    "backend/contexts/identity_federation/presentation/ops_router.py",
]

FORBIDDEN_SIBLING = "backend/contexts/eiftp"

SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key\s*=\s*['\"][A-Za-z0-9_\-]{16,}"),
    re.compile(r"(?i)secret\s*=\s*['\"][^'\"]{8,}"),
    re.compile(r"(?i)password\s*=\s*['\"][^'\"]{4,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]


def _scan_secrets(root: Path) -> list[str]:
    hits: list[str] = []
    paths = [
        root
        / "backend/contexts/identity_federation/domain/services/federation_ops_platform.py",
        root
        / "backend/contexts/identity_federation/application/commands/ops_commands.py",
        root / "backend/contexts/identity_federation/presentation/ops_router.py",
    ]
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                hits.append(f"{path.relative_to(root)}:{pat.pattern}")
    return hits


def validate_ops_deployment_foundation(*, repo_root: Path | None = None) -> dict:
    root = repo_root or REPO_ROOT
    missing = [rel for rel in REQUIRED_ARTIFACTS if not (root / rel).exists()]
    sibling = (root / FORBIDDEN_SIBLING).exists()
    secret_hits = _scan_secrets(root)

    from contexts.identity_federation.domain.services.federation_ops_platform import (
        FederationOpsPlatform,
    )

    platform = FederationOpsPlatform()
    health = platform.health()
    deploy = platform.deployment_profile()
    pipe = platform.pipeline_profile()
    obs = platform.observability_profile()

    gitops_ok = bool(deploy.get("gitops")) and health["checks"].get(
        "argocd_present"
    ) and health["checks"].get("flux_present")
    pipeline_ok = health["checks"].get("github_workflow_present", False)
    helm_ok = health["checks"].get("helm_chart_present", False)
    otel_ok = health["checks"].get("otel_bootstrap_present", False)
    tracing_ok = "OpenTelemetry" in str(obs.get("tracing") or "")
    multi_region_ok = deploy.get("multi_region") is True
    rollback_ok = "rollback" in (pipe.get("stages") or [])
    metrics_path_ok = "/api/v1/federation/ops/metrics" in (
        obs.get("scrape_paths") or []
    )

    catalogs_ok = all(
        (root / p).exists()
        for p in (
            "docs/architecture/identity/eiftp/ARCH_DEPLOYMENT.v1.yaml",
            "docs/architecture/identity/eiftp/ARCH_DEVSECOPS.v1.yaml",
            "docs/architecture/identity/eiftp/ARCH_OBSERVABILITY.v1.yaml",
        )
    )

    passed = (
        not missing
        and not sibling
        and not secret_hits
        and gitops_ok
        and pipeline_ok
        and helm_ok
        and otel_ok
        and tracing_ok
        and multi_region_ok
        and rollback_ok
        and metrics_path_ok
        and catalogs_ok
    )
    return {
        "prompt": "P200-B11",
        "adr": 225,
        "passed": passed,
        "missing_artifacts": missing,
        "forbidden_sibling_present": sibling,
        "secret_scan_hits": secret_hits,
        "gitops": gitops_ok,
        "pipeline": pipeline_ok,
        "helm": helm_ok,
        "otel": otel_ok,
        "distributed_tracing": tracing_ok,
        "multi_region": multi_region_ok,
        "rollback_stage": rollback_ok,
        "ops_metrics_scrape": metrics_path_ok,
        "b2_arch_catalogs": catalogs_ok,
        "foundation_for": "P200-B12",
        "verdict": "ENTERPRISE_GRADE" if passed else "BELOW_THRESHOLD",
    }
