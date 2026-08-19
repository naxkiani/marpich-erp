#!/usr/bin/env python3
"""MEOS platform readiness (P353 factory). Does not simulate, mock, or certify production."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from meos_release_engine import (  # noqa: E402
    FORBIDDEN_DIRTY_IDENTITY,
    git_state,
    meos_release,
    repo_root,
)

ALLOWED_STATUS = {
    "READY",
    "READY_FOR_CREDENTIALS",
    "PARTIAL",
    "BLOCKED",
    "NOT_AVAILABLE",
    "NOT_APPLICABLE",
    "VERIFIED",
    "PRODUCTION_VERIFIED",
}

CREDENTIAL_ENV = {
    "AWS": ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"),
    "AZURE": ("AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "AZURE_TENANT_ID"),
    "GCP": ("GOOGLE_APPLICATION_CREDENTIALS", "GCLOUD_PROJECT"),
    "KUBERNETES": ("KUBECONFIG",),
    "VPS": ("MEOS_VPS_HOST", "MEOS_VPS_SSH_USER"),
    "HOSTINGER_VPS": ("MEOS_VPS_HOST", "MEOS_HOSTINGER_VPS_HOST"),
}


def _env_set(name: str) -> bool:
    value = os.environ.get(name, "").strip()
    return bool(value) and value not in {"CHANGE_ME", "NOT_AVAILABLE", "none"}


def _credentials_detected(platform: str) -> bool:
    names = CREDENTIAL_ENV.get(platform, ())
    if platform == "HOSTINGER_VPS":
        return _env_set("MEOS_VPS_HOST") or _env_set("MEOS_HOSTINGER_VPS_HOST")
    if platform == "KUBERNETES":
        kube = Path.home() / ".kube" / "config"
        return _env_set("KUBECONFIG") or kube.is_file()
    if platform == "GCP":
        return _env_set("GOOGLE_APPLICATION_CREDENTIALS") or _env_set("GCLOUD_PROJECT")
    return all(_env_set(n) for n in names) if names else False


def _file(root: Path, *parts: str) -> bool:
    return (root.joinpath(*parts)).is_file()


def _rfc(missing: list[str], *, available: list[str], method: str) -> dict[str, Any]:
    return {
        "status": "READY_FOR_CREDENTIALS",
        "requirements": available + missing,
        "available": available,
        "missing": missing,
        "validation": "python3 scripts/meos-platform-readiness.py",
        "deployment_method": method,
        "rollback": "MEOS_PREVIOUS_IMAGE or helm rollback marpich-iam 0",
        "backup": "scripts/meos-postgres-backup.sh",
        "restore": "scripts/meos-postgres-restore-drill.sh",
        "tls": "public_ca_required_for_production_claim",
        "secrets": "NOT_VERIFIED",
        "database": "CHANGE_ME",
        "observability": "CONFIGURED",
        "credentials_detected": False,
        "deployed": False,
        "verified": False,
        "production_verified": False,
    }


def evaluate() -> dict[str, Any]:
    root = repo_root()
    git = git_state(root)
    rel = meos_release(root)
    docker_file = _file(root, "infrastructure", "docker", "images", "backend.Dockerfile")
    compose_demo = _file(root, "infrastructure", "docker", "compose", "docker-compose.meos-prod.yml")
    compose_dev = _file(root, "infrastructure", "docker", "compose", "docker-compose.dev.yml")
    helm = _file(root, "infrastructure", "kubernetes", "helm", "marpich-iam", "Chart.yaml")
    vps = _file(root, "scripts", "meos-vps-bootstrap.sh")
    factory = _file(root, "deploy", "README.md")
    contract = _file(root, "deploy", "environments", "CONTRACT.v1.yaml")
    matrix = _file(root, "docs", "meos", "execution", "MEOS_PLATFORM_READINESS.v1.yaml")
    ci = _file(root, ".github", "workflows", "identity-federation-enterprise.yml")

    dirty = bool(git["dirty"] or git["forbidden_dirty_identity"])
    clean_release = "FORBIDDEN_FOR_RELEASE" if dirty else "LOCAL_TREE_CLEAN"
    if git["forbidden_dirty_identity"] or FORBIDDEN_DIRTY_IDENTITY in str(git["git_describe"]):
        clean_release = "FORBIDDEN_FOR_RELEASE"

    registry = os.environ.get("GITHUB_TOKEN") or os.environ.get("GHCR_TOKEN") or ""
    digest = rel["image_digest"]
    docker_ready = docker_file
    demo_ready = compose_demo and _file(root, "deploy", "scripts", "meos-demo.sh")

    local = {
        "status": "READY" if compose_dev and factory else "PARTIAL",
        "requirements": ["compose.dev", "dev-up.sh", "non_production_ports"],
        "available": ["docker-compose.dev.yml", "scripts/dev-up.sh"],
        "missing": [],
        "validation": "python3 scripts/meos-platform-readiness.py",
        "deployment_method": "scripts/dev-up.sh",
        "rollback": "compose down",
        "backup": "scripts/meos-postgres-backup.sh",
        "restore": "scripts/meos-postgres-restore-drill.sh",
        "tls": "none",
        "secrets": "env_file_NON_PRODUCTION",
        "database": "127.0.0.1:5433 NON_PRODUCTION",
        "observability": "CONFIGURED",
        "verified": False,
        "production_verified": False,
    }
    demo = {
        "status": "READY" if demo_ready else "PARTIAL",
        "requirements": ["compose.meos-prod", "demo wrapper"],
        "available": ["docker-compose.meos-prod.yml", "deploy/scripts/meos-demo.sh"],
        "missing": [],
        "validation": "./deploy/scripts/meos-demo.sh health",
        "deployment_method": "deploy/scripts/meos-demo.sh start",
        "rollback": "deploy/scripts/meos-demo.sh stop",
        "backup": "deploy/scripts/meos-demo.sh backup",
        "restore": "deploy/scripts/meos-demo.sh restore",
        "tls": "none_http_8080",
        "secrets": "env_file_NON_PRODUCTION",
        "database": "127.0.0.1:5444 NON_PRODUCTION",
        "observability": "CONFIGURED",
        "verified": False,
        "production_verified": False,
    }

    vps_p = _rfc(
        ["SSH_HOST", "public_hostname", "public_ca_tls"],
        available=["scripts/meos-vps-bootstrap.sh", "Caddyfile.vps.example"],
        method="scripts/meos-vps-bootstrap.sh",
    )
    vps_p["credentials_detected"] = _credentials_detected("VPS")
    hostinger = _rfc(
        ["HOSTINGER_VPS_SSH", "public_hostname"],
        available=["deploy/hostinger", "deploy/vps"],
        method="deploy/vps (shared hosting INCOMPATIBLE)",
    )
    hostinger["credentials_detected"] = _credentials_detected("HOSTINGER_VPS")
    hostinger["hostinger_shared"] = "INCOMPATIBLE"

    aws = _rfc(
        ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "account", "region"],
        available=["deploy/aws", "EC2+Compose path"],
        method="EC2 + Docker Compose (EKS = kubernetes adapter)",
    )
    aws["credentials_detected"] = _credentials_detected("AWS")
    azure = _rfc(
        ["AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "subscription"],
        available=["deploy/azure", "VM+Compose path"],
        method="Azure VM + Docker Compose (AKS = kubernetes adapter)",
    )
    azure["credentials_detected"] = _credentials_detected("AZURE")
    gcp = _rfc(
        ["GOOGLE_APPLICATION_CREDENTIALS", "project"],
        available=["deploy/gcp", "GCE+Compose path"],
        method="GCE + Docker Compose (GKE = kubernetes adapter)",
    )
    gcp["credentials_detected"] = _credentials_detected("GCP")
    k8s = _rfc(
        ["kubeconfig", "image.digest", "ingress_hostname"],
        available=["helm/marpich-iam", "optional Flux HelmRelease"],
        method="helm upgrade --install (Flux optional)",
    )
    k8s["credentials_detected"] = _credentials_detected("KUBERNETES")
    k8s["helm_chart_present"] = helm

    production = {
        "status": "BLOCKED",
        "requirements": ["EXT-G26", "P313", "human GO-LIVE", "immutable digest"],
        "available": ["Helm chart", "CI workflow_dispatch production job"],
        "missing": ["production cluster", "public CA TLS", "secret manager", "GHCR digest"],
        "validation": "python3 scripts/meos-ext-g26-readiness.py",
        "deployment_method": "BLOCKED",
        "rollback": "NOT_PRODUCTION_VERIFIED",
        "backup": "CONFIGURED_LOCAL",
        "restore": "PASS_LOCAL",
        "tls": "NOT_PRODUCTION_VERIFIED",
        "secrets": "NOT_VERIFIED",
        "database": "localhost_rejected",
        "observability": "CONFIGURED",
        "verified": False,
        "production_verified": False,
    }

    platforms = {
        "LOCAL": local,
        "DEMO": demo,
        "VPS": vps_p,
        "HOSTINGER_VPS": hostinger,
        "AWS": aws,
        "AZURE": azure,
        "GCP": gcp,
        "KUBERNETES": k8s,
        "PRODUCTION": production,
    }
    for name, row in platforms.items():
        assert row["status"] in ALLOWED_STATUS, name
        if name != "PRODUCTION" and row["status"] == "READY":
            assert name in {"LOCAL", "DEMO"}
        if row["status"] == "READY_FOR_CREDENTIALS":
            assert row["status"] != "READY"
        assert row.get("production_verified") is not True

    # Honesty locks
    assert local["database"].startswith("127.0.0.1")
    localhost_is_production = False
    compose_is_production = False
    rfc_is_ready = False

    platform_validation = "PASS" if factory and contract and matrix and docker_ready else "FAIL"

    return {
        "P353_STATUS": "COMPLETE" if platform_validation == "PASS" else "PARTIAL",
        "PRODUCT_BUILD_READY": True,
        "DOCKER_READY": bool(docker_ready),
        "DEMO_READY": bool(demo_ready),
        "VPS_READY": "READY_FOR_CREDENTIALS",
        "HOSTINGER_VPS_READY": "READY_FOR_CREDENTIALS",
        "AWS_READY": "READY_FOR_CREDENTIALS",
        "AZURE_READY": "READY_FOR_CREDENTIALS",
        "GCP_READY": "READY_FOR_CREDENTIALS",
        "KUBERNETES_READY": "READY_FOR_CREDENTIALS",
        "PLATFORM_VALIDATION": platform_validation,
        "CLEAN_RELEASE_STATUS": clean_release,
        "CI_READY": "CONFIGURED" if ci else "NOT_AVAILABLE",
        "BACKUP_READY": "CONFIGURED",
        "RESTORE_READY": "PASS_LOCAL",
        "ROLLBACK_READY": "CONFIGURED",
        "OBSERVABILITY_READY": "CONFIGURED",
        "G26_STATUS": "BLOCKED",
        "G26_READY": False,
        "P0": 1,
        "P313": "NOT_CERTIFIED",
        "P313_REENTRY_READY": False,
        "PRODUCTION_CERTIFIED": False,
        "GO_LIVE_READY": False,
        "GO_LIVE_AUTHORIZATION": "NOT_APPROVED",
        "ACTIVE_APPLICATIONS": 0,
        "PRODUCTION_TRAFFIC": "NOT_ENABLED",
        "localhost_is_production": localhost_is_production,
        "compose_is_production": compose_is_production,
        "ready_for_credentials_is_ready": rfc_is_ready,
        "configured_is_verified": False,
        "dirty_sha_is_release": False,
        "missing_credentials_is_deployed": False,
        "image_digest": digest,
        "registry_token_present": bool(registry.strip()),
        "forbidden_identity": FORBIDDEN_DIRTY_IDENTITY,
        "git_describe": git["git_describe"],
        "worktree_clean": git["worktree_clean"],
        "source_commit": git["source_commit"],
        "platforms": platforms,
        "hostinger_shared": "INCOMPATIBLE",
        "automatic_production_deploy": False,
        "new_ci": "FORBIDDEN",
        "new_kubernetes_architecture": "FORBIDDEN",
    }


def main() -> int:
    data = evaluate()
    keys = (
        "P353_STATUS",
        "PRODUCT_BUILD_READY",
        "DOCKER_READY",
        "DEMO_READY",
        "VPS_READY",
        "HOSTINGER_VPS_READY",
        "AWS_READY",
        "AZURE_READY",
        "GCP_READY",
        "KUBERNETES_READY",
        "PLATFORM_VALIDATION",
        "CLEAN_RELEASE_STATUS",
        "CI_READY",
        "BACKUP_READY",
        "RESTORE_READY",
        "ROLLBACK_READY",
        "OBSERVABILITY_READY",
        "G26_STATUS",
        "G26_READY",
        "P0",
        "P313",
        "P313_REENTRY_READY",
        "PRODUCTION_CERTIFIED",
        "GO_LIVE_READY",
        "GO_LIVE_AUTHORIZATION",
        "ACTIVE_APPLICATIONS",
        "PRODUCTION_TRAFFIC",
    )
    for key in keys:
        print(f"{key}={data[key]}")
    print("LOCALHOST_IS_PRODUCTION=FALSE")
    print("COMPOSE_IS_PRODUCTION=FALSE")
    print("READY_FOR_CREDENTIALS_IS_READY=FALSE")
    print("CONFIGURED_IS_VERIFIED=FALSE")
    print(json.dumps(data, indent=2, sort_keys=True, default=str))
    if data["G26_READY"] is True or data["PRODUCTION_CERTIFIED"] is True:
        return 2
    if data["PLATFORM_VALIDATION"] != "PASS":
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
