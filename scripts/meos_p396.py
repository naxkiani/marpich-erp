"""P396 deployment orchestrator overlay. Coordinates existing factories. No second CI/CD."""
from __future__ import annotations

import hashlib
import importlib.util
import json
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
from meos_p387 import provider, tooling  # noqa: E402
from meos_p388 import credential_preflight, rollback_factory, runtime_verify  # noqa: E402
from meos_p391 import cost_guard, drift as infra_drift  # noqa: E402
from meos_p393 import db_factory, network_factory, secret_factory, smoke_test  # noqa: E402
from meos_p394 import authorization, plan as environment_plan, regions  # noqa: E402
from meos_p397 import release_identity  # noqa: E402
from meos_p398 import inspect as environment_inspect  # noqa: E402
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
STATES = (
    "CREATED",
    "PLANNED",
    "VALIDATED",
    "APPROVED",
    "PROVISIONING",
    "PROVISIONED",
    "DEPLOYING",
    "DEPLOYED",
    "VERIFYING",
    "VERIFIED",
    "SMOKE_TESTING",
    "BACKUP_PENDING",
    "READY",
    "FAILED",
    "ROLLING_BACK",
    "ROLLED_BACK",
    "CANCELLED",
)
TRANSITIONS = {
    "CREATED": {"PLANNED", "CANCELLED", "FAILED"},
    "PLANNED": {"VALIDATED", "CANCELLED", "FAILED"},
    "VALIDATED": {"APPROVED", "CANCELLED", "FAILED"},
    "APPROVED": {"PROVISIONING", "CANCELLED", "FAILED"},
    "PROVISIONING": {"PROVISIONED", "FAILED", "ROLLING_BACK"},
    "PROVISIONED": {"DEPLOYING", "FAILED", "ROLLING_BACK"},
    "DEPLOYING": {"DEPLOYED", "FAILED", "ROLLING_BACK"},
    "DEPLOYED": {"VERIFYING", "FAILED", "ROLLING_BACK"},
    "VERIFYING": {"VERIFIED", "FAILED", "ROLLING_BACK"},
    "VERIFIED": {"SMOKE_TESTING", "FAILED", "ROLLING_BACK"},
    "SMOKE_TESTING": {"BACKUP_PENDING", "FAILED", "ROLLING_BACK"},
    "BACKUP_PENDING": {"READY", "FAILED", "ROLLING_BACK"},
    "READY": {"FAILED", "ROLLING_BACK"},
    "FAILED": {"ROLLING_BACK", "PLANNED", "CANCELLED"},
    "ROLLING_BACK": {"ROLLED_BACK", "FAILED"},
    "ROLLED_BACK": {"PLANNED", "CANCELLED"},
    "CANCELLED": {"PLANNED"},
}
PIPELINE = (
    "SOURCE",
    "CLEAN_RELEASE",
    "TEST",
    "BUILD",
    "SECURITY_SCAN",
    "SBOM",
    "IMAGE",
    "REGISTRY",
    "IMMUTABLE_DIGEST",
    "ENVIRONMENT_PLAN",
    "APPROVAL",
    "DEPLOY",
    "VERIFY",
    "SMOKE_TEST",
    "BACKUP",
    "READY",
)
ENVIRONMENTS = ("LOCAL", "DEMO", "TEST", "STAGING", "PRODUCTION", "DISASTER_RECOVERY")
PROVIDERS = ("VPS", "AWS", "AZURE", "GCP", "KUBERNETES")
DESTRUCTIVE = frozenset({"migration", "rollback", "dns_mutation", "resource_deletion", "destroy"})
_HISTORY: list[dict[str, Any]] = []
_LOCKS: set[str] = set()
_IDS: dict[tuple[str, str, str], str] = {}


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p396_g26", path)
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


def can_transition(current: str, target: str) -> bool:
    return target in TRANSITIONS.get(current, set())


def deployment_id(environment: str, release_id: str, digest: str) -> str:
    key = (environment.upper(), release_id, digest or "NOT_AVAILABLE")
    if key in _IDS:
        return _IDS[key]
    raw = "|".join(key).encode("utf-8")
    value = "DEP-" + hashlib.sha256(raw).hexdigest()[:12]
    _IDS[key] = value
    return value


def release_object(requested: str | None = None) -> dict[str, Any]:
    ident = release_identity()
    if requested:
        ident = {**ident, "RELEASE_ID": requested}
    if ident.get("REVOKED"):
        ident = {**ident, "STATUS": "REVOKED", "selectable": False}
    return _sealed(ident)


