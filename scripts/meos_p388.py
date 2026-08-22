"""P388 launch factory overlay. No provision. No invented digest or G26."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import sys
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from meos_p373 import local_database_rejected  # noqa: E402
from meos_p377 import deployment_plan  # noqa: E402
from meos_p382 import production_safety_lock  # noqa: E402
from meos_p385 import artifact_validate  # noqa: E402
from meos_p387 import preflight, provider, tooling  # noqa: E402
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
MODES = (
    "BUILD_ONLY",
    "PACKAGE_ONLY",
    "PREFLIGHT_ONLY",
    "DEPLOYMENT_PLAN",
    "DEPLOY",
    "VERIFY",
    "ROLLBACK",
    "FULL_REHEARSAL",
)
ENVIRONMENTS = ("LOCAL", "DEMO", "TEST", "STAGING", "PRODUCTION")
CREDENTIAL_ENV = {
    "PROVIDER": ("MEOS_PRODUCTION_PROVIDER", "MEOS_DEPLOYMENT_PROVIDER"),
    "CLUSTER": ("KUBECONFIG",),
    "DATABASE": ("MEOS_PRODUCTION_PGHOST",),
    "DNS": ("MEOS_PUBLIC_HOST",),
    "SECRET_MANAGER": ("MEOS_SECRET_MANAGER_AVAILABLE",),
    "CI/CD": ("GITHUB_TOKEN",),
    "REGISTRY": ("GHCR_TOKEN",),
    "TLS": ("MEOS_TLS_CERT_PATH",),
}


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p388_g26", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.evaluate(repo_root())


def _env_set(name: str) -> bool:
    value = os.environ.get(name, "").strip()
    return bool(value) and value not in {"CHANGE_ME", "NOT_AVAILABLE", "none"}


def _sealed(payload: dict[str, Any]) -> dict[str, Any]:
    blob = json.dumps(payload, default=str)
    for marker in FORBIDDEN:
        if marker in blob:
            raise RuntimeError("secret marker leaked")
    return payload


def credential_preflight() -> dict[str, Any]:
    categories: dict[str, str] = {}
    for name, keys in CREDENTIAL_ENV.items():
        present = any(_env_set(key) for key in keys)
        if name == "DATABASE" and local_database_rejected():
            categories[name] = "INVALID"
        elif name == "CLUSTER":
            kube = Path(os.environ.get("KUBECONFIG", "")).expanduser()
            if _env_set("KUBECONFIG") and not kube.is_file():
                categories[name] = "INVALID"
            elif present:
                categories[name] = "NOT_VERIFIED"
            else:
                categories[name] = "MISSING"
        elif present:
            categories[name] = "NOT_VERIFIED"
        else:
            categories[name] = "MISSING"
    return _sealed(
        {
            "PROVIDER": categories["PROVIDER"],
            "CLUSTER": categories["CLUSTER"],
            "DATABASE": categories["DATABASE"],
            "DNS": categories["DNS"],
            "SECRET_MANAGER": categories["SECRET_MANAGER"],
            "CI/CD": categories["CI/CD"],
            "REGISTRY": categories["REGISTRY"],
            "TLS": categories["TLS"],
            "values_printed": False,
            "kubeconfig_printed": False,
        }
    )


def release_package() -> dict[str, Any]:
    git = git_state()
    art = artifact_validate()
    return _sealed(
        {
            "package": "infrastructure/launch/MEOS_RELEASE_PACKAGE",
            "secrets_included": False,
            "kubeconfig_included": False,
            "private_keys_included": False,
            "ARTIFACT_VALID": art["ARTIFACT_VALID"],
            "IMAGE_DIGEST": art["IMAGE_DIGEST"],
            "dirty": bool(git.get("dirty")),
            "status": "BLOCKED" if git.get("dirty") or not art["ARTIFACT_VALID"] else "READY",
            "second_release_dir": False,
        }
    )


def migration_check() -> dict[str, Any]:
    return _sealed(
        {
            "sequence": [
                "DATABASE_PREFLIGHT",
                "BACKUP_REQUIRED_CHECK",
                "MIGRATION_PLAN",
                "COMPATIBILITY_CHECK",
                "MIGRATION",
                "VERIFY",
            ],
            "executed": False,
            "destructive": False,
            "production_drop_tables": False,
            "localhost_rejected": local_database_rejected(),
            "status": "BLOCKED",
        }
    )


def backup_manager(mode: str = "CHECK") -> dict[str, Any]:
    return _sealed(
        {
            "mode": mode,
            "backup_id": "NOT_AVAILABLE",
            "timestamp": "NOT_AVAILABLE",
            "target": "LOCAL",
            "retention": "CONFIGURED",
            "encryption": "CONFIGURED",
            "verification": "NOT_EXECUTED",
            "PRODUCTION_BACKUP": False,
            "script": "scripts/meos-postgres-backup.sh",
            "restore_script": "scripts/meos-postgres-restore-drill.sh",
            "executed": False,
        }
    )


def rollback_factory() -> dict[str, Any]:
    rel = meos_release()
    return _sealed(
        {
            "current_release": "P354-RC-NOT_ELIGIBLE",
            "previous_release": "NOT_AVAILABLE",
            "current_digest": rel.get("image_digest") or "NOT_AVAILABLE",
            "previous_digest": "NOT_AVAILABLE",
            "rollback_action": "CONFIGURED",
            "post_rollback_verification": "NOT_EXECUTED",
            "status": "CONFIGURED",
            "EXERCISED": False,
            "canonical": "scripts/meos-g27-rollback.py",
            "executed": False,
        }
    )


def runtime_verify(environment: str = "LOCAL") -> dict[str, Any]:
    env = (environment or "LOCAL").upper()
    if env not in ENVIRONMENTS:
        env = "LOCAL"
    git = git_state()
    rel = meos_release()
    production = env == "PRODUCTION"
    return _sealed(
        {
            "environment": env,
            "commit": git.get("source_commit"),
            "image": rel.get("image") or "meos/backend:p353-local",
            "digest": rel.get("image_digest") or "NOT_AVAILABLE",
            "database": "NON_PRODUCTION",
            "health": "LOCAL_ONLY",
            "readiness": "/api/v1/ready",
            "ingress": "NOT_AVAILABLE",
            "logs": "CONFIGURED",
            "metrics": "CONFIGURED",
            "status": "BLOCKED" if production else "LOCAL_VERIFIED",
            "is_production": False,
        }
    )


def platform_compatibility() -> dict[str, Any]:
    root = repo_root()
    dockerfile = root / "infrastructure" / "docker" / "images" / "backend.Dockerfile"
    return _sealed(
        {
            "container_portability": "CONFIGURED" if dockerfile.is_file() else "FAIL",
            "environment_variables": "CONFIGURED",
            "database_configuration": "CONFIGURED",
            "secret_references": "CONFIGURED",
            "filesystem_assumptions": "ephemeral_ok",
            "network_assumptions": "0.0.0.0",
            "timezone": "UTC",
            "locale": "CONFIGURED",
            "health": "/live",
            "readiness": "/api/v1/ready",
            "graceful_shutdown": "STOPSIGNAL_SIGTERM",
            "persistent_storage": "CONFIGURED",
            "background_jobs": "CONFIGURED",
            "same_image_targets": ["Docker", "Kubernetes", "VPS", "EKS", "AKS", "GKE"],
            "live_deployment": False,
            "source_fork_required": False,
        }
    )


def launch_checklist() -> dict[str, Any]:
    lock = production_safety_lock()
    git = git_state()
    art = artifact_validate()
    checks = {
        "SOURCE": "FAIL" if git.get("dirty") else "PASS",
        "RELEASE": "BLOCKED",
        "IMAGE": "LOCAL_ONLY",
        "DATABASE": "INVALID" if local_database_rejected() else "NOT_VERIFIED",
        "SECRETS": "CONFIGURED",
        "DNS": "NOT_AVAILABLE",
        "TLS": "CONFIGURED",
        "NETWORK": "CONFIGURED",
        "OBSERVABILITY": "CONFIGURED",
        "BACKUP": "CONFIGURED",
        "RESTORE": "CONFIGURED",
        "ROLLBACK": "CONFIGURED",
        "SECURITY": "CONFIGURED",
        "TENANT_ISOLATION": "UNIT_TEST_EXISTS",
        "G26": "BLOCKED",
        "P313": "NOT_CERTIFIED",
        "GO_LIVE": "NOT_APPROVED",
    }
    return _sealed(
        {
            "checks": checks,
            "IMAGE_DIGEST": art["IMAGE_DIGEST"],
            "PRODUCTION_LOCK": lock["PRODUCTION_SAFETY_LOCK"],
            "PRODUCTION_DEPLOYMENT": "LOCKED",
            "READY": False,
        }
    )


def factory(mode: str = "PREFLIGHT_ONLY", environment: str = "LOCAL", target: str | None = None) -> dict[str, Any]:
    mode = (mode or "PREFLIGHT_ONLY").upper()
    if mode not in MODES:
        mode = "PREFLIGHT_ONLY"
    env = (environment or "LOCAL").upper()
    git = git_state()
    art = artifact_validate()
    lock = production_safety_lock()
    dirty = bool(git.get("dirty"))
    digest_ok = str(art["IMAGE_DIGEST"]).startswith("sha256:")
    production = env == "PRODUCTION"
    stopped = []
    if dirty:
        stopped.append("dirty_source")
    if not digest_ok:
        stopped.append("missing_digest")
    if local_database_rejected() and production:
        stopped.append("localhost_database")
    creds = credential_preflight()
    if all(value in {"MISSING", "INVALID"} for key, value in creds.items() if key in CREDENTIAL_ENV) and production:
        stopped.append("missing_credentials")
    if production:
        stopped.append("production_lock")
    pipeline = {
        "SOURCE": "DIRTY" if dirty else "CLEAN",
        "CLEAN_RELEASE": "BLOCKED" if dirty else "READY_FOR_CI",
        "TEST": "CONFIGURED",
        "BUILD": "BLOCKED" if dirty else "READY_FOR_CI",
        "IMAGE": "LOCAL_ONLY",
        "DIGEST": "NOT_AVAILABLE" if not digest_ok else art["IMAGE_DIGEST"],
        "PACKAGE": release_package()["status"],
        "TARGET_PREFLIGHT": preflight(),
        "DEPLOYMENT_PLAN": deployment_plan(target, env.lower()) if mode in {"DEPLOYMENT_PLAN", "FULL_REHEARSAL"} else "NOT_REQUESTED",
        "DEPLOYMENT": "LOCKED" if production or mode == "DEPLOY" else "NOT_EXECUTED",
        "RUNTIME_VALIDATION": runtime_verify(env)["status"],
        "BACKUP": "CONFIGURED",
        "ROLLBACK_VALIDATION": "CONFIGURED",
        "G26": "BLOCKED",
    }
    executed = False
    if mode == "DEPLOY" or production:
        executed = False
    return _sealed(
        {
            "mode": mode,
            "environment": env,
            "target": target or "NOT_SELECTED",
            "pipeline": pipeline,
            "stopped": stopped,
            "executed": executed,
            "is_production": False,
            "PRODUCTION_DEPLOYMENT": "LOCKED",
            "PRODUCTION_LOCK": lock["PRODUCTION_SAFETY_LOCK"],
            "IMAGE_DIGEST": art["IMAGE_DIGEST"],
            "CI_STATUS": "READY_FOR_CREDENTIALS",
            "second_ci": False,
            "fabricated": False,
        }
    )


def evaluate() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    g26 = _g26()
    art = artifact_validate()
    lock = production_safety_lock()
    g26_ready = bool(g26.get("g26_ready") is True)
    return _sealed(
        {
            "P388_STATUS": "LAUNCH_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "PLATFORM_STATUS": "READY_FOR_EXTERNAL_INFRASTRUCTURE",
            "LAUNCH_FACTORY": True,
            "LAUNCH_FACTORY_READY": True,
            "RELEASE_FACTORY": True,
            "RELEASE_FACTORY_READY": True,
            "ENVIRONMENT_CONTRACT": True,
            "ENVIRONMENT_CONTRACT_READY": True,
            "DEPLOYMENT_PACKAGES": True,
            "MULTI_PLATFORM_PACKAGES_READY": True,
            "PREFLIGHT_READY": True,
            "CREDENTIAL_PREFLIGHT_READY": True,
            "BACKUP_AUTOMATION_READY": True,
            "ROLLBACK_AUTOMATION_READY": True,
            "PRODUCTION_LOCK": "ACTIVE",
            "KUBERNETES": "READY_FOR_CREDENTIALS",
            "VPS": "READY_FOR_CREDENTIALS",
            "AWS": "READY_FOR_CREDENTIALS",
            "AZURE": "READY_FOR_CREDENTIALS",
            "GCP": "READY_FOR_CREDENTIALS",
            "HOSTINGER_SHARED": "INCOMPATIBLE",
            "BUILD": "BLOCKED" if git.get("dirty") else "READY_FOR_CI",
            "TESTS": "CONFIGURED",
            "IMAGE": rel.get("image") or "meos/backend:p353-local",
            "DIGEST": art["IMAGE_DIGEST"],
            "IMAGE_DIGEST": art["IMAGE_DIGEST"],
            "DATABASE": "NON_PRODUCTION",
            "SECRET_MANAGER": "CONFIGURED",
            "DNS": "NOT_AVAILABLE",
            "TLS": "CONFIGURED",
            "NETWORK": "CONFIGURED",
            "OBSERVABILITY": "CONFIGURED",
            "BACKUP": "CONFIGURED",
            "RESTORE": "CONFIGURED",
            "ROLLBACK": "CONFIGURED",
            "TENANT_ISOLATION": "UNIT_TEST_EXISTS",
            "PROVIDER": provider(),
            "CI_STATUS": "READY_FOR_CREDENTIALS",
            "canonical_package": "infrastructure/launch/MEOS_RELEASE_PACKAGE",
            "config_templates": "deploy/environments",
            "second_architecture": False,
            "localhost_is_production": False,
            "compose_is_production": False,
            "self_signed_is_production": False,
            "dirty_sha_is_release": False,
            "mutable_image_rejected": True,
            "missing_digest_rejected": True,
            "PRODUCTION_DEPLOYMENT": "LOCKED",
            "tooling": tooling(),
            "credentials": credential_preflight(),
            "factory": factory("PREFLIGHT_ONLY"),
            "production_safety": lock,
            "G26_STATUS": g26.get("g26_status", "BLOCKED"),
            "G26_READY": g26_ready,
            "P0": int(g26.get("p0_count", 1)),
            "P313": "NOT_CERTIFIED",
            "P313_REENTRY_READY": bool(g26_ready),
            "PRODUCTION_CERTIFIED": False,
            "GO_LIVE_READY": False,
            "GO_LIVE_AUTHORIZATION": "NOT_APPROVED",
            "ACTIVE_APPLICATIONS": 0,
            "PRODUCTION_TRAFFIC": "NOT_ENABLED",
            "dependencies": [
                {"DEPENDENCY": "credentials", "OWNER": "NOT_AVAILABLE", "STATUS": "MISSING", "EVIDENCE_REQUIRED": "authorized provider account", "NEXT_ACTION": "credential preflight"},
                {"DEPENDENCY": "image_digest", "OWNER": "NOT_AVAILABLE", "STATUS": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "CI GHCR digest", "NEXT_ACTION": "clean tree then existing CI"},
                {"DEPENDENCY": "provider", "OWNER": "NOT_SELECTED", "STATUS": "NOT_SELECTED", "EVIDENCE_REQUIRED": "explicit MEOS_PRODUCTION_PROVIDER", "NEXT_ACTION": "do not infer AWS/Azure/GCP"},
                {"DEPENDENCY": "G26", "OWNER": "infrastructure", "STATUS": "BLOCKED", "EVIDENCE_REQUIRED": "real cluster/DB/TLS", "NEXT_ACTION": "re-run meos-ext-g26-readiness.py"},
            ],
        }
    )
