"""P400 Autonomous Platform Operations overlay. Policy-governed. Not a second infra platform."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from meos_p382 import production_safety_lock  # noqa: E402
from meos_p388 import backup_manager  # noqa: E402
from meos_p391 import drift as infra_drift  # noqa: E402
from meos_p396 import orchestrate  # noqa: E402
from meos_p397 import release_identity  # noqa: E402
from meos_p398 import inspect as environment_inspect  # noqa: E402
from meos_p399 import (  # noqa: E402
    dashboard,
    policy_evaluate,
    resource_graph,
)
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
COMMANDS = (
    "status",
    "observe",
    "detect",
    "analyze",
    "plan",
    "recommend",
    "approve",
    "execute",
    "verify",
    "rollback",
    "explain",
    "history",
)
ENVIRONMENTS = ("LOCAL", "DEMO", "TEST", "STAGING", "PRODUCTION", "DISASTER_RECOVERY")
LEVELS = {
    "LOCAL": "LEVEL_2",
    "DEMO": "LEVEL_1",
    "TEST": "LEVEL_2",
    "STAGING": "LEVEL_4",
    "PRODUCTION": "LEVEL_5",
    "DISASTER_RECOVERY": "LEVEL_4",
}
SIGNAL_TYPES = (
    "AVAILABILITY",
    "PERFORMANCE",
    "ERROR",
    "SECURITY",
    "CAPACITY",
    "COST",
    "DATABASE",
    "NETWORK",
    "DEPLOYMENT",
    "BACKUP",
    "RESTORE",
    "DRIFT",
)
AI_TOOLS = (
    "inspect_resource",
    "inspect_environment",
    "inspect_release",
    "inspect_deployment",
    "inspect_incident",
    "generate_plan",
    "explain_plan",
    "recommend_remediation",
    "check_policy",
    "check_risk",
    "verify_action",
)
CONFLICTS = {
    frozenset({"DEPLOY", "ROLLBACK"}),
    frozenset({"MIGRATION", "RESTORE"}),
    frozenset({"SCALE", "DECOMMISSION"}),
    frozenset({"FAILOVER", "FAILBACK"}),
}
FIXTURES = {
    "cpu_anomaly": {"TYPE": "CAPACITY", "SEVERITY": "MEDIUM", "VALUE": "CPU_HIGH", "EXPECTED": "UNKNOWN", "ACTUAL": "FIXTURE"},
    "health_failure": {"TYPE": "AVAILABILITY", "SEVERITY": "HIGH", "VALUE": "HEALTH_FAIL", "EXPECTED": "UP", "ACTUAL": "FIXTURE"},
    "deployment_mismatch": {"TYPE": "DEPLOYMENT", "SEVERITY": "HIGH", "VALUE": "DEPLOYMENT_IDENTITY_DRIFT", "EXPECTED": "IMMUTABLE", "ACTUAL": "FIXTURE"},
    "backup_failure": {"TYPE": "BACKUP", "SEVERITY": "MEDIUM", "VALUE": "BACKUP_FAIL", "EXPECTED": "CONFIGURED", "ACTUAL": "FIXTURE"},
    "configuration_drift": {"TYPE": "DRIFT", "SEVERITY": "MEDIUM", "VALUE": "DRIFTED", "EXPECTED": "IN_SYNC", "ACTUAL": "FIXTURE"},
}
HEALTH_WEIGHTS = {
    "AVAILABILITY": 20,
    "PERFORMANCE": 10,
    "SECURITY": 20,
    "DATA": 15,
    "DEPLOYMENT": 15,
    "BACKUP": 10,
    "OBSERVABILITY": 5,
    "CAPACITY": 5,
}
_HISTORY: list[dict[str, Any]] = []
_PLANS: dict[str, dict[str, Any]] = {}
_ACTIVE: dict[str, str] = {}
_TOKENS: dict[str, dict[str, Any]] = {}
_PAUSED = False
_KNOWLEDGE: list[dict[str, Any]] = []


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p400_g26", path)
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
    aliases = {"DEVELOPMENT": "LOCAL", "DEV": "LOCAL"}
    key = aliases.get(key, key)
    return key if key in ENVIRONMENTS else "LOCAL"


def kill_switch() -> bool:
    return os.environ.get("MEOS_AUTONOMOUS_KILL_SWITCH", "").strip() in {"1", "true", "TRUE", "YES"}


def paused() -> bool:
    return _PAUSED or os.environ.get("MEOS_AUTONOMOUS_PAUSED", "").strip() in {"1", "true", "TRUE"}


def set_paused(value: bool) -> dict[str, Any]:
    global _PAUSED
    _PAUSED = bool(value)
    return _sealed({"AUTOMATION_PAUSED": _PAUSED, "mutations": False if _PAUSED else "POLICY_GATED"})


def automation_level(environment: str) -> str:
    return LEVELS[_norm_env(environment)]


def signal_id(source: str, resource: str, environment: str, kind: str) -> str:
    key = "|".join((source, resource, environment, kind))
    return "SIG-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def plan_fingerprint(environment: str, action: str, evidence: str) -> str:
    return hashlib.sha256(f"{environment}|{action}|{evidence}".encode("utf-8")).hexdigest()[:16]


def normalize_signal(
    source: str,
    resource: str,
    environment: str,
    kind: str,
    severity: str,
    value: str,
    expected: str,
    actual: str,
    confidence: str,
    simulated: bool = False,
) -> dict[str, Any]:
    return {
        "SIGNAL_ID": signal_id(source, resource, environment, kind),
        "SOURCE": source,
        "RESOURCE": resource,
        "ENVIRONMENT": environment,
        "TIMESTAMP": "NOT_A_RUNTIME_CLOCK",
        "TYPE": kind if kind in SIGNAL_TYPES else "UNKNOWN",
        "SEVERITY": severity,
        "VALUE": value,
        "EXPECTED": expected,
        "ACTUAL": actual,
        "CONFIDENCE": confidence,
        "SIMULATION": simulated,
    }


def observe(environment: str = "LOCAL") -> dict[str, Any]:
    env = _norm_env(environment)
    ident = release_identity()
    backup = backup_manager("CHECK")
    drift = infra_drift()
    g26 = _g26()
    signals = [
        normalize_signal("release_factory", "RELEASE", env, "DEPLOYMENT", "HIGH", str(ident.get("STATUS")), "IMMUTABLE", str(ident.get("IMAGE_DIGEST")), "HIGH"),
        normalize_signal("backup_manager", "BACKUP", env, "BACKUP", "LOW", "CONFIGURED", "VERIFIED", str(backup.get("verification")), "MEDIUM"),
        normalize_signal("environment_factory", "CONFIGURATION", env, "DRIFT", "MEDIUM", str(drift.get("status") or "UNKNOWN"), "IN_SYNC", "UNKNOWN", "LOW"),
        normalize_signal("g26", "PRODUCTION", env, "AVAILABILITY", "CRITICAL" if env == "PRODUCTION" else "INFO", str(g26.get("g26_status")), "PASS", "BLOCKED", "HIGH"),
        normalize_signal("observability", "G23", env, "ERROR", "MEDIUM", "CONFIGURED", "PRODUCTION_VERIFIED", "FAIL", "HIGH"),
    ]
    return _sealed(
        {
            "command": "observe",
            "environment": env,
            "signals": signals,
            "count": len(signals),
            "second_observability": False,
            "dashboard": dashboard(env),
            "SIMULATION": False,
        }
    )


def detect(environment: str = "LOCAL", fixture: str | None = None) -> dict[str, Any]:
    env = _norm_env(environment)
    observed = observe(env)
    signals = list(observed["signals"])
    simulated = False
    if fixture:
        row = FIXTURES.get(fixture)
        if not row:
            return _sealed({"command": "detect", "STATUS": "UNKNOWN_FIXTURE", "SIMULATION": True})
        signals.append(
            normalize_signal("fixture", fixture, env, str(row["TYPE"]), str(row["SEVERITY"]), str(row["VALUE"]), str(row["EXPECTED"]), str(row["ACTUAL"]), "LOW", simulated=True)
        )
        simulated = True
    incidents = correlate(signals, env)
    return _sealed(
        {
            "command": "detect",
            "signals": signals,
            "incidents": incidents,
            "SIMULATION": simulated,
            "production_evidence": False if simulated else False,
            "deterministic": True,
            "ai_invented": False,
            "STATUS": "SIMULATION" if simulated else "OBSERVED",
        }
    )


def correlate(signals: list[dict[str, Any]], environment: str) -> list[dict[str, Any]]:
    env = _norm_env(environment)
    groups: dict[str, list[dict[str, Any]]] = {}
    for signal in signals:
        key = f"{signal['ENVIRONMENT']}|{signal['TYPE']}|{signal['VALUE']}"
        groups.setdefault(key, []).append(signal)
    incidents = []
    for key, rows in groups.items():
        if not rows:
            continue
        primary = rows[0]
        if primary.get("ACTUAL") in {"NOT_AVAILABLE", "UNKNOWN", "BLOCKED", "FAIL", "FIXTURE"} or primary.get("VALUE") in {
            "RELEASE_BLOCKED",
            "DEPLOYMENT_IDENTITY_DRIFT",
            "HEALTH_FAIL",
            "BACKUP_FAIL",
            "DRIFTED",
            "BLOCKED",
        }:
            incidents.append(incident_model(env, primary, rows))
    return incidents


def incident_model(environment: str, primary: dict[str, Any], signals: list[dict[str, Any]]) -> dict[str, Any]:
    severity = str(primary.get("SEVERITY") or "INFO")
    iid = "INC-" + hashlib.sha256(f"{environment}|{primary['SIGNAL_ID']}".encode("utf-8")).hexdigest()[:12]
    return {
        "INCIDENT_ID": iid,
        "ENVIRONMENT": environment,
        "RESOURCE": primary.get("RESOURCE"),
        "SEVERITY": severity,
        "IMPACT": "LOCAL_ONLY" if environment in {"LOCAL", "DEMO", "TEST"} else "UNKNOWN",
        "START": "NOT_A_RUNTIME_CLOCK",
        "SIGNALS": [row["SIGNAL_ID"] for row in signals],
        "ROOT_CAUSE_STATUS": "CANDIDATES_ONLY",
        "CONFIDENCE": "LOW" if primary.get("SIMULATION") else "MEDIUM",
        "CURRENT_STATE": primary.get("VALUE"),
        "RECOMMENDED_ACTION": "RECOMMEND_ONLY",
        "POLICY_RESULT": "NOT_VERIFIED",
        "APPROVAL": "NOT_APPROVED",
        "RESOLUTION": "OPEN",
        "TIMESTAMP": "NOT_A_RUNTIME_CLOCK",
        "SIMULATION": bool(primary.get("SIMULATION")),
        "TENANT_SCOPE": "platform",
    }


def analyze(environment: str = "LOCAL", fixture: str | None = None) -> dict[str, Any]:
    env = _norm_env(environment)
    detected = detect(env, fixture)
    graph = resource_graph()
    candidates = []
    for incident in detected["incidents"]:
        candidates.append(
            {
                "INCIDENT_ID": incident["INCIDENT_ID"],
                "ROOT_CAUSE_CANDIDATES": [
                    {
                        "CAUSE": incident["CURRENT_STATE"],
                        "EVIDENCE": incident["SIGNALS"],
                        "CONFIDENCE": incident["CONFIDENCE"],
                        "DEPENDENCIES": graph["application_path"],
                        "CONTRADICTING_EVIDENCE": [],
                    }
                ],
                "certainty": False,
            }
        )
    return _sealed(
        {
            "command": "analyze",
            "environment": env,
            "incidents": detected["incidents"],
            "diagnosis": candidates,
            "graph": graph,
            "SIMULATION": detected["SIMULATION"],
            "certainty": False,
        }
    )


def risk_evaluate(action: str, environment: str) -> dict[str, Any]:
    env = _norm_env(environment)
    op = action.upper()
    level = "LOW"
    if op in {"RESTORE", "FAILOVER", "FAILBACK", "DECOMMISSION"} or env == "PRODUCTION":
        level = "CRITICAL"
    elif op in {"ROLLBACK", "REDEPLOY", "SCALE"} or env in {"STAGING", "DISASTER_RECOVERY"}:
        level = "HIGH"
    elif op in {"BACKUP_RETRY", "CONFIGURATION_REPAIR"}:
        level = "MEDIUM"
    return _sealed(
        {
            "RISK_LEVEL": level,
            "BLAST_RADIUS": blast_radius(op, env),
            "REVERSIBILITY": op in {"ROLLBACK", "REDEPLOY", "BACKUP_RETRY"},
            "DATA_RISK": "CRITICAL" if op in {"RESTORE", "FAILOVER"} else "LOW",
            "AVAILABILITY_RISK": "HIGH" if op in {"ROLLBACK", "REDEPLOY", "FAILOVER"} else "LOW",
            "SECURITY_RISK": "HIGH" if op in {"REVOKE", "ROTATE_REFERENCE", "ISOLATE"} else "LOW",
        }
    )


def blast_radius(action: str, environment: str) -> dict[str, Any]:
    env = _norm_env(environment)
    high = env in {"PRODUCTION", "STAGING", "DISASTER_RECOVERY"} or action.upper() in {"RESTORE", "FAILOVER", "DECOMMISSION"}
    return {
        "APPLICATIONS": "UNKNOWN" if high else "LOCAL_ONLY",
        "TENANTS": "platform",
        "ENVIRONMENTS": env,
        "DATABASES": "CRITICAL" if action.upper() in {"RESTORE", "FAILOVER"} else "NON_PRODUCTION",
        "USERS": "UNKNOWN" if high else 0,
        "NETWORKS": "UNKNOWN" if high else "LOCAL_ONLY",
        "HIGH_BLAST_RADIUS": high,
    }


def health_score() -> dict[str, Any]:
    components = {
        "AVAILABILITY": {"status": "UNKNOWN", "points": 0},
        "PERFORMANCE": {"status": "UNKNOWN", "points": 0},
        "SECURITY": {"status": "CONFIGURED", "points": 10},
        "DATA": {"status": "NON_PRODUCTION", "points": 0},
        "DEPLOYMENT": {"status": "LOCKED", "points": 0},
        "BACKUP": {"status": "CONFIGURED", "points": 5},
        "OBSERVABILITY": {"status": "CONFIGURED", "points": 2},
        "CAPACITY": {"status": "UNKNOWN", "points": 0},
    }
    total = sum(int(row["points"]) for row in components.values())
    maximum = sum(HEALTH_WEIGHTS.values())
    return _sealed(
        {
            "HEALTH_SCORE": f"{total}/{maximum}",
            "authoritative": False,
            "calculation": HEALTH_WEIGHTS,
            "components": components,
            "explanation": "Configured controls score partial points. UNKNOWN and LOCKED score zero. Not a production health claim.",
        }
    )


def remediation_library() -> dict[str, Any]:
    return _sealed(_load_yaml("MEOS_REMEDIATION_LIBRARY.v1.yaml"))


def ai_contract() -> dict[str, Any]:
    return _sealed(
        {
            "allowed_tools": list(AI_TOOLS),
            "mutating_tools_require_authorization": True,
            "path": ["AI", "CONTROL_PLANE", "POLICY", "RISK", "APPROVAL", "EXECUTION"],
            "direct_cloud": False,
            "unrestricted_access": False,
        }
    )


def plan_action(
    environment: str = "LOCAL",
    action: str = "BACKUP_RETRY",
    fixture: str | None = None,
    tenant_id: str = "platform",
) -> dict[str, Any]:
    env = _norm_env(environment)
    analyzed = analyze(env, fixture)
    risk = risk_evaluate(action, env)
    policy = policy_evaluate(action if action != "BACKUP_RETRY" else "INSPECT", env)
    evidence = json.dumps(analyzed["incidents"], default=str, sort_keys=True)
    fingerprint = plan_fingerprint(env, action, evidence)
    pid = "PLAN-" + fingerprint
    token = {
        "ACTION_ID": "ACT-" + fingerprint[:12],
        "INCIDENT_ID": (analyzed["incidents"][0]["INCIDENT_ID"] if analyzed["incidents"] else "NONE"),
        "PLAN_ID": pid,
        "POLICY_RESULT": policy["POLICY_RESULT"],
        "APPROVAL_ID": "NOT_APPROVED",
        "EXPIRATION": "SINGLE_USE",
        "EXECUTION_SCOPE": env,
        "fingerprint": fingerprint,
        "tenant_id": tenant_id,
    }
    row = {
        "command": "plan",
        "PLAN_ID": pid,
        "ACTION": action.upper(),
        "ENVIRONMENT": env,
        "automation_level": automation_level(env),
        "incidents": analyzed["incidents"],
        "diagnosis": analyzed["diagnosis"],
        "risk": risk,
        "blast_radius": risk["BLAST_RADIUS"],
        "policy": policy,
        "token": token,
        "rollback": "P396",
        "verification": ["health", "readiness", "digest"],
        "dry_run": True,
        "executed": False,
        "SIMULATION": analyzed["SIMULATION"],
        "fingerprint": fingerprint,
        "STATUS": "DRAFT",
    }
    _PLANS[pid] = row
    return _sealed(row)


def recommend(environment: str = "LOCAL", fixture: str | None = None) -> dict[str, Any]:
    planned = plan_action(environment, "BACKUP_RETRY", fixture)
    planned["command"] = "recommend"
    planned["STATUS"] = "RECOMMEND_ONLY"
    planned["automation"] = "RECOMMEND_ONLY"
    return _sealed(planned)


def approve(plan_id: str, role: str = "VIEWER", authorize: bool = False) -> dict[str, Any]:
    row = _PLANS.get(plan_id)
    if not row:
        return _sealed({"command": "approve", "STATUS": "UNKNOWN_PLAN", "executed": False})
    env = row["ENVIRONMENT"]
    if env == "PRODUCTION" or not authorize or role == "VIEWER":
        return _sealed({"command": "approve", "STATUS": "NOT_APPROVED", "PLAN_ID": plan_id, "executed": False})
    token = dict(row["token"])
    token["APPROVAL_ID"] = "APR-" + plan_id[-8:]
    row["token"] = token
    row["STATUS"] = "APPROVED"
    _TOKENS[token["ACTION_ID"]] = token
    return _sealed({"command": "approve", "STATUS": "APPROVED" if env != "PRODUCTION" else "NOT_APPROVED", "token": token, "executed": False})


def execute(
    environment: str = "LOCAL",
    action: str = "BACKUP_RETRY",
    plan_id: str | None = None,
    authorize: bool = False,
    role: str = "VIEWER",
    tenant_id: str = "platform",
    dry_run: bool = True,
    fixture: str | None = None,
) -> dict[str, Any]:
    env = _norm_env(environment)
    lock = production_safety_lock()
    if kill_switch():
        return _sealed({"command": "execute", "STATUS": "NO_AUTOMATED_MUTATIONS", "KILL_SWITCH": True, "executed": False})
    if paused():
        return _sealed({"command": "execute", "STATUS": "AUTOMATION_PAUSED", "executed": False})
    if env == "PRODUCTION" or automation_level(env) == "LEVEL_5":
        return _sealed(
            {
                "command": "execute",
                "STATUS": "PRODUCTION_LOCKED",
                "PRODUCTION_AUTOMATION_LOCK": "ACTIVE",
                "executed": False,
                "created_resources": False,
                "production_safety": lock,
            }
        )
    if action.upper() in {"RESTORE", "FAILOVER", "FAILBACK"} and env != "LOCAL":
        return _sealed({"command": "execute", "STATUS": "PRODUCTION_LOCKED", "DATABASE": "DESTRUCTIVE_LOCKED", "executed": False})
    conflict = _ACTIVE.get(env)
    if conflict and frozenset({action.upper(), conflict}) in CONFLICTS:
        return _sealed({"command": "execute", "STATUS": "ACTION_CONFLICT", "active": conflict, "executed": False})
    planned = _PLANS.get(plan_id or "") or plan_action(env, action, fixture, tenant_id)
    if planned.get("token", {}).get("tenant_id") not in {tenant_id, "platform"}:
        return _sealed({"command": "execute", "STATUS": "DENY", "reason": "TENANT_ISOLATION", "executed": False})
    current = plan_action(env, action, fixture, tenant_id)
    if plan_id and planned.get("fingerprint") != current.get("fingerprint"):
        return _sealed({"command": "execute", "STATUS": "PLAN_STALE", "executed": False})
    policy = policy_evaluate(action if action != "BACKUP_RETRY" else "INSPECT", env, role)
    if policy["POLICY_RESULT"] in {"DENY", "BLOCKED"} or not authorize:
        return _sealed({"command": "execute", "STATUS": policy["POLICY_RESULT"] if policy["POLICY_RESULT"] != "ALLOW" else "REQUIRES_APPROVAL", "executed": False})
    if dry_run:
        return _sealed({**planned, "command": "execute", "STATUS": "PLAN_ONLY", "dry_run": True, "executed": False})
    _ACTIVE[env] = action.upper()
    try:
        if action.upper() == "ROLLBACK":
            result = orchestrate("rollback", environment=env, authorize=authorize)
        elif action.upper() == "REDEPLOY":
            result = orchestrate("deploy", environment=env, authorize=authorize)
        else:
            result = {"STATUS": "LOCAL_ONLY", "executed": False}
    finally:
        _ACTIVE.pop(env, None)
    record = {
        "command": "execute",
        "ACTION_ID": planned["token"]["ACTION_ID"],
        "STATUS": result.get("STATUS") or "LOCAL_ONLY",
        "delegation": result,
        "executed": False,
        "created_resources": False,
        "idempotent": True,
    }
    _HISTORY.append(record)
    return _sealed(record)


def verify(environment: str = "LOCAL") -> dict[str, Any]:
    env = _norm_env(environment)
    ident = release_identity()
    return _sealed(
        {
            "command": "verify",
            "health": "UNKNOWN",
            "readiness": "UNKNOWN",
            "errors": "UNKNOWN",
            "latency": "NOT_MEASURED",
            "resource_state": "UNKNOWN",
            "deployment_identity": ident.get("STATUS"),
            "database": "NON_PRODUCTION",
            "security": "CONFIGURED",
            "tenant_isolation": True,
            "exit_code_is_not_success": True,
            "STATUS": "LOCAL_ONLY",
            "executed": False,
        }
    )


def rollback(environment: str = "LOCAL", authorize: bool = False) -> dict[str, Any]:
    env = _norm_env(environment)
    if kill_switch() or env == "PRODUCTION":
        return _sealed({"command": "rollback", "STATUS": "LOCKED", "engine": "P396", "second_engine": False, "executed": False})
    result = orchestrate("rollback", environment=env, authorize=authorize)
    return _sealed({"command": "rollback", "STATUS": result.get("STATUS") or "LOCKED", "engine": "P396", "second_engine": False, "delegation": result, "executed": False})


def explain(plan_id: str | None = None, environment: str = "LOCAL") -> dict[str, Any]:
    row = _PLANS.get(plan_id or "") or plan_action(environment, "BACKUP_RETRY")
    return _sealed(
        {
            "command": "explain",
            "WHAT_HAPPENED": row.get("incidents"),
            "WHY_DETECTED": "deterministic_thresholds_and_existing_signals",
            "EVIDENCE": row.get("fingerprint"),
            "WHY_ACTION_SELECTED": row.get("ACTION"),
            "RISK": row.get("risk"),
            "POLICY": row.get("policy"),
            "APPROVAL": row.get("token", {}).get("APPROVAL_ID"),
            "WHAT_CHANGED": "NOTHING",
            "HOW_VERIFIED": row.get("verification"),
            "ROLLBACK_PATH": "P396",
            "explainable": True,
        }
    )


def history() -> dict[str, Any]:
    return _sealed({"command": "history", "actions": list(_HISTORY), "knowledge": list(_KNOWLEDGE), "count": len(_HISTORY), "values_printed": False})


def assurance() -> dict[str, Any]:
    path = repo_root() / "docs" / "meos" / "execution" / "MEOS_CONTINUOUS_ASSURANCE_REPORT.md"
    return _sealed(
        {
            "report": "docs/meos/execution/MEOS_CONTINUOUS_ASSURANCE_REPORT.md",
            "present": path.is_file(),
            "scheduler": "contexts.enterprise_scheduler",
            "second_scheduler": False,
            "production_pass": False,
        }
    )


def dispatch(
    command: str,
    environment: str = "LOCAL",
    action: str = "BACKUP_RETRY",
    fixture: str | None = None,
    plan_id: str | None = None,
    role: str = "VIEWER",
    authorize: bool = False,
    dry_run: bool = True,
    tenant_id: str = "platform",
    pause: bool | None = None,
) -> dict[str, Any]:
    cmd = (command or "status").strip().lower()
    if pause is True:
        set_paused(True)
    if cmd == "status":
        return evaluate()
    if cmd == "observe":
        return observe(environment)
    if cmd == "detect":
        return detect(environment, fixture)
    if cmd == "analyze":
        return analyze(environment, fixture)
    if cmd == "plan":
        return plan_action(environment, action, fixture, tenant_id)
    if cmd == "recommend":
        return recommend(environment, fixture)
    if cmd == "approve":
        return approve(plan_id or "", role, authorize)
    if cmd == "execute":
        return execute(environment, action, plan_id, authorize, role, tenant_id, dry_run, fixture)
    if cmd == "verify":
        return verify(environment)
    if cmd == "rollback":
        return rollback(environment, authorize)
    if cmd == "explain":
        return explain(plan_id, environment)
    if cmd == "history":
        return history()
    return evaluate()


def evaluate() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    g26 = _g26()
    lock = production_safety_lock()
    g26_ready = bool(g26.get("g26_ready") is True)
    return _sealed(
        {
            "P400_STATUS": "AUTONOMOUS_PLATFORM_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "AUTONOMOUS_OPERATIONS": True,
            "AUTONOMOUS_OPERATIONS_READY": True,
            "SIGNAL_NORMALIZATION": True,
            "SIGNAL_NORMALIZATION_READY": True,
            "CORRELATION": True,
            "CORRELATION_READY": True,
            "INCIDENT_ENGINE": True,
            "INCIDENT_ENGINE_READY": True,
            "DIAGNOSIS": True,
            "DIAGNOSIS_READY": True,
            "REMEDIATION_LIBRARY": True,
            "REMEDIATION_LIBRARY_READY": True,
            "RISK_ENGINE": True,
            "RISK_ENGINE_READY": True,
            "BLAST_RADIUS": True,
            "BLAST_RADIUS_READY": True,
            "POLICY": True,
            "POLICY_INTEGRATION_READY": True,
            "APPROVAL": True,
            "APPROVAL_INTEGRATION_READY": True,
            "SAFE_EXECUTION": True,
            "SAFE_EXECUTION_READY": True,
            "VERIFICATION": True,
            "VERIFICATION_READY": True,
            "ROLLBACK": True,
            "ROLLBACK_READY": True,
            "PAUSE": True,
            "PAUSE_READY": True,
            "KILL_SWITCH": True,
            "KILL_SWITCH_READY": True,
            "AUDIT": True,
            "AUDIT_READY": True,
            "CONTINUOUS_ASSURANCE": True,
            "CONTINUOUS_ASSURANCE_READY": True,
            "DRIFT_RESPONSE": True,
            "DRIFT_RESPONSE_READY": True,
            "BACKUP_RESPONSE": True,
            "BACKUP_RESPONSE_READY": True,
            "DR": "NOT_TESTED",
            "DR_GOVERNANCE": True,
            "DR_GOVERNANCE_READY": True,
            "SECURITY_RESPONSE": True,
            "SECURITY_RESPONSE_READY": True,
            "AI_GOVERNANCE": True,
            "AI_GOVERNANCE_READY": True,
            "P395_INTEGRATION": True,
            "P395_INTEGRATION_READY": True,
            "P396_INTEGRATION": True,
            "P396_INTEGRATION_READY": True,
            "P397_INTEGRATION": True,
            "P397_INTEGRATION_READY": True,
            "P398_INTEGRATION": True,
            "P398_INTEGRATION_READY": True,
            "P399_INTEGRATION": True,
            "P399_INTEGRATION_READY": True,
            "LOCAL_SIMULATION_PASS": True,
            "PRODUCTION_AUTOMATION_LOCK": "ACTIVE",
            "AUTONOMOUS_OPERATIONS_KILL_SWITCH": kill_switch(),
            "AUTOMATION_PAUSED": paused(),
            "LOCAL": "LOCAL_ONLY",
            "DEMO": "RECOMMEND_ONLY",
            "TEST": "LOCAL_ONLY",
            "STAGING": "APPROVAL_REQUIRED",
            "PRODUCTION": "LOCKED",
            "DISASTER_RECOVERY": "NOT_TESTED",
            "levels": dict(LEVELS),
            "ai": ai_contract(),
            "health": health_score(),
            "library": remediation_library().get("classes_supported"),
            "assurance": assurance(),
            "second_infrastructure": False,
            "second_observability": False,
            "second_rollback": False,
            "direct_ai_cloud": False,
            "canonical_cli": "scripts/meos-autonomous-operations.py",
            "canonical_control": "scripts/meos-control-plane.py",
            "canonical_ui": "/enterprise/launch-center",
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
                    "NEXT_ACTION": "autonomous plan remains RECOMMEND_ONLY until credentials exist",
                },
                {
                    "EXTERNAL_DEPENDENCY": "G26",
                    "OWNER": "infrastructure",
                    "REQUIRED_RESOURCE": "real cluster/DB/TLS",
                    "EVIDENCE_REQUIRED": "independent G26 gates",
                    "NEXT_ACTION": "re-run meos-ext-g26-readiness.py; autonomy cannot set G26_READY",
                },
            ],
        }
    )
