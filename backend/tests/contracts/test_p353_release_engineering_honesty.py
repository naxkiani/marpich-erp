"""P353 release engineering must not fake digests, G26, or production."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
REPORT = EXEC / "MEOS_P353_RELEASE_ENGINEERING_REPORT.md"
MANIFEST = EXEC / "MEOS_RELEASE_MANIFEST.v1.yaml"
CERT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
COMPOSE = REPO / "infrastructure" / "docker" / "compose" / "docker-compose.meos-prod.yml"
HELPERS = REPO / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "templates" / "_helpers.tpl"
VALUES_PROD = REPO / "infrastructure" / "kubernetes" / "helm" / "marpich-iam" / "values-production.yaml"
REL = REPO / "scripts" / "meos-release-readiness.py"
SCAN = REPO / "scripts" / "meos-secret-scan.py"
VPS = REPO / "scripts" / "meos-vps-bootstrap.sh"
G26 = REPO / "scripts" / "meos-ext-g26-readiness.py"


def test_p353_artifacts_exist():
    for path in (REPORT, MANIFEST, REL, SCAN, VPS, COMPOSE, HELPERS, VALUES_PROD):
        assert path.is_file(), path
    report = REPORT.read_text(encoding="utf-8")
    assert "LOCAL_RELEASE_READY" in report
    assert "PRODUCTION_CERTIFIED" in report
    assert "G26_READY" in report
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    digest = str(manifest["image_digest"])
    assert digest == "NOT_AVAILABLE" or digest.startswith("sha256:")
    assert manifest["artifact_status"] in {
        "LOCAL_BUILD",
        "CI_BUILT",
        "REGISTRY_PUSHED",
        "IMMUTABLE_DIGEST_AVAILABLE",
        "DEPLOYMENT_READY",
        "PRODUCTION_DEPLOYED",
        "READY_FOR_CREDENTIALS",
        "NOT_AVAILABLE",
    }
    assert manifest.get("production_certified") in {False, "FALSE", "NO"}
    assert "latest" not in str(manifest.get("release_identity", "")).lower()


def test_p353_vps_and_helm_prefer_digest():
    compose = COMPOSE.read_text(encoding="utf-8")
    assert "MEOS_IMAGE" in compose
    assert "COMPOSE_IS_PRODUCTION = FALSE" in compose
    helpers = HELPERS.read_text(encoding="utf-8")
    assert ".Values.image.digest" in helpers
    values = VALUES_PROD.read_text(encoding="utf-8")
    assert 'digest: ""' in values
    assert 'tag: "latest"' not in values
    assert "image.tag: latest" not in values
    vps = VPS.read_text(encoding="utf-8")
    assert "MEOS_IMAGE" in vps
    assert "Do not use :latest" in vps


def test_p353_release_validator_distinguishes_local_and_registry(monkeypatch):
    import importlib.util

    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GHCR_TOKEN", raising=False)
    spec = importlib.util.spec_from_file_location("meos_release_readiness", REL)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    data = mod.evaluate()
    assert data["compose_is_production"] is False
    assert data["g26_not_overridden"] is True
    assert data["PRODUCTION_RELEASE_READY"] is False
    assert data["image_digest"] == "NOT_AVAILABLE"
    assert data["IMMUTABLE_DIGEST_AVAILABLE"] is False
    assert data["REGISTRY_RELEASE_READY"] == "READY_FOR_CREDENTIALS"
    assert data["DEPLOYMENT_RELEASE_READY"] == "READY_FOR_CREDENTIALS"
    if data["dirty_state"]:
        assert data["LOCAL_RELEASE_READY"] is False
        assert data["RELEASE_READY"] is False


def test_p353_does_not_start_p313_or_golive():
    assert "P353" in CERT.read_text(encoding="utf-8")
    assert "P353" in MASTER.read_text(encoding="utf-8")
    report = REPORT.read_text(encoding="utf-8")
    assert "GO_LIVE_AUTHORIZATION" in report
    assert "NOT_APPROVED" in report or "NOT APPROVED" in report
    assert G26.is_file()
    assert "G26_READY" in G26.read_text(encoding="utf-8")
