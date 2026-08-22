"""P397 Release Factory must reuse existing supply chain and never invent a digest."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
LIB = REPO / "scripts" / "meos_p397.py"
CLI = REPO / "scripts" / "meos-release-factory.py"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
TENANT = REPO / "backend" / "contexts" / "crm" / "tests" / "test_crm_flow.py"
CLIENT = REPO / "frontend" / "apps" / "admin_portal" / "src" / "lib" / "launchCenterClient.ts"
UI = REPO / "frontend" / "apps" / "admin_portal" / "src" / "components" / "LaunchCenterPage.tsx"
ORCH = REPO / "scripts" / "meos_p396.py"
FORBIDDEN = ("BEGIN PRIVATE", "BEGIN RSA", "AKIA", "AWS_SECRET_ACCESS_KEY=")


def _load():
    spec = importlib.util.spec_from_file_location("meos_p397", LIB)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_p397_pointers():
    assert CLI.is_file()
    assert (REPO / "scripts" / "meos-release.py").is_file()
    assert (EXEC / "MEOS_RELEASE_FACTORY.v1.md").is_file()
    assert (EXEC / "MEOS_RELEASE_COMPATIBILITY.v1.yaml").is_file()
    assert (REPO / ".github" / "workflows" / "identity-federation-enterprise.yml").is_file()
    assert not (REPO / "infra" / "terraform").is_dir()
    matrix = yaml.safe_load((EXEC / "MEOS_RELEASE_COMPATIBILITY.v1.yaml").read_text(encoding="utf-8"))
    assert matrix["digest"] == "NOT_AVAILABLE"
    assert matrix["environments"]["PRODUCTION"]["status"] == "BLOCKED"
    assert matrix["rebuild_on_promote"] is False
    manifest = yaml.safe_load((EXEC / "MEOS_RELEASE_MANIFEST.v1.yaml").read_text(encoding="utf-8"))
    assert manifest["version"] == "0.1.0"
    assert manifest["version_authority"] == "backend/pyproject.toml"
    assert manifest["digest"] == "NOT_AVAILABLE"
    assert "release_identity" in ORCH.read_text(encoding="utf-8")
    assert "VERSION" in UI.read_text(encoding="utf-8")
    assert "PROMOTION" in CLIENT.read_text(encoding="utf-8")


def test_p397_evaluate_and_locks(monkeypatch):
    monkeypatch.setenv("G26_READY", "TRUE")
    monkeypatch.setenv("FORCE_PRODUCTION", "1")
    mod = _load()
    data = mod.evaluate()
    assert data["P397_STATUS"] == "RELEASE_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED"
    for key in (
        "RELEASE_FACTORY_READY",
        "VERSION_GOVERNANCE_READY",
        "CLEAN_TREE_GATE_READY",
        "BUILD_REPRODUCIBILITY_READY",
        "IMAGE_PIPELINE_READY",
        "SBOM_READY",
        "SECURITY_GATE_READY",
        "PROVENANCE_READY",
        "REGISTRY_INTEGRATION_READY",
        "RELEASE_MANIFEST_READY",
        "COMPATIBILITY_MATRIX_READY",
        "PROMOTION_READY",
        "APPROVAL_READY",
        "REVOCATION_READY",
        "ROLLBACK_RELEASE_READY",
        "RELEASE_HISTORY_READY",
        "LAUNCH_CENTER_INTEGRATION_READY",
        "DEPLOYMENT_INTEGRATION_READY",
        "LOCAL_REHEARSAL_PASS",
    ):
        assert data[key] is True
    assert data["PRODUCTION_RELEASE_LOCK"] == "ACTIVE"
    assert data["PRODUCTION"] == "LOCKED"
    assert data["VERSION"] == "0.1.0"
    assert data["IMAGE_DIGEST"] == "NOT_AVAILABLE"
    assert data["G26_READY"] is False
    assert data["P0"] == 1
    assert data["P313_REENTRY_READY"] is False
    assert data["GO_LIVE_AUTHORIZATION"] == "NOT_APPROVED"
    assert data["ACTIVE_APPLICATIONS"] == 0
    assert data["second_cicd"] is False
    assert data["published"] is False
    assert data["sbom_scanned"] is False
    assert data["signature_faked"] is False
    assert data["rebuild_on_promote"] is False
    assert data["release"]["STATUS"] == "RELEASE_BLOCKED"
    assert data["release"]["REASON"] == "DIRTY_TREE"
    assert data["version_authority"]["source"] == "backend/pyproject.toml"
    validate = mod.factory("validate")
    assert validate["TREE_STATE"] == "DIRTY"
    assert validate["executed"] is False
    build = mod.factory("build")
    assert build["STATUS"] == "BUILD_BLOCKED"
    assert build["executed"] is False
    promote = mod.factory("promote", source="staging", target="production")
    assert promote["executed"] is False
    assert promote["rebuild"] is False
    assert promote["PRODUCTION_PROMOTION"] == "LOCKED"
    revoke = mod.factory("revoke")
    assert revoke["STATUS"] == "REVOKED"
    assert revoke["deployable"] is False
    assert revoke["published"] is False
    ident = mod.release_identity()
    assert ident["REVOKED"] is True
    lock = data["production_safety"]
    assert lock["deploy_allowed"] is False
    mod._REVOKED.clear()


def test_p397_cli_and_docs():
    status = subprocess.run(["python3", str(CLI), "status"], cwd=REPO, capture_output=True, text=True)
    assert status.returncode == 2
    assert "P397_STATUS=RELEASE_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED" in status.stdout
    assert "VERSION=0.1.0" in status.stdout
    plan = subprocess.run(["python3", str(CLI), "plan"], cwd=REPO, capture_output=True, text=True)
    assert plan.returncode == 2
    assert "executed=False" in plan.stdout
    promote = subprocess.run(
        ["python3", str(CLI), "promote", "--from", "staging", "--to", "production"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert promote.returncode == 2
    assert "LOCKED" in promote.stdout
    for marker in FORBIDDEN:
        assert marker not in status.stdout + plan.stdout + promote.stdout
    assert "P397" in MASTER.read_text(encoding="utf-8")
    assert "def test_crm_tenant_b_cannot_list_tenant_a_contacts" in TENANT.read_text(encoding="utf-8")
    manifest = yaml.safe_load((EXEC / "MEOS_RELEASE_MANIFEST.v1.yaml").read_text(encoding="utf-8"))
    assert manifest["p397_status"] == "RELEASE_FACTORY_READY_EXTERNAL_INFRASTRUCTURE_REQUIRED"
    assert manifest["digest"] == "NOT_AVAILABLE"
    plat = yaml.safe_load((EXEC / "MEOS_PLATFORM_STATUS.v1.yaml").read_text(encoding="utf-8"))
    assert str(plat["phase"]).startswith(("P3", "P4"))
    assert plat["g26_ready"] is False
    for path in (
        EXEC / "MEOS_RELEASE_FACTORY.v1.md",
        EXEC / "MEOS_RELEASE_COMPATIBILITY.v1.yaml",
        MASTER,
    ):
        assert "PRODUCTION_READY" not in path.read_text(encoding="utf-8")
