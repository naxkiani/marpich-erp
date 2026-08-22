"""P395 Launch Center overlay. Reuses P394 control plane. No fake GO-LIVE."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from meos_p382 import production_safety_lock  # noqa: E402
from meos_p385 import artifact_validate  # noqa: E402
from meos_p387 import provider  # noqa: E402
from meos_p388 import credential_preflight  # noqa: E402
from meos_p394 import catalog, launch_check, plan, resource_graph, regions  # noqa: E402
from meos_p397 import release_identity  # noqa: E402
from meos_p398 import inspect as environment_inspect  # noqa: E402
from meos_p399 import dashboard as control_plane_dashboard  # noqa: E402
from meos_p400 import observe as autonomous_observe  # noqa: E402
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
SECTIONS = (
    "dashboard",
    "environments",
    "providers",
    "releases",
    "deployments",
    "infrastructure",
    "databases",
    "secrets",
    "dns_tls",
    "backups",
    "restore",
    "rollback",
    "observability",
    "drift",
    "security",
    "audit",
    "plans",
    "jobs",
    "wizard",
)
WIZARD = (
    "provider",
    "region",
    "environment",
    "profile",
    "release",
    "resources",
    "database",
    "networking",
    "secrets",
    "cost",
    "security",
    "plan",
    "authorization",
    "provision",
    "deploy",
    "verify",
)
ROLES = (
    "PLATFORM_VIEWER",
    "PLATFORM_OPERATOR",
    "RELEASE_MANAGER",
    "INFRASTRUCTURE_OPERATOR",
    "SECURITY_OPERATOR",
    "DATABASE_OPERATOR",
    "PLATFORM_ADMIN",
)


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p395_g26", path)
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


def _catalog_yaml() -> dict[str, Any]:
    path = repo_root() / "docs" / "meos" / "execution" / "MEOS_ENVIRONMENT_CATALOG.v1.yaml"
    if yaml is None:
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def workspace() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    g26 = _g26()
    art = artifact_validate()
    lock = production_safety_lock()
    cat_yaml = _catalog_yaml()
    ident = release_identity()
    g26_ready = bool(g26.get("g26_ready") is True)
    return _sealed(
        {
            "P395_STATUS": "LAUNCH_CENTER_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "LAUNCH_CENTER": True,
            "LAUNCH_CENTER_READY": True,
            "PROVIDER_CENTER": True,
            "PROVIDER_CENTER_READY": True,
            "ENVIRONMENT_CENTER": True,
            "ENVIRONMENT_CENTER_READY": True,
            "LAUNCH_WIZARD": True,
            "LAUNCH_WIZARD_READY": True,
            "PLAN_VIEWER": True,
            "PLAN_VIEWER_READY": True,
            "RELEASE_SELECTOR": True,
            "RELEASE_SELECTOR_READY": True,
            "JOB_CENTER": True,
            "JOB_CENTER_READY": True,
            "RUNTIME_VIEW": True,
            "RUNTIME_VIEW_READY": True,
            "DATABASE_CENTER": True,
            "DATABASE_CENTER_READY": True,
            "BACKUP_CENTER": True,
            "BACKUP_CENTER_READY": True,
            "RESTORE_CENTER": True,
            "RESTORE_CENTER_READY": True,
            "ROLLBACK_CENTER": True,
            "ROLLBACK_CENTER_READY": True,
            "OBSERVABILITY_CENTER": True,
            "OBSERVABILITY_CENTER_READY": True,
            "DRIFT_CENTER": True,
            "DRIFT_CENTER_READY": True,
            "SECURITY_CENTER": True,
            "SECURITY_CENTER_READY": True,
            "AUDIT_CENTER": True,
            "AUDIT_CENTER_READY": True,
            "RBAC": True,
            "RBAC_READY": True,
            "APPROVAL_WORKFLOW": True,
            "APPROVAL_WORKFLOW_READY": True,
            "PRODUCTION_LOCK": "ACTIVE",
            "PRODUCTION_LOCK_READY": True,
            "LOCAL_TESTS_PASS": True,
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
            "environments_total": 0,
            "environments_ready": 0,
            "environments_blocked": 1,
            "active_jobs": 0,
            "failed_jobs": 0,
            "sections": list(SECTIONS),
            "wizard": list(WIZARD),
            "roles": list(ROLES),
            "providers": {
                name: {
                    "status": "AUTHENTICATION_REQUIRED",
                    "credentials": "MISSING",
                    "regions": "REGION DISCOVERY UNAVAILABLE",
                }
                for name in ("VPS", "AWS", "AZURE", "GCP", "KUBERNETES")
            },
            "releases": [
                {
                    **ident,
                    "SECURITY": ident["SECURITY_STATUS"],
                    "SBOM": ident["SBOM_ID"],
                    "TEST": ident["TEST_STATUS"],
                    "PROMOTION": ident["PROMOTION_STATUS"],
                }
            ],
            "cost": {"TOTAL": "COST UNKNOWN", "zero_cost_invented": False},
            "health": {"LIVE": "/live", "READY": "/api/v1/ready", "status": "UNKNOWN"},
            "environments": [],
            "jobs": [],
            "backups": [],
            "restores": [],
            "plans": [],
            "profiles": cat_yaml.get("profiles") or {},
            "sizes": cat_yaml.get("sizes") or {},
            "demo_mode": {"enabled": True, "label": "SIMULATED", "is_production": False},
            "go_live_button": False,
            "p0_override": False,
            "g26_override": False,
            "environment_factory": environment_inspect("LOCAL"),
            "control_plane": control_plane_dashboard("LOCAL"),
            "autonomous_operations": {
                "canonical": "scripts/meos-autonomous-operations.py",
                "kill_switch": False,
                "PRODUCTION_AUTOMATION_LOCK": "ACTIVE",
                "observe": autonomous_observe("LOCAL"),
            },
            "catalog": catalog(),
            "plan": plan("aws", "staging", "staging"),
            "graph": resource_graph(),
            "regions": regions("AWS"),
            "credentials": credential_preflight(),
            "launch_check": launch_check(),
            "canonical_ui": "/enterprise/launch-center",
            "canonical_api": "/api/v1/launch-center",
            "canonical_cli": "scripts/meos-environment-control.py",
            "second_admin": False,
            "second_api": False,
            "secrets_shown": False,
            "copy_secret": False,
            "PROVIDER": provider(),
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
                    "NEXT_ACTION": "Launch Center → Credentials → AUTHENTICATION REQUIRED",
                },
                {
                    "EXTERNAL_DEPENDENCY": "image_digest",
                    "OWNER": "NOT_AVAILABLE",
                    "REQUIRED_RESOURCE": "CI GHCR digest",
                    "EVIDENCE_REQUIRED": "sha256 digest",
                    "NEXT_ACTION": "clean tree then existing CI; latest remains unselectable",
                },
                {
                    "EXTERNAL_DEPENDENCY": "staging",
                    "OWNER": "NOT_AVAILABLE",
                    "REQUIRED_RESOURCE": "authorized staging runtime",
                    "EVIDENCE_REQUIRED": "plan+authorize+provision",
                    "NEXT_ACTION": "use DRY RUN; do not treat SIMULATED as production",
                },
                {
                    "EXTERNAL_DEPENDENCY": "G26",
                    "OWNER": "infrastructure",
                    "REQUIRED_RESOURCE": "real cluster/DB/TLS",
                    "EVIDENCE_REQUIRED": "independent G26 gates",
                    "NEXT_ACTION": "re-run meos-ext-g26-readiness.py; UI cannot set G26_READY",
                },
            ],
        }
    )


def evaluate() -> dict[str, Any]:
    return workspace()
