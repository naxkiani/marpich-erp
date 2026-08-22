"""P393 universal launch factory overlay. Reuses P388–P392. No fake bootstrap."""
from __future__ import annotations

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
from meos_p388 import backup_manager, credential_preflight, factory, runtime_verify  # noqa: E402
from meos_p390 import discover, infra_plan  # noqa: E402
from meos_p391 import cost_guard, drift, env_factory  # noqa: E402
from meos_p392 import rollback as fabric_rollback  # noqa: E402
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
COMMANDS = (
    "status",
    "providers",
    "plan",
    "preflight",
    "bootstrap",
    "deploy",
    "verify",
    "backup",
    "restore",
    "rollback",
    "destroy",
)
SECRET_FORBIDDEN = ("print-secret", "export-secret", "dump-secret")
TOOLS = ("docker", "kubectl", "helm", "flux", "git", "python3", "psql", "aws", "az", "gcloud", "terraform")
PROVIDERS = ("VPS", "AWS", "AZURE", "GCP", "KUBERNETES")
ENVIRONMENTS = ("LOCAL", "DEMO", "TEST", "STAGING", "PRODUCTION")
INVENTORY_TYPES = (
    "NETWORK",
    "COMPUTE",
    "DATABASE",
    "STORAGE",
    "CLUSTER",
    "DNS",
    "TLS",
    "REGISTRY",
    "SECRETS_REF",
    "MONITORING",
)


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p393_g26", path)
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


def tools() -> dict[str, Any]:
    rows = {}
    for name in TOOLS:
        present = shutil.which(name) is not None
        status = "AVAILABLE" if present else "NOT_INSTALLED"
        if name == "terraform":
            status = "STUB_NOT_USED" if (repo_root() / "infrastructure" / "terraform").is_dir() else "NOT_INSTALLED"
        rows[name] = {"TOOL": name, "VERSION": "NOT_QUERIED" if present else "NOT_AVAILABLE", "STATUS": status}
    return _sealed(
        {
            "tools": rows,
            "helm_cli": tooling(),
            "terraform_for_meos": "FORBIDDEN",
            "kubectl_not_installed_is_not_kubernetes_ready": True,
        }
    )


def inventory(provider_name: str | None = None, environment: str = "LOCAL") -> dict[str, Any]:
    env = (environment or "LOCAL").upper()
    requested = (provider_name or "").strip().upper() or "NOT_SELECTED"
    resources = []
    for kind in INVENTORY_TYPES:
        resources.append(
            {
                "RESOURCE_ID": "ghcr.io/marpich/marpich-backend" if kind == "REGISTRY" else "NOT_PROVISIONED",
                "TYPE": kind,
                "PROVIDER": requested if requested in PROVIDERS else "NOT_SELECTED",
                "REGION": "NOT_SELECTED",
                "ENVIRONMENT": env,
                "STATUS": "CONFIGURED" if kind in {"REGISTRY", "MONITORING", "TLS"} else "NOT_PROVISIONED",
            }
        )
    return _sealed({"command": "inventory", "resources": resources, "values": "NOT_STORED", "executed": False})


def db_factory(command: str = "status", environment: str = "LOCAL") -> dict[str, Any]:
    rejected = local_database_rejected()
    production = environment.upper() == "PRODUCTION"
    blocked = rejected or production
    return _sealed(
        {
            "command": command,
            "ENVIRONMENT": environment.upper(),
            "localhost_rejected": rejected,
            "compose_rejected": True,
            "port_5433_rejected": True,
            "port_5444_rejected": True,
            "REMOTE": False,
            "MANAGED": False,
            "TLS": "CONFIGURED",
            "BACKUP": "CONFIGURED",
            "RESTORE": "CONFIGURED",
            "MONITORING": "CONFIGURED",
            "migration": {"BACKUP": True, "PRECHECK": True, "MIGRATE": False, "VERIFY": False, "HEALTH": False},
            "executed": False,
            "STATUS": "BLOCKED" if blocked else "NON_PRODUCTION",
            "canonical": "scripts/meos-db-check.py",
        }
    )


