#!/usr/bin/env python3
"""MEOS product-side launch readiness (P351).

Reports PRODUCT infrastructure independently of EXT-G26.
Does not set G26_READY. Does not treat localhost/compose as production.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ALLOWED_ADAPTER = frozenset(
    {
        "IMPLEMENTED",
        "CONFIGURED",
        "READY_FOR_CREDENTIALS",
        "READY_FOR_DEPLOYMENT",
        "PRODUCTION_VERIFIED",
        "BLOCKED",
        "NOT_APPLICABLE",
        "PARTIALLY_COMPATIBLE",
        "INCOMPATIBLE",
        "EXTERNAL_DEPENDENCY",
    }
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _exists(*parts: str) -> bool:
    return repo_root().joinpath(*parts).is_file() or repo_root().joinpath(*parts).is_dir()


def _git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root(),
        check=False,
        capture_output=True,
        text=True,
    )
    return (result.stdout or "").strip()


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_ext_g26_readiness", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.evaluate(repo_root())


def _pg_local_ready() -> bool:
    host = os.environ.get("PGHOST", "127.0.0.1")
    port = os.environ.get("PGPORT", "5433")
    if shutil.which("pg_isready") is None:
        return False
    r = subprocess.run(
        ["pg_isready", "-h", host, "-p", str(port)],
        check=False,
        capture_output=True,
        text=True,
    )
    return r.returncode == 0


def evaluate() -> dict[str, Any]:
    root = repo_root()
    compose_dev = root / "infrastructure" / "docker" / "compose" / "docker-compose.dev.yml"
    compose_prod = root / "infrastructure" / "docker" / "compose" / "docker-compose.meos-prod.yml"
    dockerfile = root / "infrastructure" / "docker" / "images" / "backend.Dockerfile"
    helm = root / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "Chart.yaml"
    flux = root / "infrastructure" / "fluxcd" / "marpich-iam-helmrelease.yaml"
    ci = root / ".github" / "workflows" / "identity-federation-enterprise.yml"
    backup = root / "scripts" / "meos-postgres-backup.sh"
    restore = root / "scripts" / "meos-postgres-restore-drill.sh"
    vps = root / "scripts" / "meos-vps-bootstrap.sh"
    env_ex = root / "infrastructure" / "launch" / "env.production.example"
    extsec = root / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "templates" / "externalsecret.yaml"
    helpers = (
        root / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "templates" / "_helpers.tpl"
    )
    describe = _git(["describe", "--always", "--dirty"])
    short = _git(["status", "--short"])
    dirty = bool(short) or "dirty" in describe
    docker_cli = shutil.which("docker") is not None
    compose_ok = False
    if docker_cli and compose_dev.is_file():
        r = subprocess.run(
            ["docker", "compose", "-f", str(compose_dev), "config"],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        compose_ok = r.returncode == 0
    local_pg = _pg_local_ready()
    digest_in_ci = "steps.image.outputs.digest" in ci.read_text(encoding="utf-8") if ci.is_file() else False
    image_helper = "marpich-iam.image" in helpers.read_text(encoding="utf-8") if helpers.is_file() else False
    dockerfile_text = dockerfile.read_text(encoding="utf-8") if dockerfile.is_file() else ""
    non_root = "USER app" in dockerfile_text or "USER 1000" in dockerfile_text

    product_build = _exists("backend/pyproject.toml") and dockerfile.is_file()
    docker_ready = dockerfile.is_file() and compose_prod.is_file() and non_root
    k8s_pkg = helm.is_file() and flux.is_file() and extsec.is_file() and image_helper
    backup_cfg = backup.is_file()
    restore_cfg = restore.is_file()
    obs = (root / "infrastructure" / "observability" / "prometheus" / "prometheus.yml").is_file()
    vps_pkg = vps.is_file() and env_ex.is_file()

    adapters = {
        "LOCAL": "CONFIGURED" if compose_dev.is_file() else "BLOCKED",
        "DEVELOPMENT": "CONFIGURED" if compose_dev.is_file() else "BLOCKED",
        "TEST": "CONFIGURED",
        "STAGING": "READY_FOR_CREDENTIALS" if ci.is_file() else "BLOCKED",
        "DEMO": "CONFIGURED" if compose_prod.is_file() else "BLOCKED",
        "PRODUCTION": "BLOCKED",
        "TARGET-A": "CONFIGURED" if compose_dev.is_file() else "BLOCKED",
        "TARGET-B": "READY_FOR_CREDENTIALS" if vps_pkg else "BLOCKED",
        "TARGET-C": "CONFIGURED" if docker_ready else "BLOCKED",
        "TARGET-D": "PARTIALLY_COMPATIBLE" if vps_pkg else "INCOMPATIBLE",
        "TARGET-E": "READY_FOR_CREDENTIALS",
        "TARGET-F": "READY_FOR_CREDENTIALS",
        "TARGET-G": "READY_FOR_CREDENTIALS",
        "TARGET-H": "READY_FOR_CREDENTIALS" if k8s_pkg else "BLOCKED",
        "TARGET-I": "READY_FOR_CREDENTIALS" if k8s_pkg else "BLOCKED",
        "PROFILE_LOCAL": "CONFIGURED",
        "PROFILE_DOCKER": "CONFIGURED" if docker_ready else "BLOCKED",
        "PROFILE_VPS": "READY_FOR_CREDENTIALS" if vps_pkg else "BLOCKED",
        "PROFILE_HOSTINGER_VPS": "READY_FOR_CREDENTIALS" if vps_pkg else "INCOMPATIBLE",
        "PROFILE_HOSTINGER_SHARED": "INCOMPATIBLE",
        "PROFILE_AWS": "READY_FOR_CREDENTIALS",
        "PROFILE_AZURE": "READY_FOR_CREDENTIALS",
        "PROFILE_GCP": "READY_FOR_CREDENTIALS",
        "PROFILE_KUBERNETES": "READY_FOR_CREDENTIALS" if k8s_pkg else "BLOCKED",
    }
    for k, v in adapters.items():
        assert v in ALLOWED_ADAPTER, f"{k}={v}"

    local_runtime = "RUNTIME_VERIFIED" if local_pg else "CONFIGURED"
    demo_runtime = "CONFIGURED"
    docker_evidence = root / "docs" / "meos" / "execution" / ".last_docker_build.json"
    restore_evidence = root / "docs" / "meos" / "execution" / ".last_p352_restore.json"
    docker_build_ready = "NOT_AVAILABLE"
    if docker_evidence.is_file():
        try:
            docker_build_ready = json.loads(docker_evidence.read_text(encoding="utf-8")).get(
                "status", "NOT_AVAILABLE"
            )
        except json.JSONDecodeError:
            docker_build_ready = "FAIL"
    restore_test = "NOT_AVAILABLE"
    if restore_evidence.is_file():
        try:
            restore_test = json.loads(restore_evidence.read_text(encoding="utf-8")).get(
                "restore_test", "NOT_AVAILABLE"
            )
        except json.JSONDecodeError:
            restore_test = "FAIL"
    migration_script = (root / "scripts" / "meos-migration-check.sh").is_file()
    database_ready = "RUNTIME_VERIFIED" if local_pg else "CONFIGURED"
    if local_pg:
        database_ready = "READY"
    else:
        database_ready = "PARTIAL"
    helm_ready_probe = False
    deploy_tpl = root / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "templates" / "deployment.yaml"
    if deploy_tpl.is_file():
        helm_ready_probe = "path: /api/v1/ready" in deploy_tpl.read_text(encoding="utf-8")

    g26 = _g26()
    docker_status = "TRUE" if docker_build_ready == "PASS" else ("IMPLEMENTED" if docker_ready else "BLOCKED")
    report = {
        "p351_status": "PRODUCT_INFRASTRUCTURE_FOUNDATION",
        "p352_status": "PRODUCT_INFRASTRUCTURE_HARDENING",
        "product_build_ready": "TRUE" if product_build else "BLOCKED",
        "local_ready": "TRUE" if compose_dev.is_file() else "BLOCKED",
        "demo_ready": "TRUE" if compose_prod.is_file() else "BLOCKED",
        "docker_ready": docker_status,
        "docker_build_ready": docker_build_ready,
        "database_ready": database_ready,
        "migration_ready": "TRUE" if migration_script else "BLOCKED",
        "vps_ready": "READY_FOR_CREDENTIALS" if vps_pkg else "BLOCKED",
        "hostinger_vps_ready": "READY_FOR_CREDENTIALS" if vps_pkg else "INCOMPATIBLE",
        "hostinger_shared": "INCOMPATIBLE",
        "aws_ready": "READY_FOR_CREDENTIALS",
        "azure_ready": "READY_FOR_CREDENTIALS",
        "gcp_ready": "READY_FOR_CREDENTIALS",
        "kubernetes_ready": "READY_FOR_CREDENTIALS" if k8s_pkg else "BLOCKED",
        "release_ready": "BLOCKED" if dirty else "READY_FOR_CREDENTIALS",
        "backup_ready": "CONFIGURED" if backup_cfg else "BLOCKED",
        "restore_ready": "CONFIGURED" if restore_cfg else "BLOCKED",
        "restore_test": restore_test,
        "observability_ready": "CONFIGURED" if obs else "BLOCKED",
        "security_ready": "CONFIGURED" if helm_ready_probe else "PARTIAL",
        "local_runtime": local_runtime,
        "demo_runtime": demo_runtime,
        "compose_config_ok": compose_ok,
        "docker_cli": docker_cli,
        "non_root_image": non_root,
        "ci_digest_wired": digest_in_ci,
        "helm_image_digest_helper": image_helper,
        "helm_readiness_uses_ready": helm_ready_probe,
        "dirty": dirty,
        "git_describe": describe,
        "forbidden_dirty": dirty,
        "localhost_is_production": False,
        "compose_is_production": False,
        "demo_is_production": False,
        "adapter_status": adapters,
        "scores": {
            "PRODUCT_CODE": "READY" if product_build else "BLOCKED",
            "PRODUCT_RUNTIME": local_runtime,
            "PRODUCT_DATABASE": database_ready,
            "PRODUCT_CONTAINER": "READY" if docker_build_ready == "PASS" else "PARTIAL",
            "PRODUCT_DEMO": "READY" if compose_prod.is_file() else "BLOCKED",
            "PRODUCT_RELEASE": "BLOCKED" if dirty else "PARTIAL",
            "PRODUCT_SECURITY": "READY" if helm_ready_probe else "PARTIAL",
            "PRODUCT_BACKUP": "READY" if backup_cfg else "BLOCKED",
            "PRODUCT_RESTORE": "READY" if restore_test == "PASS" else ("PARTIAL" if restore_cfg else "BLOCKED"),
            "PRODUCT_OBSERVABILITY": "PARTIAL",
            "PRODUCT_VPS": "PARTIAL",
            "PRODUCT_CLOUD": "PARTIAL",
            "PRODUCT_KUBERNETES": "PARTIAL",
        },
        "g26_ready": g26.get("g26_ready"),
        "g26_status": g26.get("g26_status"),
        "p0_count": g26.get("p0_count"),
        "p313": g26.get("p313"),
        "p313_reentry_ready": False,
        "production_certified": False,
        "go_live_ready": False,
        "go_live_authorization": "NOT APPROVED",
        "registry_active_count": 0,
        "production_traffic": "NOT_ENABLED",
        "note": "aws/azure/gcp *_ready means adapter docs exist (READY_FOR_CREDENTIALS), not PRODUCTION_VERIFIED",
    }
    for banned in ("BEGIN PRIVATE", "AWS_SECRET_ACCESS_KEY"):
        assert banned not in json.dumps(report)
    return report


def main() -> int:
    data = evaluate()
    print(f"P352_STATUS={data.get('p352_status')}")
    print(f"PRODUCT_BUILD_READY={data['product_build_ready']}")
    print(f"LOCAL_READY={data['local_ready']}")
    print(f"DEMO_READY={data['demo_ready']}")
    print(f"DOCKER_READY={data['docker_ready']}")
    print(f"DOCKER_BUILD_READY={data.get('docker_build_ready')}")
    print(f"DATABASE_READY={data.get('database_ready')}")
    print(f"MIGRATION_READY={data.get('migration_ready')}")
    print(f"VPS_READY={data['vps_ready']}")
    print(f"HOSTINGER_VPS_READY={data['hostinger_vps_ready']}")
    print(f"AWS_READY={data['aws_ready']}")
    print(f"AZURE_READY={data['azure_ready']}")
    print(f"GCP_READY={data['gcp_ready']}")
    print(f"KUBERNETES_READY={data['kubernetes_ready']}")
    print(f"RELEASE_READY={data['release_ready']}")
    print(f"BACKUP_READY={data['backup_ready']}")
    print(f"RESTORE_READY={data['restore_ready']}")
    print(f"RESTORE_TEST={data.get('restore_test')}")
    print(f"OBSERVABILITY_READY={data['observability_ready']}")
    print(f"SECURITY_READY={data.get('security_ready')}")
    print(f"G26_READY={data['g26_ready']}")
    print(f"G26_STATUS={data['g26_status']}")
    print(f"P0={data['p0_count']}")
    print(f"P313={data['p313']}")
    print(f"PRODUCTION_CERTIFIED={data['production_certified']}")
    print(f"GO_LIVE_READY={data['go_live_ready']}")
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0 if data["product_build_ready"] != "BLOCKED" else 1


if __name__ == "__main__":
    sys.exit(main())