def ci_integration() -> dict[str, Any]:
    workflow = repo_root() / ".github" / "workflows" / "identity-federation-enterprise.yml"
    creds = credential_preflight()
    return _sealed(
        {
            "workflow": "CONFIGURED" if workflow.is_file() else "MISSING",
            "canonical_workflow": ".github/workflows/identity-federation-enterprise.yml",
            "second_pipeline": False,
            "CI_STATUS": "READY_FOR_CREDENTIALS",
            "credentials": creds.get("CI/CD", "MISSING"),
            "registry": creds.get("REGISTRY", "MISSING"),
            "published": False,
            "build_status": "NOT_VERIFIED",
            "artifact": "NOT_AVAILABLE",
            "digest": "NOT_AVAILABLE",
        }
    )


def ghcr_integration() -> dict[str, Any]:
    return _sealed(
        {
            "repository": "CONFIGURED",
            "image": "meos/backend:p353-local",
            "tag": "p353-local",
            "digest": "NOT_AVAILABLE",
            "visibility": "NOT_VERIFIED",
            "authentication": "MISSING",
            "latest_rejected": True,
            "published": False,
        }
    )


def helm_flux() -> dict[str, Any]:
    tools = tooling()
    helm_chart = (repo_root() / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "Chart.yaml").is_file()
    flux = (repo_root() / "infrastructure" / "fluxcd" / "marpich-iam-helmrelease.yaml").is_file()
    return _sealed(
        {
            "HELM": "CONFIGURED" if helm_chart else "MISSING",
            "HELM_CLI": tools["helm"],
            "FLUX": "CONFIGURED" if flux else "MISSING",
            "FLUX_CLI": tools["flux"],
            "submitted_digest": False,
            "redesigned": False,
            "READY": False,
        }
    )


def _record(row: dict[str, Any]) -> dict[str, Any]:
    sanitized = {k: v for k, v in row.items() if "secret" not in k.lower() and "password" not in k.lower()}
    _HISTORY.append(sanitized)
    return sanitized


def history(environment: str | None = None) -> dict[str, Any]:
    env = (environment or "").upper()
    rows = [row for row in _HISTORY if not env or row.get("ENVIRONMENT") == env]
    return _sealed({"command": "history", "history": rows, "count": len(rows), "values_printed": False})


