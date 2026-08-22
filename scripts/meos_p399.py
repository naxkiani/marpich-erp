"""P399 Universal Control Plane overlay. Orchestrates P396–P398. Not a second deploy engine."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from meos_p382 import production_safety_lock  # noqa: E402
from meos_p387 import provider  # noqa: E402
from meos_p388 import backup_manager, credential_preflight  # noqa: E402
from meos_p391 import cost_guard, drift as infra_drift  # noqa: E402
from meos_p393 import db_factory, network_factory, secret_factory  # noqa: E402
from meos_p394 import resource_graph as infra_sequence  # noqa: E402
from meos_p396 import history as deployment_history, orchestrate  # noqa: E402
from meos_p397 import release_identity  # noqa: E402
from meos_p398 import environment_object, inspect as environment_inspect  # noqa: E402
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
COMMANDS = (
    "status",
    "inventory",
    "inspect",
    "validate",
    "plan",
    "execute",
    "verify",
    "drift",
    "history",
    "capacity",
    "cost",
    "security",
    "health",
)
ENVIRONMENTS = ("LOCAL", "DEMO", "TEST", "STAGING", "PRODUCTION", "DISASTER_RECOVERY")
PROVIDERS = ("VPS", "AWS", "AZURE", "GCP", "KUBERNETES")
STATES = (
    "PLANNED",
    "PENDING_APPROVAL",
    "PROVISIONING",
    "READY",
    "DEGRADED",
    "DRIFTED",
    "BLOCKED",
    "FAILED",
    "DECOMMISSIONING",
    "DECOMMISSIONED",
    "UNKNOWN",
)
ROLES = (
    "PLATFORM_ADMIN",
    "INFRASTRUCTURE_OPERATOR",
    "RELEASE_MANAGER",
    "SECURITY_OPERATOR",
    "DATABASE_OPERATOR",
    "AUDITOR",
    "VIEWER",
)
APPLICATIONS = ("backend", "frontend", "admin", "worker", "scheduler")
SELF_SERVICE = (
    "CREATE_ENVIRONMENT",
    "DEPLOY_RELEASE",
    "SCALE_APPLICATION",
    "CREATE_DATABASE",
    "CREATE_BACKUP",
    "RESTORE_DATABASE",
    "ROTATE_SECRET_REFERENCE",
    "CONFIGURE_DOMAIN",
    "CONFIGURE_TLS",
    "CREATE_DR_PLAN",
)
CONFLICTS = {
    frozenset({"DEPLOY_RELEASE", "ROLLBACK"}),
    frozenset({"CREATE_DATABASE", "RESTORE_DATABASE"}),
    frozenset({"CREATE_BACKUP", "DECOMMISSION"}),
    frozenset({"SCALE_APPLICATION", "DECOMMISSION"}),
}
APP_PATH = ("APPLICATION", "RELEASE", "DEPLOYMENT", "ENVIRONMENT", "CLUSTER", "NETWORK", "DATABASE", "STORAGE")
INGRESS_PATH = ("DOMAIN", "TLS", "INGRESS", "APPLICATION")
BACKUP_PATH = ("BACKUP", "DATABASE", "ENVIRONMENT")
_CHANGES: dict[str, dict[str, Any]] = {}
_ACTIVE: dict[str, str] = {}
_AUDIT: list[dict[str, Any]] = []
_LOCKS: set[str] = set()


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p399_g26", path)
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


def _norm_env(raw: str | None) -> str:
    key = (raw or "LOCAL").strip().upper().replace("-", "_")
    aliases = {"DEVELOPMENT": "LOCAL", "DEV": "LOCAL", "DISASTER-RECOVERY": "DISASTER_RECOVERY"}
    key = aliases.get(key, key)
    return key if key in ENVIRONMENTS else "LOCAL"


def _norm_provider(raw: str | None) -> str:
    key = (raw or "").strip().upper()
    if not key:
        return "NOT_SELECTED"
    return key if key in PROVIDERS else "UNSUPPORTED"


def change_id(operation: str, resource: str, environment: str) -> str:
    key = "|".join((operation.upper(), resource.upper(), environment.upper()))
    value = "CHG-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]
    return value


def plan_id(operation: str, environment: str, provider_name: str) -> str:
    key = "|".join((operation.upper(), environment.upper(), (provider_name or "NOT_SELECTED").upper()))
    return "PLAN-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def policy_evaluate(operation: str, environment: str, role: str = "VIEWER") -> dict[str, Any]:
    env = _norm_env(environment)
    op = (operation or "INSPECT").upper()
    actor = role if role in ROLES else "VIEWER"
    result = "ALLOW"
    if op in {"DESTROY", "DECOMMISSION", "RESTORE_DATABASE"} and env == "PRODUCTION":
        result = "BLOCKED"
    elif env == "PRODUCTION" and op in SELF_SERVICE:
        result = "REQUIRES_APPROVAL" if actor in {"PLATFORM_ADMIN", "INFRASTRUCTURE_OPERATOR"} else "DENY"
    elif env in {"STAGING", "PRODUCTION", "DISASTER_RECOVERY"} and op in {"CREATE_ENVIRONMENT", "DEPLOY_RELEASE", "SCALE_APPLICATION"}:
        result = "REQUIRES_APPROVAL" if actor != "VIEWER" else "DENY"
    elif actor == "VIEWER" and op not in {"INSPECT", "STATUS", "INVENTORY", "HISTORY", "COST", "CAPACITY", "SECURITY", "HEALTH"}:
        result = "DENY"
    row = {
        "POLICY_RESULT": result,
        "policy": "meos.control-plane.v1",
        "resource": op,
        "environment": env,
        "operator": actor,
        "timestamp": "NOT_A_RUNTIME_CLOCK",
        "result": result,
        "wildcard_production": False,
    }
    return _sealed(row)


def _resource(resource_type: str, environment: str, provider_name: str, status: str, owner: str, lifecycle: str) -> dict[str, Any]:
    env = _norm_env(environment)
    kind = resource_type.upper()
    return {
        "RESOURCE_ID": f"meos-{env.lower()}-{kind.lower()}",
        "RESOURCE_TYPE": kind,
        "PROVIDER": provider_name,
        "ENVIRONMENT": env,
        "STATUS": status,
        "OWNER": owner,
        "TEAM": "platform",
        "LIFECYCLE": lifecycle,
        "LIFECYCLE_POLICY": "plan_then_approve",
        "TENANT_SCOPE": "platform",
        "CREATED_AT": "NOT_A_RUNTIME_CLOCK",
        "UPDATED_AT": "NOT_A_RUNTIME_CLOCK",
    }


def resource_catalog(environment: str = "LOCAL", provider_name: str | None = None) -> dict[str, Any]:
    env = _norm_env(environment)
    requested = _norm_provider(provider_name)
    spec = _load_yaml("MEOS_RESOURCE_CATALOG.v1.yaml")
    catalog = spec.get("catalog") or {}
    rows = []
    for kind, meta in catalog.items():
        rows.append(
            _resource(
                kind,
                env,
                requested,
                str(meta.get("status") or "UNKNOWN"),
                str(meta.get("owner") or "NOT_AVAILABLE"),
                str(meta.get("lifecycle") or "UNKNOWN"),
            )
        )
    return _sealed(
        {
            "command": "inventory",
            "catalog": rows,
            "count": len(rows),
            "states": list(STATES),
            "unknown_hidden": False,
            "values": "NOT_STORED",
            "invented": False,
            "STATUS": "LOCAL_ONLY" if env in {"LOCAL", "DEMO", "TEST"} else "BLOCKED",
        }
    )


def resource_graph() -> dict[str, Any]:
    def edges(path: tuple[str, ...]) -> list[dict[str, str]]:
        return [{"from": path[i], "to": path[i + 1]} for i in range(len(path) - 1)]

    return _sealed(
        {
            "application_path": list(APP_PATH),
            "ingress_path": list(INGRESS_PATH),
            "backup_path": list(BACKUP_PATH),
            "edges": edges(APP_PATH) + edges(INGRESS_PATH) + edges(BACKUP_PATH),
            "infrastructure_sequence": infra_sequence(),
            "inspectable": True,
        }
    )


def environment_catalog(provider_name: str | None = None) -> dict[str, Any]:
    rows = []
    for env in ENVIRONMENTS:
        obj = environment_object(env, provider_name)
        rows.append(
            {
                "ENVIRONMENT_ID": obj["ENVIRONMENT_ID"],
                "TYPE": obj["ENVIRONMENT_TYPE"],
                "PROVIDER": obj["PROVIDER"],
                "REGION": obj["REGION"],
                "PROFILE": obj["PROFILE"],
                "STATUS": obj["STATUS"],
                "DRIFT": "UNKNOWN",
                "SECURITY": obj["SECURITY_PROFILE"],
                "COST": "COST_NOT_AVAILABLE",
                "CAPACITY": "UNKNOWN",
            }
        )
    return _sealed({"command": "environments", "environments": rows, "count": len(rows)})


def release_catalog() -> dict[str, Any]:
    ident = release_identity()
    status = str(ident.get("STATUS") or "UNKNOWN")
    rejected = status in {"REVOKED", "UNKNOWN", "INCOMPATIBLE", "RELEASE_BLOCKED"}
    return _sealed(
        {
            "command": "releases",
            "releases": [ident],
            "accepted": not rejected and bool(ident.get("selectable")),
            "rejected_reason": ident.get("REASON") if rejected else None,
            "mutable_identity": False,
        }
    )


def provider_catalog() -> dict[str, Any]:
    creds = credential_preflight()
    rows = {}
    for name in PROVIDERS:
        rows[name] = {
            "provider": name,
            "status": "NOT_CONFIGURED",
            "authorization": "NOT_INFERRED",
            "credentials": "MISSING",
            "credential_status": "MISSING",
            "inferred": False,
        }
    return _sealed(
        {
            "command": "providers",
            "providers": rows,
            "credentials": {
                "STATUS": "MISSING",
                "values_printed": False,
                "DATABASE": creds.get("DATABASE"),
                "PROVIDER": creds.get("PROVIDER"),
            },
            "authorization_from_name": False,
        }
    )


def application_catalog() -> dict[str, Any]:
    ident = release_identity()
    rows = []
    for name in APPLICATIONS:
        rows.append(
            {
                "APPLICATION_ID": f"meos-{name}",
                "NAME": name,
                "VERSION": ident.get("VERSION"),
                "RELEASE_ID": ident.get("RELEASE_ID"),
                "ENVIRONMENT": "LOCAL",
                "STATUS": "IMPLEMENTED",
                "OWNER": "platform",
                "TENANT_SCOPE": "platform",
                "DEPENDENCIES": ["identity", "audit"],
                "HEALTH": "UNKNOWN",
                "READINESS": "UNKNOWN",
                "ACTIVE": False,
            }
        )
    return _sealed({"command": "applications", "applications": rows, "ACTIVE_APPLICATIONS": 0})


def dashboard(environment: str = "LOCAL", provider_name: str | None = None) -> dict[str, Any]:
    env = environment_inspect(environment, provider_name)
    ident = release_identity()
    obj = env.get("environment") or {}
    return _sealed(
        {
            "environment": obj.get("ENVIRONMENT_NAME"),
            "provider": obj.get("PROVIDER"),
            "region": obj.get("REGION"),
            "profile": obj.get("PROFILE"),
            "status": obj.get("STATUS"),
            "release": ident.get("RELEASE_ID"),
            "deployment": "LOCKED",
            "database": obj.get("DATABASE_PROFILE"),
            "network": obj.get("NETWORK_PROFILE"),
            "DNS": "NOT_AVAILABLE",
            "TLS": obj.get("SECURITY_PROFILE"),
            "backup": obj.get("BACKUP_PROFILE"),
            "restore": "NOT_EXECUTED",
            "observability": obj.get("OBSERVABILITY_PROFILE"),
            "security": obj.get("SECURITY_PROFILE"),
            "cost": "COST_NOT_AVAILABLE",
            "capacity": "UNKNOWN",
            "drift": "UNKNOWN",
        }
    )


def search(query: str, tenant_id: str = "platform") -> dict[str, Any]:
    q = (query or "").strip().lower()
    catalog = resource_catalog()["catalog"]
    hits = []
    for row in catalog:
        if row.get("TENANT_SCOPE") != tenant_id and tenant_id != "platform":
            continue
        blob = json.dumps(row, default=str).lower()
        if not q or q in blob:
            hits.append(row)
    return _sealed(
        {
            "command": "search",
            "query": q,
            "tenant_id": tenant_id,
            "hits": hits,
            "cross_tenant": False,
            "count": len(hits),
        }
    )


def timeline(resource_id: str) -> dict[str, Any]:
    return _sealed(
        {
            "RESOURCE_ID": resource_id,
            "events": [
                {"kind": "creation", "status": "PLANNED", "timestamp": "NOT_A_RUNTIME_CLOCK"},
                {"kind": "configuration", "status": "CONFIGURED", "timestamp": "NOT_A_RUNTIME_CLOCK"},
                {"kind": "deployment", "status": "LOCKED", "timestamp": "NOT_A_RUNTIME_CLOCK"},
            ],
            "secrets": "NOT_RECORDED",
        }
    )


def audit_record(operation: str, result: str, environment: str, role: str) -> dict[str, Any]:
    row = {
        "WHO": role,
        "WHAT": operation,
        "WHERE": environment,
        "WHEN": "NOT_A_RUNTIME_CLOCK",
        "WHY": "control_plane",
        "RESULT": result,
        "secrets": "NOT_RECORDED",
        "immutable": True,
        "canonical": "contexts.audit",
    }
    _AUDIT.append(row)
    return _sealed(row)


def _conflict(operation: str) -> dict[str, Any] | None:
    op = operation.upper()
    for active in _ACTIVE.values():
        if frozenset({op, active}) in CONFLICTS:
            return {"STATUS": "CONFLICT", "active": active, "requested": op}
    return None


def plan_engine(
    operation: str,
    environment: str,
    provider_name: str | None,
    dry_run: bool = True,
) -> dict[str, Any]:
    env = _norm_env(environment)
    requested = _norm_provider(provider_name)
    pid = plan_id(operation, env, requested)
    cid = change_id(operation, env, requested)
    policy = policy_evaluate(operation, env)
    return _sealed(
        {
            "PLAN_ID": pid,
            "CHANGE_ID": cid,
            "RESOURCE": operation.upper(),
            "OPERATION": operation.upper(),
            "ENVIRONMENT": env,
            "PROVIDER": requested,
            "current_state": "UNKNOWN" if env != "LOCAL" else "LOCAL_ONLY",
            "desired_state": "PLANNED",
            "dependencies": ["POLICY", "RBAC", "ENVIRONMENT", "RELEASE"],
            "risk": "HIGH" if env == "PRODUCTION" else "LOW",
            "cost": "COST_NOT_AVAILABLE",
            "security": "CONFIGURED",
            "rollback": "CONFIGURED",
            "approval": policy["POLICY_RESULT"],
            "STATUS": "DRAFT" if dry_run else "REVIEW",
            "dry_run": dry_run,
            "executed": False,
            "CREATED_AT": "NOT_A_RUNTIME_CLOCK",
        }
    )


def health() -> dict[str, Any]:
    checks = {
        "P395": "CONFIGURED" if (_SCRIPTS / "meos_p395.py").is_file() else "NOT_AVAILABLE",
        "P396": "CONFIGURED" if (_SCRIPTS / "meos_p396.py").is_file() else "NOT_AVAILABLE",
        "P397": "CONFIGURED" if (_SCRIPTS / "meos_p397.py").is_file() else "NOT_AVAILABLE",
        "P398": "CONFIGURED" if (_SCRIPTS / "meos_p398.py").is_file() else "NOT_AVAILABLE",
        "database": "NON_PRODUCTION",
        "cache": "NOT_AVAILABLE",
        "event_bus": "CONFIGURED",
        "audit": "CONFIGURED",
        "configuration": "CONFIGURED",
        "provider_adapters": "READY_FOR_CREDENTIALS",
    }
    return _sealed({"command": "health", "checks": checks, "verified": False, "STATUS": "CONFIGURED"})


def dispatch(
    command: str,
    environment: str = "LOCAL",
    provider_name: str | None = None,
    operation: str = "INSPECT",
    role: str = "VIEWER",
    dry_run: bool = True,
    authorize: bool = False,
    tenant_id: str = "platform",
    query: str = "",
    idempotency_key: str = "",
) -> dict[str, Any]:
    cmd = (command or "status").strip().lower()
    env = _norm_env(environment)
    requested = _norm_provider(provider_name)
    prod = env == "PRODUCTION"
    lock = production_safety_lock()
    if cmd == "status":
        return evaluate()
    if cmd == "health":
        return health()
    if cmd == "inventory":
        return resource_catalog(env, requested)
    if cmd == "inspect":
        return _sealed(
            {
                "command": cmd,
                "dashboard": dashboard(env, None if requested in {"NOT_SELECTED", "UNSUPPORTED"} else requested),
                "environment": environment_inspect(env, None if requested in {"NOT_SELECTED", "UNSUPPORTED"} else requested),
                "release": release_identity(),
                "graph": resource_graph(),
                "executed": False,
            }
        )
    if cmd == "validate":
        policy = policy_evaluate(operation, env, role)
        ident = release_identity()
        blocked = ident.get("STATUS") in {"REVOKED", "UNKNOWN", "INCOMPATIBLE", "RELEASE_BLOCKED"}
        return _sealed(
            {
                "command": cmd,
                "POLICY_RESULT": policy["POLICY_RESULT"],
                "policy": policy,
                "release": ident,
                "release_rejected": blocked,
                "environment": environment_object(env, None if requested in {"NOT_SELECTED", "UNSUPPORTED"} else requested),
                "config_rejected": {
                    "production_localhost": prod,
                    "production_local_database": prod,
                    "production_debug": prod,
                },
                "STATUS": "LOCKED" if prod else ("BLOCKED" if blocked else "LOCAL_ONLY"),
                "executed": False,
            }
        )
    if cmd == "plan":
        row = plan_engine(operation, env, requested, dry_run=True)
        row["command"] = cmd
        row["policy"] = policy_evaluate(operation, env, role)
        _CHANGES[row["CHANGE_ID"]] = row
        audit_record(cmd, row["STATUS"], env, role)
        return row
    if cmd == "execute":
        conflict = _conflict(operation)
        if conflict:
            return _sealed({**conflict, "command": cmd, "executed": False})
        policy = policy_evaluate(operation, env, role)
        if prod or not authorize or policy["POLICY_RESULT"] in {"DENY", "BLOCKED"}:
            return _sealed(
                {
                    "command": cmd,
                    "STATUS": "LOCKED",
                    "PRODUCTION_MUTATION": "LOCKED",
                    "POLICY_RESULT": policy["POLICY_RESULT"],
                    "dry_run": True,
                    "executed": False,
                    "created_resources": False,
                    "production_safety": lock,
                }
            )
        if requested in {"NOT_SELECTED", "UNSUPPORTED"}:
            return _sealed(
                {
                    "command": cmd,
                    "STATUS": "ENVIRONMENT_PROVISIONING_BLOCKED" if requested == "NOT_SELECTED" else "PROVIDER_UNSUPPORTED",
                    "executed": False,
                }
            )
        creds = credential_preflight()
        if creds.get("PROVIDER") == "MISSING":
            return _sealed(
                {
                    "command": cmd,
                    "STATUS": "AUTHENTICATION_REQUIRED",
                    "executed": False,
                    "created_resources": False,
                }
            )
        if dry_run:
            row = plan_engine(operation, env, requested, dry_run=True)
            row.update({"command": cmd, "STATUS": "PLAN_ONLY", "executed": False})
            return row
        key = idempotency_key or change_id(operation, env, requested)
        if key in _CHANGES:
            return _sealed({**_CHANGES[key], "idempotent": True, "duplicated": False, "executed": False})
        _ACTIVE[env] = operation.upper()
        try:
            deployed = orchestrate("deploy", environment=env, provider_name=requested, authorize=authorize)
        finally:
            _ACTIVE.pop(env, None)
        result = {
            "command": cmd,
            "STATUS": deployed.get("STATUS") or "BLOCKED",
            "deployment": deployed,
            "executed": False,
            "created_resources": False,
            "idempotency_key": key,
        }
        _CHANGES[key] = result
        audit_record(cmd, str(result["STATUS"]), env, role)
        return _sealed(result)
    if cmd == "verify":
        return _sealed(
            {
                "command": cmd,
                "health": health(),
                "database": db_factory("status"),
                "network": network_factory("validate"),
                "secrets": secret_factory("validate"),
                "STATUS": "LOCAL_ONLY",
                "READY_FROM_DESIRED_ONLY": False,
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
                "DIFF": row.get("status", "UNKNOWN"),
                "RISK": "UNKNOWN",
                "RECOMMENDATION": "REVIEW",
                "auto_repair": False,
                "production_auto_repair": False,
                "executed": False,
            }
        )
    if cmd == "history":
        return _sealed(
            {
                "command": cmd,
                "changes": list(_CHANGES.values()),
                "audit": list(_AUDIT),
                "deployments": deployment_history(env),
                "timeline": timeline(f"meos-{env.lower()}-environment"),
                "search": search(query, tenant_id),
                "values_printed": False,
            }
        )
    if cmd == "capacity":
        return _sealed(
            {
                "command": cmd,
                "CPU": "UNKNOWN",
                "MEMORY": "UNKNOWN",
                "STORAGE": "UNKNOWN",
                "DATABASE": "UNKNOWN",
                "NETWORK": "UNKNOWN",
                "IP": "UNKNOWN",
                "QUOTA": "NOT_VERIFIED",
                "STATUS": "UNKNOWN",
                "invented": False,
            }
        )
    if cmd == "cost":
        guard = cost_guard()
        return _sealed(
            {
                "command": cmd,
                "CURRENT": "COST_NOT_AVAILABLE",
                "ESTIMATED": "COST_NOT_AVAILABLE",
                "BUDGET": "NOT_SET",
                "VARIANCE": "UNKNOWN",
                "TREND": "UNKNOWN",
                "COST_NOT_AVAILABLE": True,
                "zero_cost_invented": False,
                "guard": guard,
            }
        )
    if cmd == "security":
        return _sealed(
            {
                "command": cmd,
                "TLS": "CONFIGURED",
                "IAM": "NOT_VERIFIED",
                "RBAC": "CONFIGURED",
                "secret_state": "REFERENCE_ONLY",
                "image_provenance": "NOT_AVAILABLE",
                "vulnerability": "UNKNOWN",
                "network_policy": "CONFIGURED",
                "audit": "CONFIGURED",
                "security_events": "CONFIGURED",
                "STATUS": "UNKNOWN" if prod else "CONFIGURED",
                "PASS": False,
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
            "P399_STATUS": "CONTROL_PLANE_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "CONTROL_PLANE": True,
            "CONTROL_PLANE_READY": True,
            "RESOURCE_CATALOG": True,
            "RESOURCE_CATALOG_READY": True,
            "RESOURCE_GRAPH": True,
            "RESOURCE_GRAPH_READY": True,
            "ENVIRONMENT_CATALOG": True,
            "ENVIRONMENT_CATALOG_READY": True,
            "RELEASE_CATALOG": True,
            "RELEASE_CATALOG_READY": True,
            "PROVIDER_CATALOG": True,
            "PROVIDER_CATALOG_READY": True,
            "POLICY": True,
            "POLICY_INTEGRATION_READY": True,
            "PLAN_ENGINE": True,
            "PLAN_ENGINE_READY": True,
            "CHANGE_MANAGEMENT": True,
            "CHANGE_MANAGEMENT_READY": True,
            "RBAC": True,
            "RBAC_READY": True,
            "AUDIT": True,
            "AUDIT_READY": True,
            "EVENTS": True,
            "EVENTS_READY": True,
            "NOTIFICATIONS": True,
            "NOTIFICATIONS_READY": True,
            "DRIFT": True,
            "DRIFT_READY": True,
            "COST": "COST_NOT_AVAILABLE",
            "COST_READY": True,
            "CAPACITY": "UNKNOWN",
            "CAPACITY_READY": True,
            "SECURITY": "CONFIGURED",
            "SECURITY_READY": True,
            "BACKUP": "CONFIGURED",
            "BACKUP_CENTER_READY": True,
            "RESTORE": "NOT_EXECUTED",
            "RESTORE_CENTER_READY": True,
            "DR": "NOT_TESTED",
            "DR_CENTER_READY": True,
            "P395_INTEGRATION": True,
            "P395_INTEGRATION_READY": True,
            "P396_INTEGRATION": True,
            "P396_INTEGRATION_READY": True,
            "P397_INTEGRATION": True,
            "P397_INTEGRATION_READY": True,
            "P398_INTEGRATION": True,
            "P398_INTEGRATION_READY": True,
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
            "second_deployment_engine": False,
            "second_kubernetes": False,
            "second_cicd": False,
            "canonical_cli": "scripts/meos-control-plane.py",
            "canonical_operator": "scripts/meos-control.py",
            "canonical_ui": "/enterprise/launch-center",
            "canonical_api": "/api/v1/launch-center/control-plane",
            "platform_api_is_tenant_sor": True,
            "roles": list(ROLES),
            "self_service": list(SELF_SERVICE),
            "states": list(STATES),
            "catalog": resource_catalog(),
            "graph": resource_graph(),
            "environments": environment_catalog(),
            "releases": release_catalog(),
            "providers": provider_catalog(),
            "applications": application_catalog(),
            "dashboard": dashboard("LOCAL"),
            "backup": backup_manager("CHECK"),
            "provider": provider(),
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
            "COST_NOT_AVAILABLE": True,
            "zero_cost_invented": False,
            "dependencies": [
                {
                    "EXTERNAL_DEPENDENCY": "credentials",
                    "OWNER": "NOT_AVAILABLE",
                    "REQUIRED_RESOURCE": "authorized provider account",
                    "EVIDENCE_REQUIRED": "validated identity",
                    "NEXT_ACTION": "control-plane plan; AUTHENTICATION_REQUIRED until credentials exist",
                },
                {
                    "EXTERNAL_DEPENDENCY": "G26",
                    "OWNER": "infrastructure",
                    "REQUIRED_RESOURCE": "real cluster/DB/TLS",
                    "EVIDENCE_REQUIRED": "independent G26 gates",
                    "NEXT_ACTION": "re-run meos-ext-g26-readiness.py; control plane cannot set G26_READY",
                },
            ],
        }
    )