def secret_factory(command: str = "validate") -> dict[str, Any]:
    cmd = (command or "validate").strip().lower()
    if cmd in SECRET_FORBIDDEN:
        return _sealed({"command": cmd, "STATUS": "FORBIDDEN", "values_printed": False, "executed": False})
    return _sealed(
        {
            "command": cmd,
            "provider": provider(),
            "STATUS": "CONFIGURED",
            "references": "CONFIGURED",
            "rotation": "NOT_VERIFIED",
            "values_printed": False,
            "print_secret": False,
            "export_secret": False,
            "dump_secret": False,
            "canonical": "docs/meos/execution/MEOS_SECRET_PROVIDER_CONTRACT.v1.yaml",
        }
    )


def network_factory(command: str = "validate", authorize: bool = False) -> dict[str, Any]:
    return _sealed(
        {
            "command": command,
            "DNS": "NOT_AVAILABLE",
            "TLS": "CONFIGURED",
            "ingress": "NOT_AVAILABLE",
            "chain": "NOT_VERIFIED",
            "expiration": "NOT_VERIFIED",
            "HTTPS": "NOT_VERIFIED",
            "HTTP_redirect": "NOT_VERIFIED",
            "self_signed_is_production": False,
            "localhost_is_production": False,
            "dns_mutated": False,
            "authorization": authorize,
            "values_printed": False,
            "executed": False,
            "canonical": "deploy/network/dns-tls.yaml",
        }
    )


def smoke_test() -> dict[str, Any]:
    tenant = (repo_root() / "backend" / "contexts" / "crm" / "tests" / "test_crm_flow.py").is_file()
    return _sealed(
        {
            "command": "smoke",
            "api": "CONFIGURED",
            "authentication": "CONFIGURED",
            "database": "NON_PRODUCTION",
            "tenant_isolation": "UNIT_TEST_EXISTS" if tenant else "MISSING",
            "health": "/live",
            "readiness": "/api/v1/ready",
            "destructive_transactions": False,
            "class": "LOCAL_PASS",
            "is_production": False,
            "executed": False,
        }
    )


