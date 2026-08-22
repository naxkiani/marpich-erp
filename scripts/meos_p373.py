"""P373 universal deployment packaging. Fail closed. No secrets. No G26 manufacture."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import sys

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

TARGETS = (
    "vps",
    "hostinger-vps",
    "managed-container",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
)
TARGET_FILES = {
    "vps": "deploy/targets/vps.yaml",
    "hostinger-vps": "deploy/targets/hostinger-vps.yaml",
    "managed-container": "deploy/targets/managed-container.yaml",
    "kubernetes": "deploy/targets/kubernetes.yaml",
    "aws": "deploy/targets/aws.yaml",
    "azure": "deploy/targets/azure.yaml",
    "gcp": "deploy/targets/gcp.yaml",
}
LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1", "0.0.0.0"}
LOCAL_PORTS = {5433, 5444}
CREDENTIAL_ENV = {
    "vps": ("MEOS_VPS_HOST", "MEOS_VPS_SSH_USER"),
    "hostinger-vps": ("MEOS_VPS_HOST", "MEOS_HOSTINGER_VPS_HOST"),
    "managed-container": ("MEOS_MANAGED_CONTAINER_ACCOUNT",),
    "kubernetes": ("KUBECONFIG",),
    "aws": ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"),
    "azure": ("AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "AZURE_TENANT_ID"),
    "gcp": ("GOOGLE_APPLICATION_CREDENTIALS", "GCLOUD_PROJECT"),
}
SECRET_MARKERS = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=", "PASSWORD=")
PLAN_FILES = (
    "01_PREFLIGHT.md",
    "02_INFRASTRUCTURE.md",
    "03_SECRETS.md",
    "04_DATABASE.md",
    "05_DEPLOYMENT.md",
    "06_VERIFICATION.md",
    "07_BACKUP.md",
    "08_ROLLBACK.md",
)


def _load(filename: str, name: str):
    path = repo_root() / "scripts" / filename
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _env_set(name: str) -> bool:
    value = os.environ.get(name, "").strip()
    return bool(value) and value not in {"CHANGE_ME", "NOT_AVAILABLE", "none"}


def _g26() -> dict[str, Any]:
    return _load("meos-ext-g26-readiness.py", "meos_p373_g26").evaluate(repo_root())


def _digest(rel: dict[str, Any] | None = None) -> str:
    rel = rel or meos_release()
    digest = str(rel.get("image_digest") or os.environ.get("MEOS_IMAGE_DIGEST") or "NOT_AVAILABLE")
    if digest.startswith("sha256:") and "dirty" not in digest.lower():
        return digest
    return "NOT_AVAILABLE"


def _db_host_port() -> tuple[str, str]:
    host = os.environ.get("MEOS_PRODUCTION_PGHOST", os.environ.get("PGHOST", "127.0.0.1"))
    port = os.environ.get("MEOS_PRODUCTION_PGPORT", os.environ.get("PGPORT", "5433"))
    return host, str(port)


def local_database_rejected(host: str | None = None, port: str | None = None) -> bool:
    if host is None or port is None:
        host, port = _db_host_port()
    try:
        port_i = int(port)
    except (TypeError, ValueError):
        port_i = -1
    return host.strip().lower() in LOCAL_HOSTS or port_i in LOCAL_PORTS


def credentials_present(target: str) -> bool:
    if target == "kubernetes":
        kube = Path(os.environ.get("KUBECONFIG", "")).expanduser()
        home = Path(os.environ.get("MEOS_KUBE_HOME", str(Path.home()))) / ".kube" / "config"
        return _env_set("KUBECONFIG") and kube.is_file() or home.is_file()
    names = CREDENTIAL_ENV.get(target, ())
    if target == "hostinger-vps":
        return _env_set("MEOS_VPS_HOST") or _env_set("MEOS_HOSTINGER_VPS_HOST")
    return all(_env_set(n) for n in names) if names else False


def normalize_target(raw: str | None) -> str:
    key = (raw or "").strip().lower()
    if not key:
        return "NOT_SELECTED"
    if key in TARGETS:
        return key
    return "UNKNOWN"


def category(status: str) -> str:
    if status not in {"AVAILABLE", "MISSING", "INVALID", "NOT_VERIFIED"}:
        return "NOT_VERIFIED"
    return status


def frozen() -> dict[str, Any]:
    g26 = _g26()
    ready = bool(g26.get("g26_ready") is True)
    return {
        "G26_STATUS": g26.get("g26_status", "BLOCKED"),
        "G26_READY": ready,
        "P0": int(g26.get("p0_count", 1)),
        "P313": "NOT_STARTED" if ready else g26.get("p313", "NOT_CERTIFIED"),
        "P313_REENTRY_READY": ready,
        "PRODUCTION_CERTIFIED": False,
        "GO_LIVE_READY": False,
        "GO_LIVE_AUTHORIZATION": "NOT_APPROVED",
        "ACTIVE_APPLICATIONS": 0,
        "PRODUCTION_TRAFFIC": "NOT_ENABLED",
        "G23": g26.get("g23", "FAIL"),
    }


def environment_preflight() -> dict[str, Any]:
    git = git_state()
    digest = _digest()
    host, port = _db_host_port()
    local_db = local_database_rejected(host, port)
    sm = os.environ.get("MARPICH_SECRET_MANAGER_BACKEND", os.environ.get("MEOS_SECRET_MANAGER_BACKEND", "env"))
    sm_ok = sm.strip().lower() not in {"", "env", "dotenv", "file"} and os.environ.get(
        "MEOS_SECRET_MANAGER_AVAILABLE", ""
    ).strip() == "1"
    dns = os.environ.get("MEOS_PRODUCTION_DNS", "").strip()
    tls = os.environ.get("MEOS_PUBLIC_CA_TLS", "").strip() == "1"
    categories = {
        "APPLICATION": category("AVAILABLE" if (repo_root() / "backend").is_dir() else "MISSING"),
        "DATABASE": category("INVALID" if local_db else "NOT_VERIFIED"),
        "SECRETS": category("AVAILABLE" if sm_ok else "MISSING"),
        "TLS": category("AVAILABLE" if tls and dns else "MISSING"),
        "DNS": category("AVAILABLE" if dns and dns.lower() not in LOCAL_HOSTS else "MISSING"),
        "NETWORK": category("NOT_VERIFIED"),
        "OBSERVABILITY": category("NOT_VERIFIED"),
        "BACKUP": category("NOT_VERIFIED"),
        "RESTORE": category("NOT_VERIFIED"),
        "ROLLBACK": category("NOT_VERIFIED"),
    }
    report = {
        "P373_STATUS": "UNIVERSAL_DEPLOYMENT_PACKAGE_READY",
        "categories": categories,
        "SECRET_MANAGER": "AVAILABLE" if sm_ok else "MISSING",
        "IMAGE_DIGEST": digest,
        "COMMIT_DIRTY": bool(git.get("dirty")),
        "LOCAL_DATABASE_REJECTED": local_db,
        "COMPOSE_IS_PRODUCTION": False,
        "LOCALHOST_IS_PRODUCTION": False,
        **frozen(),
    }
    _assert_no_secrets(report)
    return report


def target_adapter(target: str | None) -> dict[str, Any]:
    name = normalize_target(target)
    if name == "NOT_SELECTED":
        return {
            "TARGET": "NOT_SELECTED",
            "STATUS": "BLOCKED",
            "TARGET_ADAPTER_STATUS": "IMPLEMENTED",
            "DEPLOYMENT_ALLOWED": False,
            **frozen(),
        }
    if name == "UNKNOWN":
        return {
            "TARGET": "UNKNOWN",
            "STATUS": "BLOCKED",
            "REASON": "unknown_target",
            "DEPLOYMENT_ALLOWED": False,
            **frozen(),
        }
    creds = credentials_present(name)
    profile = TARGET_FILES[name]
    hostinger_shared = "INCOMPATIBLE" if name == "hostinger-vps" else "NOT_APPLICABLE"
    report = {
        "TARGET": name.upper().replace("-", "_"),
        "PROFILE": profile,
        "STATUS": "READY_FOR_CREDENTIALS" if not creds else "READY_FOR_CREDENTIALS",
        "CREDENTIALS": "AVAILABLE" if creds else "MISSING",
        "HOSTINGER_SHARED_HOSTING": hostinger_shared,
        "HOSTINGER_VPS": "SUPPORTED_TARGET" if name == "hostinger-vps" else "NOT_APPLICABLE",
        "INSTRUCTIONS": f"Reuse {profile}; do not invent access",
        "ENVIRONMENT_CHECKLIST": environment_preflight()["categories"],
        "VERIFICATION_CHECKLIST": [
            "health GET /api/v1/health",
            "ready GET /api/v1/ready",
            "digest match",
            "non-localhost database",
        ],
        "FABRICATED_ACCESS": False,
        "DEPLOYMENT_ALLOWED": False,
        **frozen(),
    }
    _assert_no_secrets(report)
    return report


def deployment_preflight(target: str | None) -> dict[str, Any]:
    name = normalize_target(target)
    git = git_state()
    digest = _digest()
    dirty = bool(git.get("dirty"))
    local_db = local_database_rejected()
    dns = os.environ.get("MEOS_PRODUCTION_DNS", "").strip()
    tls = os.environ.get("MEOS_PUBLIC_CA_TLS", "").strip() == "1"
    sm_ok = environment_preflight()["SECRET_MANAGER"] == "AVAILABLE"
    creds = credentials_present(name) if name in TARGETS else False
    checks = {
        "REPOSITORY": "FAIL" if dirty else "PASS",
        "BUILD": "CONFIGURED",
        "TESTS": "NOT_EXECUTED" if name in TARGETS else "NOT_EXECUTED",
        "IMAGE": "LOCAL_IMAGE",
        "DIGEST": "MISSING" if digest == "NOT_AVAILABLE" else "AVAILABLE",
        "DATABASE": "INVALID" if local_db else "NOT_VERIFIED",
        "SECRETS": "MISSING" if not sm_ok else "AVAILABLE",
        "DNS": "MISSING" if not dns or dns.lower() in LOCAL_HOSTS else "NOT_VERIFIED",
        "TLS": "MISSING" if not tls else "NOT_VERIFIED",
        "NETWORK": "NOT_VERIFIED",
        "OBSERVABILITY": "NOT_VERIFIED",
        "BACKUP": "NOT_VERIFIED",
        "RESTORE": "NOT_VERIFIED",
        "ROLLBACK": "NOT_VERIFIED",
        "TARGET": name.upper().replace("-", "_") if name in TARGETS else name,
    }
    allowed = False
    if name == "NOT_SELECTED":
        status = "BLOCKED"
        reason = "TARGET_NOT_SELECTED"
    elif name == "UNKNOWN":
        status = "BLOCKED"
        reason = "UNKNOWN_TARGET"
    elif dirty:
        status = "FAIL"
        reason = "DIRTY_SHA"
    elif digest == "NOT_AVAILABLE":
        status = "BLOCKED"
        reason = "MISSING_DIGEST"
    elif local_db:
        status = "BLOCKED"
        reason = "LOCAL_DATABASE_REJECTED"
    elif not creds:
        status = "READY_FOR_CREDENTIALS"
        reason = "MISSING_CREDENTIALS"
    elif not dns or not tls or not sm_ok:
        status = "BLOCKED"
        reason = "MISSING_TLS_DNS_OR_SECRETS"
    else:
        status = "BLOCKED"
        reason = "RUNTIME_NOT_VERIFIED"
    report = {
        "P373_STATUS": "UNIVERSAL_DEPLOYMENT_PACKAGE_READY",
        "TARGET": checks["TARGET"],
        "DEPLOYMENT_ALLOWED": allowed,
        "PREFLIGHT_STATUS": status,
        "REASON": reason,
        "checks": checks,
        "LOCAL_IS_PRODUCTION": False,
        "DEMO_IS_PRODUCTION": False,
        "COMPOSE_IS_PRODUCTION": False,
        **frozen(),
    }
    _assert_no_secrets(report)
    return report


def deploy(target: str | None, *, confirm: bool = False, environment: str | None = None) -> dict[str, Any]:
    env = (environment or "").strip().upper() or "NOT_SELECTED"
    pre = deployment_preflight(target)
    if not confirm:
        report = {
            "EXECUTED": False,
            "DEPLOYMENT": "NO_DEPLOYMENT",
            "REASON": "CONFIRMATION_REQUIRED",
            "DEPLOYMENT_ALLOWED": False,
            "ENVIRONMENT": env,
            **pre,
        }
        _assert_no_secrets(report)
        return report
    if env in {"LOCAL", "DEVELOPMENT", "TEST", "DEMO"}:
        report = {
            "EXECUTED": False,
            "DEPLOYMENT": "REFUSED",
            "REASON": "NON_PRODUCTION_ENVIRONMENT",
            "ENVIRONMENT": env,
            **pre,
        }
        _assert_no_secrets(report)
        return report
    if env == "PRODUCTION" and normalize_target(target) not in TARGETS:
        report = {
            "EXECUTED": False,
            "DEPLOYMENT": "REFUSED",
            "REASON": "PRODUCTION_REQUIRES_EXPLICIT_TARGET",
            "ENVIRONMENT": env,
            **pre,
        }
        _assert_no_secrets(report)
        return report
    report = {
        "EXECUTED": False,
        "DEPLOYMENT": "REFUSED",
        "REASON": pre.get("REASON") or "PREFLIGHT_FAILED",
        "ENVIRONMENT": env,
        **pre,
        "DEPLOYMENT_ALLOWED": False,
    }
    _assert_no_secrets(report)
    return report


def post_deploy_verify() -> dict[str, Any]:
    deployed_commit = os.environ.get("MEOS_DEPLOYED_COMMIT", "").strip()
    deployed_digest = os.environ.get("MEOS_DEPLOYED_DIGEST", "").strip()
    health = os.environ.get("MEOS_HEALTH_URL", "http://127.0.0.1:8000/api/v1/health")
    local_health = any(h in health for h in ("127.0.0.1", "localhost", "[::1]"))
    identity = bool(deployed_commit and deployed_digest.startswith("sha256:") and not local_health)
    report = {
        "DEPLOYMENT_IDENTITY": "VERIFIED" if identity else "NOT_AVAILABLE",
        "COMMIT": deployed_commit or "NOT_AVAILABLE",
        "IMAGE_DIGEST": deployed_digest if deployed_digest.startswith("sha256:") else "NOT_AVAILABLE",
        "HEALTH": "NOT_VERIFIED",
        "READINESS": "NOT_VERIFIED",
        "TLS": "NOT_VERIFIED",
        "DNS": "NOT_VERIFIED",
        "LOGS": "NOT_VERIFIED",
        "METRICS": "NOT_VERIFIED",
        "ALERTS": "NOT_VERIFIED",
        "LOCAL_HEALTH_IS_PRODUCTION": False,
        "PROCESS_EXISTENCE_IS_SUCCESS": False,
        **frozen(),
    }
    _assert_no_secrets(report)
    return report


def _yaml(data: dict[str, Any]) -> str:
    lines = []
    for key, value in data.items():
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif isinstance(value, (list, tuple)):
            rendered = "[" + ", ".join(str(v) for v in value) + "]"
        elif value is None:
            rendered = "NOT_AVAILABLE"
        else:
            rendered = str(value)
        lines.append(f"{key}: {rendered}")
    return "\n".join(lines) + "\n"


def package_dir(root: Path | None = None) -> Path:
    return (root or repo_root()) / "dist" / "meos-release"


def build_release(*, run_tests: bool = False, build_image: bool = False) -> dict[str, Any]:
    root = repo_root()
    git = git_state()
    rel = meos_release()
    digest = _digest(rel)
    dirty = bool(git.get("dirty"))
    dest = package_dir(root)
    dest.mkdir(parents=True, exist_ok=True)
    test_status = "NOT_EXECUTED"
    if run_tests:
        python = root / "backend" / ".venv" / "bin" / "python"
        runner = [str(python if python.is_file() else "python3"), "-m", "pytest", "tests/contracts/test_p372_multiplatform_launch.py", "-q"]
        result = subprocess.run(runner, cwd=root / "backend", check=False, capture_output=True, text=True)
        test_status = "PASS" if result.returncode == 0 else "FAIL"
    docker_status = "NOT_AVAILABLE"
    evidence = root / "docs" / "meos" / "execution" / ".last_docker_build.json"
    image_name = "meos/backend"
    image_tag = "p353-local"
    image_id = "NOT_AVAILABLE"
    if evidence.is_file():
        try:
            payload = json.loads(evidence.read_text(encoding="utf-8"))
            docker_status = str(payload.get("status") or "NOT_AVAILABLE")
            image = str(payload.get("image") or image_name)
            if ":" in image:
                image_name, image_tag = image.split(":", 1)
            image_id = str(payload.get("image_id") or "NOT_AVAILABLE")
        except json.JSONDecodeError:
            docker_status = "NOT_AVAILABLE"
    if build_image and shutil.which("docker"):
        docker_status = docker_status if docker_status == "PASS" else "NOT_EXECUTED"
    manifest = {
        "release_id": "MEOS-P373-PACKAGE",
        "version": str(rel.get("release_version") or "0.1.0"),
        "commit_sha": git.get("source_commit") or "NOT_AVAILABLE",
        "commit_state": "DIRTY" if dirty else "CLEAN",
        "build_id": str(rel.get("build_id") or "NOT_AVAILABLE"),
        "image": f"{image_name}:{image_tag}",
        "image_digest": digest,
        "image_class": "LOCAL_IMAGE" if digest == "NOT_AVAILABLE" else "REGISTRY_DIGEST",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "database_schema_version": str(rel.get("schema_version") or "NOT_AVAILABLE"),
        "migration_set": "infrastructure/docker/migrations",
        "supported_targets": list(TARGETS),
        "health_endpoint": "/api/v1/health",
        "readiness_endpoint": "/api/v1/ready",
        "security_profile": "CONFIGURED",
        "backup_profile": "CONFIGURED",
        "rollback_profile": "CONFIGURED",
        "immutable": False if dirty or digest == "NOT_AVAILABLE" else True,
        "dirty_sha": "INVALID" if dirty else "CLEAN",
        "missing_digest": "NOT_PUBLISHED" if digest == "NOT_AVAILABLE" else "PRESENT",
        "local_image": "NON_PRODUCTION",
        "mutable_latest": "NON_CERTIFICATION_EVIDENCE",
        "production_certified": False,
        "g26_ready": False,
    }
    files = {
        "manifest.yaml": _yaml(manifest),
        "deployment-contract.yaml": _yaml(
            {
                "source": "docs/meos/execution/MEOS_MULTI_PLATFORM_DEPLOYMENT_CONTRACT.v1.yaml",
                "duplicate_architecture": "FORBIDDEN",
            }
        ),
        "image.yaml": _yaml(
            {
                "IMAGE_NAME": image_name,
                "IMAGE_TAG": image_tag,
                "IMAGE_DIGEST": digest,
                "IMAGE_ID_LOCAL": image_id,
                "COMMIT_SHA": manifest["commit_sha"],
                "BUILD_ID": manifest["build_id"],
                "REGISTRY_STATUS": "NOT_AVAILABLE",
                "IMAGE_CLASS": "LOCAL_IMAGE",
            }
        ),
        "migrations.yaml": _yaml(
            {
                "path": "infrastructure/docker/migrations",
                "schema_version": manifest["database_schema_version"],
                "apply": "NOT_EXECUTED",
            }
        ),
        "health.yaml": _yaml({"endpoint": "/api/v1/health", "localhost_is_production": False}),
        "readiness.yaml": _yaml({"endpoint": "/api/v1/ready", "localhost_is_production": False}),
        "security.yaml": _yaml(
            {
                "tls": "REQUIRED_FOR_PRODUCTION",
                "secrets": "REFERENCES_ONLY",
                "non_root": "CONFIGURED",
            }
        ),
        "backup.yaml": _yaml(
            {
                "script": "scripts/meos-postgres-backup.sh",
                "workstation_backup_is_production": False,
                "BACKUP_ID": "NOT_AVAILABLE",
            }
        ),
        "restore.yaml": _yaml(
            {
                "script": "scripts/meos-postgres-restore-drill.sh",
                "local_restore_is_production": False,
            }
        ),
        "rollback.yaml": _yaml(
            {
                "CURRENT_RELEASE": manifest["image"],
                "PREVIOUS_RELEASE": "NOT_AVAILABLE",
                "ROLLBACK_ACTION": "previous IMAGE_DIGEST or helm rollback",
                "POST_ROLLBACK_HEALTH": "NOT_EXECUTED",
                "configured_equals_exercised": False,
            }
        ),
        "README.md": (
            "# MEOS universal release package (P373)\n\n"
            "Pointers only. No application source copy. No secrets.\n"
            "Dirty SHA = INVALID. Missing digest = NOT_PUBLISHED. Local image = NON_PRODUCTION.\n"
            "Canonical application package remains `infrastructure/launch/MEOS_RELEASE_PACKAGE/`.\n"
        ),
    }
    for rel_path, text in files.items():
        path = dest / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    for target, profile in TARGET_FILES.items():
        tdir = dest / "targets" / target
        tdir.mkdir(parents=True, exist_ok=True)
        body = {
            "target": target,
            "profile": profile,
            "status": "READY_FOR_CREDENTIALS",
            "application_fork": "FORBIDDEN",
        }
        if target == "hostinger-vps":
            body["HOSTINGER_SHARED_HOSTING"] = "INCOMPATIBLE"
            body["HOSTINGER_VPS"] = "SUPPORTED_TARGET"
        if target == "kubernetes":
            body["helm"] = "infrastructure/kubernetes/helm/marpich-iam"
            body["flux"] = "infrastructure/fluxcd/marpich-iam-helmrelease.yaml"
            body["new_kubernetes_layer"] = "FORBIDDEN"
        (tdir / "adapter.yaml").write_text(_yaml(body), encoding="utf-8")
    checksums = []
    for path in sorted(p for p in dest.rglob("*") if p.is_file() and p.name != "SHA256SUMS"):
        digest_file = hashlib.sha256(path.read_bytes()).hexdigest()
        checksums.append(f"{digest_file}  {path.relative_to(dest).as_posix()}")
    (dest / "SHA256SUMS").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    report = {
        "P373_STATUS": "UNIVERSAL_DEPLOYMENT_PACKAGE_READY",
        "BUILD_STATUS": "PACKAGE_GENERATED",
        "TEST_STATUS": test_status,
        "DOCKER_STATUS": docker_status,
        "RELEASE_PACKAGE_STATUS": "NON_IMMUTABLE" if dirty or digest == "NOT_AVAILABLE" else "IMMUTABLE",
        "MANIFEST_STATUS": "GENERATED",
        "PACKAGE_DIR": str(dest),
        "IMMUTABLE": False if dirty or digest == "NOT_AVAILABLE" else True,
        "image_digest": digest,
        **frozen(),
    }
    _assert_no_secrets(report)
    return report


def write_launch_plan(target: str | None) -> dict[str, Any]:
    name = normalize_target(target)
    dest = package_dir() / "plans" / (name if name in TARGETS else "NOT_SELECTED")
    dest.mkdir(parents=True, exist_ok=True)
    adapter = target_adapter(target)
    pre = deployment_preflight(target)
    pages = {
        "01_PREFLIGHT.md": f"# Preflight\n\nTARGET={adapter['TARGET']}\nDEPLOYMENT_ALLOWED=FALSE\nREASON={pre.get('REASON')}\n",
        "02_INFRASTRUCTURE.md": f"# Infrastructure\n\nProfile: {adapter.get('PROFILE', 'NOT_SELECTED')}\nDo not create cloud resources from this plan.\n",
        "03_SECRETS.md": "# Secrets\n\nSECRET_MANAGER checklist only. Never store values.\n",
        "04_DATABASE.md": "# Database\n\nReject localhost / :5433 / :5444 / Compose for production.\n",
        "05_DEPLOYMENT.md": "# Deployment\n\nThis plan does not execute deployment.\n",
        "06_VERIFICATION.md": "# Verification\n\nHealth and ready endpoints. Local /health is not production.\n",
        "07_BACKUP.md": "# Backup\n\nReuse scripts/meos-postgres-backup.sh. Workstation backup is not production.\n",
        "08_ROLLBACK.md": "# Rollback\n\nConfigured rollback is not exercised rollback.\n",
    }
    for filename, text in pages.items():
        (dest / filename).write_text(text, encoding="utf-8")
    report = {
        "LAUNCH_PLAN_STATUS": "GENERATED",
        "PLAN_DIR": str(dest),
        "EXECUTED_DEPLOYMENT": False,
        "TARGET": adapter["TARGET"],
        **frozen(),
    }
    _assert_no_secrets(report)
    return report


def prepare_launch(target: str | None, *, run_tests: bool = False) -> dict[str, Any]:
    built = build_release(run_tests=run_tests)
    plan = write_launch_plan(target)
    pre = deployment_preflight(target)
    report = {
        "P373_STATUS": "UNIVERSAL_DEPLOYMENT_PACKAGE_READY",
        "PREPARED": True,
        "DEPLOYED": False,
        "TRAFFIC_ENABLED": False,
        **built,
        **plan,
        "DEPLOYMENT_ALLOWED": pre["DEPLOYMENT_ALLOWED"],
        "PREFLIGHT_STATUS": pre["PREFLIGHT_STATUS"],
        "TARGET_ADAPTER_STATUS": "IMPLEMENTED",
    }
    _assert_no_secrets(report)
    return report


def _assert_no_secrets(payload: Any) -> None:
    blob = json.dumps(payload, default=str)
    for marker in SECRET_MARKERS:
        if marker in blob:
            raise RuntimeError("secret marker leaked")
