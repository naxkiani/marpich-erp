"""P390 infrastructure-on-demand overlay. No provision without auth. No Terraform fork."""
from __future__ import annotations

import importlib.util
import json
import os
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
from meos_p387 import provider  # noqa: E402
from meos_p388 import credential_preflight  # noqa: E402
from meos_release_engine import git_state, meos_release, repo_root  # noqa: E402

FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")
PROVIDERS = ("VPS", "AWS", "AZURE", "GCP", "KUBERNETES")
CLIS = {
    "AWS": "aws",
    "AZURE": "az",
    "GCP": "gcloud",
    "KUBERNETES": "kubectl",
    "VPS": "docker",
}
INFRA_COMMANDS = (
    "infra-status",
    "infra-discover",
    "infra-plan",
    "infra-dry-run",
    "infra-provision",
    "infra-verify",
    "environment-create",
    "environment-status",
    "environment-destroy",
)
PLAN_RESOURCES = (
    "NETWORK",
    "CLUSTER",
    "DATABASE",
    "STORAGE",
    "SECRET_MANAGER",
    "REGISTRY",
    "DNS",
    "TLS",
    "OBSERVABILITY",
    "BACKUP",
    "RESTORE",
    "ROLLBACK",
)


def _g26() -> dict[str, Any]:
    path = repo_root() / "scripts" / "meos-ext-g26-readiness.py"
    spec = importlib.util.spec_from_file_location("meos_p390_g26", path)
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


def _env_set(name: str) -> bool:
    value = os.environ.get(name, "").strip()
    return bool(value) and value not in {"CHANGE_ME", "NOT_AVAILABLE", "none"}


def credentials_expanded() -> dict[str, Any]:
    base = credential_preflight()
    extra = {
        "ACCOUNT": "NOT_VERIFIED" if _env_set("MEOS_CLOUD_ACCOUNT") else "MISSING",
        "REGION": "NOT_VERIFIED" if _env_set("MEOS_REGION") else "MISSING",
        "GHCR": "NOT_VERIFIED" if _env_set("GHCR_TOKEN") or _env_set("GITHUB_TOKEN") else "MISSING",
    }
    return _sealed({**base, **extra, "created": False, "written_to_repo": False})


def discover(name: str | None = None) -> dict[str, Any]:
    selected = provider()
    rows = {}
    for item in PROVIDERS:
        cli = CLIS[item]
        installed = shutil.which(cli) is not None
        if not installed:
            identity = "NOT_INSTALLED"
        elif item == "AWS" and _env_set("AWS_ACCESS_KEY_ID"):
            identity = "NOT_VERIFIED"
        elif item == "AZURE" and _env_set("AZURE_CLIENT_ID"):
            identity = "NOT_VERIFIED"
        elif item == "GCP" and _env_set("GOOGLE_APPLICATION_CREDENTIALS"):
            identity = "NOT_VERIFIED"
        elif item == "KUBERNETES" and _env_set("KUBECONFIG"):
            identity = "INVALID" if not Path(os.environ.get("KUBECONFIG", "")).expanduser().is_file() else "NOT_VERIFIED"
        elif item == "VPS" and _env_set("MEOS_VPS_HOST"):
            identity = "NOT_VERIFIED"
        else:
            identity = "UNAUTHENTICATED"
        rows[item] = {
            "CLI": "AVAILABLE" if installed else "NOT_INSTALLED",
            "identity": identity,
            "production": False,
            "authenticated": identity in {"AUTHENTICATED", "NOT_VERIFIED"},
        }
    requested = (name or "").strip().upper()
    return _sealed(
        {
            "PROVIDER": selected if not requested else ("REQUESTED_NOT_READY" if requested in PROVIDERS else "UNKNOWN"),
            "SELECTED": selected,
            "providers": rows,
            "cli_is_not_production": True,
            "values_printed": False,
        }
    )


def adapter(name: str, operation: str) -> dict[str, Any]:
    key = (name or "").strip().upper()
    op = (operation or "status").strip().lower()
    allowed = {"validate_credentials", "validate_account", "plan", "provision", "configure", "destroy", "status"}
    if key not in PROVIDERS:
        return _sealed({"PROVIDER": "NOT_SELECTED", "OPERATION": op, "STATUS": "NOT_SELECTED", "executed": False})
    if op not in allowed:
        return _sealed({"PROVIDER": key, "OPERATION": op, "STATUS": "INVALID", "executed": False})
    creds = credentials_expanded()
    authorized = os.environ.get("MEOS_AUTHORIZE_PROVISION", "").strip() == "1"
    executed = False
    provisioned = False
    status = "READY_FOR_CREDENTIALS"
    if op in {"provision", "destroy", "configure"}:
        status = "BLOCKED"
        if op == "destroy":
            status = "BLOCKED"
    return _sealed(
        {
            "PROVIDER": key,
            "OPERATION": op,
            "STATUS": status,
            "CREDENTIALS": creds["PROVIDER"],
            "authorized": authorized,
            "executed": executed,
            "provisioned": provisioned,
            "canonical": "scripts/meos-provider-bootstrap.py",
            "application_uses_provider_sdk": False,
        }
    )


