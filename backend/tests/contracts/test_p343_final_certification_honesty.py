"""P343 final certification must not manufacture P0=0, production, or GO_LIVE."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OVERLAY = EXEC / "MEOS_P343_FINAL_CERTIFICATION.v1.yaml"
P342 = EXEC / "MEOS_P313_RECERTIFICATION.v1.yaml"
REPORT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
CHECKLIST = EXEC / "MEOS_GO_LIVE_CHECKLIST.md"
MATRIX = EXEC / "MEOS_P313_PRODUCTION_CERTIFICATION.md"
REGISTRY = EXEC / "MEOS_APPLICATION_REGISTRY.v1.yaml"
DECISIONS = EXEC / "MEOS_DECISION_REGISTRY.v1.yaml"
OUTCOMES = EXEC / "MEOS_OUTCOME_REGISTRY.v1.yaml"
P339 = EXEC / "MEOS_DECISION_EXECUTION.v1.yaml"

ALLOWED = frozenset({"PASS", "FAIL", "BLOCKED", "NOT_APPLICABLE"})
CHECKLIST_ALLOWED = frozenset(
    {"CERTIFIED", "PENDING", "BLOCKED", "REQUIRES_HUMAN_APPROVAL", "PASS", "NOT_APPLICABLE"}
)


def _overlay() -> dict:
    return yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))


def test_p342_blocked_and_p343_does_not_self_certify():
    p342 = yaml.safe_load(P342.read_text(encoding="utf-8"))
    data = _overlay()
    assert p342["outcome"] == "OUTCOME_B"
    assert p342["p341_outcome"] == "B_BLOCKED"
    assert data["p342_outcome"] == "B_BLOCKED"
    assert data["outcome"] == "OUTCOME_B"
    assert data["production_certified"] is False
    assert data["production_certified_state"] == "NO"
    assert data["go_live_ready"] is False
    assert data["go_live_ready_state"] == "NO"
    assert data["go_live"] == "NOT APPROVED"
    assert data["go_live_authorization"] == "REQUIRES_HUMAN_APPROVAL"
    assert data["go_live_declaration"] == "FORBIDDEN"
    assert data["p0_count"] == 1
    assert data["p313_eligible"] is False
    assert data["p314_prepared"] is False
    assert data["real_environment"] is False
    assert data["production_identity"]["status"] == "NON_PRODUCTION"
    assert data["production_identity"]["database"] == "NOT_IDENTIFIED"
    assert data["production_identity"]["image"] == "NOT_AVAILABLE"
    assert data["production_identity"]["tls"] == "MISSING"
    assert "dirty" in str(data["git_describe"])


def test_gates_match_p342_and_p0_not_reduced():
    data = _overlay()
    p342 = yaml.safe_load(P342.read_text(encoding="utf-8"))
    gates = data["gates"]
    assert set(gates) == {f"G{i:02d}" for i in range(1, 29)}
    by_status: dict[str, int] = {}
    for gid, row in gates.items():
        assert row["status"] in ALLOWED
        assert row["owner"] == "NOT_AVAILABLE"
        by_status[row["status"]] = by_status.get(row["status"], 0) + 1
        assert row["status"] == p342["gates"][gid]["status"]
    assert data["totals"]["PASS"] == by_status.get("PASS", 0) == 20
    assert data["totals"]["FAIL"] == by_status.get("FAIL", 0) == 6
    assert data["totals"]["BLOCKED"] == by_status.get("BLOCKED", 0) == 2
    assert data["p0_count"] == p342["p0_count"] == 1
    assert gates["G26"]["status"] == "BLOCKED"
    assert gates["G27"]["status"] == "BLOCKED"
    assert gates["G25"]["status"] == "FAIL"
    assert gates["G23"]["status"] == "FAIL"
    assert data["production_restore"] == "UNVERIFIED"
    assert data["production_rto_rpo"] == "NOT_MEASURED"


def test_no_invented_value_or_active_apps():
    data = _overlay()
    assert data["registry_active_count"] == 0
    assert data["authorized_action_count"] == 0
    assert data["realized_benefit_count"] == 0
    assert data["outcome_measured_count"] == 0
    assert data["autonomy"] == "L0"
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert registry["overall_status"] == "NOT_READY"
    assert not any(a.get("status") == "ACTIVE" for a in registry["applications"])
    outcomes = yaml.safe_load(OUTCOMES.read_text(encoding="utf-8"))
    assert outcomes["measured_count"] == 0
    p339 = yaml.safe_load(P339.read_text(encoding="utf-8"))
    assert p339["authorized_action_count"] == 0
    decisions = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    assert decisions["executed_count"] == 0
    holds = {d["id"]: d["selected_option"] for d in decisions["decisions"]}
    assert holds["DEC-P314-001"] == "NOT APPROVED"
    assert holds["DEC-P319-001"] == "BLOCK_AUTOMATION"


def test_p313_checklist_and_report():
    report = REPORT.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    matrix = MATRIX.read_text(encoding="utf-8")
    assert "PRODUCTION_CERTIFIED = NO" in report
    assert "GO_LIVE_READY = NO" in report
    assert "G26 | DEPLOYMENT | **BLOCKED**" in matrix
    assert "- [ ] P313 PRODUCTION_CERTIFIED" in checklist
    assert "- [x] P313 PRODUCTION_CERTIFIED" not in checklist
    assert "| 14 | PRODUCTION_CERTIFIED | **BLOCKED**" in checklist
    assert "REQUIRES_HUMAN_APPROVAL" in checklist
    for line in checklist.splitlines():
        if line.startswith("|") and "Prerequisite" not in line and line.count("|") >= 4:
            status = line.split("|")[3].strip().replace("*", "")
            if status and status not in {"Status"} and not set(status) <= {"-"}:
                assert status in CHECKLIST_ALLOWED
    data = _overlay()
    assert "INIT-G26" in data["next_operational_action"]
    assert "P314" in data["next_operational_action"]
