"""P351 product infrastructure must not manufacture G26 or treat local as production."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
ADAPTER = EXEC / "MEOS_PLATFORM_ADAPTER_STATUS.v1.yaml"
BLUEPRINT = EXEC / "MEOS_PRODUCT_INFRASTRUCTURE_BLUEPRINT.md"
MATRIX = EXEC / "MEOS_MULTI_PLATFORM_LAUNCH_MATRIX.md"
PROFILES = EXEC / "MEOS_LAUNCH_PROFILES.md"
RELEASE = EXEC / "MEOS_RELEASE_ENGINEERING_RUNBOOK.md"
BACKUP = EXEC / "MEOS_BACKUP_RESTORE_RUNBOOK.md"
CERT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
DOCKERFILE = REPO / "infrastructure" / "docker" / "images" / "backend.Dockerfile"
HELPERS = REPO / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "templates" / "_helpers.tpl"
EXTSEC = REPO / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "templates" / "externalsecret.yaml"
CI = REPO / ".github" / "workflows" / "identity-federation-enterprise.yml"
ENVEX = REPO / "infrastructure" / "launch" / "env.production.example"
LAUNCH = REPO / "scripts" / "meos-launch-readiness.py"
G26 = REPO / "scripts" / "meos-ext-g26-readiness.py"


def test_p351_adapter_yaml_not_production():
    data = yaml.safe_load(ADAPTER.read_text(encoding="utf-8"))
    assert data["p351_status"] == "PRODUCT_INFRASTRUCTURE_FOUNDATION"
    assert data["g26_ready"] is False
    assert data["g26_status"] == "BLOCKED"
    assert data["p0_count"] == 1
    assert data["p313"] == "NOT_CERTIFIED"
    assert data["p313_reentry_ready"] is False
    assert data["production_certified"] is False
    assert data["go_live_ready"] is False
    assert data["go_live_authorization"] == "NOT_APPROVED"
    assert data["localhost_is_production"] is False
    assert data["compose_is_production"] is False
    assert data["demo_is_production"] is False
    assert data["environments"]["PRODUCTION"] == "BLOCKED"
    assert data["environments"]["LOCAL"] != "PRODUCTION_VERIFIED"
    assert data["targets"]["TARGET-D_HOSTINGER_SHARED"] == "INCOMPATIBLE"
    assert "PRODUCTION_VERIFIED" not in data["targets"].values()
    assert data["new_deployment_platform"] == "FORBIDDEN"
    assert data["credentials"]["cloud_account"] == "NOT_AVAILABLE"


def test_p351_packages_reuse_existing_path():
    assert DOCKERFILE.is_file()
    assert "USER app" in DOCKERFILE.read_text(encoding="utf-8")
    assert "marpich-iam.image" in HELPERS.read_text(encoding="utf-8")
    assert EXTSEC.is_file()
    ci = CI.read_text(encoding="utf-8")
    assert "steps.image.outputs.digest" in ci
    assert "meos-image-digest" in ci
    env = ENVEX.read_text(encoding="utf-8")
    assert "CHANGE_ME" in env
    assert "BEGIN PRIVATE" not in env
    for path in (BLUEPRINT, MATRIX, PROFILES, RELEASE, BACKUP, LAUNCH, G26):
        assert path.is_file(), path


def test_p351_docs_isolate_g26():
    blob = "\n".join(p.read_text(encoding="utf-8") for p in (BLUEPRINT, MATRIX, PROFILES, RELEASE))
    assert "LOCAL" in blob
    assert "PRODUCTION" in blob
    for path in (CERT, MASTER):
        assert "P351" in path.read_text(encoding="utf-8")


def test_p351_launch_readiness_does_not_override_g26(monkeypatch):
    import importlib.util

    monkeypatch.setenv("MEOS_KUBE_HOME", str(REPO / ".meos-no-kube-home"))
    monkeypatch.delenv("MEOS_PUBLIC_CA_TLS", raising=False)
    monkeypatch.delenv("MEOS_SECRET_MANAGER_AVAILABLE", raising=False)
    spec = importlib.util.spec_from_file_location("meos_launch_readiness", LAUNCH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    data = mod.evaluate()
    assert data["g26_ready"] is False
    assert data["g26_status"] == "BLOCKED"
    assert data["p0_count"] == 1
    assert data["localhost_is_production"] is False
    assert data["compose_is_production"] is False
    assert data["demo_is_production"] is False
    assert data["release_ready"] == "BLOCKED"
    assert data["aws_ready"] == "READY_FOR_CREDENTIALS"
    assert data["adapter_status"]["PRODUCTION"] == "BLOCKED"
    dumped = str(data)
    assert "BEGIN PRIVATE" not in dumped