def infra_plan(name: str | None = None, environment: str = "LOCAL", *, dry_run: bool = True) -> dict[str, Any]:
    selected = provider() if not name else (name or "").strip().upper()
    if selected not in PROVIDERS and selected not in {"NOT_SELECTED", "REQUESTED_NOT_READY"}:
        selected = "NOT_SELECTED"
    resources = {
        item: {
            "RESOURCE_ID": "NOT_PROVISIONED",
            "RESOURCE_TYPE": item,
            "PROVIDER": selected if selected in PROVIDERS else "NOT_SELECTED",
            "ENVIRONMENT": environment.upper(),
            "OWNER": "NOT_AVAILABLE",
            "STATUS": "READY_FOR_CREDENTIALS",
            "DEPENDENCIES": [],
            "EVIDENCE": "PLAN_ONLY",
        }
        for item in PLAN_RESOURCES
    }
    resources["REGISTRY"]["STATUS"] = "READY_FOR_CREDENTIALS"
    resources["REGISTRY"]["RESOURCE_ID"] = "ghcr.io/marpich/marpich-backend"
    resources["DATABASE"]["STATUS"] = "INVALID" if local_database_rejected() else "READY_FOR_CREDENTIALS"
    return _sealed(
        {
            "mode": "DRY_RUN" if dry_run else "PLAN",
            "PROVIDER": selected if selected in PROVIDERS else "NOT_SELECTED",
            "ENVIRONMENT": environment.upper(),
            "resources": resources,
            "estimated_monthly_cost": "NOT_AVAILABLE",
            "executed": False,
            "created_cloud_resources": False,
            "created_databases": False,
            "created_dns": False,
            "issued_certificates": False,
            "created_secrets": False,
            "deployed_applications": False,
            "terraform_for_meos": "FORBIDDEN",
            "existing_terraform": "STUB_identity-digital-twin",
        }
    )


def provision(*, authorize: bool = False, environment: str = "LOCAL", name: str | None = None) -> dict[str, Any]:
    plan = infra_plan(name, environment, dry_run=False)
    production = environment.upper() == "PRODUCTION"
    if not authorize or os.environ.get("MEOS_AUTHORIZE_PROVISION", "").strip() != "1":
        return _sealed({**plan, "PROVISIONED": False, "STATUS": "BLOCKED", "REASON": "HUMAN_AUTHORIZATION_REQUIRED", "executed": False})
    if production:
        return _sealed({**plan, "PROVISIONED": False, "STATUS": "BLOCKED", "REASON": "PRODUCTION_PROVISION_LOCKED", "executed": False})
    return _sealed({**plan, "PROVISIONED": False, "STATUS": "READY_FOR_CREDENTIALS", "REASON": "CREDENTIALS_MISSING", "executed": False})


def environment_factory(command: str, environment: str = "DEMO") -> dict[str, Any]:
    env = (environment or "DEMO").upper()
    cmd = (command or "status").lower()
    destroy_blocked = env in {"PRODUCTION", "STAGING"} and cmd == "destroy"
    return _sealed(
        {
            "command": cmd,
            "ENVIRONMENT": env,
            "STATUS": "BLOCKED" if destroy_blocked else ("READY_FOR_CREDENTIALS" if env in {"STAGING", "PRODUCTION"} else "LOCAL"),
            "executed": False,
            "destroyed": False,
            "production_destroy_blocked": destroy_blocked,
            "database_delete_blocked": env == "PRODUCTION",
            "canonical": "scripts/meos-environment-factory.py",
            "is_production": False,
        }
    )


