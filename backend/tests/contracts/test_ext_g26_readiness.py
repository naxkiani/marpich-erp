"""EXT-G26 validator must not treat localhost/compose/dirty SHA as production."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "scripts" / "meos-ext-g26-readiness.py"
CONTRACT = REPO / "docs" / "meos" / "execution" / "MEOS_EXT_G26_INFRASTRUCTURE.v1.yaml"
COMPOSE = REPO / "infrastructure" / "docker" / "compose" / "docker-compose.meos-prod.yml"
HANDOFF = REPO / "docs" / "meos" / "execution" / "MEOS_EXT_G26_INFRASTRUCTURE_HANDOFF.md"
ALLOWED = frozenset({"PASS", "FAIL", "BLOCKED", "NOT_AVAILABLE", "NOT_APPLICABLE"})
GATE_IDS = [f"G26-{i:02d}" for i in range(1, 11)]


def _mod():
    spec = importlib.util.spec_from_file_location("meos_ext_g26_readiness", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_contract_statuses_and_p0():
    data = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    assert data["ext_g26_status"] == "UNRESOLVED"
    assert data["g26_status"] == "BLOCKED"
    assert data["g26_ready"] is False
    assert data["p0_count"] == 1
    assert data["p313"] == "NOT_CERTIFIED"
    assert data["p313_auto_start"] is False
    assert data["production_certified"] is False
    assert data["go_live_ready"] is False
    assert data["go_live_authorization"] == "NOT APPROVED"
    assert data["registry_active_count"] == 0
    assert data["production_traffic"] == "NOT_ENABLED"
    assert data["forbidden_sha"] == "47258dfd-dirty"
    ids = [row["id"] for row in data["dependencies"]]
    assert ids == GATE_IDS
    for row in data["dependencies"]:
        assert row["status"] in ALLOWED
        assert row["status"] != "PASS"
        assert row["owner"] == "NOT_AVAILABLE"
        assert row["required"] is True
    assert HANDOFF.is_file()
    assert "NOT_AVAILABLE" in HANDOFF.read_text(encoding="utf-8")


def test_validator_detects_missing_external_deps(monkeypatch):
    monkeypatch.setenv("MEOS_KUBE_HOME", str(REPO / ".meos-no-kube-home"))
    monkeypatch.delenv("MEOS_PUBLIC_CA_TLS", raising=False)
    monkeypatch.delenv("MEOS_SECRET_MANAGER_AVAILABLE", raising=False)
    monkeypatch.delenv("MEOS_IMAGE_DIGEST", raising=False)
    monkeypatch.delenv("MEOS_PRODUCTION_DNS", raising=False)
    monkeypatch.delenv("MEOS_DEPLOYED_COMMIT", raising=False)
    monkeypatch.delenv("MEOS_DEPLOYED_DIGEST", raising=False)
    monkeypatch.delenv("MEOS_ROLLBACK_EXERCISED", raising=False)
    monkeypatch.setenv("PGHOST", "127.0.0.1")
    monkeypatch.setenv("PGPORT", "5433")
    monkeypatch.setenv("MEOS_HEALTH_URL", "http://127.0.0.1:8000/api/v1/health")
    result = _mod().evaluate(REPO)
    assert result["g26_ready"] is False
    assert result["g26_status"] == "BLOCKED"
    assert result["p0_count"] == 1
    assert result["production"] is False
    assert result["production_identity"] == "LOCAL"
    assert result["localhost_health_is_production"] is False
    assert result["compose_is_production"] is False
    assert result["forbidden_dirty"] is True
    assert result["git_status_short_empty"] is False
    assert "dirty" in str(result["git_describe"])
    assert result["p313_auto_start"] is False
    assert result["go_live_authorization"] == "NOT APPROVED"
    assert result["production_certified"] is False
    gates = result["gates"]
    assert gates["G26-01"]["status"] == "BLOCKED"
    assert gates["G26-02"]["status"] == "BLOCKED"
    assert gates["G26-03"]["status"] == "BLOCKED"
    assert gates["G26-04"]["status"] == "BLOCKED"
    assert gates["G26-05"]["status"] == "FAIL"
    assert gates["G26-06"]["status"] == "BLOCKED"
    assert gates["G26-07"]["status"] == "NOT_AVAILABLE"
    assert gates["G26-08"]["status"] == "BLOCKED"
    assert gates["G26-09"]["status"] == "NOT_AVAILABLE"
    assert gates["G26-10"]["status"] == "BLOCKED"
    dumped = json.dumps(result)
    for banned in ("PGPASSWORD", "AWS_SECRET_ACCESS_KEY", "JWT_SECRET", "BEGIN PRIVATE"):
        assert banned not in dumped


def test_localhost_and_compose_are_not_production():
    text = COMPOSE.read_text(encoding="utf-8")
    assert "not a cloud" in text.lower()
    assert "5444:5432" in text
    result = _mod().evaluate(REPO)
    assert result["production"] is False
    assert result["localhost_health_is_production"] is False


def test_p313_not_auto_started_even_if_ready_flag_documented():
    data = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    assert "explicit re-entry" in data["p313_reentry"].lower() or "STOP P348" in data["p313_reentry"]
    assert data["p313_auto_start"] is False
