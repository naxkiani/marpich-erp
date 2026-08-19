"""Launch risk overlay must not invent scores, owners, or resolved risks."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
RISKS = EXEC / "MEOS_RISK_REGISTRY.v1.yaml"
CONTROLS = EXEC / "MEOS_CONTROL_EFFECTIVENESS.v1.yaml"
ALLOWED_IDS = {"R-01", "R-02", "R-03", "R-04", "R-05", "R-06", "R-07"}
FORBIDDEN_STATUS = frozenset({"RESOLVED", "CLOSED", "MONITORED", "ACCEPTED"})


def test_only_launch_risks_unresolved_unscored():
    data = yaml.safe_load(RISKS.read_text(encoding="utf-8"))
    assert data["risk_appetite"] == "NOT_DECLARED"
    assert data["numeric_score"] == "NOT_SCORED"
    assert data["resolved_count"] == 0
    assert data["monitored_count"] == 0
    assert data["unowned_count"] == 7
    assert data["unowned_critical_count"] == 1
    ids = {row["id"] for row in data["risks"]}
    assert ids == ALLOWED_IDS
    for row in data["risks"]:
        assert row["status"] not in FORBIDDEN_STATUS
        assert row["owner"] == "NOT_AVAILABLE"
        assert row["score"] == "NOT_SCORED"
        assert row["review_date"] == "NOT_SET"


def test_no_production_effective_controls():
    data = yaml.safe_load(CONTROLS.read_text(encoding="utf-8"))
    assert data["production_effective_count"] == 0
    assert data["monitored_count"] == 0
    for row in data["controls"]:
        assert row["effectiveness"] != "EFFECTIVE"
        assert row["status"] != "EFFECTIVE"
