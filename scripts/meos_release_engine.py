#!/usr/bin/env python3
"""MEOS universal release/install engine (P354).

Reuses existing Docker, Compose, Helm, Flux, CI, backup, and migrations.
Does not invent GHCR digests, TLS, credentials, or G26_READY.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FORBIDDEN_DIRTY_IDENTITY = "47258dfd-dirty"
FORBIDDEN_PROD_PORTS = {5433, 5444}
FORBIDDEN_PROD_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}
MUTABLE_TAGS = {"latest", "7.0.0"}

PACKAGE_MEMBERS = (
    "docs/meos/execution/MEOS_RELEASE_MANIFEST.v1.yaml",
    "docs/meos/execution/MEOS_RELEASE_OPERATIONS.md",
    "docs/meos/execution/MEOS_BACKUP_RESTORE_RUNBOOK.md",
    "docs/meos/execution/MEOS_RELEASE_ENGINEERING_RUNBOOK.md",
    "infrastructure/docker/compose/docker-compose.dev.yml",
    "infrastructure/docker/compose/docker-compose.meos-prod.yml",
    "infrastructure/docker/compose/Caddyfile.vps.example",
    "infrastructure/docker/compose/env.meos-prod.example",
    "infrastructure/docker/images/backend.Dockerfile",
    "infrastructure/fluxcd/marpich-iam-helmrelease.yaml",
    "infrastructure/launch/env.production.example",
    "infrastructure/kubernetes/helm/marpich-iam/Chart.yaml",
    "infrastructure/kubernetes/helm/marpich-iam/values.yaml",
    "infrastructure/kubernetes/helm/marpich-iam/values-production.yaml",
    "infrastructure/kubernetes/helm/marpich-iam/templates/_helpers.tpl",
    "infrastructure/kubernetes/helm/marpich-iam/templates/externalsecret.yaml",
    "scripts/meos-install.py",
    "scripts/meos-release.py",
    "scripts/meos-vps-bootstrap.sh",
    "scripts/meos-postgres-backup.sh",
    "scripts/meos-postgres-restore-drill.sh",
    "scripts/meos-migration-check.sh",
    "scripts/meos-install-readiness.py",
)

PLATFORMS = (
    "DEMO",
    "LOCAL",
    "VPS",
    "HOSTINGER_VPS",
    "AWS",
    "AZURE",
    "GCP",
    "KUBERNETES",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _run(args: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd or repo_root(), check=False, capture_output=True, text=True)


def git_state(root: Path | None = None) -> dict[str, Any]:
    root = root or repo_root()
    short = (_run(["git", "status", "--short"], cwd=root).stdout or "").strip()
    describe = (_run(["git", "describe", "--always", "--dirty"], cwd=root).stdout or "").strip()
    sha = (_run(["git", "rev-parse", "HEAD"], cwd=root).stdout or "").strip() or "NOT_AVAILABLE"
    branch = (_run(["git", "branch", "--show-current"], cwd=root).stdout or "").strip() or "NOT_AVAILABLE"
    dirty = bool(short) or "dirty" in describe or describe == FORBIDDEN_DIRTY_IDENTITY
    return {
        "source_commit": sha,
        "branch": branch,
        "git_describe": describe,
        "worktree_clean": short == "",
        "dirty": dirty,
        "forbidden_dirty_identity": describe == FORBIDDEN_DIRTY_IDENTITY or FORBIDDEN_DIRTY_IDENTITY in describe,
    }


def schema_version(root: Path | None = None) -> str:
    migrations = (root or repo_root()) / "infrastructure" / "docker" / "migrations"
    if not migrations.is_dir():
        return "NOT_AVAILABLE"
    files = sorted(p.name for p in migrations.glob("*.sql"))
    if not files:
        return "NOT_AVAILABLE"
    return files[-1].split("_", 1)[0]


def config_version(root: Path | None = None) -> str:
    path = (root or repo_root()) / "infrastructure" / "launch" / "env.production.example"
    if not path.is_file():
        return "NOT_AVAILABLE"
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return "cv-" + digest[:12]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_p353_manifest(root: Path | None = None) -> dict[str, Any]:
    path = (root or repo_root()) / "docs" / "meos" / "execution" / "MEOS_RELEASE_MANIFEST.v1.yaml"
    if not path.is_file():
        return {}
    try:
        import yaml
    except ImportError:
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def meos_release(root: Path | None = None) -> dict[str, Any]:
    root = root or repo_root()
    git = git_state(root)
    manifest = load_p353_manifest(root)
    image = str(manifest.get("image") or "NOT_AVAILABLE")
    image_digest = str(manifest.get("image_digest") or "NOT_AVAILABLE")
    if image_digest in {"", "None"}:
        image_digest = "NOT_AVAILABLE"
    pyproject = root / "backend" / "pyproject.toml"
    version = str(manifest.get("version") or "0.1.0")
    if pyproject.is_file() and 'version = "0.1.0"' in pyproject.read_text(encoding="utf-8"):
        version = "0.1.0"
    build_id = os.environ.get("GITHUB_RUN_ID") or os.environ.get("MEOS_BUILD_ID") or "NOT_AVAILABLE"
    created = str(manifest.get("build_timestamp") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    verification = "LOCAL_BUILD" if image_digest == "NOT_AVAILABLE" else "IMMUTABLE_DIGEST_AVAILABLE"
    if git["dirty"] or git["forbidden_dirty_identity"]:
        verification = "FORBIDDEN_DIRTY"
    return {
        "release_id": "MEOS_RELEASE",
        "release_version": version,
        "source_commit": git["source_commit"],
        "build_id": build_id,
        "image": image,
        "image_digest": image_digest,
        "image_id": str(manifest.get("image_id") or "NOT_AVAILABLE"),
        "schema_version": schema_version(root),
        "config_version": config_version(root),
        "created_at": created,
        "artifacts": list(PACKAGE_MEMBERS),
        "supported_platforms": list(PLATFORMS),
        "verification_status": verification,
        "registry": str(manifest.get("registry") or "ghcr.io/marpich/marpich-backend"),
        "versioning_gap": str(manifest.get("versioning_gap") or "NOT_AVAILABLE"),
        "production_certified": False,
        "g26_ready": False,
    }


def identity_ok(release: dict[str, Any] | None = None, *, require_digest: bool = False) -> dict[str, Any]:
    rel = release or meos_release()
    git = git_state()
    digest = str(rel.get("image_digest") or "NOT_AVAILABLE")
    image = str(rel.get("image") or "")
    mutable = any(tag and f":{tag}" in image for tag in MUTABLE_TAGS) and "@sha256:" not in image
    blocked_reasons: list[str] = []
    if git["dirty"] or git["forbidden_dirty_identity"]:
        blocked_reasons.append("DIRTY_RELEASE")
    if mutable:
        blocked_reasons.append("MUTABLE_ONLY_IMAGE")
    if require_digest and (digest == "NOT_AVAILABLE" or not digest.startswith("sha256:")):
        blocked_reasons.append("IMAGE_DIGEST_MISSING")
    return {
        "source_commit": rel.get("source_commit"),
        "image_digest": digest,
        "release_version": rel.get("release_version"),
        "mutable_only": mutable,
        "ok": not blocked_reasons,
        "blocked": blocked_reasons or None,
    }


def production_db_rejected(host: str, port: str | int) -> bool:
    host_l = (host or "").strip().lower()
    try:
        port_i = int(port)
    except (TypeError, ValueError):
        port_i = -1
    return host_l in FORBIDDEN_PROD_HOSTS or port_i in FORBIDDEN_PROD_PORTS


def classify_environment(
    platform_name: str,
    *,
    claim_production: bool = False,
    env_production: bool = False,
) -> dict[str, Any]:
    name = (platform_name or "LOCAL").upper()
    if name not in PLATFORMS and name != "PRODUCTION":
        name = "LOCAL"
    kube = Path.home() / ".kube" / "config"
    kube_present = kube.is_file() or bool(os.environ.get("KUBECONFIG"))
    public_ca = os.environ.get("MEOS_PUBLIC_CA_TLS") == "1"
    secret_mgr = os.environ.get("MEOS_SECRET_MANAGER_AVAILABLE") == "1"
    digest = str(load_p353_manifest().get("image_digest") or "NOT_AVAILABLE")
    evidence = kube_present and public_ca and secret_mgr and digest.startswith("sha256:")
    production = False
    if claim_production or env_production or name == "PRODUCTION":
        production = False
        reason = "ENV_OR_FLAG_IS_NOT_PRODUCTION_EVIDENCE"
    else:
        reason = "NOT_CLAIMED"
    if evidence:
        reason = "INFRA_EVIDENCE_PRESENT_BUT_G26_VALIDATOR_REQUIRED"
        production = False
    return {
        "platform": name if name != "PRODUCTION" else "LOCAL",
        "detected_class": "LOCAL" if not kube_present else name,
        "claim_production": claim_production or env_production or name == "PRODUCTION",
        "production": production,
        "production_reason": reason,
        "localhost_is_production": False,
        "compose_is_production": False,
    }


def resource_preflight() -> dict[str, Any]:
    cpu = os.cpu_count() or 0
    mem_kb = 0
    meminfo = Path("/proc/meminfo")
    if meminfo.is_file():
        for line in meminfo.read_text(encoding="utf-8").splitlines():
            if line.startswith("MemTotal:"):
                parts = line.split()
                mem_kb = int(parts[1]) if len(parts) > 1 else 0
                break
    disk = shutil.disk_usage(str(repo_root()))
    return {
        "os": platform.system(),
        "cpu_count": cpu,
        "ram_mb": mem_kb // 1024 if mem_kb else "NOT_AVAILABLE",
        "disk_free_gb": round(disk.free / (1024**3), 2),
        "status": "PASS" if cpu >= 1 else "BLOCKED",
    }


def tool_status() -> dict[str, Any]:
    docker = shutil.which("docker") is not None
    compose = False
    if docker:
        compose = _run(["docker", "compose", "version"]).returncode == 0
    return {
        "docker": "PASS" if docker else "BLOCKED",
        "compose": "PASS" if compose else "BLOCKED",
        "kubectl": "PASS" if shutil.which("kubectl") else "READY_FOR_CREDENTIALS",
        "helm": "PASS" if shutil.which("helm") else "READY_FOR_CREDENTIALS",
        "flux": "PASS" if shutil.which("flux") else "READY_FOR_CREDENTIALS",
    }


def secrets_status() -> dict[str, str]:
    ext = os.environ.get("MEOS_SECRET_MANAGER_AVAILABLE") == "1"
    kube_ref = (
        repo_root() / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "templates" / "externalsecret.yaml"
    ).is_file()
    env_example = (repo_root() / "infrastructure" / "launch" / "env.production.example").is_file()
    if ext:
        value = "AVAILABLE"
    elif kube_ref and env_example:
        value = "NOT_VERIFIED"
    else:
        value = "MISSING"
    return {
        "external_secret_manager": "AVAILABLE" if ext else "MISSING",
        "env_injection_template": "AVAILABLE" if env_example else "MISSING",
        "kubernetes_secret_refs": "AVAILABLE" if kube_ref else "MISSING",
        "overall": value,
    }


def tls_status(platform_name: str, *, production: bool) -> dict[str, str]:
    example = (repo_root() / "infrastructure" / "docker" / "compose" / "Caddyfile.vps.example").is_file()
    public_ca = os.environ.get("MEOS_PUBLIC_CA_TLS") == "1"
    if production and not public_ca:
        return {"status": "BLOCKED", "class": "PRODUCTION_REQUIRES_PUBLIC_CA", "fabricated": "FALSE"}
    if platform_name in {"LOCAL", "DEMO"} and example:
        return {"status": "PASS", "class": "DEVELOPMENT_OR_SELF_SIGNED_ALLOWED", "fabricated": "FALSE"}
    if example:
        return {"status": "READY_FOR_CREDENTIALS", "class": "TEMPLATE_ONLY", "fabricated": "FALSE"}
    return {"status": "MISSING", "class": "NOT_AVAILABLE", "fabricated": "FALSE"}


def observability_status() -> dict[str, str]:
    return {
        "logs": "CONFIGURED",
        "metrics": "CONFIGURED",
        "alerts": "CONFIGURED",
        "health": "CONFIGURED",
        "readiness": "CONFIGURED",
        "g23": "FAIL",
        "g23_class": "CONFIGURED_NOT_PRODUCTION_VERIFIED",
    }


def checksum_package(root: Path | None = None) -> dict[str, str]:
    root = root or repo_root()
    out: dict[str, str] = {}
    for rel in PACKAGE_MEMBERS:
        path = root / rel
        if path.is_file():
            out[rel] = file_sha256(path)
    return out


def write_release_package(root: Path | None = None) -> Path:
    root = root or repo_root()
    dest = root / "infrastructure" / "launch" / "MEOS_RELEASE_PACKAGE"
    dest.mkdir(parents=True, exist_ok=True)
    release = meos_release(root)
    checksums = checksum_package(root)
    (dest / "MEOS_RELEASE.v1.yaml").write_text(
        _dump_yaml(release) + "\n",
        encoding="utf-8",
    )
    lines = [f"{digest}  {name}" for name, digest in sorted(checksums.items())]
    (dest / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
    readme = dest / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# MEOS_RELEASE_PACKAGE",
                "",
                "No secrets. No local databases. No generated credentials.",
                "Image identity: prefer IMAGE@DIGEST. Never :latest for certification.",
                "Installer default: PLAN_ONLY. See docs/meos/execution/MEOS_RELEASE_OPERATIONS.md",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return dest


def _dump_yaml(data: Any, indent: int = 0) -> str:
    try:
        import yaml

        return yaml.safe_dump(data, sort_keys=False, default_flow_style=False)
    except ImportError:
        return json.dumps(data, indent=2, sort_keys=True)


def installation_plan(
    platform_name: str,
    *,
    execute: bool = False,
    apply: bool = False,
    claim_production: bool = False,
    authorize_migrate: bool = False,
    authorize_destructive: bool = False,
    db_host: str = "",
    db_port: str = "",
) -> dict[str, Any]:
    env_prod = os.environ.get("MARPICH_ENVIRONMENT", "").lower() == "production"
    env = classify_environment(platform_name, claim_production=claim_production, env_production=env_prod)
    rel = meos_release()
    ident = identity_ok(rel, require_digest=env["claim_production"])
    tools = tool_status()
    resources = resource_preflight()
    secrets = secrets_status()
    tls = tls_status(env["platform"], production=bool(env["claim_production"]))
    host = db_host or os.environ.get("PGHOST", "127.0.0.1")
    port = db_port or os.environ.get("PGPORT", "5433")
    db_block = production_db_rejected(host, port) if env["claim_production"] else False
    mode = "PLAN_ONLY"
    if execute and apply:
        mode = "APPLY"
    elif execute:
        mode = "EXECUTE_DECLARED_PLAN_ONLY"
    blocked: list[str] = []
    if ident["blocked"]:
        blocked.extend(ident["blocked"])
    if env["claim_production"]:
        blocked.append("PRODUCTION_REQUIRES_EXT_G26")
        if db_block:
            blocked.append("PRODUCTION_DB_LOCALHOST_OR_DEMO_PORT")
        if tls["status"] == "BLOCKED":
            blocked.append("PRODUCTION_TLS_PUBLIC_CA_MISSING")
        if secrets["external_secret_manager"] != "AVAILABLE":
            blocked.append("PRODUCTION_SECRET_MANAGER_MISSING")
    if authorize_destructive:
        blocked.append("DESTRUCTIVE_MIGRATION_BLOCKED")
    if env["platform"] in {"AWS", "AZURE", "GCP", "KUBERNETES", "VPS", "HOSTINGER_VPS"}:
        deploy_status = "READY_FOR_CREDENTIALS"
    elif env["platform"] in {"LOCAL", "DEMO"}:
        deploy_status = "READY" if tools["docker"] == "PASS" else "BLOCKED"
    else:
        deploy_status = "BLOCKED"
    if mode == "APPLY" and env["platform"] not in {"LOCAL", "DEMO"}:
        blocked.append("APPLY_FORBIDDEN_WITHOUT_CREDENTIALS")
        mode = "PLAN_ONLY"
    if mode == "APPLY" and env["claim_production"]:
        blocked.append("APPLY_PRODUCTION_FORBIDDEN")
        mode = "PLAN_ONLY"
    commands = _platform_commands(env["platform"])
    return {
        "INSTALLATION_PLAN": True,
        "mode": mode,
        "platform": env["platform"],
        "environment": env,
        "release": {
            "release_version": rel["release_version"],
            "source_commit": rel["source_commit"],
            "image": rel["image"],
            "image_digest": rel["image_digest"],
            "schema_version": rel["schema_version"],
            "config_version": rel["config_version"],
            "verification_status": rel["verification_status"],
        },
        "preflight": {
            "cpu_ram_disk": resources,
            "tools": tools,
            "identity": ident,
            "database": {
                "host_class": "LOCAL_OR_UNSPECIFIED",
                "production_rejected": db_block,
                "status": "BLOCKED" if db_block else ("READY_FOR_CREDENTIALS" if env["claim_production"] else "PASS"),
            },
            "tls": tls,
            "secrets": secrets,
            "migration": {
                "preflight": "scripts/meos-migration-check.sh",
                "apply": "scripts/run-migrations.sh",
                "destructive": "BLOCKED",
                "authorize_migrate": authorize_migrate,
                "status": "BLOCKED" if authorize_destructive else "READY",
            },
            "backup": {
                "script": "scripts/meos-postgres-backup.sh",
                "class": "LOCAL_NON_PRODUCTION" if env["platform"] in {"LOCAL", "DEMO"} else "READY_FOR_CREDENTIALS",
                "production_backup": "NOT_VERIFIED",
            },
            "rollback": {
                "current_artifact": rel["image"] if rel["image_digest"] == "NOT_AVAILABLE" else f"{rel['registry']}@{rel['image_digest']}",
                "previous_artifact": "NOT_AVAILABLE",
                "command": commands["rollback"],
                "rollback_tested": False,
            },
            "observability": observability_status(),
        },
        "deployment_method": commands["deploy"],
        "verify": commands["verify"],
        "would_run": commands["deploy"] if mode == "APPLY" else [],
        "blocked": blocked,
        "status": "BLOCKED" if blocked else deploy_status,
        "g26_ready": False,
        "production_certified": False,
        "note": "PLAN_ONLY by default. APPLY is LOCAL/DEMO only. Production requires EXT-G26 evidence.",
    }


def _platform_commands(platform_name: str) -> dict[str, Any]:
    compose = "infrastructure/docker/compose/docker-compose.meos-prod.yml"
    compose_dev = "infrastructure/docker/compose/docker-compose.dev.yml"
    helm = "infrastructure/kubernetes/helm/marpich-iam"
    common_verify = [
        "curl -fsS http://127.0.0.1:8000/api/v1/health  # PROCESS_HEALTH (LOCAL/DEMO only)",
        "curl -fsS http://127.0.0.1:8000/api/v1/ready   # APPLICATION_READINESS (LOCAL/DEMO only)",
        "python3 scripts/meos-ext-g26-readiness.py      # PRODUCTION_READINESS (independent)",
    ]
    table = {
        "LOCAL": {
            "deploy": ["./scripts/dev-up.sh", "cd backend && uvicorn core.presentation.api.main:app --host 0.0.0.0 --port 8000"],
            "rollback": ["docker compose -f " + compose_dev + " down"],
            "verify": common_verify,
        },
        "DEMO": {
            "deploy": [
                "docker compose -p meosprod --env-file infrastructure/docker/compose/.env.meos-prod -f "
                + compose
                + " up -d"
            ],
            "rollback": ["MEOS_IMAGE=$MEOS_PREVIOUS_IMAGE docker compose -p meosprod -f " + compose + " up -d"],
            "verify": common_verify,
        },
        "VPS": {
            "deploy": ["./scripts/meos-vps-bootstrap.sh", "MEOS_IMAGE=ghcr.io/marpich/marpich-backend@sha256:<digest> docker compose -p meosprod up -d"],
            "rollback": ["MEOS_IMAGE=$MEOS_PREVIOUS_IMAGE docker compose -p meosprod up -d"],
            "verify": ["public HTTPS /api/v1/ready (not localhost)", "python3 scripts/meos-ext-g26-readiness.py"],
        },
        "HOSTINGER_VPS": {
            "deploy": ["ssh user@vps", "./scripts/meos-vps-bootstrap.sh"],
            "rollback": ["MEOS_IMAGE=$MEOS_PREVIOUS_IMAGE docker compose up -d"],
            "verify": ["public HTTPS /api/v1/ready", "Hostinger shared hosting is INCOMPATIBLE"],
        },
        "KUBERNETES": {
            "deploy": [
                "helm lint " + helm,
                "helm upgrade --install marpich-iam " + helm + " --set-string image.digest=<digest>",
            ],
            "rollback": ["helm rollback marpich-iam 0 --namespace marpich"],
            "verify": ["kubectl -n marpich get pods", "python3 scripts/meos-ext-g26-readiness.py"],
        },
        "AWS": {
            "deploy": ["# existing Helm/Flux on EKS or Compose on EC2 — no second architecture", "helm upgrade --install marpich-iam " + helm + " --set-string image.digest=<digest>"],
            "rollback": ["helm rollback marpich-iam 0 --namespace marpich"],
            "verify": ["non-local /api/v1/ready", "python3 scripts/meos-ext-g26-readiness.py"],
        },
        "AZURE": {
            "deploy": ["# existing Helm on AKS or Compose on VM", "helm upgrade --install marpich-iam " + helm + " --set-string image.digest=<digest>"],
            "rollback": ["helm rollback marpich-iam 0 --namespace marpich"],
            "verify": ["non-local /api/v1/ready", "python3 scripts/meos-ext-g26-readiness.py"],
        },
        "GCP": {
            "deploy": ["# existing Helm on GKE or Compose on GCE", "helm upgrade --install marpich-iam " + helm + " --set-string image.digest=<digest>"],
            "rollback": ["helm rollback marpich-iam 0 --namespace marpich"],
            "verify": ["non-local /api/v1/ready", "python3 scripts/meos-ext-g26-readiness.py"],
        },
    }
    return table.get(platform_name, table["LOCAL"])


def registry_credentials_present() -> bool:
    if os.environ.get("GITHUB_TOKEN") or os.environ.get("GHCR_TOKEN"):
        return True
    cfg = Path.home() / ".docker" / "config.json"
    if cfg.is_file():
        try:
            payload = json.loads(cfg.read_text(encoding="utf-8"))
            keys = " ".join(list(payload.get("auths") or {}) + list(payload.get("credHelpers") or {})).lower()
            return "ghcr.io" in keys
        except (OSError, json.JSONDecodeError):
            return False
    return False


def publish_status(*, confirm: bool) -> dict[str, Any]:
    ident = identity_ok(require_digest=True)
    if not confirm:
        return {"status": "REFUSED", "reason": "PUBLISH_REQUIRES_EXPLICIT_CONFIRM", "silent_publish": False}
    if not registry_credentials_present():
        return {"status": "READY_FOR_CREDENTIALS", "reason": "GHCR_CREDENTIALS_MISSING", "silent_publish": False}
    if not ident["ok"]:
        return {"status": "BLOCKED", "reason": ident["blocked"], "silent_publish": False}
    return {
        "status": "NOT_EXECUTED",
        "reason": "CREDENTIALS_PRESENT_BUT_PUSH_NOT_PERFORMED_IN_P354",
        "silent_publish": False,
    }


def redact_for_output(text: str) -> str:
    lowered = text.lower()
    if any(token in lowered for token in ("password=", "secret=", "token=", "begin private")):
        return "[REDACTED]"
    return text


if __name__ == "__main__":
    json.dump(meos_release(), sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
