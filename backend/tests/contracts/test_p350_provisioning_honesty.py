"""P350 must block provisioning without credentials/provider and must not force G26."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OVERLAY = EXEC / "MEOS_EXT_G26_PROVISIONING_STATUS.v1.yaml"
P349 = EXEC / "MEOS_P349_INFRASTRUCTURE_DISCOVERY.v1.yaml"
REPORT = EXEC / "MEOS_P350_PROVISIONING_REPORT.md"
ENVREC = EXEC / "MEOS_PRODUCTION_ENVIRONMENT_RECORD.md"
CONTRACT = EXEC / "MEOS_EXT_G26_INFRASTRUCTURE.v1.yaml"
CHECKLIST = EXEC / "MEOS_GO_LIVE_CHECKLIST.md"
RUNBOOK = EXEC / "MEOS_PRODUCTION_RUNBOOK.md"
CERT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"
REGISTRY = EXEC / "MEOS_APPLICATION_REGISTRY.v1.yaml"
ALLOWED = frozenset({"PASS", "FAIL", "BLOCKED", "NOT_AVAILABLE", "NOT_APPLICABLE"})
CRED = frozenset({"AVAILABLE", "MISSING", "INVALID", "NOT_VERIFIED"})
GATE_IDS = [f"G26-{i:02d}" for i in range(1, 11)]


def _overlay() -> dict:
    return yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))


def test_p349_gate_pass_but_p350_blocked():
    p349 = yaml.safe_load(P349.read_text(encoding="utf-8"))
    data = _overlay()
    assert p349["p349_status"] == "REQUIREMENTS_IDENTIFIED"
    assert data["p349_gate"] == "PASS"
    assert data["p350_status"] == "BLOCKED"
    assert data["provisioning"] == "BLOCKED"
    assert data["credentials_required"] is True
    assert data["provider_gate"] == "BLOCKED"
    assert data["credential_gate"] == "BLOCKED"
    assert data["provider"] == "NOT_SELECTED"
    assert data["provider_switched"] is False
    assert data["deployment_executed"] is False
    assert data["helm_deployed"] is False
    assert data["flux_applied"] is False
    assert data["migrations_executed"] is False
    assert data["applications_activated"] is False
    assert data["p351_created"] is False
    assert data["p350_does_not_simulate"] is True
    assert data["reuse"]["new_deployment_platform"] == "FORBIDDEN"
    assert data["reuse"]["new_ci_platform"] == "FORBIDDEN"


def test_p350_does_not_certify_or_golive():
    data = _overlay()
    assert data["g26_ready"] is False
    assert data["g26_status"] == "BLOCKED"
    assert data["p0_count"] == 1
    assert data["p0_changed_by_p350"] is False
    assert data["p313"] == "NOT_CERTIFIED"
    assert data["p313_auto_start"] is False
    assert data["p313_reentry"] == "NOT_STARTED"
    assert data["p313_reentry_ready"] is False
    assert data["p350_does_not_start_p313"] is True
    assert data["production_certified"] is False
    assert data["go_live_ready"] is False
    assert data["go_live_authorization"] == "NOT_APPROVED"
    assert data["registry_active_count"] == 0
    assert data["production_traffic"] == "NOT_ENABLED"
    assert data["production_identity"] == "LOCAL"
    assert data["forbidden_sha"] == "47258dfd-dirty"
    assert data["g23"] == "FAIL"
    contract = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    assert contract["g26_ready"] is False
    assert contract["p0_count"] == 1
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert not any(a.get("status") == "ACTIVE" for a in registry["applications"])


def test_p350_credentials_and_gates():
    data = _overlay()
    for key, val in data["credentials"].items():
        assert val in CRED, f"{key}={val}"
        assert val != "AVAILABLE"
    assert data["credentials"]["kubeconfig"] == "MISSING"
    assert data["credentials"]["cloud_account"] == "MISSING"
    assert data["local_non_production"]["class"] == "LOCAL"
    assert data["local_non_production"]["pgport"] == "5433"
    gates = data["gates"]
    assert list(gates) == GATE_IDS
    for gid in GATE_IDS:
        row = gates[gid]
        assert row["status"] in ALLOWED
        assert row["status"] != "PASS"
        assert row["blocker"]
        assert row["timestamp"]
        assert row["source"]
        assert row["evidence"]
    dumped = yaml.safe_dump(data)
    for banned in ("BEGIN PRIVATE", "-----BEGIN"):
        assert banned not in dumped


def test_p350_artifacts_and_cross_links():
    assert REPORT.is_file()
    assert ENVREC.is_file()
    report = REPORT.read_text(encoding="utf-8")
    assert "BLOCKED" in report
    assert "NOT_SELECTED" in report
    env = ENVREC.read_text(encoding="utf-8")
    assert "NOT_AVAILABLE" in env
    for path in (CHECKLIST, RUNBOOK, CERT, MASTER):
        assert "P350" in path.read_text(encoding="utf-8")
