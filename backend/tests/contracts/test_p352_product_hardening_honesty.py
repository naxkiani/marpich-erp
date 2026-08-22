"""P352 hardening must not manufacture G26 or treat compose as production."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
HARDEN = EXEC / "MEOS_P352_PRODUCT_INFRASTRUCTURE_HARDENING.md"
RELEASE = EXEC / "MEOS_RELEASE_READINESS_REPORT.md"
MATRIX = EXEC / "MEOS_LAUNCH_READINESS_MATRIX.md"
RESTORE = EXEC / ".last_p352_restore.json"
DOCKERFILE = REPO / "infrastructure" / "docker" / "images" / "backend.Dockerfile"
DEPLOY = REPO / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "templates" / "deployment.yaml"
COMPOSE = REPO / "infrastructure" / "docker" / "compose" / "docker-compose.meos-prod.yml"
CERT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
LAUNCH = REPO / "scripts" / "meos-launch-readiness.py"
REL = REPO / "scripts" / "meos-release-readiness.py"


def test_p352_docs_and_probes():
    assert HARDEN.is_file()
    assert RELEASE.is_file()
    assert MATRIX.is_file()
    assert "COMPOSE_IS_PRODUCTION" in HARDEN.read_text(encoding="utf-8")
    df = DOCKERFILE.read_text(encoding="utf-8")
    assert "COPY shared" in df
    assert "USER app" in df
    deploy = DEPLOY.read_text(encoding="utf-8")
    assert "path: /api/v1/ready" in deploy
    assert "path: /api/v1/live" in deploy
    assert "COMPOSE_IS_PRODUCTION = FALSE" in COMPOSE.read_text(encoding="utf-8")
    restore = yaml.safe_load(RESTORE.read_text(encoding="utf-8"))
    assert restore["restore_test"] == "PASS"
    assert restore["production_restore"] == "NOT_VERIFIED"
    assert restore["port"] == "5433"


def test_p352_release_validator_no_fake_digest():
    import importlib.util

    spec = importlib.util.spec_from_file_location("meos_release_readiness", REL)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    data = mod.evaluate()
    assert data["registry_status"] == "READY_FOR_CREDENTIALS"
    assert data["compose_is_production"] is False
    assert data["g26_not_overridden"] is True
    if data["dirty_state"]:
        assert data["forbidden_for_certified_release"] is True


def test_p352_launch_does_not_set_g26(monkeypatch):
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
    assert data["p313_reentry_ready"] is False
    assert data["compose_is_production"] is False
    assert data["go_live_authorization"] == "NOT APPROVED"
    for path in (CERT, MASTER):
        assert "P352" in path.read_text(encoding="utf-8")
