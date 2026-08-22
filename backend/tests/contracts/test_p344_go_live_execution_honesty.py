"""P344 must STOP when P343 is not PASS. Must not deploy or authorize GO_LIVE."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OVERLAY = EXEC / "MEOS_P344_GO_LIVE_EXECUTION.v1.yaml"
P343 = EXEC / "MEOS_P343_FINAL_CERTIFICATION.v1.yaml"
REPORT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
CHECKLIST = EXEC / "MEOS_GO_LIVE_CHECKLIST.md"
REGISTRY = EXEC / "MEOS_APPLICATION_REGISTRY.v1.yaml"
DECISIONS = EXEC / "MEOS_DECISION_REGISTRY.v1.yaml"
MASTER = EXEC / "MEOS_EXECUTION_MASTER_PLAN.md"


def _overlay() -> dict:
    return yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))


def test_entry_gate_stop_no_deploy():
    p343 = yaml.safe_load(P343.read_text(encoding="utf-8"))
    data = _overlay()
    assert p343["outcome"] == "OUTCOME_B"
    assert p343["production_certified"] is False
    assert p343["go_live_ready"] is False
    assert p343["p0_count"] == 1
    assert data["p343_outcome"] == "B_BLOCKED"
    assert data["p343_pass"] is False
    assert data["entry_gate"] == "FAIL"
    assert data["outcome"] == "STOPPED"
    assert data["deployment_executed"] is False
    assert data["go_live_executed"] is False
    assert data["go_live"] == "NOT APPROVED"
    assert data["go_live_authorization"] == "NOT APPROVED"
    assert data["human_authorization"] == "NOT APPROVED"
    assert data["p0_count"] == 1
    assert data["runtime_status"] == "NOT_LAUNCHED"
    assert data["production_traffic"] == "NOT_ENABLED"
    assert data["smoke_tests"] == "NOT_EXECUTED"
    assert data["user_onboarding"] == "NOT_EXECUTED"
    assert data["certified_release"] == "NOT_AVAILABLE"
    assert data["deployed_commit"] == "NOT_DEPLOYED"
    assert data["failed_gate"] == "G26"
    assert data["architecture_expansion"] == "FORBIDDEN"


def test_no_activation_or_invented_value():
    data = _overlay()
    assert data["registry_active_count"] == 0
    assert data["kpi_measured_count"] == 0
    assert data["outcome_measured_count"] == 0
    assert data["benefit_measured_count"] == 0
    assert data["autonomy"] == "L0"
    assert data["incidents"] == 0
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert registry["overall_status"] == "NOT_READY"
    assert not any(a.get("status") == "ACTIVE" for a in registry["applications"])
    decisions = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    assert decisions["executed_count"] == 0
    holds = {d["id"]: d["selected_option"] for d in decisions["decisions"]}
    assert holds["DEC-P314-001"] == "NOT APPROVED"
    assert holds["DEC-P319-001"] == "BLOCK_AUTOMATION"


def test_docs_record_stop_not_go_live():
    report = REPORT.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    master = MASTER.read_text(encoding="utf-8")
    assert "P344" in report
    assert "no production deployment" in report.lower() or "NOT_LAUNCHED" in report
    assert "- [ ] P313 PRODUCTION_CERTIFIED" in checklist
    assert "- [x] P313 PRODUCTION_CERTIFIED" not in checklist
    assert "REQUIRES_HUMAN_APPROVAL" in checklist
    assert "P344" in master
    assert "STOPPED" in master or "not deploy" in master.lower()
    data = _overlay()
    assert "INIT-G26" in data["next_operational_action"]
    assert "Do not deploy" in data["next_operational_action"]
