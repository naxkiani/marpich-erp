"""Strategic registries must not invent ACTIVE OKRs, costs, or executed decisions."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OBJECTIVES = EXEC / "MEOS_STRATEGIC_OBJECTIVES.v1.yaml"
INITIATIVES = EXEC / "MEOS_INITIATIVE_PORTFOLIO.v1.yaml"
DECISIONS = EXEC / "MEOS_DECISION_REGISTRY.v1.yaml"
DEBT = EXEC / "MEOS_TECHNICAL_DEBT_REGISTRY.v1.yaml"

FORBIDDEN_OBJ = frozenset({"ACTIVE", "AT_RISK", "ACHIEVED"})


def test_objectives_are_draft_platform_gates():
    data = yaml.safe_load(OBJECTIVES.read_text(encoding="utf-8"))
    assert data["overall_status"] == "NOT_DECLARED"
    assert data["active_count"] == 0
    assert data["achieved_count"] == 0
    assert data["class"] == "PLATFORM_GATE"
    for row in data["objectives"]:
        assert row["status"] not in FORBIDDEN_OBJ
        assert row["class"] == "PLATFORM_GATE"
        assert row["owner"] == "NOT_AVAILABLE"
        assert row["timeframe"] == "NOT_SET"
        assert row["confidence"] == "NOT_AVAILABLE"


def test_initiatives_have_no_invented_cost_and_map_to_debt():
    port = yaml.safe_load(INITIATIVES.read_text(encoding="utf-8"))
    debt = yaml.safe_load(DEBT.read_text(encoding="utf-8"))
    debt_ids = {item["id"] for item in debt["items"]}
    assert port["in_progress_count"] == 0
    assert port["cost_measured_count"] == 0
    for row in port["initiatives"]:
        assert row["debt_id"] in debt_ids
        assert row["cost"] == "NOT_MEASURED"
        assert row["effort"] == "NOT_MEASURED"
        assert row["value"] == "NOT_MEASURED"
        assert row["owner"] == "NOT_AVAILABLE"
        assert row["timeline"] == "NOT_SET"


def test_decisions_are_documented_not_executed():
    data = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    assert data["executed_count"] == 0
    assert data["measured_followup_count"] == 0
    for row in data["decisions"]:
        assert row["lifecycle"] == "DECIDE"
        assert row["owner"] == "NOT_AVAILABLE"
        assert row["workflow_task_id"] == "NOT_AVAILABLE"
        assert str(row["evidence"]).startswith("docs/meos/execution/")
        assert row["actual_outcome"] in {
            "NOT_MEASURED",
            "production_release_count = 0",
            "measured_count = 0",
        }
