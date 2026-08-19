"""P342 recertification must not declare PRODUCTION_CERTIFIED or GO_LIVE while G26 is BLOCKED."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OVERLAY = EXEC / "MEOS_P313_RECERTIFICATION.v1.yaml"
P341 = EXEC / "MEOS_PRODUCTION_INFRASTRUCTURE_READINESS.v1.yaml"
P313_MATRIX = EXEC / "MEOS_P313_PRODUCTION_CERTIFICATION.md"
REPORT = EXEC / "MEOS_P313_CERTIFICATION_REPORT.md"
CHECKLIST = EXEC / "MEOS_GO_LIVE_CHECKLIST.md"
REGISTRY = EXEC / "MEOS_APPLICATION_REGISTRY.v1.yaml"
DECISIONS = EXEC / "MEOS_DECISION_REGISTRY.v1.yaml"

ALLOWED = frozenset({"PASS", "FAIL", "BLOCKED", "NOT_APPLICABLE"})
CHECKLIST_ALLOWED = frozenset(
    {"PASS", "PENDING", "BLOCKED", "NOT_APPLICABLE", "CERTIFIED", "REQUIRES_HUMAN_APPROVAL"}
)


def _overlay() -> dict:
    return yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))


def test_p341_was_blocked_and_p342_does_not_self_certify():
    p341 = yaml.safe_load(P341.read_text(encoding="utf-8"))
    data = _overlay()
    assert p341["outcome"] == "OUTCOME_B"
    assert data["p341_outcome"] == "B_BLOCKED"
    assert data["outcome"] == "OUTCOME_B"
    assert data["production_certified"] is False
    assert data["p313_recertification_ready"] is False
    assert data["go_live"] == "NOT APPROVED"
    assert data["go_live_ready"] is False
    assert data["p0_count"] == 1
    assert data["go_live_declaration"] == "FORBIDDEN"
    assert data["holds_preserved"] is True
    assert data["production_target"] == "NOT_AVAILABLE"
    assert "dirty" in str(data["git_describe"])


def test_all_g01_g28_have_allowed_status_and_counts():
    data = _overlay()
    gates = data["gates"]
    assert set(gates) == {f"G{i:02d}" for i in range(1, 29)}
    by_status: dict[str, int] = {}
    for gid, row in gates.items():
        assert row["status"] in ALLOWED
        assert row["owner"] == "NOT_AVAILABLE"
        by_status[row["status"]] = by_status.get(row["status"], 0) + 1
    assert data["totals"]["PASS"] == by_status.get("PASS", 0) == 20
    assert data["totals"]["FAIL"] == by_status.get("FAIL", 0) == 6
    assert data["totals"]["BLOCKED"] == by_status.get("BLOCKED", 0) == 2
    assert gates["G26"]["status"] == "BLOCKED"
    assert gates["G27"]["status"] == "BLOCKED"
    assert gates["G25"]["status"] == "FAIL"
    assert gates["G23"]["status"] == "FAIL"
    assert gates["G18"]["status"] == "FAIL"
    assert gates["G19"]["status"] == "FAIL"


def test_p313_and_checklist_not_go_live():
    matrix = P313_MATRIX.read_text(encoding="utf-8")
    report = REPORT.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    assert "G26 | DEPLOYMENT | **BLOCKED**" in matrix
    assert "PRODUCTION_CERTIFIED = NO" in report
    assert "- [ ] P313 PRODUCTION_CERTIFIED" in checklist
    assert "- [x] P313 PRODUCTION_CERTIFIED" not in checklist
    for line in checklist.splitlines():
        if line.startswith("|") and "Prerequisite" not in line and line.count("|") >= 4:
            status = line.split("|")[3].strip().replace("*", "")
            if status and status not in {"Status"} and not set(status) <= {"-"}:
                assert status in CHECKLIST_ALLOWED
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert registry["overall_status"] == "NOT_READY"
    assert not any(a.get("status") == "ACTIVE" for a in registry["applications"])
    decisions = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    assert decisions["executed_count"] == 0
    holds = {d["id"]: d["selected_option"] for d in decisions["decisions"]}
    assert holds["DEC-P314-001"] == "NOT APPROVED"
    assert holds["DEC-P319-001"] == "BLOCK_AUTOMATION"


def test_critical_blockers_have_remediation():
    data = _overlay()
    ids = {row["id"] for row in data["critical_blockers"]}
    assert {"G26", "G27", "G25", "G23", "G19", "G18"} <= ids
    for row in data["critical_blockers"]:
        assert row["status"] in {"BLOCKED", "FAIL"}
        assert row["evidence"]
        assert row["dependency"]
        assert row["remediation"]
        assert row["next_verification"]
    assert "INIT-G26" in data["next_operational_action"]
