"""P398 Environment Factory must reuse P364/P390/P394 and never provision production."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
LIB = REPO / "scripts" / "meos_p398.py"
CLI = REPO / "scripts" / "meos-environment-factory.py"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
TENANT = REPO / "backend" / "contexts" / "crm" / "tests" / "test_crm_flow.py"
ORCH = REPO / "scripts" / "meos_p396.py"
CENTER = REPO / "scripts" / "meos_p395.py"
FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")


def _load():
    spec = importlib.util.spec_from_file_location("meos_p398", LIB)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_p398_pointers():
    assert CLI.is_file()
    assert (REPO / "scripts" / "meos-environment-control.py").is_file()
    assert (EXEC / "MEOS_ENVIRONMENT_FACTORY.v1.md").is_file()
    assert (EXEC / "MEOS_ENVIRONMENT_SPEC.v1.yaml").is_file()
    assert (EXEC / "MEOS_ENVIRONMENT_PROVIDER_MATRIX.v1.yaml").is_file()
    assert (EXEC / "MEOS_ENVIRONMENT_CONTRACT.v1.md").is_file()
    assert (EXEC / "MEOS_ENVIRONMENT_CONTRACT.v1.yaml").is_file()
    assert not (REPO / "infra" / "terraform").is_dir()
    spec = yaml.safe_load((EXEC / "MEOS_ENVIRONMENT_SPEC.v1.yaml").read_text(encoding="utf-8"))
    assert spec["terraform_for_meos"] == "FORBIDDEN"
    assert spec["values"] == "NOT_STORED"
    matrix = yaml.safe_load((EXEC / "MEOS_ENVIRONMENT_PROVIDER_MATRIX.v1.yaml").read_text(encoding="utf-8"))
    assert matrix["providers"]["AWS"]["status"] == "READY_FOR_CREDENTIALS"
    assert matrix["providers"]["KUBERNETES"]["status"] == "READY_FOR_CREDENTIALS"
    assert "environment_inspect" in ORCH.read_text(encoding="utf-8")
    assert "environment_inspect" in CENTER.read_text(encoding="utf-8")


def test_p398_evaluate_and_locks(monkeypatch):
    monkeypatch.setenv("G26_READY", "TRUE")
    monkeypatch.setenv("FORCE_PRODUCTION", "1")
    monkeypatch.setenv("MEOS_PRODUCTION_PROVIDER", "aws")
    mod = _load()
    data = mod.evaluate()
    assert data["P398_STATUS"] == "ENVIRONMENT_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED"
    for key in (
        "ENVIRONMENT_FACTORY_READY",
        "ENVIRONMENT_SPEC_READY",
        "PROVIDER_ABSTRACTION_READY",
        "PROVIDER_MATRIX_READY",
        "CONFIGURATION_FACTORY_READY",
        "NETWORK_PLAN_READY",
        "DATABASE_PLAN_READY",
        "SECRET_REFERENCE_READY",
        "DNS_TLS_PLAN_READY",
        "OBSERVABILITY_PLAN_READY",
        "BOOTSTRAP_READY",
        "IDEMPOTENCY_READY",
        "LOCKING_READY",
        "DRIFT_DETECTION_READY",
        "SNAPSHOT_READY",
        "DESTROY_PROTECTION_READY",
        "REPRODUCTION_READY",
        "P396_INTEGRATION_READY",
        "P397_INTEGRATION_READY",
        "P395_INTEGRATION_READY",
        "LOCAL_REHEARSAL_PASS",
    ):
        assert data[key] is True
    assert data["PRODUCTION_LOCK"] == "ACTIVE"
    assert data["PRODUCTION"] == "LOCKED"
    assert data["terraform_for_meos"] == "FORBIDDEN"
    assert data["G26_READY"] is False
    assert data["P0"] == 1
    assert data["P313_REENTRY_READY"] is False
    assert data["GO_LIVE_AUTHORIZATION"] == "NOT_APPROVED"
    assert data["ACTIVE_APPLICATIONS"] == 0
    assert data["COST_ESTIMATE_UNAVAILABLE"] is True
    missing = mod.adapter(None)
    assert missing["STATUS"] == "ENVIRONMENT_PROVISIONING_BLOCKED"
    unsupported = mod.adapter("OPENSTACK")
    assert unsupported["STATUS"] == "PROVIDER_UNSUPPORTED"
    plan = mod.factory("plan", environment="staging", provider_name="aws")
    assert plan["executed"] is False
    assert plan["zero_cost_invented"] is False
    first = mod.plan_id("STAGING", "AWS")
    second = mod.plan_id("STAGING", "AWS")
    assert first == second
    boot = mod.factory("bootstrap", environment="PRODUCTION", provider_name="aws")
    assert boot["executed"] is False
    assert boot["PRODUCTION_PROVISIONING"] == "LOCKED"
    aws = mod.factory("bootstrap", environment="staging", provider_name="aws")
    assert aws["STATUS"] == "READY_FOR_CREDENTIALS"
    assert aws["executed"] is False
    destroy = mod.factory("destroy-plan", environment="PRODUCTION", provider_name="aws")
    assert destroy["destroyed"] is False
    assert destroy["production_destroy"] == "FORBIDDEN"
    lock = data["production_safety"]
    assert lock["deploy_allowed"] is False


def test_p398_cli_p364_compat_and_docs():
    legacy = subprocess.run(["python3", str(CLI)], cwd=REPO, capture_output=True, text=True)
    assert legacy.returncode == 0
    assert "ENVIRONMENT_FACTORY=REFERENCE_ONLY" in legacy.stdout
    status = subprocess.run(["python3", str(CLI), "status"], cwd=REPO, capture_output=True, text=True)
    assert status.returncode == 2
    assert "P398_STATUS=ENVIRONMENT_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED" in status.stdout
    plan = subprocess.run(
        ["python3", str(CLI), "plan", "--environment", "staging", "--provider", "aws"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert plan.returncode == 2
    assert "executed=False" in plan.stdout
    destroy = subprocess.run(
        ["python3", str(CLI), "destroy-plan", "--environment", "PRODUCTION", "--provider", "aws"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert destroy.returncode == 2
    assert "LOCKED" in destroy.stdout or "FORBIDDEN" in destroy.stdout
    for marker in FORBIDDEN:
        assert marker not in legacy.stdout + status.stdout + plan.stdout + destroy.stdout
    assert "P398" in MASTER.read_text(encoding="utf-8")
    assert "def test_crm_tenant_b_cannot_list_tenant_a_contacts" in TENANT.read_text(encoding="utf-8")
    manifest = yaml.safe_load((EXEC / "MEOS_RELEASE_MANIFEST.v1.yaml").read_text(encoding="utf-8"))
    assert manifest["p398_status"] == "ENVIRONMENT_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED"
    plat = yaml.safe_load((EXEC / "MEOS_PLATFORM_STATUS.v1.yaml").read_text(encoding="utf-8"))
    assert str(plat["phase"]).startswith(("P3", "P4"))
    assert plat["g26_ready"] is False
    for path in (
        EXEC / "MEOS_ENVIRONMENT_FACTORY.v1.md",
        EXEC / "MEOS_ENVIRONMENT_SPEC.v1.yaml",
        EXEC / "MEOS_ENVIRONMENT_CONTRACT.v1.md",
        MASTER,
    ):
        assert "PRODUCTION_READY" not in path.read_text(encoding="utf-8")
