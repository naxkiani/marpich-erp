"""P389 deployment control plane. No second engine. No fake G26 or deploy."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from meos_p373 import deploy as p373_deploy, local_database_rejected  # noqa: E402
from meos_p377 import deployment_plan  # noqa: E402
from meos_p382 import production_safety_lock  # noqa: E402
from meos_p385 import artifact_validate  # noqa: E402
from meos_p386 import promote as p386_promote  # noqa: E402
from meos_p387 import provider, tooling  # noqa: E402
from meos_p388 import (  # noqa: E402
    backup_manager,
    credential_preflight,
    factory,
    launch_checklist,
    rollback_factory,
    runtime_verify,
)
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
STATES = (
    "CREATED",
    "PREFLIGHT",
    "READY_TO_DEPLOY",
    "DEPLOYING",
    "DEPLOYED",
    "RUNTIME_VERIFY",
    "BACKUP_VERIFY",
    "ROLLBACK_VERIFY",
    "G26_VERIFY",
    "G26_READY",
    "P313_REENTRY_READY",
)
FAILURE_STATES = ("BLOCKED", "FAILED", "ROLLBACK_REQUIRED", "EXTERNAL_DEPENDENCY")
TARGETS = ("KUBERNETES", "VPS", "AWS", "AZURE", "GCP")
COMMANDS = (
    "status",
    "preflight",
    "plan",
    "build",
    "package",
    "promote",
    "deploy",
    "verify",
    "backup",
    "restore",
    "rollback",
    "g26",
    "audit",
)


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p389_g26", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.evaluate(repo_root())


def _sealed(payload: dict[str, Any]) -> dict[str, Any]:
    blob = json.dumps(payload, default=str)
    for marker in FORBIDDEN:
        if marker in blob:
            raise RuntimeError("secret marker leaked")
    return payload


def _op(status: str, evidence: str, source: str, blocker: str, next_action: str) -> dict[str, str]:
    return {
        "STATUS": status,
        "EVIDENCE": evidence,
        "SOURCE": source,
        "TIMESTAMP": "NOT_A_RUNTIME_CLOCK",
        "BLOCKER": blocker,
        "NEXT_ACTION": next_action,
    }


def error(code: str, category: str, evidence: str, blocker: str, next_action: str) -> dict[str, str]:
    return {
        "ERROR_CODE": code,
        "CATEGORY": category,
        "EVIDENCE": evidence,
        "BLOCKER": blocker,
        "NEXT_ACTION": next_action,
    }


def normalize_target(raw: str | None) -> str:
    key = (raw or "").strip().upper()
    if not key:
        return "NOT_SELECTED"
    if key in TARGETS:
        return key
    return "UNKNOWN"


def state_machine() -> dict[str, Any]:
    git = git_state()
    art = artifact_validate()
    lock = production_safety_lock()
    creds = credential_preflight()
    g26 = _g26()
    current = "CREATED"
    reason = "control_plane_initialized"
    if git.get("dirty") or not str(art["IMAGE_DIGEST"]).startswith("sha256:"):
        current = "EXTERNAL_DEPENDENCY"
        reason = "dirty_or_missing_digest"
    else:
        current = "PREFLIGHT"
        reason = "artifact_present"
        if any(creds.get(name) in {"MISSING", "INVALID"} for name in ("CLUSTER", "DATABASE", "SECRET_MANAGER")):
            current = "EXTERNAL_DEPENDENCY"
            reason = "credentials_or_database"
        elif g26.get("g26_ready") is True:
            current = "G26_READY"
            reason = "g26_independent"
        else:
            current = "BLOCKED"
            reason = "g26_not_pass"
    return _sealed(
        {
            "states": list(STATES),
            "failure_states": list(FAILURE_STATES),
            "current": current,
            "reason": reason,
            "skipped": False,
            "READY_TO_DEPLOY": False,
            "DEPLOYED": False,
            "G26_READY": bool(g26.get("g26_ready") is True),
            "PRODUCTION_LOCK": lock["PRODUCTION_SAFETY_LOCK"],
        }
    )


def control_plane() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    art = artifact_validate()
    g26 = _g26()
    return _sealed(
        {
            "release": _op("BLOCKED", "P354-RC-NOT_ELIGIBLE", "MEOS_RELEASE_MANIFEST.v1.yaml", "dirty_or_missing_digest", "clean tree then CI"),
            "environment": _op("NOT_SELECTED", "MEOS_ENVIRONMENT", "deploy/environments", "production_not_inferred", "explicit environment"),
            "target": _op(provider(), "P349", "MEOS_EXT_G26_PROVIDER_COMPATIBILITY.md", "NOT_SELECTED", "do not infer provider"),
            "provider": _op(provider(), "P349", "deploy/providers", "NOT_SELECTED", "explicit MEOS_PRODUCTION_PROVIDER"),
            "credentials": _op("MISSING", "credential_preflight", "scripts/meos-credential-preflight.py", "authorized account", "supply credentials"),
            "preflight": _op("EXTERNAL_DEPENDENCY", "exit_2", "scripts/meos-launch-preflight.py", "external_deps", "preflight after credentials"),
            "artifact": _op("BLOCKED", art["IMAGE_DIGEST"], "meos_p385.artifact_validate", "IMAGE_DIGEST", "existing CI"),
            "deployment": _op("LOCKED", "PRODUCTION_DEPLOYMENT", "scripts/meos-deploy.py", "G26+P313+GO-LIVE", "do not --deploy production"),
            "runtime": _op("LOCAL_VERIFIED", "not_production", "scripts/meos-runtime-verify.py", "no_production_runtime", "verify after deploy"),
            "database": _op("NON_PRODUCTION", "localhost_5433", "MEOS_DATABASE_DEPLOYMENT_CONTRACT.v1.yaml", "managed_postgres", "reject localhost"),
            "secrets": _op("CONFIGURED", "values_not_stored", "MEOS_SECRET_PROVIDER_CONTRACT.v1.yaml", "not_verified", "do not treat env flag as proof"),
            "network": _op("CONFIGURED", "postgres_public_forbidden", "MEOS_PRODUCTION_NETWORK_CONTRACT.v1.yaml", "no_public_postgres", "private DB egress"),
            "TLS": _op("CONFIGURED", "self_signed_non_production", "deploy/network/dns-tls.yaml", "public_ca", "public DNS+CA"),
            "observability": _op("CONFIGURED", "G23_FAIL", "G23", "not_production_verified", "do not upgrade from config"),
            "backup": _op("CONFIGURED", "LOCAL_ONLY", "scripts/meos-backup-manager.py", "no_production_backup", "real backup after infra"),
            "rollback": _op("CONFIGURED", "not_exercised", "scripts/meos-rollback.py", "G26-10", "exercise after first deploy"),
            "G26": _op(str(g26.get("g26_status", "BLOCKED")), "meos-ext-g26-readiness.py", "scripts/meos-ext-g26-readiness.py", "external_infra", "re-run unchanged"),
            "P313": _op("NOT_CERTIFIED", "not_started", "MEOS_P313_CERTIFICATION_REPORT.md", "G26_READY_FALSE", "do not start P313"),
            "GO-LIVE": _op("NOT_APPROVED", "zero_apps", "MEOS_GO_LIVE_CHECKLIST.md", "NOT_APPROVED", "do not approve"),
            "commit": git.get("source_commit"),
            "image": rel.get("image") or "meos/backend:p353-local",
            "digest": art["IMAGE_DIGEST"],
        }
    )


def dry_run(target: str | None = None, environment: str = "LOCAL") -> dict[str, Any]:
    plan = deployment_plan(target, environment)
    return _sealed(
        {
            "mode": "DRY_RUN",
            "inspect": True,
            "validate": True,
            "plan": plan,
            "executed": False,
            "deployed": False,
            "dns_changed": False,
            "secrets_changed": False,
            "database_changed": False,
            "applications_activated": False,
            "traffic_enabled": False,
            "is_production": False,
        }
    )


def deploy_command(*, confirm: bool = False, environment: str = "LOCAL", target: str | None = None) -> dict[str, Any]:
    if not confirm:
        return _sealed({**dry_run(target, environment), "DEPLOY": "NOT_REQUESTED", "hint": "pass --deploy to request; production still locked"})
    result = p373_deploy(target, confirm=True, environment=environment)
    result["PRODUCTION_DEPLOYMENT"] = "LOCKED"
    result["is_production"] = False
    return _sealed(result)


def audit_record(command: str, result: str) -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    art = artifact_validate()
    return _sealed(
        {
            "execution_id": "PLAN_ONLY",
            "release": "P354-RC-NOT_ELIGIBLE",
            "commit": git.get("source_commit"),
            "digest": art["IMAGE_DIGEST"],
            "target": "NOT_SELECTED",
            "environment": "LOCAL",
            "operator": "CONTROL_PLANE",
            "start_time": "NOT_EXECUTED",
            "end_time": "NOT_EXECUTED",
            "preflight": "EXTERNAL_DEPENDENCY",
            "deployment": "LOCKED",
            "runtime": "LOCAL_VERIFIED",
            "backup": "CONFIGURED",
            "rollback": "CONFIGURED",
            "G26": "BLOCKED",
            "result": result,
            "command": command,
            "secrets": "NOT_RECORDED",
            "image": rel.get("image") or "meos/backend:p353-local",
        }
    )


def dispatch(command: str, *, target: str | None = None, environment: str = "LOCAL", deploy: bool = False) -> dict[str, Any]:
    command = (command or "status").strip().lower()
    if command not in COMMANDS:
        return _sealed({"command": command, "error": error("E_UNKNOWN_COMMAND", "CONFIGURATION", command, "unknown_command", "use meos-control.py --help")})
    if command == "status":
        return evaluate()
    if command == "preflight":
        return _sealed({"command": command, "factory": factory("PREFLIGHT_ONLY", environment, target), "credentials": credential_preflight()})
    if command == "plan":
        return _sealed({"command": command, **dry_run(target, environment)})
    if command == "build":
        return _sealed({"command": command, "factory": factory("BUILD_ONLY", environment, target), "executed": False})
    if command == "package":
        return _sealed({"command": command, "factory": factory("PACKAGE_ONLY", environment, target)})
    if command == "promote":
        return _sealed({"command": command, "promote": p386_promote("DEVELOPMENT", "TEST"), "canonical": "scripts/meos-release-promote.py"})
    if command == "deploy":
        return _sealed({"command": command, "deploy": deploy_command(confirm=deploy, environment=environment, target=target)})
    if command == "verify":
        return _sealed({"command": command, "runtime": runtime_verify(environment)})
    if command == "backup":
        return _sealed({"command": command, "backup": backup_manager("CHECK")})
    if command == "restore":
        return _sealed({"command": command, "restore": backup_manager("RESTORE_TEST"), "PRODUCTION_RESTORE": False})
    if command == "rollback":
        return _sealed({"command": command, "rollback": rollback_factory()})
    if command == "g26":
        g26 = _g26()
        return _sealed({"command": command, "G26_READY": bool(g26.get("g26_ready") is True), "G26_STATUS": g26.get("g26_status", "BLOCKED"), "p0_count": g26.get("p0_count", 1)})
    return _sealed({"command": command, "audit": audit_record(command, "PLAN_ONLY")})


def evaluate() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    g26 = _g26()
    art = artifact_validate()
    lock = production_safety_lock()
    machine = state_machine()
    g26_ready = bool(g26.get("g26_ready") is True)
    return _sealed(
        {
            "P389_STATUS": "CONTROL_PLANE_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "DEPLOYMENT_CONTROL_PLANE": "READY",
            "STATE_MACHINE": "READY",
            "RELEASE_PROMOTION": "READY",
            "DEPLOYMENT_PLAN": "READY",
            "DRY_RUN": "READY",
            "RUNTIME_VERIFICATION": "READY",
            "BACKUP_GATE": "READY",
            "ROLLBACK_GATE": "READY",
            "AUDIT_LOGGING": "READY",
            "PRODUCTION_LOCK": "ACTIVE",
            "PRODUCTION_DEPLOYMENT_LOCKED": True,
            "KUBERNETES": "READY_FOR_CREDENTIALS",
            "VPS": "READY_FOR_CREDENTIALS",
            "AWS": "READY_FOR_CREDENTIALS",
            "AZURE": "READY_FOR_CREDENTIALS",
            "GCP": "READY_FOR_CREDENTIALS",
            "HOSTINGER_SHARED": "INCOMPATIBLE",
            "RELEASE": "P354-RC-NOT_ELIGIBLE",
            "COMMIT": git.get("source_commit"),
            "IMAGE": rel.get("image") or "meos/backend:p353-local",
            "DIGEST": art["IMAGE_DIGEST"],
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
            "TARGET_STATUS": "NOT_SELECTED" if provider() == "NOT_SELECTED" else provider(),
            "current_state": machine["current"],
            "state_machine": machine,
            "control_plane": control_plane(),
            "checklist": launch_checklist(),
            "tooling": tooling(),
            "credentials": credential_preflight(),
            "localhost_is_production": False,
            "compose_is_production": False,
            "self_signed_is_production": False,
            "dirty_sha_is_release": False,
            "mutable_image_rejected": True,
            "secret_flag_is_not_proof": True,
            "second_architecture": False,
            "canonical_promote": "scripts/meos-release-promote.py",
            "canonical_deploy": "scripts/meos-deploy.py",
            "canonical_launch": "scripts/meos-launch.py",
            "errors": [
                error("E_DIGEST_MISSING", "SECURITY", "IMAGE_DIGEST=NOT_AVAILABLE", "immutable_digest", "clean tree then existing CI"),
                error("E_CREDENTIALS_MISSING", "CREDENTIAL", "credential_preflight", "authorized account", "python3 scripts/meos-credential-preflight.py"),
                error("E_G26_BLOCKED", "GOVERNANCE", "G26_STATUS=BLOCKED", "external_infra", "python3 scripts/meos-ext-g26-readiness.py"),
            ],
            "dependencies": [
                {"DEPENDENCY": "credentials", "OWNER": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "authorized provider account", "NEXT_ACTION": "credential preflight"},
                {"DEPENDENCY": "image_digest", "OWNER": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "CI GHCR digest", "NEXT_ACTION": "clean tree then existing CI"},
                {"DEPENDENCY": "provider", "OWNER": "NOT_SELECTED", "EVIDENCE_REQUIRED": "explicit MEOS_PRODUCTION_PROVIDER", "NEXT_ACTION": "do not infer AWS/Azure/GCP"},
                {"DEPENDENCY": "G26", "OWNER": "infrastructure", "EVIDENCE_REQUIRED": "real cluster/DB/TLS", "NEXT_ACTION": "re-run meos-ext-g26-readiness.py"},
            ],
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
            "local_database_rejected": local_database_rejected(),
        }
    )