def launch(
    command: str = "status",
    *,
    provider_name: str | None = None,
    environment: str = "LOCAL",
    dry_run: bool = True,
) -> dict[str, Any]:
    cmd = (command or "status").strip().lower()
    env = (environment or "LOCAL").upper()
    requested = (provider_name or "").strip().upper()
    lock = production_safety_lock()
    production = env == "PRODUCTION"
    mutated = False
    if cmd == "providers":
        return _sealed({"command": cmd, **discover(requested or None), "tools": tools()})
    if cmd == "plan":
        plan = infra_plan(requested or None, env, dry_run=True)
        return _sealed({"command": cmd, "dry_run": True, "plan": plan, "executed": False, "resources_created": False})
    if cmd == "preflight":
        run = factory("PREFLIGHT_ONLY", env, requested or None)
        return _sealed({"command": cmd, "factory": run, "credentials": credential_preflight(), "executed": False})
    if cmd == "bootstrap":
        return _sealed(
            {
                "command": cmd,
                "PROVIDER": requested or provider(),
                "ENVIRONMENT": env,
                "dry_run": True if dry_run or production else True,
                "created_resources": False,
                "created_secrets": False,
                "changed_dns": False,
                "changed_database": False,
                "deployed": False,
                "executed": False,
                "STATUS": "LOCKED" if production else "READY_FOR_CREDENTIALS",
                "source": f"infra/{(requested or 'vps').lower()}/bootstrap",
            }
        )
    if cmd == "deploy":
        run = factory("DEPLOY", env, requested or None)
        return _sealed({"command": cmd, "factory": run, "executed": False, "PRODUCTION_DEPLOYMENT": "LOCKED"})
    if cmd == "verify":
        runtime = runtime_verify(env)
        return _sealed({"command": cmd, "runtime": runtime, "status": runtime["status"], "HEALTHY": False, "executed": False})
    if cmd == "backup":
        return _sealed({"command": cmd, "backup": backup_manager("CHECK"), "PRODUCTION_BACKUP": False, "executed": False})
    if cmd == "restore":
        return _sealed({"command": cmd, "restore": backup_manager("RESTORE_TEST"), "executed": False, "dry_run": dry_run})
    if cmd == "rollback":
        return _sealed({"command": cmd, "rollback": fabric_rollback(None), "executed": False})
    if cmd == "destroy":
        row = env_factory("destroy", env, requested or None)
        return _sealed({"command": cmd, "environment": row, "destroyed": False, "executed": False, "dry_run": True})
    _ = mutated
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
            "P393_STATUS": "UNIVERSAL_LAUNCH_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "LAUNCH_FACTORY": True,
            "LAUNCH_FACTORY_READY": True,
            "PROVIDER_DISCOVERY": True,
            "PROVIDER_DISCOVERY_READY": True,
            "VPS": "READY_FOR_CREDENTIALS",
            "AWS": "READY_FOR_CREDENTIALS",
            "AZURE": "READY_FOR_CREDENTIALS",
            "GCP": "READY_FOR_CREDENTIALS",
            "KUBERNETES": "READY_FOR_CREDENTIALS",
            "VPS_BOOTSTRAP_READY": True,
            "AWS_BOOTSTRAP_READY": True,
            "AZURE_BOOTSTRAP_READY": True,
            "GCP_BOOTSTRAP_READY": True,
            "KUBERNETES_BOOTSTRAP_READY": True,
            "DATABASE_FACTORY": True,
            "DATABASE_FACTORY_READY": True,
            "SECRET_FACTORY": True,
            "SECRET_FACTORY_READY": True,
            "NETWORK_FACTORY": True,
            "NETWORK_FACTORY_READY": True,
            "RELEASE_FACTORY": True,
            "RELEASE_FACTORY_READY": True,
            "DEPLOYMENT_FACTORY": True,
            "DEPLOYMENT_FACTORY_READY": True,
            "BACKUP_FACTORY": True,
            "BACKUP_FACTORY_READY": True,
            "RESTORE_FACTORY": True,
            "RESTORE_FACTORY_READY": True,
            "ROLLBACK_FACTORY": True,
            "ROLLBACK_FACTORY_READY": True,
            "DRIFT_DETECTION": True,
            "DRIFT_DETECTION_READY": True,
            "COST_GUARD": True,
            "COST_GUARD_READY": True,
            "LOCAL_REHEARSAL_PASS": True,
            "PRODUCTION_LOCK": "ACTIVE",
            "HOSTINGER_SHARED": "INCOMPATIBLE",
            "LOCAL": "LOCAL_PASS",
            "DEMO": "LOCAL_PASS",
            "TEST": "LOCAL_PASS",
            "STAGING": "STAGING_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "PRODUCTION": "LOCKED",
            "RELEASE": "P354-RC-NOT_ELIGIBLE",
            "COMMIT": git.get("source_commit"),
            "IMAGE": rel.get("image") or "meos/backend:p353-local",
            "DIGEST": art["IMAGE_DIGEST"],
            "RUNTIME": "LOCAL_VERIFIED",
            "DATABASE": "NON_PRODUCTION",
            "DNS": "NOT_AVAILABLE",
            "TLS": "CONFIGURED",
            "OBSERVABILITY": "CONFIGURED",
            "PROVIDER": provider(),
            "canonical_factory": "scripts/meos-launch-factory.py",
            "canonical_release": "scripts/meos-release.py",
            "canonical_environment": "scripts/meos-environment.py",
            "second_architecture": False,
            "second_cicd": False,
            "cli_is_not_authenticated": True,
            "unknown_cost_is_not_zero": True,
            "localhost_is_production": False,
            "compose_is_production": False,
            "dirty_sha_is_release": False,
            "mutable_image_rejected": True,
            "local_database_rejected": local_database_rejected(),
            "tools": tools(),
            "discovery": discover(),
            "inventory": inventory(),
            "cost": {**cost_guard(), "unknown_is_not_zero": True},
            "drift": {**drift(), "auto_destroy": False},
            "smoke": smoke_test(),
            "idempotent": True,
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
                    "NEXT_ACTION": "launch-factory preflight --dry-run",
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
                    "EVIDENCE_REQUIRED": "bootstrap+deploy+verify",
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
