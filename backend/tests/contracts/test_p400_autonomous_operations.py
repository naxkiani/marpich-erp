"""P400 autonomy must stay policy-governed and never mutate production."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
LIB = REPO / "scripts" / "meos_p400.py"
CLI = REPO / "scripts" / "meos-autonomous-operations.py"
PLANE = REPO / "scripts" / "meos-control-plane.py"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
TENANT = REPO / "backend" / "contexts" / "crm" / "tests" / "test_crm_flow.py"
CENTER = REPO / "scripts" / "meos_p395.py"
ROUTER = REPO / "backend" / "contexts" / "core_platform" / "presentation" / "launch_center_router.py"
FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")


def _load():
    spec = importlib.util.spec_from_file_location("meos_p400", LIB)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_p400_pointers():
    assert CLI.is_file()
    assert PLANE.is_file()
    assert (EXEC / "MEOS_AUTONOMOUS_OPERATIONS.v1.md").is_file()
    assert (EXEC / "MEOS_REMEDIATION_LIBRARY.v1.yaml").is_file()
    assert (EXEC / "MEOS_CONTINUOUS_ASSURANCE_REPORT.md").is_file()
    assert not (REPO / "infra" / "terraform").is_dir()
    library = yaml.safe_load((EXEC / "MEOS_REMEDIATION_LIBRARY.v1.yaml").read_text(encoding="utf-8"))
    assert library["values"] == "NOT_STORED"
    assert library["second_rollback_engine"] is False
    assert library["classes_supported"]["ROLLBACK"]["engine"] == "P396"
    assert "meos_p400" in CENTER.read_text(encoding="utf-8")
    assert "/autonomous-operations" in ROUTER.read_text(encoding="utf-8")


def test_p400_evaluate_and_safety(monkeypatch):
    monkeypatch.setenv("G26_READY", "TRUE")
    monkeypatch.setenv("FORCE_PRODUCTION", "1")
    monkeypatch.setenv("MEOS_PRODUCTION_PROVIDER", "aws")
    mod = _load()
    data = mod.evaluate()
    assert data["P400_STATUS"] == "AUTONOMOUS_PLATFORM_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED"
    for key in (
        "AUTONOMOUS_OPERATIONS_READY",
        "SIGNAL_NORMALIZATION_READY",
        "CORRELATION_READY",
        "INCIDENT_ENGINE_READY",
        "DIAGNOSIS_READY",
        "REMEDIATION_LIBRARY_READY",
        "RISK_ENGINE_READY",
        "BLAST_RADIUS_READY",
        "POLICY_INTEGRATION_READY",
        "APPROVAL_INTEGRATION_READY",
        "SAFE_EXECUTION_READY",
        "VERIFICATION_READY",
        "ROLLBACK_READY",
        "PAUSE_READY",
        "KILL_SWITCH_READY",
        "AUDIT_READY",
        "CONTINUOUS_ASSURANCE_READY",
        "DRIFT_RESPONSE_READY",
        "BACKUP_RESPONSE_READY",
        "DR_GOVERNANCE_READY",
        "SECURITY_RESPONSE_READY",
        "AI_GOVERNANCE_READY",
        "P395_INTEGRATION_READY",
        "P396_INTEGRATION_READY",
        "P397_INTEGRATION_READY",
        "P398_INTEGRATION_READY",
        "P399_INTEGRATION_READY",
        "LOCAL_SIMULATION_PASS",
    ):
        assert data[key] is True
    assert data["PRODUCTION_AUTOMATION_LOCK"] == "ACTIVE"
    assert data["PRODUCTION"] == "LOCKED"
    assert data["G26_READY"] is False
    assert data["P0"] == 1
    assert data["P313_REENTRY_READY"] is False
    assert data["GO_LIVE_AUTHORIZATION"] == "NOT_APPROVED"
    assert data["ACTIVE_APPLICATIONS"] == 0
    assert data["direct_ai_cloud"] is False
    assert data["health"]["authoritative"] is False
    sim = mod.detect("LOCAL", fixture="cpu_anomaly")
    assert sim["SIMULATION"] is True
    assert sim["ai_invented"] is False
    assert all(row.get("SIMULATION") for row in sim["signals"] if row["SOURCE"] == "fixture")
    exe = mod.execute(environment="PRODUCTION", action="REDEPLOY", authorize=True, role="PLATFORM_ADMIN", dry_run=False)
    assert exe["executed"] is False
    assert exe["STATUS"] == "PRODUCTION_LOCKED"
    restore = mod.execute(environment="STAGING", action="RESTORE", authorize=True, role="PLATFORM_ADMIN", dry_run=False)
    assert restore["STATUS"] == "PRODUCTION_LOCKED"
    stale = mod.execute(environment="LOCAL", action="BACKUP_RETRY", plan_id="PLAN-missing", authorize=True, role="PLATFORM_ADMIN", dry_run=True)
    assert stale["STATUS"] in {"PLAN_STALE", "PLAN_ONLY", "UNKNOWN_PLAN", "REQUIRES_APPROVAL"}
    assert data["ai"]["direct_cloud"] is False
    assert "inspect_environment" in data["ai"]["allowed_tools"]
    assert "deploy_cloud" not in data["ai"]["allowed_tools"]
    tenant = mod.execute(environment="LOCAL", action="BACKUP_RETRY", tenant_id="tenant-b", authorize=True, role="PLATFORM_ADMIN")
    assert tenant["executed"] is False
    assert "def test_crm_tenant_b_cannot_list_tenant_a_contacts" in TENANT.read_text(encoding="utf-8")
    lock = data["production_safety"]
    assert lock["deploy_allowed"] is False


def test_p400_kill_switch_and_cli(monkeypatch):
    monkeypatch.setenv("MEOS_AUTONOMOUS_KILL_SWITCH", "1")
    mod = _load()
    killed = mod.execute(environment="LOCAL", action="BACKUP_RETRY", authorize=True, role="PLATFORM_ADMIN", dry_run=False)
    assert killed["STATUS"] == "NO_AUTOMATED_MUTATIONS"
    assert killed["executed"] is False
    status = subprocess.run(["python3", str(CLI), "status"], cwd=REPO, capture_output=True, text=True)
    assert status.returncode == 2
    assert "P400_STATUS=AUTONOMOUS_PLATFORM_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED" in status.stdout
    detect = subprocess.run(["python3", str(CLI), "detect", "--environment", "local", "--fixture", "health_failure"], cwd=REPO, capture_output=True, text=True)
    assert detect.returncode == 2
    assert "SIMULATION=true" in detect.stdout
    exe = subprocess.run(
        ["python3", str(CLI), "execute", "--environment", "PRODUCTION", "--action", "REDEPLOY", "--authorize"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert exe.returncode == 2
    assert "LOCKED" in exe.stdout or "NO_AUTOMATED_MUTATIONS" in exe.stdout
    for marker in FORBIDDEN:
        assert marker not in status.stdout + detect.stdout + exe.stdout
    assert "P400" in MASTER.read_text(encoding="utf-8")
    manifest = yaml.safe_load((EXEC / "MEOS_RELEASE_MANIFEST.v1.yaml").read_text(encoding="utf-8"))
    assert manifest["p400_status"] == "AUTONOMOUS_PLATFORM_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED"
    plat = yaml.safe_load((EXEC / "MEOS_PLATFORM_STATUS.v1.yaml").read_text(encoding="utf-8"))
    assert str(plat["phase"]).startswith(("P3", "P4"))
    assert plat["g26_ready"] is False
    for path in (
        EXEC / "MEOS_AUTONOMOUS_OPERATIONS.v1.md",
        EXEC / "MEOS_REMEDIATION_LIBRARY.v1.yaml",
        EXEC / "MEOS_CONTINUOUS_ASSURANCE_REPORT.md",
        MASTER,
    ):
        assert "PRODUCTION_READY" not in path.read_text(encoding="utf-8")