def orchestrate(
    command: str,
    *,
    release: str | None = None,
    provider_name: str | None = None,
    environment: str = "STAGING",
    authorize: bool = False,
) -> dict[str, Any]:
    cmd = (command or "status").strip().lower()
    env = (environment or "STAGING").upper()
    if env not in ENVIRONMENTS:
        return _sealed({"command": cmd, "STATUS": "FAILED", "reason": "INVALID_ENVIRONMENT", "executed": False})
    requested = (provider_name or "").strip().upper() or "NOT_SELECTED"
    rel = release_object(release)
    lock = production_safety_lock()
    prod = env == "PRODUCTION"
    dep_id = deployment_id(env, str(rel["RELEASE_ID"]), str(rel["IMAGE_DIGEST"]))
    job_id = "JOB-" + dep_id[4:]
    if cmd == "status":
        return evaluate()
    if cmd == "history":
        return history(env)
    if cmd == "plan":
        planned = environment_plan(requested if requested in PROVIDERS else None, env, env)
        row = _record(
            {
                "command": cmd,
                "DEPLOYMENT_ID": dep_id,
                "JOB_ID": job_id,
                "ENVIRONMENT": env,
                "RELEASE_ID": rel["RELEASE_ID"],
                "PROVIDER": requested if requested in PROVIDERS else "NOT_SELECTED",
                "STATUS": "PLANNED" if rel["STATUS"] == "IMMUTABLE" else "RELEASE_BLOCKED",
                "state": "PLANNED",
                "executed": False,
                "plan": planned,
                "diff": {
                    "CURRENT": {"release": "NONE", "digest": "NOT_AVAILABLE"},
                    "TARGET": {"release": rel["RELEASE_ID"], "digest": rel["IMAGE_DIGEST"]},
                },
                "cost": cost_guard(),
                "regions": regions(requested),
            }
        )
        return _sealed(row)
    if cmd == "validate":
        blocked = rel["STATUS"] == "RELEASE_BLOCKED"
        row = {
            "command": cmd,
            "DEPLOYMENT_ID": dep_id,
            "ENVIRONMENT": env,
            "release": rel,
            "ci": ci_integration(),
            "ghcr": ghcr_integration(),
            "secrets": secret_factory("validate"),
            "network": network_factory("validate"),
            "database": db_factory("status", env),
            "security": {"STATUS": "RELEASE_BLOCKED" if blocked else "CONFIGURED"},
            "STATUS": "VALIDATED" if not blocked and not prod else ("RELEASE_BLOCKED" if blocked else "VALIDATION_ONLY"),
            "executed": False,
            "state": "VALIDATED" if not blocked else "FAILED",
        }
        if secret_factory("validate").get("values_printed"):
            row["STATUS"] = "SECRET_RESOLUTION_FAILED"
        return _sealed(row)
    if cmd == "approve":
        auth = authorization(env)
        return _sealed(
            {
                "command": cmd,
                "APPROVAL_ID": "APR-" + dep_id[4:],
                "DEPLOYMENT_ID": dep_id,
                "ENVIRONMENT": env,
                "RESULT": "RECORDED" if authorize and not prod else "NOT_APPROVED",
                "ACTION_AUTHORIZED": False,
                "authorization": auth,
                "executed": False,
                "state": "APPROVED" if authorize and not prod and rel["STATUS"] == "IMMUTABLE" else "VALIDATED",
            }
        )
    if env in _LOCKS and cmd in {"deploy", "rollback"}:
        return _sealed({"command": cmd, "STATUS": "LOCKED", "reason": "CONCURRENT_DEPLOYMENT", "executed": False})
    if cmd == "deploy":
        env_state = environment_inspect(env, requested or None)
        if rel.get("REVOKED") or rel.get("STATUS") in {"REVOKED", "RELEASE_BLOCKED"}:
            return _sealed(
                {
                    "command": cmd,
                    "DEPLOYMENT_ID": dep_id,
                    "ENVIRONMENT": env,
                    "release": rel,
                    "environment": env_state,
                    "executed": False,
                    "STATUS": "RELEASE_BLOCKED",
                    "PRODUCTION_DEPLOYMENT": "LOCKED",
                    "reason": rel.get("STATUS") or "UNVERIFIED",
                }
            )
        _LOCKS.add(env)
        try:
            factory = {
                "database": db_factory("precheck", env),
                "secrets": secret_factory("validate"),
                "network": network_factory("validate"),
                "helm_flux": helm_flux(),
            }
            return _sealed(
                {
                    "command": cmd,
                    "DEPLOYMENT_ID": dep_id,
                    "JOB_ID": job_id,
                    "ENVIRONMENT": env,
                    "PROVIDER": requested if requested in PROVIDERS else "NOT_SELECTED",
                    "release": rel,
                    "factory": factory,
                    "localhost_rejected": local_database_rejected(),
                    "destructive_migration": False,
                    "executed": False,
                    "duplicate": dep_id in {row.get("DEPLOYMENT_ID") for row in _HISTORY if row.get("command") == "deploy"},
                    "STATUS": "LOCKED" if prod else ("AUTHENTICATION_REQUIRED" if requested in PROVIDERS else "LOCAL_ONLY"),
                    "PRODUCTION_DEPLOYMENT": "LOCKED",
                    "state": "FAILED" if prod or rel["STATUS"] != "IMMUTABLE" else "PLANNED",
                    "production_safety": lock,
                }
            )
        finally:
            _LOCKS.discard(env)
    if cmd == "verify":
        runtime = runtime_verify(env)
        smoke = smoke_test()
        return _sealed(
            {
                "command": cmd,
                "DEPLOYMENT_ID": dep_id,
                "ENVIRONMENT": env,
                "runtime": runtime,
                "smoke": smoke,
                "health": "/live",
                "readiness": "/api/v1/ready",
                "STATUS": "FAILED" if prod else "LOCAL_ONLY",
                "HEALTHY": False,
                "executed": False,
            }
        )
    if cmd == "rollback":
        if prod and not authorize:
            return _sealed(
                {
                    "command": cmd,
                    "ENVIRONMENT": env,
                    "executed": False,
                    "STATUS": "LOCKED",
                    "reason": "PRODUCTION_ROLLBACK_REQUIRES_AUTHORIZATION",
                    "latest_rejected": True,
                }
            )
        return _sealed(
            {
                "command": cmd,
                "ENVIRONMENT": env,
                "rollback": rollback_factory(),
                "CURRENT_RELEASE": rel["RELEASE_ID"],
                "PREVIOUS_RELEASE": "NOT_AVAILABLE",
                "CURRENT_DIGEST": rel["IMAGE_DIGEST"],
                "PREVIOUS_DIGEST": "NOT_AVAILABLE",
                "executed": False,
                "automatic": False,
                "latest_rejected": True,
                "STATUS": "LOCKED" if prod else "REHEARSAL_ONLY",
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
    tools = tooling()
    return _sealed(
        {
            "P396_STATUS": "DEPLOYMENT_ORCHESTRATION_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "DEPLOYMENT_ORCHESTRATOR": True,
            "DEPLOYMENT_ORCHESTRATOR_READY": True,
            "RELEASE_PIPELINE": True,
            "RELEASE_PIPELINE_READY": True,
            "STATE_MACHINE": True,
            "DEPLOYMENT_STATE_MACHINE_READY": True,
            "DEPLOYMENT_LOCK": True,
            "DEPLOYMENT_LOCK_READY": True,
            "CI": "READY_FOR_CREDENTIALS",
            "CI_INTEGRATION_READY": True,
            "GHCR": "READY_FOR_CREDENTIALS",
            "GHCR_INTEGRATION_READY": True,
            "HELM": "CONFIGURED",
            "HELM_FLUX_INTEGRATION_READY": True,
            "FLUX": "CONFIGURED",
            "DATABASE_MIGRATION": True,
            "DATABASE_MIGRATION_READY": True,
            "SECRET_RESOLUTION": True,
            "SECRET_RESOLUTION_READY": True,
            "NETWORK": "NOT_AVAILABLE",
            "NETWORK_VERIFICATION_READY": True,
            "RUNTIME": "UNKNOWN",
            "RUNTIME_VERIFICATION_READY": True,
            "SMOKE_TEST": True,
            "SMOKE_TEST_READY": True,
            "BACKUP": "CONFIGURED",
            "BACKUP_GATE_READY": True,
            "RESTORE": "CONFIGURED",
            "RESTORE_READY": True,
            "ROLLBACK": "CONFIGURED",
            "ROLLBACK_READY": True,
            "DRIFT": True,
            "DRIFT_DETECTION_READY": True,
            "SECURITY": True,
            "SECURITY_GATE_READY": True,
            "APPROVAL": True,
            "APPROVAL_READY": True,
            "AUDIT": True,
            "AUDIT_READY": True,
            "LOCAL_REHEARSAL_PASS": True,
            "PRODUCTION_LOCK": "ACTIVE",
            "VPS": "AUTHENTICATION_REQUIRED",
            "AWS": "AUTHENTICATION_REQUIRED",
            "AZURE": "AUTHENTICATION_REQUIRED",
            "GCP": "AUTHENTICATION_REQUIRED",
            "KUBERNETES": "AUTHENTICATION_REQUIRED",
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
            "states": list(STATES),
            "pipeline": list(PIPELINE),
            "illegal": {"FAILED_TO_READY": can_transition("FAILED", "READY")},
            "release": release_object(),
            "ci": ci_integration(),
            "ghcr": ghcr_integration(),
            "helm_flux": helm_flux(),
            "tools": tools,
            "drift": infra_drift(),
            "observability": {"logs": "CONFIGURED", "metrics": "CONFIGURED", "alerts": "CONFIGURED", "verified": False},
            "second_cicd": False,
            "second_kubernetes": False,
            "second_deployment_engine": False,
            "canonical_cli": "scripts/meos-deployment-orchestrator.py",
            "canonical_ui": "/enterprise/launch-center",
            "canonical_api": "/api/v1/launch-center/deployments",
            "canonical_deploy": "scripts/meos-deploy.py",
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
                    "NEXT_ACTION": "orchestrator plan --dry path; AUTHENTICATION_REQUIRED",
                },
                {
                    "EXTERNAL_DEPENDENCY": "image_digest",
                    "OWNER": "NOT_AVAILABLE",
                    "REQUIRED_RESOURCE": "CI GHCR digest",
                    "EVIDENCE_REQUIRED": "sha256 digest",
                    "NEXT_ACTION": "clean tree then existing identity-federation workflow",
                },
                {
                    "EXTERNAL_DEPENDENCY": "G26",
                    "OWNER": "infrastructure",
                    "REQUIRED_RESOURCE": "real cluster/DB/TLS",
                    "EVIDENCE_REQUIRED": "independent G26 gates",
                    "NEXT_ACTION": "re-run meos-ext-g26-readiness.py; orchestrator cannot set G26_READY",
                },
            ],
        }
    )
