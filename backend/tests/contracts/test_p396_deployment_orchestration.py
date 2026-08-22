"""P396 orchestrator must reuse existing factories and never unlock production."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
LIB = REPO / "scripts" / "meos_p396.py"
CLI = REPO / "scripts" / "meos-deployment-orchestrator.py"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
TENANT = REPO / "backend" / "contexts" / "crm" / "tests" / "test_crm_flow.py"
CLIENT = REPO / "frontend" / "apps" / "admin_portal" / "src" / "lib" / "launchCenterClient.ts"
ROUTER = REPO / "backend" / "contexts" / "core_platform" / "presentation" / "launch_center_router.py"
FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")


def _load():
    spec = importlib.util.spec_from_file_location("meos_p396", LIB)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_p396_pointers():
    assert CLI.is_file()
    assert (EXEC / "MEOS_DEPLOYMENT_ORCHESTRATION.v1.md").is_file()
    assert (EXEC / "MEOS_DEPLOYMENT_STATE.v1.yaml").is_file()
    assert (REPO / "scripts" / "meos-deploy.py").is_file()
    assert (REPO / "scripts" / "meos-smoke-test.py").is_file()
    assert (REPO / ".github" / "workflows" / "identity-federation-enterprise.yml").is_file()
    assert not (REPO / "infra" / "terraform").is_dir()
    state = yaml.safe_load((EXEC / "MEOS_DEPLOYMENT_STATE.v1.yaml").read_text(encoding="utf-8"))
    assert state["second_cicd"] is False
    assert state["second_deployment_engine"] is False
    assert state["deployments"] == []
    assert state["environments"]["PRODUCTION"] == "LOCKED"
    assert "meos_p396" in ROUTER.read_text(encoding="utf-8")
    assert "/api/v1/launch-center/deployments/plan" in CLIENT.read_text(encoding="utf-8")


def test_p396_evaluate_and_locks(monkeypatch):
    monkeypatch.setenv("G26_READY", "TRUE")
    monkeypatch.setenv("FORCE_PRODUCTION", "1")
    monkeypatch.setenv("MEOS_PRODUCTION_PROVIDER", "aws")
    mod = _load()
    data = mod.evaluate()
    assert data["P396_STATUS"] == "DEPLOYMENT_ORCHESTRATION_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED"
    for key in (
        "DEPLOYMENT_ORCHESTRATOR_READY",
        "RELEASE_PIPELINE_READY",
        "DEPLOYMENT_STATE_MACHINE_READY",
        "DEPLOYMENT_LOCK_READY",
        "CI_INTEGRATION_READY",
        "GHCR_INTEGRATION_READY",
        "HELM_FLUX_INTEGRATION_READY",
        "DATABASE_MIGRATION_READY",
        "SECRET_RESOLUTION_READY",
        "NETWORK_VERIFICATION_READY",
        "RUNTIME_VERIFICATION_READY",
        "SMOKE_TEST_READY",
        "BACKUP_GATE_READY",
        "RESTORE_READY",
        "ROLLBACK_READY",
        "DRIFT_DETECTION_READY",
        "SECURITY_GATE_READY",
        "APPROVAL_READY",
        "AUDIT_READY",
        "LOCAL_REHEARSAL_PASS",
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
    assert data["second_cicd"] is False
    assert data["second_deployment_engine"] is False
    assert data["ci"]["CI_STATUS"] == "READY_FOR_CREDENTIALS"
    assert data["ci"]["published"] is False
    assert data["release"]["STATUS"] == "RELEASE_BLOCKED"
    assert data["release"]["latest_rejected"] is True
    assert data["illegal"]["FAILED_TO_READY"] is False
    assert mod.can_transition("CREATED", "PLANNED") is True
    assert mod.can_transition("FAILED", "READY") is False
    plan = mod.orchestrate("plan", provider_name="aws", environment="staging")
    assert plan["executed"] is False
    validate = mod.orchestrate("validate", provider_name="aws", environment="staging")
    assert validate["executed"] is False
    deploy = mod.orchestrate("deploy", provider_name="aws", environment="PRODUCTION")
    assert deploy["executed"] is False
    assert deploy["PRODUCTION_DEPLOYMENT"] == "LOCKED"
    rollback = mod.orchestrate("rollback", environment="PRODUCTION")
    assert rollback["executed"] is False
    assert rollback["STATUS"] == "LOCKED"
    dry = mod.orchestrate("deploy", provider_name="gcp", environment="staging")
    assert dry["executed"] is False
    assert dry["STATUS"] in {"AUTHENTICATION_REQUIRED", "RELEASE_BLOCKED"}
    first = mod.deployment_id("STAGING", "P354-RC-NOT_ELIGIBLE", "NOT_AVAILABLE")
    second = mod.deployment_id("STAGING", "P354-RC-NOT_ELIGIBLE", "NOT_AVAILABLE")
    assert first == second
    lock = data["production_safety"]
    assert lock["deploy_allowed"] is False


def test_p396_cli_and_docs():
    status = subprocess.run(["python3", str(CLI), "status"], cwd=REPO, capture_output=True, text=True)
    assert status.returncode == 2
    assert "P396_STATUS=DEPLOYMENT_ORCHESTRATION_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED" in status.stdout
    plan = subprocess.run(
        ["python3", str(CLI), "plan", "--provider", "aws", "--environment", "staging", "--release", "P354-RC-NOT_ELIGIBLE"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert plan.returncode == 2
    assert "executed=False" in plan.stdout
    deploy = subprocess.run(
        ["python3", str(CLI), "deploy", "--provider", "aws", "--environment", "PRODUCTION"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert deploy.returncode == 2
    assert "LOCKED" in deploy.stdout
    for marker in FORBIDDEN:
        assert marker not in status.stdout + plan.stdout + deploy.stdout
    assert "P396" in MASTER.read_text(encoding="utf-8")
    assert "def test_crm_tenant_b_cannot_list_tenant_a_contacts" in TENANT.read_text(encoding="utf-8")
    manifest = yaml.safe_load((EXEC / "MEOS_RELEASE_MANIFEST.v1.yaml").read_text(encoding="utf-8"))
    assert manifest["p396_status"] == "DEPLOYMENT_ORCHESTRATION_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED"
    assert manifest["digest"] == "NOT_AVAILABLE"
    plat = yaml.safe_load((EXEC / "MEOS_PLATFORM_STATUS.v1.yaml").read_text(encoding="utf-8"))
    assert str(plat["phase"]).startswith(("P3", "P4"))
    assert plat["g26_ready"] is False
    for path in (
        EXEC / "MEOS_DEPLOYMENT_ORCHESTRATION.v1.md",
        EXEC / "MEOS_DEPLOYMENT_STATE.v1.yaml",
        MASTER,
    ):
        assert "PRODUCTION_READY" not in path.read_text(encoding="utf-8")
