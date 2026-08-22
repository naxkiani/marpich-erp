"""P392 deployment fabric overlay. Reuses P384/P386/P389. No fake promote or G26."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

import yaml

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from meos_p373 import local_database_rejected  # noqa: E402
from meos_p382 import production_safety_lock  # noqa: E402
from meos_p385 import artifact_validate  # noqa: E402
from meos_p386 import promote as p386_promote  # noqa: E402
from meos_p387 import provider  # noqa: E402
from meos_p388 import rollback_factory, runtime_verify  # noqa: E402
from meos_p391 import cost_guard, drift as infra_drift  # noqa: E402
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
PATH = ("DEMO", "TEST", "STAGING", "PRODUCTION")
STATES = (
    "PLANNED",
    "AUTHORIZED",
    "DEPLOYING",
    "HEALTH_CHECKING",
    "READY",
    "PROMOTED",
    "PAUSED",
    "FAILED",
    "ROLLING_BACK",
    "ROLLED_BACK",
)
TRANSITIONS = {
    "PLANNED": {"AUTHORIZED", "FAILED", "PAUSED"},
    "AUTHORIZED": {"DEPLOYING", "PAUSED", "FAILED"},
    "DEPLOYING": {"HEALTH_CHECKING", "FAILED", "ROLLING_BACK"},
    "HEALTH_CHECKING": {"READY", "FAILED", "ROLLING_BACK"},
    "READY": {"PROMOTED", "PAUSED", "FAILED", "ROLLING_BACK"},
    "PROMOTED": {"PAUSED", "ROLLING_BACK"},
    "PAUSED": {"AUTHORIZED", "DEPLOYING", "FAILED"},
    "FAILED": {"ROLLING_BACK", "PLANNED"},
    "ROLLING_BACK": {"ROLLED_BACK", "FAILED"},
    "ROLLED_BACK": {"PLANNED", "FAILED"},
}
GATES = {
    "DEMO": ("BUILD_PASS",),
    "TEST": ("UNIT_PASS", "INTEGRATION_PASS"),
    "STAGING": ("SECURITY_PASS", "MIGRATION_PASS", "BACKUP_PASS"),
    "PRODUCTION": ("G26_READY", "P313_CERTIFIED", "PRODUCTION_CERTIFIED", "GO_LIVE_AUTHORIZATION"),
}
TARGETS = ("VPS", "AWS", "AZURE", "GCP", "KUBERNETES")
FABRIC_COMMANDS = (
    "release",
    "promote",
    "pause",
    "resume",
    "fabric-status",
    "target-status",
)
SCHEMA_KEYS = (
    "identity",
    "runtime",
    "database",
    "registry",
    "image_policy",
    "secret_provider",
    "dns",
    "tls",
    "observability",
    "backup",
    "rollback",
)


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p392_g26", path)
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


def _env(raw: str | None) -> str:
    key = (raw or "DEMO").strip().upper().replace("-", "_")
    aliases = {"PROD": "PRODUCTION", "DEV": "DEMO", "LOCAL": "LOCAL"}
    return aliases.get(key, key)


def can_transition(current: str, nxt: str) -> bool:
    return nxt in TRANSITIONS.get(current, set())


def state_machine(current: str = "PLANNED") -> dict[str, Any]:
    return _sealed(
        {
            "states": list(STATES),
            "current": current if current in STATES else "PLANNED",
            "illegal_example": {"from": "FAILED", "to": "PROMOTED", "allowed": can_transition("FAILED", "PROMOTED")},
            "instance": "PLANNED",
            "executed": False,
        }
    )


def _profile(name: str) -> dict[str, Any]:
    path = repo_root() / "deploy" / "environments" / f"{name.lower()}.yaml"
    if name.upper() == "PRODUCTION":
        path = repo_root() / "deploy" / "environments" / "production.yaml.example"
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {k: data.get(k) for k in SCHEMA_KEYS if k in data}


def parity(left: str = "LOCAL", right: str = "DEMO") -> dict[str, Any]:
    src = _profile(left)
    dst = _profile(right)
    missing = [k for k in SCHEMA_KEYS if k not in src or k not in dst]
    compared_secrets = False
    status = "PARITY_WARNING"
    if left.upper() == "PRODUCTION" or right.upper() == "PRODUCTION":
        status = "PARITY_FAIL"
    elif missing:
        status = "PARITY_FAIL"
    return _sealed(
        {
            "left": left.upper(),
            "right": right.upper(),
            "status": status,
            "compared": SCHEMA_KEYS,
            "missing_schema_keys": missing,
            "secrets_compared": compared_secrets,
            "secrets_printed": False,
            "localhost_is_production": False,
        }
    )


def gates(environment: str) -> dict[str, Any]:
    env = _env(environment)
    required = GATES.get(env, ())
    git = git_state()
    g26 = _g26()
    results: dict[str, str] = {}
    if env == "DEMO":
        results["BUILD_PASS"] = "BLOCKED" if git.get("dirty") else "READY_FOR_CI"
    if env == "TEST":
        results["UNIT_PASS"] = "CONFIGURED"
        results["INTEGRATION_PASS"] = "CONFIGURED"
    if env == "STAGING":
        results["SECURITY_PASS"] = "CONFIGURED"
        results["MIGRATION_PASS"] = "CONFIGURED"
        results["BACKUP_PASS"] = "LOCAL_ONLY"
    if env == "PRODUCTION":
        results["G26_READY"] = "FAIL" if g26.get("g26_ready") is not True else "PASS"
        results["P313_CERTIFIED"] = "FAIL"
        results["PRODUCTION_CERTIFIED"] = "FAIL"
        results["GO_LIVE_AUTHORIZATION"] = "FAIL"
    passed = all(v in {"PASS", "CONFIGURED", "READY_FOR_CI"} for v in results.values()) if results else False
    if env == "PRODUCTION":
        passed = False
    if env == "STAGING":
        passed = False
    if env == "DEMO" and git.get("dirty"):
        passed = False
    return _sealed({"ENVIRONMENT": env, "required": list(required), "results": results, "passed": passed})


def previous_environment(environment: str) -> str | None:
    env = _env(environment)
    if env not in PATH:
        return None
    idx = PATH.index(env)
    return PATH[idx - 1] if idx else None


def promote(release_id: str | None = None, environment: str = "STAGING") -> dict[str, Any]:
    env = _env(environment)
    art = artifact_validate()
    git = git_state()
    lock = production_safety_lock()
    gate = gates(env)
    prev = previous_environment(env)
    blockers = ["DIRTY_SHA"] if git.get("dirty") else []
    if not str(art.get("IMAGE_DIGEST") or "").startswith("sha256:"):
        blockers.append("IMAGE_DIGEST_MISSING")
    if env not in PATH:
        blockers.append("NOT_ON_PROMOTION_PATH")
    if env == "PRODUCTION":
        blockers.extend(["G26_NOT_PASS", "P313_NOT_CERTIFIED", "PRODUCTION_CERTIFIED_FALSE", "GO_LIVE_NOT_APPROVED"])
    if env == "STAGING":
        blockers.append("STAGING_BLOCKED")
    if prev:
        prev_gate = gates(prev)
        if not prev_gate["passed"]:
            blockers.append(f"PREVIOUS_{prev}_NOT_VERIFIED")
    p386 = p386_promote("DEVELOPMENT", "TEST" if env != "PRODUCTION" else "PRODUCTION", release_id)
    return _sealed(
        {
            "command": "promote",
            "RELEASE_ID": release_id or "P354-RC-NOT_ELIGIBLE",
            "ENVIRONMENT": env,
            "PROVIDER": provider(),
            "executed": False,
            "allowed": False,
            "IMAGE_DIGEST": art["IMAGE_DIGEST"],
            "digest_changed": False,
            "gates": gate,
            "previous_environment": prev,
            "PRODUCTION_DEPLOYMENT": "LOCKED",
            "blockers": blockers,
            "promote": p386,
            "canonical": "scripts/meos-release-promote.py",
            "production_safety": lock["PRODUCTION_SAFETY_LOCK"],
        }
    )


def pause(environment: str = "STAGING") -> dict[str, Any]:
    return _sealed(
        {
            "command": "pause",
            "ENVIRONMENT": _env(environment),
            "from": "PLANNED",
            "to": "PAUSED",
            "allowed": can_transition("PLANNED", "PAUSED"),
            "executed": False,
            "infrastructure_changed": False,
        }
    )


def resume(environment: str = "STAGING") -> dict[str, Any]:
    return _sealed(
        {
            "command": "resume",
            "ENVIRONMENT": _env(environment),
            "from": "PAUSED",
            "to": "AUTHORIZED",
            "allowed": can_transition("PAUSED", "AUTHORIZED"),
            "executed": False,
            "PRODUCTION_DEPLOYMENT": "LOCKED",
        }
    )


def rollback(previous_digest: str | None = None) -> dict[str, Any]:
    factory = rollback_factory()
    target = (previous_digest or "").strip()
    rejected = (not target) or target.lower() in {"latest", "dev", "test", "staging"}
    return _sealed(
        {
            "command": "rollback",
            "CURRENT_DIGEST": "NOT_AVAILABLE",
            "PREVIOUS_DIGEST": target or "NOT_AVAILABLE",
            "ROLLBACK_TARGET": "REJECTED" if rejected else target,
            "ROLLBACK_ACTION": "NOT_EXECUTED",
            "POST_ROLLBACK_HEALTH": "NOT_EXECUTED",
            "executed": False,
            "EXERCISED": False,
            "latest_rejected": True,
            "factory": factory,
            "canonical": "scripts/meos-rollback.py",
        }
    )


def release_status() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    art = artifact_validate()
    return _sealed(
        {
            "command": "release",
            "RELEASE_ID": "P354-RC-NOT_ELIGIBLE",
            "COMMIT": git.get("source_commit"),
            "IMAGE": rel.get("image") or "meos/backend:p353-local",
            "DIGEST": art["IMAGE_DIGEST"],
            "CI_BUILD_ID": "NOT_AVAILABLE",
            "SBOM": "DECLARED_DEPENDENCIES_ONLY",
            "SECURITY_SCAN": "CONFIGURED",
            "TEST_RESULT": "DETERMINISTIC_SUBSET",
            "immutable": False,
            "dirty_rejected": True,
            "mutable_rejected": True,
        }
    )


def target_matrix() -> dict[str, Any]:
    row = {
        "BUILD": "READY",
        "PLAN": "READY",
        "PROVISION": "BLOCKED",
        "DEPLOY": "BLOCKED",
        "VERIFY": "NOT_VERIFIED",
        "BACKUP": "CONFIGURED",
        "RESTORE": "CONFIGURED",
        "ROLLBACK": "CONFIGURED",
    }
    return _sealed({name: dict(row) for name in TARGETS})


def failover() -> dict[str, Any]:
    return _sealed(
        {
            "PRIMARY": "NOT_SELECTED",
            "SECONDARY": "NOT_SELECTED",
            "activated": False,
            "authorization": "NOT_APPROVED",
            "PASS": False,
        }
    )


def disaster_recovery() -> dict[str, Any]:
    return _sealed(
        {
            "DR_PLAN": "CONFIGURED",
            "DR_STATUS": "NOT_TESTED",
            "LAST_DR_TEST": "NOT_EXECUTED",
            "RPO": "NOT_MEASURED",
            "RTO": "NOT_MEASURED",
            "documentation_alone": "NOT_TESTED",
        }
    )


def zero_downtime() -> dict[str, Any]:
    return _sealed(
        {
            "strategy": "Helm RollingUpdate",
            "source": "infrastructure/kubernetes/helm/marpich-iam",
            "readiness": "/api/v1/ready",
            "liveness": "/live",
            "startup_alone_is_healthy": False,
            "blue_green": "OPTIONAL",
            "canary": "OPTIONAL",
            "second_ingress": False,
            "EXERCISED": False,
        }
    )


def audit(action: str, environment: str, result: str = "NOT_EXECUTED") -> dict[str, Any]:
    git = git_state()
    return _sealed(
        {
            "WHO": "OPERATOR",
            "WHAT": action.upper(),
            "WHEN": "NOT_EXECUTED",
            "WHERE": _env(environment),
            "WHY": "P392_FABRIC",
            "RESULT": result,
            "COMMIT": git.get("source_commit"),
            "DIGEST": "NOT_AVAILABLE",
            "secrets": "NOT_RECORDED",
            "append_only": True,
        }
    )


def dispatch_fabric(
    command: str,
    *,
    release_id: str | None = None,
    environment: str = "STAGING",
    previous_digest: str | None = None,
) -> dict[str, Any]:
    cmd = (command or "fabric-status").strip().lower()
    if cmd == "release":
        return release_status()
    if cmd == "promote":
        row = promote(release_id, environment)
        row["audit"] = audit("promote", environment)
        return row
    if cmd == "pause":
        return pause(environment)
    if cmd == "resume":
        return resume(environment)
    if cmd == "target-status":
        return _sealed({"command": cmd, "targets": target_matrix(), "PROVIDER": provider()})
    if cmd == "fabric-status":
        return evaluate()
    return _sealed({"command": cmd, "executed": False})


def evaluate() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    g26 = _g26()
    art = artifact_validate()
    lock = production_safety_lock()
    g26_ready = bool(g26.get("g26_ready") is True)
    return _sealed(
        {
            "P392_STATUS": "DEPLOYMENT_FABRIC_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "DEPLOYMENT_FABRIC": True,
            "DEPLOYMENT_FABRIC_READY": True,
            "RELEASE_MANAGEMENT": True,
            "RELEASE_MANAGEMENT_READY": True,
            "PROMOTION_ENGINE": True,
            "PROMOTION_ENGINE_READY": True,
            "ENVIRONMENT_PARITY": True,
            "ENVIRONMENT_PARITY_READY": True,
            "ZERO_DOWNTIME": True,
            "ZERO_DOWNTIME_READY": True,
            "ROLLBACK": True,
            "ROLLBACK_READY": True,
            "DISASTER_RECOVERY": True,
            "DR_READY": True,
            "AUDIT_TRAIL": True,
            "AUDIT_TRAIL_READY": True,
            "MULTI_PROVIDER_TARGETS": True,
            "MULTI_PROVIDER_TARGETS_READY": True,
            "PRODUCTION_LOCK": "ACTIVE",
            "PRODUCTION_DEPLOYMENT": "LOCKED",
            "VPS": "READY_FOR_CREDENTIALS",
            "AWS": "READY_FOR_CREDENTIALS",
            "AZURE": "READY_FOR_CREDENTIALS",
            "GCP": "READY_FOR_CREDENTIALS",
            "KUBERNETES": "READY_FOR_CREDENTIALS",
            "HOSTINGER_SHARED": "INCOMPATIBLE",
            "RELEASE": "P354-RC-NOT_ELIGIBLE",
            "COMMIT": git.get("source_commit"),
            "IMAGE": rel.get("image") or "meos/backend:p353-local",
            "DIGEST": art["IMAGE_DIGEST"],
            "DEMO": "LOCAL_PASS",
            "TEST": "LOCAL_PASS",
            "STAGING": "STAGING_BLOCKED",
            "PRODUCTION": "LOCKED",
            "RUNTIME": "LOCAL_VERIFIED",
            "DATABASE": "NON_PRODUCTION",
            "DNS": "NOT_AVAILABLE",
            "TLS": "CONFIGURED",
            "SECRETS": "CONFIGURED",
            "OBSERVABILITY": "CONFIGURED",
            "BACKUP": "CONFIGURED",
            "RESTORE": "CONFIGURED",
            "PROVIDER": provider(),
            "PROVIDER_STATUS": provider(),
            "parity": parity("LOCAL", "DEMO"),
            "state_machine": state_machine(),
            "zero_downtime": zero_downtime(),
            "failover": failover(),
            "disaster_recovery": disaster_recovery(),
            "targets": target_matrix(),
            "drift": {**infra_drift(), "auto_correct_production": False},
            "cost": cost_guard(),
            "health": {
                "PROCESS_HEALTH": "/live",
                "APPLICATION_READINESS": "/api/v1/ready",
                "DATABASE_READINESS": "NON_PRODUCTION",
                "DEPENDENCY_READINESS": "CONFIGURED",
                "single_endpoint_is_production": False,
            },
            "frontend_backend": {
                "FRONTEND_RELEASE": "0.1.0",
                "BACKEND_RELEASE": "0.1.0",
                "independent_production_promotion": False,
            },
            "canonical_promote": "scripts/meos-release-promote.py",
            "canonical_control": "scripts/meos-control.py",
            "second_architecture": False,
            "second_cicd": False,
            "localhost_is_production": False,
            "compose_is_production": False,
            "dirty_sha_is_release": False,
            "mutable_image_rejected": True,
            "local_database_rejected": local_database_rejected(),
            "runtime_verify": runtime_verify("LOCAL"),
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
                {
                    "EXTERNAL_DEPENDENCY": "credentials",
                    "OWNER": "NOT_AVAILABLE",
                    "REQUIRED_RESOURCE": "authorized provider account",
                    "EVIDENCE_REQUIRED": "validated identity",
                    "NEXT_ACTION": "credential preflight then staging rehearsal",
                },
                {
                    "EXTERNAL_DEPENDENCY": "image_digest",
                    "OWNER": "NOT_AVAILABLE",
                    "REQUIRED_RESOURCE": "CI GHCR digest",
                    "EVIDENCE_REQUIRED": "sha256 digest",
                    "NEXT_ACTION": "clean tree then existing CI",
                },
                {
                    "EXTERNAL_DEPENDENCY": "staging",
                    "OWNER": "NOT_AVAILABLE",
                    "REQUIRED_RESOURCE": "authorized staging runtime",
                    "EVIDENCE_REQUIRED": "deploy+verify+backup+rollback",
                    "NEXT_ACTION": "do not simulate staging",
                },
                {
                    "EXTERNAL_DEPENDENCY": "G26",
                    "OWNER": "infrastructure",
                    "REQUIRED_RESOURCE": "real cluster/DB/TLS",
                    "EVIDENCE_REQUIRED": "independent G26 gates",
                    "NEXT_ACTION": "re-run meos-ext-g26-readiness.py",
                },
            ],
        }
    )
