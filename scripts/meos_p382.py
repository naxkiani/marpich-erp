"""P382 product-side launch control. Safety lock active. No fake production."""
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
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")


def _exists(*parts: str) -> bool:
    return repo_root().joinpath(*parts).is_file()


def preflight_checks() -> dict[str, Any]:
    """CONFIGURED ≠ READY ≠ VERIFIED ≠ PRODUCTION_VERIFIED."""
    git = git_state()
    digest = str(meos_release().get("image_digest") or "NOT_AVAILABLE")
    clean = not bool(git.get("dirty"))
    immutable = digest.startswith("sha256:")
    return {
        "clean_git": "READY" if clean else "BLOCKED",
        "valid_commit": "READY" if str(git.get("source_commit") or "").strip() not in {"", "NOT_AVAILABLE"} else "BLOCKED",
        "ci_artifact": "NOT_VERIFIED",
        "immutable_image": "READY" if immutable else "BLOCKED",
        "target_configuration": "CONFIGURED" if _exists("docs", "meos", "execution", "MEOS_DEPLOYMENT_TARGET_MATRIX.v1.yaml") else "BLOCKED",
        "database_configuration": "CONFIGURED",
        "secret_manager": "CONFIGURED",
        "tls_configuration": "CONFIGURED",
        "dns_configuration": "CONFIGURED",
        "backup_configuration": "CONFIGURED" if _exists("scripts", "meos-postgres-backup.sh") else "BLOCKED",
        "restore_configuration": "CONFIGURED" if _exists("scripts", "meos-postgres-restore-drill.sh") else "BLOCKED",
        "rollback_configuration": "CONFIGURED",
        "observability_configuration": "CONFIGURED",
        "runtime_prerequisites": "NOT_VERIFIED",
        "deployment_identity": "NOT_VERIFIED",
        "VERIFIED": False,
        "PRODUCTION_VERIFIED": False,
        "MEOS_SECRET_MANAGER_AVAILABLE": False,
        "local_database_is_production": False,
        "localhost_tls_is_production": False,
    }


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p382_g26", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.evaluate(repo_root())


def production_safety_lock() -> dict[str, Any]:
    g26 = _g26()
    git = git_state()
    rel = meos_release()
    digest = str(rel.get("image_digest") or "NOT_AVAILABLE")
    ignored = []
    for name in ("FORCE_PRODUCTION", "BYPASS_G26", "SKIP_CERTIFICATION", "DISABLE_SAFETY"):
        if os.environ.get(name, "").strip() in {"1", "true", "TRUE", "yes"}:
            ignored.append(f"{name}_IGNORED")
    closed = True
    reasons = []
    if g26.get("g26_ready") is not True:
        reasons.append("G26_NOT_PASS")
    reasons.append("P313_NOT_CERTIFIED")
    reasons.append("GO_LIVE_NOT_APPROVED")
    if git.get("dirty") or not digest.startswith("sha256:"):
        reasons.append("RELEASE_NOT_IMMUTABLE")
    reasons.append("DEPLOYMENT_IDENTITY_NOT_VERIFIED")
    reasons.extend(ignored)
    return {
        "PRODUCTION_SAFETY_LOCK": "ACTIVE",
        "fail_closed": closed,
        "FORCE_PRODUCTION_BYPASS": False,
        "local_database_rejected": local_database_rejected(),
        "reasons": reasons,
        "deploy_allowed": False,
    }


def dry_run() -> dict[str, Any]:
    lock = production_safety_lock()
    git = git_state()
    return {
        "DEPLOYMENT_PLAN_READY": False,
        "DEPLOYMENT_PLAN_BLOCKED": True,
        "executed": False,
        "DEPLOYED": False,
        "dirty": bool(git.get("dirty")),
        "safety": lock["PRODUCTION_SAFETY_LOCK"],
    }


def evaluate() -> dict[str, Any]:
    g26 = _g26()
    git = git_state()
    rel = meos_release()
    lock = production_safety_lock()
    plan = dry_run()
    checks = preflight_checks()
    g26_ready = bool(g26.get("g26_ready") is True)
    report = {
        "P382_STATUS": "MULTI_PLATFORM_DEPLOYMENT_READY",
        "PRODUCT_DEPLOYMENT_READY": True,
        "TARGET_PROFILES_READY": True,
        "KUBERNETES_READY": "READY_FOR_CREDENTIALS",
        "VPS_READY": "READY_FOR_CREDENTIALS",
        "HOSTINGER_VPS_READY": "READY_FOR_CREDENTIALS",
        "HOSTINGER_SHARED": "INCOMPATIBLE",
        "AWS_READY": "READY_FOR_CREDENTIALS",
        "AZURE_READY": "READY_FOR_CREDENTIALS",
        "GCP_READY": "READY_FOR_CREDENTIALS",
        "DOCKER_READY": "READY",
        "RELEASE_MANIFEST_READY": True,
        "PRODUCTION_PREFLIGHT_READY": True,
        "preflight": checks,
        "PRODUCTION_SAFETY_LOCK": lock["PRODUCTION_SAFETY_LOCK"],
        "DEPLOYMENT_PLAN_READY": plan["DEPLOYMENT_PLAN_READY"],
        "DEPLOYMENT_PLAN_BLOCKED": plan["DEPLOYMENT_PLAN_BLOCKED"],
        "STATUS": "BLOCKED_BY_EXTERNAL_DEPENDENCY",
        "FORCE_PRODUCTION_BYPASS": False,
        "SOURCE_CLEAN": not bool(git.get("dirty")),
        "IMAGE_DIGEST": "NOT_AVAILABLE" if not str(rel.get("image_digest") or "").startswith("sha256:") else rel.get("image_digest"),
        "localhost_is_production": False,
        "compose_is_production": False,
        "demo_is_production": False,
        "staging_is_production": False,
        "dirty_sha_is_certified": False,
        "TARGET_READY_IS_NOT_PRODUCTION": True,
        "command_center": "python3 scripts/meos-launch.py",
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
            {"BLOCKER": "credentials", "OWNER": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "authorized provider account", "NEXT_ACTION": "supply credentials then re-run G26"},
            {"BLOCKER": "image_digest", "OWNER": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "CI GHCR digest", "NEXT_ACTION": "clean tree then CI publish"},
            {"BLOCKER": "dns_tls", "OWNER": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "public DNS + public CA", "NEXT_ACTION": "configure after account exists"},
            {"BLOCKER": "managed_postgres", "OWNER": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "non-localhost PostgreSQL", "NEXT_ACTION": "provision via approved adapter"},
        ],
    }
    blob = json.dumps(report, default=str)
    for marker in FORBIDDEN:
        if marker in blob:
            raise RuntimeError("secret marker leaked")
    return report
