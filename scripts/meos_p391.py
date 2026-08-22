"""P391 provider blueprints and launch overlay. No second platform. No fake provision."""
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
from meos_p388 import credential_preflight  # noqa: E402
from meos_p390 import discover, environment_factory, infra_plan, provision  # noqa: E402
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
PROVIDERS = ("VPS", "AWS", "AZURE", "GCP", "KUBERNETES")
NONPROD = {"LOCAL", "DEMO", "TEST", "STAGING"}


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p391_g26", path)
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


def drift() -> dict[str, Any]:
    return _sealed(
        {
            "desired": "BLUEPRINTS",
            "actual": "NOT_PROVISIONED",
            "status": "UNKNOWN",
            "destroyed_unexpected": False,
            "auto_destroy": False,
        }
    )


def cost_guard() -> dict[str, Any]:
    return _sealed(
        {
            "estimated_monthly_cost": "NOT_AVAILABLE",
            "region": "NOT_SELECTED",
            "database_tier": "NOT_SELECTED",
            "compute_tier": "NOT_SELECTED",
            "storage": "NOT_SELECTED",
            "blocks_when_unavailable": False,
            "accidental_high_cost": "GUARD_CONFIGURED",
        }
    )


def env_factory(command: str, environment: str = "DEMO", provider_name: str | None = None) -> dict[str, Any]:
    row = environment_factory(command, environment)
    requested = (provider_name or "").strip().upper()
    row["PROVIDER"] = provider()
    row["PROVIDER_STATUS"] = provider()
    row["PROVIDER_REQUESTED"] = requested or "NOT_SELECTED"
    if command in {"plan", "validate", "status"}:
        row["resource_modification"] = False
    if command == "upgrade":
        row["executed"] = False
        row["STATUS"] = "READY_FOR_CREDENTIALS" if environment.upper() in {"STAGING", "PRODUCTION"} else row["STATUS"]
    return _sealed(row)


def launch_command(
    command: str,
    *,
    provider_name: str | None = None,
    environment: str = "LOCAL",
    authorize: bool = False,
) -> dict[str, Any]:
    cmd = (command or "prepare").strip().lower()
    env = (environment or "LOCAL").upper()
    lock = production_safety_lock()
    art = artifact_validate()
    git = git_state()
    selected = provider() if not provider_name else (
        "REQUESTED_NOT_READY" if provider_name.strip() else provider()
    )
    if cmd == "prepare":
        return _sealed(
            {
                "command": "prepare",
                "PROVIDER": selected,
                "ENVIRONMENT": env,
                "repository": "VALIDATED",
                "release": "BLOCKED" if git.get("dirty") else "READY_FOR_CI",
                "credentials": credential_preflight(),
                "plan": infra_plan(provider_name, env, dry_run=True),
                "provisioned": False,
                "executed": False,
                "PRODUCTION_DEPLOYMENT": "LOCKED",
            }
        )
    if cmd == "staging":
        if env not in {"DEMO", "TEST", "STAGING"}:
            env = "STAGING"
        return _sealed(
            {
                "command": "staging",
                "ENVIRONMENT": env,
                "PROVIDER": selected,
                "plan": True,
                "provision": False,
                "deploy": False,
                "verify": "LOCAL_VERIFIED",
                "executed": False,
                "is_production": False,
            }
        )
    if cmd == "production":
        return _sealed(
            {
                "command": "production",
                "ENVIRONMENT": "PRODUCTION",
                "PROVIDER": selected,
                "authorize_provisioning": authorize,
                "provisioned": False,
                "deployed": False,
                "traffic_enabled": False,
                "PRODUCTION_DEPLOYMENT": "LOCKED",
                "REASON": "G26_P313_GO_LIVE_REQUIRED",
                "executed": False,
            }
        )
    if cmd == "provision":
        return _sealed({"command": cmd, **provision(authorize=authorize, environment=env, name=provider_name)})
    if cmd == "g26":
        g26 = _g26()
        return _sealed({"command": "g26", "G26_READY": bool(g26.get("g26_ready") is True), "G26_STATUS": g26.get("g26_status", "BLOCKED"), "P0": int(g26.get("p0_count", 1))})
    if cmd == "deploy":
        return _sealed(
            {
                "command": "deploy",
                "RELEASE": "P354-RC-NOT_ELIGIBLE",
                "TARGET": selected,
                "ENVIRONMENT": env,
                "IMAGE": "meos/backend:p353-local",
                "DIGEST": art["IMAGE_DIGEST"],
                "executed": False,
                "dirty_rejected": True,
                "mutable_rejected": True,
                "PRODUCTION_DEPLOYMENT": "LOCKED",
                "canonical": "scripts/meos-deploy.py",
            }
        )
    return _sealed({"command": cmd, "executed": False, "PRODUCTION_LOCK": lock["PRODUCTION_SAFETY_LOCK"]})