def evaluate() -> dict[str, Any]:
    git = git_state()
    rel = meos_release()
    g26 = _g26()
    art = artifact_validate()
    lock = production_safety_lock()
    g26_ready = bool(g26.get("g26_ready") is True)
    return _sealed(
        {
            "P390_STATUS": "INFRASTRUCTURE_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "INFRASTRUCTURE_CONTROL": True,
            "INFRASTRUCTURE_CONTROL_READY": True,
            "PROVIDER_DISCOVERY": True,
            "PROVIDER_DISCOVERY_READY": True,
            "CREDENTIAL_PREFLIGHT": True,
            "CREDENTIAL_PREFLIGHT_READY": True,
            "INFRASTRUCTURE_PLAN": True,
            "INFRASTRUCTURE_PLAN_READY": True,
            "DRY_RUN": True,
            "DRY_RUN_READY": True,
            "PROVISIONING": "BLOCKED",
            "ENVIRONMENT_FACTORY": True,
            "ENVIRONMENT_FACTORY_READY": True,
            "MULTI_PLATFORM_READY": True,
            "PRODUCTION_LOCK": "ACTIVE",
            "NETWORK": "CONFIGURED",
            "CLUSTER": "NOT_AVAILABLE",
            "DATABASE": "NON_PRODUCTION",
            "SECRET_MANAGER": "CONFIGURED",
            "REGISTRY": "ghcr.io/marpich/marpich-backend",
            "DNS": "NOT_AVAILABLE",
            "TLS": "CONFIGURED",
            "OBSERVABILITY": "CONFIGURED",
            "RELEASE": "P354-RC-NOT_ELIGIBLE",
            "IMAGE": rel.get("image") or "meos/backend:p353-local",
            "DIGEST": art["IMAGE_DIGEST"],
            "DEPLOYMENT": "LOCKED",
            "RUNTIME": "LOCAL_VERIFIED",
            "BACKUP": "CONFIGURED",
            "RESTORE": "CONFIGURED",
            "ROLLBACK": "CONFIGURED",
            "KUBERNETES": "READY_FOR_CREDENTIALS",
            "VPS": "READY_FOR_CREDENTIALS",
            "AWS": "READY_FOR_CREDENTIALS",
            "AZURE": "READY_FOR_CREDENTIALS",
            "GCP": "READY_FOR_CREDENTIALS",
            "HOSTINGER_SHARED": "INCOMPATIBLE",
            "PROVIDER": provider(),
            "COMMIT": git.get("source_commit"),
            "terraform_for_meos": "FORBIDDEN",
            "second_architecture": False,
            "provisioned": False,
            "INFRASTRUCTURE_READY": False,
            "localhost_is_production": False,
            "compose_is_production": False,
            "self_signed_is_production": False,
            "dirty_sha_is_release": False,
            "cli_is_not_production": True,
            "secret_flag_is_not_proof": True,
            "cost_estimate": "NOT_AVAILABLE",
            "discovery": discover(),
            "plan": infra_plan(dry_run=True),
            "credentials": credentials_expanded(),
            "control_plane": "scripts/meos-control.py",
            "canonical_bootstrap": "scripts/meos-provider-bootstrap.py",
            "production_safety": lock,
            "PRODUCTION_DEPLOYMENT_LOCKED": True,
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
            "P389_STATUS": "CONTROL_PLANE_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED",
            "dependencies": [
                {"EXTERNAL_DEPENDENCY": "credentials", "OWNER": "NOT_AVAILABLE", "REQUIRED_RESOURCE": "authorized provider account", "STATUS": "MISSING", "EVIDENCE_REQUIRED": "validated identity", "NEXT_ACTION": "provider discovery then credential preflight"},
                {"EXTERNAL_DEPENDENCY": "image_digest", "OWNER": "NOT_AVAILABLE", "REQUIRED_RESOURCE": "CI GHCR digest", "STATUS": "NOT_AVAILABLE", "EVIDENCE_REQUIRED": "sha256 digest", "NEXT_ACTION": "clean tree then existing CI"},
                {"EXTERNAL_DEPENDENCY": "provider", "OWNER": "NOT_SELECTED", "REQUIRED_RESOURCE": "explicit MEOS_PRODUCTION_PROVIDER", "STATUS": "NOT_SELECTED", "EVIDENCE_REQUIRED": "P349 selection", "NEXT_ACTION": "do not infer AWS/Azure/GCP"},
                {"EXTERNAL_DEPENDENCY": "G26", "OWNER": "infrastructure", "REQUIRED_RESOURCE": "real cluster/DB/TLS", "STATUS": "BLOCKED", "EVIDENCE_REQUIRED": "independent G26 gates", "NEXT_ACTION": "provision only after human authorization then re-run G26"},
            ],
        }
    )


def dispatch_infra(command: str, *, target: str | None = None, environment: str = "LOCAL", authorize: bool = False) -> dict[str, Any]:
    command = (command or "infra-status").strip().lower()
    if command in {"infra-status", "infra-discover"}:
        return _sealed({"command": command, "discovery": discover(target), "evaluate": evaluate() if command == "infra-status" else {}})
    if command in {"infra-plan", "infra-dry-run"}:
        return _sealed({"command": command, **infra_plan(target, environment, dry_run=True)})
    if command == "infra-provision":
        return _sealed({"command": command, **provision(authorize=authorize, environment=environment, name=target)})
    if command == "infra-verify":
        return _sealed({"command": command, "PROVISIONED": False, "status": "READY_FOR_CREDENTIALS"})
    if command == "environment-create":
        return _sealed({"command": command, **environment_factory("create", environment)})
    if command == "environment-status":
        return _sealed({"command": command, **environment_factory("status", environment)})
    if command == "environment-destroy":
        return _sealed({"command": command, **environment_factory("destroy", environment)})
    return _sealed({"command": command, "STATUS": "UNKNOWN"})
