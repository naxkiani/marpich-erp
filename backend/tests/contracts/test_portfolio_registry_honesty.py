"""P335 portfolio overlay must not invent ACTIVE portfolios, budgets, or ROI."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
PORTFOLIO = EXEC / "MEOS_PORTFOLIO_INTELLIGENCE.v1.yaml"
INITIATIVES = EXEC / "MEOS_INITIATIVE_PORTFOLIO.v1.yaml"
CHANGES = EXEC / "MEOS_CHANGE_REGISTRY.v1.yaml"
OBJECTIVES = EXEC / "MEOS_STRATEGIC_OBJECTIVES.v1.yaml"
OUTCOMES = EXEC / "MEOS_OUTCOME_REGISTRY.v1.yaml"
DEBT = EXEC / "MEOS_TECHNICAL_DEBT_REGISTRY.v1.yaml"
READINESS = EXEC / "MEOS_CAPABILITY_READINESS.v1.yaml"

FORBIDDEN_STATUS = frozenset(
    {"ACTIVE", "APPROVED", "AT_RISK", "PAUSED", "COMPLETED", "CANCELLED", "RETIRED"}
)
ALLOWED_ITEM_STATUS = frozenset({"PROPOSED", "ASSESSED", "IDENTIFIED"})
ALLOWED_RECOMMEND = frozenset({"CONTINUE", "DEFER", "REASSESS"})
MONEY_FIELDS = (
    "investment",
    "expected_value",
    "realized_value",
)


def test_portfolio_is_inventoried_not_operating():
    data = yaml.safe_load(PORTFOLIO.read_text(encoding="utf-8"))
    assert data["overall_status"] == "INVENTORIED"
    assert data["maturity"] == "INVENTORIED"
    assert data["production_active"] is False
    assert data["in_progress_count"] == 0
    assert data["approved_count"] == 0
    assert data["completed_count"] == 0
    assert data["investment_measured_count"] == 0
    assert data["realized_value_count"] == 0
    assert data["forecast_count"] == 0
    assert data["scenario_count"] == 0
    assert data["budget_aggregate"] == "NOT_IMPLEMENTED"
    assert data["projects_context"] == "SCAFFOLDED"
    assert data["finance_budget"] == "NOT_IMPLEMENTED"
    assert data["autonomous_portfolio"] == "BLOCKED"
    assert data["max_autonomy_level"] == "L0"
    assert data["portfolio_health"] == "NOT_MEASURED"
    assert data["value_state"] == "NOT_MEASURED"


def test_single_launch_portfolio_maps_existing_initiatives():
    overlay = yaml.safe_load(PORTFOLIO.read_text(encoding="utf-8"))
    initiatives = yaml.safe_load(INITIATIVES.read_text(encoding="utf-8"))
    init_ids = {row["id"] for row in initiatives["initiatives"]}
    assert len(overlay["portfolios"]) == 1
    pf = overlay["portfolios"][0]
    assert pf["id"] == "PF-LAUNCH-GOVERNANCE"
    assert pf["status"] not in FORBIDDEN_STATUS
    assert pf["status"] == "ASSESSED"
    assert pf["owner"] == "NOT_AVAILABLE"
    assert pf["sponsor"] == "NOT_AVAILABLE"
    assert pf["expected_value"] == "NOT_MEASURED"
    assert pf["actual_value"] == "NOT_MEASURED"
    assert pf["investment"] == "NOT_MEASURED"
    assert pf["budget"] == "NOT_MEASURED"
    assert set(pf["initiative_ids"]) == init_ids
    for oid in pf["objective_ids"]:
        assert oid.startswith("OBJ-GATE-")


def test_items_are_transparent_and_unmeasured():
    overlay = yaml.safe_load(PORTFOLIO.read_text(encoding="utf-8"))
    initiatives = yaml.safe_load(INITIATIVES.read_text(encoding="utf-8"))
    changes = yaml.safe_load(CHANGES.read_text(encoding="utf-8"))
    debt = yaml.safe_load(DEBT.read_text(encoding="utf-8"))
    init_ids = {row["id"] for row in initiatives["initiatives"]}
    change_ids = {row["id"] for row in changes["changes"]}
    debt_ids = {item["id"] for item in debt["items"]}
    item_ids = {row["initiative_id"] for row in overlay["items"]}
    assert item_ids == init_ids
    sequences = [row["sequence"] for row in overlay["items"]]
    assert sequences == sorted(sequences)
    assert overlay["items"][0]["initiative_id"] == "INIT-G26"
    assert overlay["items"][0]["continue_pause_reassess"] == "CONTINUE"
    for row in overlay["items"]:
        assert row["status"] in ALLOWED_ITEM_STATUS
        assert row["status"] not in FORBIDDEN_STATUS
        assert row["continue_pause_reassess"] in ALLOWED_RECOMMEND
        assert row["continue_pause_reassess"] != "CANCEL"
        assert row["method"]
        assert row["inputs"]
        assert row["assumptions"]
        assert row["result"]
        assert row["confidence"] == "HIGH_FOR_SEQUENCE_ONLY"
        assert row["owner"] == "NOT_AVAILABLE"
        for field in MONEY_FIELDS:
            assert row[field] == "NOT_MEASURED"
        assert row["capability_readiness"] == "NOT_MEASURED"
        assert row["change_readiness"] == "BLOCKED"
        assert row["initiative_id"] in init_ids
        assert row["change_id"] in change_ids
        assert row["debt_id"] in debt_ids
        if row["initiative_id"] != "INIT-G26":
            assert "INIT-G26" in row.get("depends_on", [])
            assert row["continue_pause_reassess"] == "DEFER"


def test_objectives_outcomes_readiness_remain_honest():
    objectives = yaml.safe_load(OBJECTIVES.read_text(encoding="utf-8"))
    outcomes = yaml.safe_load(OUTCOMES.read_text(encoding="utf-8"))
    readiness = yaml.safe_load(READINESS.read_text(encoding="utf-8"))
    assert objectives["overall_status"] == "NOT_DECLARED"
    assert objectives["active_count"] == 0
    assert outcomes["measured_count"] == 0
    assert outcomes["achieved_count"] == 0
    assert readiness["readiness"] == "NOT_MEASURED"
    assert readiness["operational_count"] == 0


def test_concentration_is_pre_production_not_invented_growth():
    data = yaml.safe_load(PORTFOLIO.read_text(encoding="utf-8"))
    conc = data["concentration"]
    assert conc["GROWTH"] == 0
    assert conc["CUSTOMER_VALUE"] == 0
    assert conc["INNOVATION"] == 0
    assert conc["EFFICIENCY"] == 0
    assert conc["OPERATIONAL_RESILIENCE"] == 3
    assert data["resource_conflicts"]["budget"] == "NOT_MEASURED"
    assert data["resource_conflicts"]["capacity"] == "NOT_MEASURED"
    blocker_ids = {b["id"] for b in data["blockers"]}
    assert "BLK-G26" in blocker_ids
    assert "BLK-FINANCE-BUDGET" in blocker_ids
    assert "BLK-PROJECTS-EMPTY" in blocker_ids
    assert data["gates"]["FINANCIAL_GATE"] == "NOT_IMPLEMENTED"
    assert data["gates"]["BUSINESS_CASE_GATE"] == "NOT_IMPLEMENTED"
