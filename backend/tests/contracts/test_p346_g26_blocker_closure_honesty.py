"""P346 must not close G26 or start P313 recert without real infrastructure."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OVERLAY = EXEC / "MEOS_P346_G26_BLOCKER_CLOSURE.v1.yaml"
P345 = EXEC / "MEOS_P345_G26_PROVISIONING.v1.yaml"
P344 = EXEC / "MEOS_P344_GO_LIVE_EXECUTION.v1.yaml"
P343 = EXEC / "MEOS_P343_FINAL_CERTIFICATION.v1.yaml"
REPORT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
CHECKLIST = EXEC / "MEOS_GO_LIVE_CHECKLIST.md"
REGISTRY = EXEC / "MEOS_APPLICATION_REGISTRY.v1.yaml"
DECISIONS = EXEC / "MEOS_DECISION_REGISTRY.v1.yaml"
COMPOSE = REPO / "infrastructure" / "docker" / "compose" / "docker-compose.meos-prod.yml"

ALLOWED = frozenset({"PASS", "FAIL", "BLOCKED", "NOT_AVAILABLE"})
GATE_IDS = [f"G26-{i:02d}" for i in range(1, 11)]


def _overlay() -> dict:
    return yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))


def test_prior_phases_and_stop():
    p345 = yaml.safe_load(P345.read_text(encoding="utf-8"))
    p344 = yaml.safe_load(P344.read_text(encoding="utf-8"))
    p343 = yaml.safe_load(P343.read_text(encoding="utf-8"))
    data = _overlay()
    assert p345["outcome"] == "OUTCOME_B"
    assert p345["g26_status"] == "BLOCKED"
    assert p344["outcome"] == "STOPPED"
    assert p343["outcome"] == "OUTCOME_B"
    assert data["p345_outcome"] == "OUTCOME_B"
    assert data["p344_outcome"] == "STOPPED"
    assert data["outcome"] == "STOPPED"
    assert data["g26_status"] == "BLOCKED"
    assert data["p313_reentry"] == "NOT_STARTED"
    assert data["credentials"] == "EXTERNAL_DEPENDENCY_REQUIRED"
    assert data["p0_count"] == 1
    assert data["production_certified"] is False
    assert data["go_live_ready"] is False
    assert data["go_live"] == "NOT APPROVED"
    assert data["go_live_authorization"] == "NOT APPROVED"
    assert data["registry_active_count"] == 0
    assert data["production_traffic"] == "NOT_ENABLED"
    assert "dirty" in str(data["git_describe"])
    assert int(data["git_status_short_count"]) > 0
    assert data["g23"] == "FAIL"
    assert data["g27"] == "BLOCKED"
    assert data["production_g08"] == "BLOCKED"


def test_g26_subgates_none_pass():
    data = _overlay()
    gates = data["gates"]
    assert list(gates) == GATE_IDS
    for gid in GATE_IDS:
        row = gates[gid]
        assert row["status"] in ALLOWED
        assert row["evidence"]
        assert row["blocker"]
        assert row["status"] != "PASS"
    assert gates["G26-01"]["status"] == "BLOCKED"
    assert gates["G26-02"]["status"] == "BLOCKED"
    assert gates["G26-03"]["status"] == "BLOCKED"
    assert gates["G26-04"]["status"] == "BLOCKED"
    assert gates["G26-05"]["status"] == "FAIL"
    assert gates["G26-06"]["status"] == "BLOCKED"
    assert gates["G26-10"]["status"] == "BLOCKED"
    assert COMPOSE.is_file()
    text = COMPOSE.read_text(encoding="utf-8")
    assert "not a cloud" in text.lower()


def test_no_go_live_or_activation():
    data = _overlay()
    assert data["go_live_declaration"] == "FORBIDDEN"
    assert data["application_activation"] == "FORBIDDEN"
    assert data["bind_hold_decisions"] == "FORBIDDEN"
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert not any(a.get("status") == "ACTIVE" for a in registry["applications"])
    decisions = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    holds = {d["id"]: d["selected_option"] for d in decisions["decisions"]}
    assert holds["DEC-P314-001"] == "NOT APPROVED"
    checklist = CHECKLIST.read_text(encoding="utf-8")
    assert "- [ ] P313 PRODUCTION_CERTIFIED" in checklist
    report = REPORT.read_text(encoding="utf-8")
    assert "P346" in report
    assert "G26 = BLOCKED" in report or "G26 remains **BLOCKED**" in report
    ext = data["external_infrastructure_blocker"]
    assert ext["responsible_party"] == "NOT_AVAILABLE"
    assert "kubeconfig" in ext["required_resource"]
    assert "Do not execute P344" in data["next_operational_action"]
