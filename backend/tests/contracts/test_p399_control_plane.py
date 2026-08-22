"""P399 Control Plane must orchestrate P395–P398 and never mutate production."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
LIB = REPO / "scripts" / "meos_p399.py"
CLI = REPO / "scripts" / "meos-control-plane.py"
OPERATOR = REPO / "scripts" / "meos-control.py"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
TENANT = REPO / "backend" / "contexts" / "crm" / "tests" / "test_crm_flow.py"
CENTER = REPO / "scripts" / "meos_p395.py"
ORCH = REPO / "scripts" / "meos_p396.py"
ROUTER = REPO / "backend" / "contexts" / "core_platform" / "presentation" / "launch_center_router.py"
FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")


def _load():
    spec = importlib.util.spec_from_file_location("meos_p399", LIB)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_p399_pointers():
    assert CLI.is_file()
    assert OPERATOR.is_file()
    assert (EXEC / "MEOS_CONTROL_PLANE.v1.md").is_file()
    assert (EXEC / "MEOS_RESOURCE_CATALOG.v1.yaml").is_file()
    assert not (REPO / "infra" / "terraform").is_dir()
    catalog = yaml.safe_load((EXEC / "MEOS_RESOURCE_CATALOG.v1.yaml").read_text(encoding="utf-8"))
    assert catalog["values"] == "NOT_STORED"
    assert catalog["terraform_for_meos"] == "FORBIDDEN"
    assert catalog["second_deployment_engine"] is False
    assert "UNKNOWN" in catalog["states"]
    router = ROUTER.read_text(encoding="utf-8")
    assert "/control-plane" in router
    assert "meos_p399" in CENTER.read_text(encoding="utf-8")
    assert "orchestrate" in LIB.read_text(encoding="utf-8")
    assert "environment_inspect" in ORCH.read_text(encoding="utf-8")


def test_p399_evaluate_and_locks(monkeypatch):
    monkeypatch.setenv("G26_READY", "TRUE")
    monkeypatch.setenv("FORCE_PRODUCTION", "1")
    monkeypatch.setenv("MEOS_PRODUCTION_PROVIDER", "aws")
    mod = _load()
    data = mod.evaluate()
    assert data["P399_STATUS"] == "CONTROL_PLANE_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED"
    for key in (
        "CONTROL_PLANE_READY",
        "RESOURCE_CATALOG_READY",
        "RESOURCE_GRAPH_READY",
        "ENVIRONMENT_CATALOG_READY",
        "RELEASE_CATALOG_READY",
        "PROVIDER_CATALOG_READY",
        "POLICY_INTEGRATION_READY",
        "PLAN_ENGINE_READY",
        "CHANGE_MANAGEMENT_READY",
        "RBAC_READY",
        "AUDIT_READY",
        "EVENTS_READY",
        "NOTIFICATIONS_READY",
        "DRIFT_READY",
        "COST_READY",
        "CAPACITY_READY",
        "SECURITY_READY",
        "BACKUP_CENTER_READY",
        "RESTORE_CENTER_READY",
        "DR_CENTER_READY",
        "P395_INTEGRATION_READY",
        "P396_INTEGRATION_READY",
        "P397_INTEGRATION_READY",
        "P398_INTEGRATION_READY",
        "LOCAL_REHEARSAL_PASS",
    ):
        assert data[key] is True
    assert data["PRODUCTION_LOCK"] == "ACTIVE"
    assert data["PRODUCTION"] == "LOCKED"
    assert data["G26_READY"] is False
    assert data["P0"] == 1
    assert data["P313_REENTRY_READY"] is False
    assert data["GO_LIVE_AUTHORIZATION"] == "NOT_APPROVED"
    assert data["ACTIVE_APPLICATIONS"] == 0
    assert data["COST_NOT_AVAILABLE"] is True
    assert data["zero_cost_invented"] is False
    assert data["second_deployment_engine"] is False
    assert data["providers"]["authorization_from_name"] is False
    graph = data["graph"]
    assert graph["application_path"][0] == "APPLICATION"
    assert graph["application_path"][-1] == "STORAGE"
    assert any(edge["from"] == "DOMAIN" and edge["to"] == "TLS" for edge in graph["edges"])
    deny = mod.policy_evaluate("DEPLOY_RELEASE", "PRODUCTION", "VIEWER")
    assert deny["POLICY_RESULT"] == "DENY"
    blocked = mod.policy_evaluate("DESTROY", "PRODUCTION", "PLATFORM_ADMIN")
    assert blocked["POLICY_RESULT"] == "BLOCKED"
    plan = mod.dispatch("plan", environment="staging", provider_name="aws", operation="CREATE_ENVIRONMENT", role="INFRASTRUCTURE_OPERATOR")
    assert plan["executed"] is False
    assert plan["cost"] == "COST_NOT_AVAILABLE"
    first = mod.plan_id("CREATE_ENVIRONMENT", "STAGING", "AWS")
    second = mod.plan_id("CREATE_ENVIRONMENT", "STAGING", "AWS")
    assert first == second
    exe = mod.dispatch("execute", environment="PRODUCTION", provider_name="aws", operation="DEPLOY_RELEASE", role="PLATFORM_ADMIN", authorize=True)
    assert exe["executed"] is False
    assert exe["STATUS"] == "LOCKED"
    dry = mod.dispatch("execute", environment="LOCAL", provider_name="vps", operation="CREATE_ENVIRONMENT", dry_run=True, role="INFRASTRUCTURE_OPERATOR", authorize=True)
    assert dry["executed"] is False
    drift = mod.dispatch("drift")
    assert drift["auto_repair"] is False
    search = mod.search("database", tenant_id="tenant-b")
    assert search["cross_tenant"] is False
    assert search["count"] == 0
    cost = mod.dispatch("cost")
    assert cost["COST_NOT_AVAILABLE"] is True
    health = mod.dispatch("health")
    assert health["verified"] is False
    lock = data["production_safety"]
    assert lock["deploy_allowed"] is False


def test_p399_cli_and_docs():
    status = subprocess.run(["python3", str(CLI), "status"], cwd=REPO, capture_output=True, text=True)
    assert status.returncode == 2
    assert "P399_STATUS=CONTROL_PLANE_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED" in status.stdout
    inventory = subprocess.run(["python3", str(CLI), "inventory", "--environment", "local"], cwd=REPO, capture_output=True, text=True)
    assert inventory.returncode == 2
    assert "RESOURCE_ID" in inventory.stdout
    plan = subprocess.run(
        ["python3", str(CLI), "plan", "--environment", "staging", "--provider", "aws", "--operation", "CREATE_ENVIRONMENT", "--dry-run"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert plan.returncode == 2
    assert "executed=False" in plan.stdout
    exe = subprocess.run(
        ["python3", str(CLI), "execute", "--environment", "PRODUCTION", "--provider", "aws", "--operation", "DEPLOY_RELEASE", "--authorize"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert exe.returncode == 2
    assert "LOCKED" in exe.stdout
    for marker in FORBIDDEN:
        assert marker not in status.stdout + inventory.stdout + plan.stdout + exe.stdout
    assert "P399" in MASTER.read_text(encoding="utf-8")
    assert "def test_crm_tenant_b_cannot_list_tenant_a_contacts" in TENANT.read_text(encoding="utf-8")
    manifest = yaml.safe_load((EXEC / "MEOS_RELEASE_MANIFEST.v1.yaml").read_text(encoding="utf-8"))
    assert manifest["p399_status"] == "CONTROL_PLANE_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED"
    plat = yaml.safe_load((EXEC / "MEOS_PLATFORM_STATUS.v1.yaml").read_text(encoding="utf-8"))
    assert str(plat["phase"]).startswith(("P3", "P4"))
    assert plat["g26_ready"] is False
    for path in (
        EXEC / "MEOS_CONTROL_PLANE.v1.md",
        EXEC / "MEOS_RESOURCE_CATALOG.v1.yaml",
        MASTER,
    ):
        assert "PRODUCTION_READY" not in path.read_text(encoding="utf-8")