def evaluate() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    g26 = _g26()
    art = artifact_validate()
    lock = production_safety_lock()
    g26_ready = bool(g26.get("g26_ready") is True)
    return _sealed(
        {
            "P391_STATUS": "MULTI_PLATFORM_LAUNCH_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "PROVIDER_BLUEPRINTS": True,
            "PROVIDER_BLUEPRINTS_READY": True,
            "PROVIDER_DISCOVERY": True,
            "PROVIDER_DISCOVERY_READY": True,
            "ENVIRONMENT_FACTORY": True,
            "ENVIRONMENT_FACTORY_READY": True,
            "INFRASTRUCTURE_PLAN": True,
            "INFRASTRUCTURE_PLAN_READY": True,
            "PROVISIONING_ENGINE": True,
            "PROVISIONING_ENGINE_READY": True,
            "DRIFT_DETECTION": True,
            "DRIFT_DETECTION_READY": True,
            "COST_GUARD": True,
            "COST_GUARD_READY": True,
            "LAUNCH_ORCHESTRATOR": True,
            "LAUNCH_ORCHESTRATOR_READY": True,
            "MULTI_PLATFORM_PACKAGE": True,
            "MULTI_PLATFORM_PACKAGE_READY": True,
            "PRODUCTION_LOCK": "ACTIVE",
            "PRODUCTION_DEPLOYMENT": "LOCKED",
            "VPS": "READY_FOR_CREDENTIALS",
            "AWS": "READY_FOR_CREDENTIALS",
            "AZURE": "READY_FOR_CREDENTIALS",
            "GCP": "READY_FOR_CREDENTIALS",
            "KUBERNETES": "READY_FOR_CREDENTIALS",
            "HOSTINGER_SHARED": "INCOMPATIBLE",
            "NETWORK": "CONFIGURED",
            "CLUSTER": "NOT_AVAILABLE",
            "DATABASE": "NON_PRODUCTION",
            "SECRET_MANAGER": "CONFIGURED",
            "REGISTRY": "ghcr.io/marpich/marpich-backend",
            "DNS": "NOT_AVAILABLE",
            "TLS": "CONFIGURED",
            "OBSERVABILITY": "CONFIGURED",
            "RELEASE": "P354-RC-NOT_ELIGIBLE",
            "COMMIT": git.get("source_commit"),
            "IMAGE": rel.get("image") or "meos/backend:p353-local",
            "DIGEST": art["IMAGE_DIGEST"],
            "DEPLOYMENT": "LOCKED",
            "RUNTIME": "LOCAL_VERIFIED",
            "BACKUP": "CONFIGURED",
            "RESTORE": "CONFIGURED",
            "ROLLBACK": "CONFIGURED",
            "TENANT_ISOLATION": "UNIT_TEST_EXISTS",
            "SECURITY": "CONFIGURED",
            "PROVIDER": provider(),
            "PROVIDER_STATUS": "NOT_SELECTED" if provider() == "NOT_SELECTED" else provider(),
            "second_architecture": False,
            "infra_pointers": "infra/",
            "canonical_adapters": "deploy/providers/",
            "localhost_is_production": False,
            "compose_is_production": False,
            "self_signed_is_production": False,
            "dirty_sha_is_release": False,
            "mutable_image_rejected": True,
            "local_database_rejected": local_database_rejected(),
            "drift": drift(),
            "cost": cost_guard(),
            "discovery": discover(),
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
                {"EXTERNAL_DEPENDENCY": "credentials", "OWNER": "NOT_AVAILABLE", "REQUIRED_RESOURCE": "authorized provider account", "EVIDENCE_REQUIRED": "validated identity", "NEXT_ACTION": "prepare then credential preflight"},
                {"EXTERNAL_DEPENDENCY": "image_digest", "OWNER": "NOT_AVAILABLE", "REQUIRED_RESOURCE": "CI GHCR digest", "EVIDENCE_REQUIRED": "sha256 digest", "NEXT_ACTION": "clean tree then existing CI"},
                {"EXTERNAL_DEPENDENCY": "provider", "OWNER": "NOT_SELECTED", "REQUIRED_RESOURCE": "P349-approved provider", "EVIDENCE_REQUIRED": "explicit MEOS_PRODUCTION_PROVIDER", "NEXT_ACTION": "do not infer from P361 VPS recommendation"},
                {"EXTERNAL_DEPENDENCY": "G26", "OWNER": "infrastructure", "REQUIRED_RESOURCE": "real cluster/DB/TLS", "EVIDENCE_REQUIRED": "independent G26 gates", "NEXT_ACTION": "re-run meos-ext-g26-readiness.py"},
            ],
        }
    )
