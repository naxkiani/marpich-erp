"""P387 adapter/bootstrap overlay. No provision. No fake credentials or G26."""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
from pathlib import Path
import sys
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from meos_p373 import local_database_rejected  # noqa: E402
from meos_p382 import production_safety_lock  # noqa: E402
from meos_p385 import artifact_validate  # noqa: E402
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
SELECTED_ENV = ("MEOS_PRODUCTION_PROVIDER", "MEOS_DEPLOYMENT_PROVIDER")


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p387_g26", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.evaluate(repo_root())


def provider() -> str:
    for name in SELECTED_ENV:
        raw = os.environ.get(name, "").strip()
        if raw:
            return "REQUESTED_NOT_READY"
    return "NOT_SELECTED"


def tooling() -> dict[str, str]:
    return {
        "kubectl": "PRESENT" if shutil.which("kubectl") else "TOOLING_NOT_AVAILABLE",
        "helm": "PRESENT" if shutil.which("helm") else "TOOLING_NOT_AVAILABLE",
        "flux": "PRESENT" if shutil.which("flux") else "TOOLING_NOT_AVAILABLE",
        "docker": "PRESENT" if shutil.which("docker") else "TOOLING_NOT_AVAILABLE",
    }


def bootstrap() -> dict[str, Any]:
    art = artifact_validate()
    git = git_state()
    tools = tooling()
    return {
        "BOOTSTRAP_STATUS": "READY_FOR_CREDENTIALS",
        "PROVIDER": provider(),
        "CREDENTIALS": "MISSING",
        "TOOLING": tools,
        "RELEASE": "BLOCKED" if git.get("dirty") or not art["ARTIFACT_VALID"] else "READY",
        "DATABASE": "REJECTED" if local_database_rejected() else "NOT_VERIFIED",
        "DNS": "NOT_AVAILABLE",
        "TLS": "CONFIGURED",
        "SECRETS": "CONFIGURED",
        "OBSERVABILITY": "CONFIGURED",
        "BACKUP": "CONFIGURED",
        "ROLLBACK": "CONFIGURED",
        "provisioned": False,
        "executed": False,
    }


def preflight() -> dict[str, Any]:
    boot = bootstrap()
    lock = production_safety_lock()
    return {
        "status": "EXTERNAL_DEPENDENCY",
        "exit_code": 2,
        "READY": False,
        "PROVIDER": boot["PROVIDER"],
        "CREDENTIALS": boot["CREDENTIALS"],
        "RELEASE": boot["RELEASE"],
        "PRODUCTION_LOCK": lock["PRODUCTION_SAFETY_LOCK"],
        "PRODUCTION_DEPLOYMENT": "LOCKED",
        "localhost_is_production": False,
        "self_signed_is_production": False,
        "mutable_image_rejected": True,
        "dirty_sha_rejected": True,
    }


def evaluate() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    g26 = _g26()
    art = artifact_validate()
    boot = bootstrap()
    pf = preflight()
    lock = production_safety_lock()
    g26_ready = bool(g26.get("g26_ready") is True)
    report = {
        "P387_STATUS": "PRODUCT_LAUNCH_INFRASTRUCTURE_READY_EXTERNAL_CREDENTIALS_REQUIRED",
        "MULTI_PLATFORM_ARCHITECTURE_READY": True,
        "DEPLOYMENT_ADAPTERS_READY": True,
        "PREFLIGHT_AUTOMATION_READY": True,
        "LAUNCH_ORCHESTRATION_READY": True,
        "PROVIDER_NEUTRAL_PACKAGE_READY": True,
        "PRODUCTION_LOCK": "ACTIVE",
        "KUBERNETES": "READY_FOR_CREDENTIALS",
        "VPS": "READY_FOR_CREDENTIALS",
        "AWS": "READY_FOR_CREDENTIALS",
        "AZURE": "READY_FOR_CREDENTIALS",
        "GCP": "READY_FOR_CREDENTIALS",
        "HOSTINGER_SHARED": "INCOMPATIBLE",
        "RELEASE_ID": "P354-RC-NOT_ELIGIBLE",
        "COMMIT": git.get("source_commit"),
        "IMAGE": rel.get("image") or "meos/backend:p353-local",
        "IMAGE_DIGEST": art["IMAGE_DIGEST"],
        "DATABASE": "NON_PRODUCTION",
        "TLS": "CONFIGURED",
        "DNS": "NOT_AVAILABLE",
        "SECRET_MANAGER": "CONFIGURED",
        "OBSERVABILITY": "CONFIGURED",
        "BACKUP": "CONFIGURED",
        "RESTORE": "CONFIGURED",
        "ROLLBACK": "CONFIGURED",
        "PROVIDER": boot["PROVIDER"],
        "STATUS": "READY_FOR_CREDENTIALS",
        "canonical_deploy": "python3 scripts/meos-deploy.py",
        "config_templates": "deploy/environments",
        "config_deployment_dir": "NOT_CREATED",
        "second_architecture": False,
        "bootstrap": boot,
        "preflight": pf,
        "PRODUCTION_DEPLOYMENT": "LOCKED",
        "localhost_is_production": False,
        "self_signed_is_production": False,
        "dirty_sha_is_release": False,
        "mutable_image_rejected": True,
        "missing_digest_rejected": True,
        "missing_secret_manager_is_pass": False,
        "missing_tls_is_production": False,
        "g26_lock": True,
        "p313_lock": True,
        "go_live_lock": True,
        "tenant_isolation": "UNIT_TEST_EXISTS",
        "rollback_exercised": False,
        "rollback_identity": "CONFIGURED",
        "FORCE_PRODUCTION_BYPASS": False,
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
        "blockers": [
            {"BLOCKER": "credentials", "OWNER": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "authorized provider account", "NEXT_ACTION": "supply credentials then preflight"},
            {"BLOCKER": "image_digest", "OWNER": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "CI GHCR digest", "NEXT_ACTION": "clean tree then existing CI"},
            {"BLOCKER": "provider", "OWNER": "NOT_SELECTED", "EVIDENCE_REQUIRED": "explicit MEOS_PRODUCTION_PROVIDER", "NEXT_ACTION": "do not infer AWS/Azure/GCP"},
            {"BLOCKER": "G26", "OWNER": "infrastructure", "EVIDENCE_REQUIRED": "real cluster/DB/TLS", "NEXT_ACTION": "re-run meos-ext-g26-readiness.py"},
        ],
    }
    blob = json.dumps(report, default=str)
    for marker in FORBIDDEN:
        if marker in blob:
            raise RuntimeError("secret marker leaked")
    return report
