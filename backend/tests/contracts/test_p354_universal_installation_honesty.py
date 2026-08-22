"""P354 installer/release engine must not fake production, digests, or G26."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
ENGINE = REPO / "scripts" / "meos_release_engine.py"
INSTALL = REPO / "scripts" / "meos-install.py"
RELEASE = REPO / "scripts" / "meos-release.py"
READY = REPO / "scripts" / "meos-install-readiness.py"
DOC = EXEC / "MEOS_P354_UNIVERSAL_INSTALLATION.md"
OPS = EXEC / "MEOS_RELEASE_OPERATIONS.md"
MATRIX = EXEC / "MEOS_INSTALLATION_MATRIX.v1.yaml"
CERT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
FLUX = REPO / "infrastructure" / "fluxcd" / "marpich-iam-helmrelease.yaml"
G26 = REPO / "scripts" / "meos-ext-g26-readiness.py"


def _engine():
    spec = importlib.util.spec_from_file_location("meos_release_engine", ENGINE)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_p354_artifacts_exist():
    for path in (ENGINE, INSTALL, RELEASE, READY, DOC, OPS, MATRIX, FLUX):
        assert path.is_file(), path
    blob = DOC.read_text(encoding="utf-8")
    assert "DEPLOYMENT_MECHANISM_READY" in blob
    assert "PLAN_ONLY" in blob
    assert "G26_READY" in blob
    data = yaml.safe_load(MATRIX.read_text(encoding="utf-8"))
    assert data["g26_ready"] is False
    assert data["production_certified"] is False
    assert data["p313"] == "NOT_CERTIFIED"
    assert data["platforms"]["HOSTINGER_VPS"]["status"] == "READY_FOR_CREDENTIALS"
    assert "INCOMPATIBLE" in data["platforms"]["HOSTINGER_VPS"]["evidence"]
    assert data["new_ci"] == "FORBIDDEN"
    flux = FLUX.read_text(encoding="utf-8")
    assert "image.digest" in flux
    assert "Never :latest" in flux or "Never :latest" in (REPO / "infrastructure" / "fluxcd" / "marpich-iam-digest.values.example.yaml").read_text(encoding="utf-8")


def test_p354_rejects_dirty_latest_localhost_production(monkeypatch):
    mod = _engine()
    monkeypatch.delenv("MEOS_PUBLIC_CA_TLS", raising=False)
    monkeypatch.delenv("MEOS_SECRET_MANAGER_AVAILABLE", raising=False)
    monkeypatch.setenv("MARPICH_ENVIRONMENT", "production")
    env = mod.classify_environment("LOCAL", claim_production=True, env_production=True)
    assert env["production"] is False
    assert env["localhost_is_production"] is False
    assert mod.production_db_rejected("127.0.0.1", "5433") is True
    assert mod.production_db_rejected("localhost", "5444") is True
    assert mod.production_db_rejected("db.example.com", "5432") is False
    pub = mod.publish_status(confirm=False)
    assert pub["silent_publish"] is False
    assert pub["status"] == "REFUSED"
    pub2 = mod.publish_status(confirm=True)
    assert pub2["status"] in {"READY_FOR_CREDENTIALS", "BLOCKED", "NOT_EXECUTED"}
    ident = mod.identity_ok(require_digest=True)
    assert ident["ok"] is False
    assert "IMAGE_DIGEST_MISSING" in (ident["blocked"] or [])


def test_p354_plan_only_and_no_secrets_in_plan():
    mod = _engine()
    plan = mod.installation_plan("LOCAL")
    dumped = json.dumps(plan)
    assert plan["mode"] == "PLAN_ONLY"
    assert plan["g26_ready"] is False
    assert plan["production_certified"] is False
    assert "BEGIN PRIVATE" not in dumped
    assert "password=" not in dumped.lower()
    destructive = mod.installation_plan("LOCAL", authorize_destructive=True)
    assert "DESTRUCTIVE_MIGRATION_BLOCKED" in destructive["blocked"]
    prod = mod.installation_plan("VPS", claim_production=True, db_host="127.0.0.1", db_port="5433")
    assert prod["status"] == "BLOCKED"
    assert "PRODUCTION_DB_LOCALHOST_OR_DEMO_PORT" in prod["blocked"]
    apply_cloud = mod.installation_plan("AWS", execute=True, apply=True)
    assert apply_cloud["mode"] == "PLAN_ONLY"
    tls = mod.tls_status("LOCAL", production=True)
    assert tls["status"] == "BLOCKED"
    assert tls["fabricated"] == "FALSE"


def test_p354_does_not_start_p313_or_change_p0():
    assert "P354" in CERT.read_text(encoding="utf-8")
    assert "P354" in MASTER.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")
    assert "NOT_APPROVED" in doc
    assert G26.is_file()
    g26 = G26.read_text(encoding="utf-8")
    assert "G26_READY" in g26
    obs = _engine().observability_status()
    assert obs["g23"] == "FAIL"
    assert "PRODUCTION_VERIFIED" not in obs["g23_class"] or obs["g23_class"] == "CONFIGURED_NOT_PRODUCTION_VERIFIED"
