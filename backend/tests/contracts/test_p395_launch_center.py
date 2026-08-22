"""P395 Launch Center must reuse the admin shell and never unlock production."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
LIB = REPO / "scripts" / "meos_p395.py"
CLI = REPO / "scripts" / "meos-launch-center.py"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
TENANT = REPO / "backend" / "contexts" / "crm" / "tests" / "test_crm_flow.py"
NAV = REPO / "frontend" / "shared" / "src" / "platform" / "applicationRegistry.ts"
PAGE = REPO / "frontend" / "apps" / "admin_portal" / "src" / "app" / "enterprise" / "launch-center" / "page.tsx"
UI = REPO / "frontend" / "apps" / "admin_portal" / "src" / "components" / "LaunchCenterPage.tsx"
CLIENT = REPO / "frontend" / "apps" / "admin_portal" / "src" / "lib" / "launchCenterClient.ts"
ROUTER = REPO / "backend" / "contexts" / "core_platform" / "presentation" / "launch_center_router.py"
STARTUP = REPO / "backend" / "core" / "presentation" / "api" / "startup_registry.py"
GATEWAY = REPO / "backend" / "core" / "gateway" / "route_registry.yaml"
FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")


def _load():
    spec = importlib.util.spec_from_file_location("meos_p395", LIB)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_p395_pointers_and_ui():
    assert PAGE.is_file()
    assert UI.is_file()
    assert CLIENT.is_file()
    assert ROUTER.is_file()
    assert CLI.is_file()
    assert (EXEC / "MEOS_LAUNCH_CENTER.v1.md").is_file()
    assert (EXEC / "MEOS_LAUNCH_CENTER_API.v1.yaml").is_file()
    nav = NAV.read_text(encoding="utf-8")
    assert 'id: "launch-center"' in nav
    assert 'href: "/enterprise/launch-center"' in nav
    startup = STARTUP.read_text(encoding="utf-8")
    assert "launch_center_router" in startup
    gateway = GATEWAY.read_text(encoding="utf-8")
    assert "/api/v1/launch-center" in gateway
    registry = yaml.safe_load((EXEC / "MEOS_APPLICATION_REGISTRY.v1.yaml").read_text(encoding="utf-8"))
    app = next(row for row in registry["applications"] if row["id"] == "launch_center")
    assert app["status"] == "IMPLEMENTED"
    assert app["status"] not in {"ACTIVE", "PRODUCTION_READY"}
    assert "/enterprise/launch-center" in app["routes"]
    assert not (REPO / "infra" / "terraform").is_dir()
    ui = UI.read_text(encoding="utf-8")
    client = CLIENT.read_text(encoding="utf-8")
    assert "GO LIVE" not in ui
    assert "Set P0" not in ui
    assert "COPY SECRET" not in ui
    assert "PRINT SECRET" not in ui
    assert "productionExecutionLocked" in client
    assert "redactSecretFields" in client
    assert "releaseSelectable" in client


def test_p395_evaluate_and_locks(monkeypatch):
    monkeypatch.setenv("G26_READY", "TRUE")
    monkeypatch.setenv("FORCE_PRODUCTION", "1")
    monkeypatch.setenv("MEOS_PRODUCTION_PROVIDER", "aws")
    mod = _load()
    data = mod.evaluate()
    assert data["P395_STATUS"] == "LAUNCH_CENTER_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED"
    for key in (
        "LAUNCH_CENTER_READY",
        "PROVIDER_CENTER_READY",
        "ENVIRONMENT_CENTER_READY",
        "LAUNCH_WIZARD_READY",
        "PLAN_VIEWER_READY",
        "RELEASE_SELECTOR_READY",
        "JOB_CENTER_READY",
        "RUNTIME_VIEW_READY",
        "DATABASE_CENTER_READY",
        "BACKUP_CENTER_READY",
        "RESTORE_CENTER_READY",
        "ROLLBACK_CENTER_READY",
        "OBSERVABILITY_CENTER_READY",
        "DRIFT_CENTER_READY",
        "SECURITY_CENTER_READY",
        "AUDIT_CENTER_READY",
        "RBAC_READY",
        "APPROVAL_WORKFLOW_READY",
        "PRODUCTION_LOCK_READY",
        "LOCAL_TESTS_PASS",
    ):
        assert data[key] is True
    assert data["PRODUCTION_LOCK"] == "ACTIVE"
    assert data["PRODUCTION"] == "LOCKED"
    assert data["STAGING"] == "STAGING_BLOCKED"
    assert data["DIGEST"] == "NOT_AVAILABLE"
    assert data["G26_READY"] is False
    assert data["P0"] == 1
    assert data["P313_REENTRY_READY"] is False
    assert data["GO_LIVE_AUTHORIZATION"] == "NOT_APPROVED"
    assert data["ACTIVE_APPLICATIONS"] == 0
    assert data["PRODUCTION_TRAFFIC"] == "NOT_ENABLED"
    assert data["go_live_button"] is False
    assert data["p0_override"] is False
    assert data["g26_override"] is False
    assert data["second_admin"] is False
    assert data["second_api"] is False
    assert data["secrets_shown"] is False
    assert data["copy_secret"] is False
    assert data["cost"]["TOTAL"] == "COST UNKNOWN"
    assert data["cost"]["zero_cost_invented"] is False
    assert data["releases"][0]["selectable"] is False
    assert data["releases"][0]["latest_rejected"] is True
    assert data["providers"]["AWS"]["status"] == "AUTHENTICATION_REQUIRED"
    assert data["regions"]["REGION_DISCOVERY"] == "BLOCKED"
    assert data["canonical_ui"] == "/enterprise/launch-center"
    assert data["canonical_api"] == "/api/v1/launch-center"
    lock = data["production_safety"]
    assert lock["deploy_allowed"] is False
    assert "provider" in data["wizard"]
    assert "authorization" in data["wizard"]
    assert "PLATFORM_ADMIN" in data["roles"]


def test_p395_cli_and_docs():
    status = subprocess.run(["python3", str(CLI)], cwd=REPO, capture_output=True, text=True)
    assert status.returncode == 2
    assert "P395_STATUS=LAUNCH_CENTER_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED" in status.stdout
    assert "G26_READY=FALSE" in status.stdout
    for marker in FORBIDDEN:
        assert marker not in status.stdout
    assert "P395" in MASTER.read_text(encoding="utf-8")
    assert "def test_crm_tenant_b_cannot_list_tenant_a_contacts" in TENANT.read_text(encoding="utf-8")
    manifest = yaml.safe_load((EXEC / "MEOS_RELEASE_MANIFEST.v1.yaml").read_text(encoding="utf-8"))
    assert manifest["p395_status"] == "LAUNCH_CENTER_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED"
    assert manifest["digest"] == "NOT_AVAILABLE"
    plat = yaml.safe_load((EXEC / "MEOS_PLATFORM_STATUS.v1.yaml").read_text(encoding="utf-8"))
    assert str(plat["phase"]).startswith(("P3", "P4"))
    assert plat["g26_ready"] is False
    guide = (EXEC / "MEOS_LAUNCH_CENTER.v1.md").read_text(encoding="utf-8")
    api = (EXEC / "MEOS_LAUNCH_CENTER_API.v1.yaml").read_text(encoding="utf-8")
    assert "PRODUCTION_READY" not in guide
    assert "PRODUCTION_READY" not in api
    assert "VALIDATION_ONLY" in api
    for path in (
        EXEC / "MEOS_LAUNCH_CENTER.v1.md",
        EXEC / "MEOS_LAUNCH_CENTER_API.v1.yaml",
        MASTER,
    ):
        assert "PRODUCTION_READY" not in path.read_text(encoding="utf-8")
