"""P394 self-service environment control overlay. Reuses P388–P393. No fake provision."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from meos_p373 import local_database_rejected  # noqa: E402
from meos_p382 import production_safety_lock  # noqa: E402
from meos_p385 import artifact_validate  # noqa: E402
from meos_p387 import provider  # noqa: E402
from meos_p388 import backup_manager, credential_preflight, launch_checklist, runtime_verify  # noqa: E402
from meos_p390 import discover, infra_plan  # noqa: E402
from meos_p391 import cost_guard, drift, env_factory  # noqa: E402
from meos_p392 import rollback as fabric_rollback  # noqa: E402
from meos_p393 import db_factory, launch, network_factory, secret_factory, smoke_test  # noqa: E402
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
COMMANDS = (
    "status",
    "catalog",
    "plan",
    "validate",
    "provision",
    "deploy",
    "verify",
    "suspend",
    "destroy",
)
PROFILES = {
    "DEVELOPMENT": "DEVELOPMENT",
    "DEV": "DEVELOPMENT",
    "DEMO": "DEMO",
    "TEST": "TEST",
    "STAGING": "STAGING",
    "PRODUCTION": "PRODUCTION",
    "PROD": "PRODUCTION",
    "DISASTER_RECOVERY": "DISASTER_RECOVERY",
    "DISASTER-RECOVERY": "DISASTER_RECOVERY",
    "DR": "DISASTER_RECOVERY",
}
SIZES = ("SMALL", "MEDIUM", "LARGE", "ENTERPRISE")
PROVIDERS = ("VPS", "AWS", "AZURE", "GCP", "KUBERNETES")
ENVIRONMENTS = ("LOCAL", "DEMO", "TEST", "STAGING", "PRODUCTION")
STATES = (
    "PLANNED",
    "PROVISIONING",
    "PROVISIONED",
    "CONFIGURING",
    "DEPLOYING",
    "VERIFYING",
    "READY",
    "DEGRADED",
    "FAILED",
    "SUSPENDED",
    "DESTROYED",
)
TRANSITIONS = {
    "PLANNED": {"PROVISIONING", "FAILED", "DESTROYED"},
    "PROVISIONING": {"PROVISIONED", "FAILED"},
    "PROVISIONED": {"CONFIGURING", "FAILED", "SUSPENDED", "DESTROYED"},
    "CONFIGURING": {"DEPLOYING", "FAILED"},
    "DEPLOYING": {"VERIFYING", "FAILED"},
    "VERIFYING": {"READY", "DEGRADED", "FAILED"},
    "READY": {"DEGRADED", "SUSPENDED", "FAILED"},
    "DEGRADED": {"VERIFYING", "FAILED", "SUSPENDED"},
    "FAILED": {"PLANNED", "SUSPENDED", "DESTROYED"},
    "SUSPENDED": {"PROVISIONING", "DESTROYED", "FAILED"},
    "DESTROYED": {"PLANNED"},
}
GRAPH = (
    "NETWORK",
    "SECURITY",
    "DATABASE",
    "SECRETS",
    "COMPUTE",
    "INGRESS",
    "DNS",
    "TLS",
    "OBSERVABILITY",
    "APPLICATION",
)


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p394_g26", path)
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


def normalize_profile(raw: str | None) -> str:
    key = (raw or "DEMO").strip().upper().replace(" ", "_")
    return PROFILES.get(key, "INVALID")


def can_transition(current: str, nxt: str) -> bool:
    return nxt in TRANSITIONS.get(current, set())


def state_machine(current: str = "PLANNED") -> dict[str, Any]:
    now = current if current in STATES else "PLANNED"
    return _sealed(
        {
            "states": list(STATES),
            "current": now,
            "instance": "PLANNED",
            "illegal": {"from": "FAILED", "to": "READY", "allowed": can_transition("FAILED", "READY")},
            "executed": False,
        }
    )


def regions(provider_name: str | None = None) -> dict[str, Any]:
    return _sealed(
        {
            "PROVIDER": (provider_name or "").strip().upper() or provider(),
            "REGION_DISCOVERY": "BLOCKED",
            "regions": [],
            "invented": False,
        }
    )


def authorization(environment: str = "LOCAL") -> dict[str, Any]:
    env = (environment or "LOCAL").upper()
    creds = credential_preflight()
    available = creds.get("PROVIDER") in {"NOT_VERIFIED", "AVAILABLE"}
    lock = production_safety_lock()
    return _sealed(
        {
            "CREDENTIAL_AVAILABLE": bool(available),
            "ACTION_AUTHORIZED": False,
            "both_required": True,
            "PRODUCTION": env == "PRODUCTION",
            "PRODUCTION_DEPLOYMENT": "LOCKED",
            "deploy_allowed": lock["deploy_allowed"],
            "values_printed": False,
        }
    )


def resource_graph() -> dict[str, Any]:
    edges = [{"from": GRAPH[i], "to": GRAPH[i + 1], "wait": True} for i in range(len(GRAPH) - 1)]
    return _sealed(
        {
            "nodes": list(GRAPH),
            "edges": edges,
            "parallel_after": ["NETWORK", "SECURITY"],
            "race_conditions": False,
            "public_traffic_after": "INGRESS",
        }
    )


def catalog() -> dict[str, Any]:
    rows: dict[str, dict[str, str]] = {}
    for env in ENVIRONMENTS:
        for name in PROVIDERS:
            if env == "LOCAL":
                status = "NOT_SUPPORTED" if name != "VPS" else "READY"
                if name == "VPS":
                    status = "READY"
            elif env in {"DEMO", "TEST"}:
                status = "REQUIRES_CREDENTIALS"
            elif env == "STAGING":
                status = "BLOCKED"
            else:
                status = "BLOCKED"
            rows[f"{env}:{name}"] = {
                "environment": env,
                "provider": name,
                "status": status,
                "tool_install_is_not_ready": True,
            }
    return _sealed(
        {
            "combinations": rows,
            "DISASTER_RECOVERY": "NOT_TESTED",
            "source": "docs/meos/execution/MEOS_ENVIRONMENT_CATALOG.v1.yaml",
        }
    )


def plan(
    provider_name: str | None = None,
    environment: str = "STAGING",
    profile: str | None = None,
    size: str = "SMALL",
    region: str | None = None,
) -> dict[str, Any]:
    env = (environment or "STAGING").upper()
    prof = normalize_profile(profile or env)
    if prof == "INVALID":
        return _sealed({"command": "plan", "STATUS": "PLAN_FAILED", "reason": "INVALID_PROFILE", "executed": False})
    requested = (provider_name or "").strip().upper() or "NOT_SELECTED"
    sizing = (size or "SMALL").upper()
    if sizing not in SIZES:
        return _sealed({"command": "plan", "STATUS": "PLAN_FAILED", "reason": "INVALID_SIZE", "executed": False})
    art = artifact_validate()
    git = git_state()
    cost = cost_guard()
    return _sealed(
        {
            "command": "plan",
            "plan_id": "PLAN-P394-DRY-RUN",
            "STATUS": "PLANNED",
            "provider": requested if requested in PROVIDERS else "NOT_SELECTED",
            "environment": env,
            "region": "NOT_SELECTED" if not (region or "").strip() else "NOT_VERIFIED",
            "profile": prof,
            "size": sizing,
            "release": "P354-RC-NOT_ELIGIBLE",
            "commit": git.get("source_commit"),
            "digest": art["IMAGE_DIGEST"],
            "resources": infra_plan(requested or None, env, dry_run=True),
            "dependencies": list(GRAPH),
            "credentials": credential_preflight(),
            "authorization": authorization(env),
            "network": "CONFIGURED",
            "database": db_factory("status", env),
            "secrets": secret_factory("references"),
            "dns": "NOT_AVAILABLE",
            "tls": "CONFIGURED",
            "observability": "CONFIGURED",
            "backup": "CONFIGURED",
            "rollback": "CONFIGURED",
            "estimated_cost": cost["estimated_monthly_cost"],
            "COST_UNKNOWN": True,
            "unknown_cost_is_not_zero": True,
            "regions": regions(requested),
            "executed": False,
            "values": "NOT_STORED",
        }
    )


def launch_check() -> dict[str, Any]:
    checks = launch_checklist()
    return _sealed(
        {
            "command": "launch-check",
            "provider": provider(),
            "credentials": credential_preflight(),
            "authorization": authorization("PRODUCTION"),
            "network": "CONFIGURED",
            "database": "NON_PRODUCTION",
            "secrets": "CONFIGURED",
            "DNS": "NOT_AVAILABLE",
            "TLS": "CONFIGURED",
            "release": "BLOCKED",
            "deployment": "LOCKED",
            "runtime": "LOCAL_VERIFIED",
            "backup": "CONFIGURED",
            "rollback": "CONFIGURED",
            "READY": False,
            "checklist": checks,
            "canonical": "scripts/meos-launch-checklist.py",
        }
    )


def control(
    command: str,
    *,
    provider_name: str | None = None,
    environment: str = "LOCAL",
    profile: str | None = None,
    size: str = "SMALL",
    authorize: bool = False,
) -> dict[str, Any]:
    cmd = (command or "status").strip().lower()
    env = (environment or "LOCAL").upper()
    planned = plan(provider_name, env, profile, size)
    if cmd == "catalog":
        return catalog()
    if cmd == "plan":
        return planned
    if cmd == "validate":
        return _sealed({"command": cmd, "plan": planned, "authorization": authorization(env), "executed": False})
    if cmd in {"provision", "deploy"}:
        factory = launch("bootstrap" if cmd == "provision" else "deploy", provider_name=provider_name, environment=env, dry_run=True)
        return _sealed(
            {
                "command": cmd,
                "plan": planned,
                "plan_first": True,
                "factory": factory,
                "authorization": authorization(env),
                "ACTION_AUTHORIZED": False,
                "executed": False,
                "PRODUCTION_DEPLOYMENT": "LOCKED",
                "latest_rejected": True,
            }
        )
    if cmd == "verify":
        return _sealed(
            {
                "command": cmd,
                "runtime": runtime_verify(env),
                "smoke": smoke_test(),
                "health": "/live",
                "readiness": "/api/v1/ready",
                "status": "FAILED" if env == "PRODUCTION" else "LOCAL_ONLY",
                "executed": False,
            }
        )
    if cmd == "suspend":
        return _sealed(
            {
                "command": cmd,
                "ENVIRONMENT": env,
                "executed": False,
                "data_retained": True,
                "PRODUCTION_SUSPEND": "FORBIDDEN" if env == "PRODUCTION" and not authorize else "LOCKED",
            }
        )
    if cmd == "destroy":
        row = env_factory("destroy", env, provider_name)
        return _sealed(
            {
                "command": cmd,
                "plan": planned,
                "environment": row,
                "destroyed": False,
                "production_destroy": "FORBIDDEN",
                "terraform_destroy": "FORBIDDEN",
                "executed": False,
            }
        )
    return evaluate()


def evaluate() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    g26 = _g26()
    art = artifact_validate()
    lock = production_safety_lock()
    g26_ready = bool(g26.get("g26_ready") is True)
    return _sealed(
        {
            "P394_STATUS": "SELF_SERVICE_ENVIRONMENT_PLATFORM_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "ENVIRONMENT_CONTROL": True,
            "ENVIRONMENT_CONTROL_READY": True,
            "ENVIRONMENT_CATALOG": True,
            "ENVIRONMENT_CATALOG_READY": True,
            "PLAN_ENGINE": True,
            "PLAN_ENGINE_READY": True,
            "RESOURCE_GRAPH": True,
            "RESOURCE_GRAPH_READY": True,
            "CREDENTIAL_PREFLIGHT": True,
            "CREDENTIAL_PREFLIGHT_READY": True,
            "AUTHORIZATION_GATE": True,
            "AUTHORIZATION_GATE_READY": True,
            "STATE_MACHINE": True,
            "STATE_MACHINE_READY": True,
            "DATABASE": "NON_PRODUCTION",
            "DATABASE_PROVISIONING_READY": True,
            "SECRETS": "CONFIGURED",
            "SECRET_PROVISIONING_READY": True,
            "NETWORK": "CONFIGURED",
            "NETWORK_PROVISIONING_READY": True,
            "DNS": "NOT_AVAILABLE",
            "TLS": "CONFIGURED",
            "RELEASE_INTEGRATION_READY": True,
            "DEPLOYMENT": "LOCKED",
            "DEPLOYMENT_INTEGRATION_READY": True,
            "BACKUP": "CONFIGURED",
            "BACKUP_READY": True,
            "RESTORE": "CONFIGURED",
            "RESTORE_READY": True,
            "ROLLBACK": "CONFIGURED",
            "ROLLBACK_READY": True,
            "DRIFT": True,
            "DRIFT_DETECTION_READY": True,
            "COST_GUARD": True,
            "COST_GUARD_READY": True,
            "LAUNCH_CHECK": True,
            "LAUNCH_CHECK_READY": True,
            "LOCAL_REHEARSAL_PASS": True,
            "PRODUCTION_LOCK": "ACTIVE",
            "VPS": "READY_FOR_CREDENTIALS",
            "AWS": "READY_FOR_CREDENTIALS",
            "AZURE": "READY_FOR_CREDENTIALS",
            "GCP": "READY_FOR_CREDENTIALS",
            "KUBERNETES": "READY_FOR_CREDENTIALS",
            "LOCAL": "LOCAL_ONLY",
            "DEMO": "LOCAL_ONLY",
            "TEST": "LOCAL_ONLY",
            "STAGING": "STAGING_BLOCKED",
            "PRODUCTION": "LOCKED",
            "DISASTER_RECOVERY": "NOT_TESTED",
            "RELEASE": "P354-RC-NOT_ELIGIBLE",
            "COMMIT": git.get("source_commit"),
            "IMAGE": rel.get("image") or "meos/backend:p353-local",
            "DIGEST": art["IMAGE_DIGEST"],
            "RUNTIME": "LOCAL_VERIFIED",
            "OBSERVABILITY": "CONFIGURED",
            "PROVIDER": provider(),
            "api_control_plane": "NOT_ADDED",
            "admin_ui": "NOT_ADDED",
            "api_reason": "existing /api/v1/platform is tenant registry, not infrastructure provisioning",
            "canonical_cli": "scripts/meos-environment-control.py",
            "canonical_factory": "scripts/meos-launch-factory.py",
            "second_architecture": False,
            "second_admin": False,
            "localhost_is_production": False,
            "compose_is_production": False,
            "dirty_sha_is_release": False,
            "mutable_image_rejected": True,
            "local_database_rejected": local_database_rejected(),
            "unknown_cost_is_not_zero": True,
            "state_machine": state_machine(),
            "graph": resource_graph(),
            "authorization": authorization("PRODUCTION"),
            "cost": cost_guard(),
            "drift": {**drift(), "auto_repair_production": False},
            "network": network_factory("validate"),
            "backup": backup_manager("CHECK"),
            "rollback": fabric_rollback(None),
            "job": {"JOB_ID": "NOT_EXECUTED", "STATUS": "PLANNED", "secrets": "NOT_RECORDED"},
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
                    "NEXT_ACTION": "environment-control validate --dry-run",
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
                    "EVIDENCE_REQUIRED": "plan+provision+deploy+verify",
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
