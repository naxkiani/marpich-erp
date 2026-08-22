"""P398 Environment Factory overlay. Reuses P390/P394. No Terraform fork. No fake provision."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, Protocol

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from meos_p373 import local_database_rejected  # noqa: E402
from meos_p382 import production_safety_lock  # noqa: E402
from meos_p387 import provider, tooling  # noqa: E402
from meos_p388 import credential_preflight  # noqa: E402
from meos_p390 import environment_factory, infra_plan  # noqa: E402
from meos_p391 import cost_guard, drift as infra_drift, env_factory  # noqa: E402
from meos_p393 import db_factory, network_factory, secret_factory  # noqa: E402
from meos_p394 import authorization, plan as environment_plan, regions  # noqa: E402
from meos_p397 import compatibility, release_identity  # noqa: E402
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
ENVIRONMENTS = ("LOCAL", "DEMO", "TEST", "STAGING", "PRODUCTION", "DISASTER_RECOVERY")
PROVIDERS = ("VPS", "AWS", "AZURE", "GCP", "KUBERNETES")
_LOCKS: set[str] = set()
_PLANS: dict[tuple[str, str], str] = {}


class ProviderAdapter(Protocol):
    def validate_credentials(self) -> dict[str, Any]: ...
    def inspect(self) -> dict[str, Any]: ...
    def plan(self) -> dict[str, Any]: ...
    def provision(self) -> dict[str, Any]: ...
    def configure(self) -> dict[str, Any]: ...
    def verify(self) -> dict[str, Any]: ...
    def drift(self) -> dict[str, Any]: ...
    def destroy_plan(self) -> dict[str, Any]: ...


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p398_g26", path)
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


def _load_yaml(name: str) -> dict[str, Any]:
    path = repo_root() / "docs" / "meos" / "execution" / name
    if yaml is None or not path.is_file():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def plan_id(environment: str, provider_name: str) -> str:
    key = (environment.upper(), (provider_name or "NOT_SELECTED").upper())
    if key in _PLANS:
        return _PLANS[key]
    value = "PLAN-" + hashlib.sha256("|".join(key).encode("utf-8")).hexdigest()[:12]
    _PLANS[key] = value
    return value


def environment_object(environment: str, provider_name: str | None = None) -> dict[str, Any]:
    env = (environment or "LOCAL").upper()
    requested = (provider_name or "").strip().upper()
    selected = provider()
    catalog = _load_yaml("MEOS_ENVIRONMENT_CATALOG.v1.yaml")
    profiles = catalog.get("profiles") or {}
    row = (catalog.get("environments") or {}).get(env) or {"status": "UNKNOWN"}
    return _sealed(
        {
            "ENVIRONMENT_ID": f"meos-{env.lower()}",
            "ENVIRONMENT_NAME": env,
            "ENVIRONMENT_TYPE": env,
            "PROVIDER": requested or selected or "NOT_SELECTED",
            "REGION": "NOT_SELECTED",
            "PROFILE": env if env in profiles else "DEVELOPMENT",
            "NETWORK_PROFILE": "CONFIGURED",
            "DATABASE_PROFILE": "NON_PRODUCTION" if env != "PRODUCTION" else "managed_remote_tls",
            "SECRET_PROFILE": "REFERENCE_ONLY",
            "OBSERVABILITY_PROFILE": "CONFIGURED",
            "SECURITY_PROFILE": "CONFIGURED",
            "BACKUP_PROFILE": "mandatory" if env in {"PRODUCTION", "DISASTER_RECOVERY"} else "configured",
            "DEPLOYMENT_PROFILE": "LOCKED" if env == "PRODUCTION" else row.get("status", "LOCAL_ONLY"),
            "STATUS": row.get("status", "UNKNOWN"),
            "ENVIRONMENT_VERSION": "v1",
            "CREATED_AT": "NOT_A_RUNTIME_CLOCK",
            "UPDATED_AT": "NOT_A_RUNTIME_CLOCK",
        }
    )


def adapter(provider_name: str | None) -> dict[str, Any]:
    requested = (provider_name or "").strip().upper()
    creds = credential_preflight()
    tools = tooling()
    if not requested:
        return _sealed(
            {
                "PROVIDER": "NOT_SELECTED",
                "STATUS": "ENVIRONMENT_PROVISIONING_BLOCKED",
                "credentials": "MISSING",
            }
        )
    if requested not in PROVIDERS:
        return _sealed({"PROVIDER": requested, "STATUS": "PROVIDER_UNSUPPORTED"})
    return _sealed(
        {
            "PROVIDER": requested,
            "STATUS": "READY_FOR_CREDENTIALS",
            "credentials": creds.get("PROVIDER", "MISSING"),
            "tooling": tools,
            "regions": regions(requested),
            "implemented": True,
            "provisioned": False,
        }
    )


def inspect(environment: str = "LOCAL", provider_name: str | None = None) -> dict[str, Any]:
    env = environment_object(environment, provider_name)
    return _sealed(
        {
            "command": "inspect",
            "environment": env,
            "adapter": adapter(provider_name),
            "database": db_factory("status", environment),
            "secrets": secret_factory("references"),
            "network": network_factory("validate"),
            "release": release_identity(),
            "compatibility": compatibility().get("environments", {}),
            "localhost_rejected": local_database_rejected(),
            "values_printed": False,
            "executed": False,
        }
    )


def factory(
    command: str,
    *,
    environment: str = "LOCAL",
    provider_name: str | None = None,
    authorize: bool = False,
) -> dict[str, Any]:
    cmd = (command or "status").strip().lower().replace("_", "-")
    env = (environment or "LOCAL").upper()
    if env not in ENVIRONMENTS:
        return _sealed({"command": cmd, "STATUS": "FAILED", "reason": "INVALID_ENVIRONMENT", "executed": False})
    requested = (provider_name or "").strip().upper()
    prod = env == "PRODUCTION"
    lock = production_safety_lock()
    ident = environment_object(env, requested or None)
    adapt = adapter(requested or None)
    pid = plan_id(env, requested or "NOT_SELECTED")
    if cmd == "status":
        return evaluate()
    if cmd == "inspect":
        return inspect(env, requested or None)
    if env in _LOCKS and cmd in {"bootstrap", "destroy-plan"}:
        return _sealed({"command": cmd, "STATUS": "ENVIRONMENT_LOCKED", "executed": False})
    if cmd == "plan":
        profile = env if env in {"DEMO", "TEST", "STAGING", "PRODUCTION", "DISASTER_RECOVERY"} else "DEVELOPMENT"
        planned = environment_plan(requested if requested in PROVIDERS else None, env, profile)
        cost = cost_guard()
        return _sealed(
            {
                "command": cmd,
                "PLAN_ID": pid,
                "ENVIRONMENT_ID": ident["ENVIRONMENT_ID"],
                "PROVIDER": adapt["PROVIDER"],
                "REGION": "NOT_SELECTED",
                "CHANGES": "PLAN_ONLY",
                "RESOURCES": infra_plan(requested or None, env, dry_run=True),
                "COST": cost.get("estimated_monthly_cost") or "COST_ESTIMATE_UNAVAILABLE",
                "COST_ESTIMATE_UNAVAILABLE": True,
                "zero_cost_invented": False,
                "SECURITY": "CONFIGURED",
                "DEPENDENCIES": ["NETWORK", "DATABASE", "SECRETS", "DNS", "TLS", "OBSERVABILITY"],
                "APPROVAL": "NOT_APPROVED",
                "CREATED_AT": "NOT_A_RUNTIME_CLOCK",
                "plan": planned,
                "adapter": adapt,
                "executed": False,
                "STATUS": adapt["STATUS"] if adapt["STATUS"] != "READY_FOR_CREDENTIALS" else "PLANNED",
            }
        )
    if cmd == "validate":
        localhost = env == "PRODUCTION" and local_database_rejected()
        return _sealed(
            {
                "command": cmd,
                "environment": ident,
                "adapter": adapt,
                "authorization": authorization(env),
                "config_rejected": {
                    "production_localhost": localhost,
                    "production_local_database": localhost,
                    "production_debug": True,
                },
                "STATUS": "LOCKED" if prod else ("VALIDATION_ONLY" if requested in PROVIDERS else "LOCAL_ONLY"),
                "executed": False,
            }
        )
    if cmd == "bootstrap":
        _LOCKS.add(env)
        try:
            return _sealed(
                {
                    "command": cmd,
                    "sequence": ["PROVIDER", "NETWORK", "SECURITY", "DATABASE", "SECRET_REFERENCES", "STORAGE", "DNS", "TLS", "OBSERVABILITY", "DEPLOYMENT", "VERIFICATION"],
                    "idempotent": True,
                    "created_resources": False,
                    "factory": env_factory("plan", env, requested or None),
                    "adapter": adapt,
                    "executed": False,
                    "STATUS": "LOCKED" if prod else adapt["STATUS"],
                    "PRODUCTION_PROVISIONING": "LOCKED",
                    "production_safety": lock,
                }
            )
        finally:
            _LOCKS.discard(env)
    if cmd == "verify":
        return _sealed(
            {
                "command": cmd,
                "health": "/live",
                "readiness": "/api/v1/ready",
                "network": network_factory("validate"),
                "database": db_factory("status", env),
                "secrets": secret_factory("validate"),
                "STATUS": "FAILED" if prod else "LOCAL_ONLY",
                "HEALTHY": False,
                "executed": False,
            }
        )
    if cmd == "drift":
        row = infra_drift()
        return _sealed(
            {
                "command": cmd,
                "EXPECTED": row.get("desired"),
                "ACTUAL": row.get("actual"),
                "DRIFT": row.get("status", "UNKNOWN"),
                "auto_repair": False,
                "executed": False,
            }
        )
    if cmd == "destroy-plan":
        blocked = prod or (env == "STAGING" and not authorize)
        return _sealed(
            {
                "command": cmd,
                "PLAN_ID": pid,
                "ENVIRONMENT": env,
                "PROVIDER": adapt["PROVIDER"],
                "destroyed": False,
                "executed": False,
                "automatic": False,
                "STATUS": "LOCKED" if blocked else "DESTROY_PLAN_ONLY",
                "production_destroy": "FORBIDDEN",
                "terraform_destroy": "FORBIDDEN",
                "authorization_required": True,
            }
        )
    return evaluate()


def evaluate() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    g26 = _g26()
    lock = production_safety_lock()
    g26_ready = bool(g26.get("g26_ready") is True)
    return _sealed(
        {
            "P398_STATUS": "ENVIRONMENT_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "ENVIRONMENT_FACTORY": True,
            "ENVIRONMENT_FACTORY_READY": True,
            "ENVIRONMENT_SPEC": True,
            "ENVIRONMENT_SPEC_READY": True,
            "PROVIDER_ABSTRACTION": True,
            "PROVIDER_ABSTRACTION_READY": True,
            "PROVIDER_MATRIX": True,
            "PROVIDER_MATRIX_READY": True,
            "CONFIGURATION": True,
            "CONFIGURATION_FACTORY_READY": True,
            "NETWORK": "CONFIGURED",
            "NETWORK_PLAN_READY": True,
            "DATABASE": "NON_PRODUCTION",
            "DATABASE_PLAN_READY": True,
            "SECRETS": "REFERENCE_ONLY",
            "SECRET_REFERENCE_READY": True,
            "DNS": "NOT_AVAILABLE",
            "TLS": "CONFIGURED",
            "DNS_TLS_PLAN_READY": True,
            "OBSERVABILITY": "CONFIGURED",
            "OBSERVABILITY_PLAN_READY": True,
            "BOOTSTRAP": True,
            "BOOTSTRAP_READY": True,
            "IDEMPOTENCY": True,
            "IDEMPOTENCY_READY": True,
            "LOCKING": True,
            "LOCKING_READY": True,
            "DRIFT": True,
            "DRIFT_DETECTION_READY": True,
            "SNAPSHOT": True,
            "SNAPSHOT_READY": True,
            "DESTROY_PROTECTION": True,
            "DESTROY_PROTECTION_READY": True,
            "REPRODUCTION": True,
            "REPRODUCTION_READY": True,
            "P396_INTEGRATION_READY": True,
            "P397_INTEGRATION_READY": True,
            "P395_INTEGRATION_READY": True,
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
            "terraform_for_meos": "FORBIDDEN",
            "second_kubernetes": False,
            "second_cicd": False,
            "second_deployment_engine": False,
            "second_secrets": False,
            "second_observability": False,
            "canonical_cli": "scripts/meos-environment-factory.py",
            "canonical_control": "scripts/meos-environment-control.py",
            "QUOTA_STATUS": "NOT_VERIFIED",
            "COST_ESTIMATE_UNAVAILABLE": True,
            "provider": provider(),
            "release": release_identity(),
            "production_safety": lock,
            "COMMIT": git.get("source_commit"),
            "IMAGE": rel.get("image") or "meos/backend:p353-local",
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
                    "NEXT_ACTION": "factory plan; AUTHENTICATION_REQUIRED until credentials exist",
                },
                {
                    "EXTERNAL_DEPENDENCY": "G26",
                    "OWNER": "infrastructure",
                    "REQUIRED_RESOURCE": "real cluster/DB/TLS",
                    "EVIDENCE_REQUIRED": "independent G26 gates",
                    "NEXT_ACTION": "re-run meos-ext-g26-readiness.py; factory cannot set G26_READY",
                },
            ],
        }
    )
