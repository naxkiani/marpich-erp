"""P339 execution overlay must not invent actions, benefits, or a new PMO/workflow product."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OVERLAY = EXEC / "MEOS_DECISION_EXECUTION.v1.yaml"
DECISIONS = EXEC / "MEOS_DECISION_REGISTRY.v1.yaml"
OUTCOMES = EXEC / "MEOS_OUTCOME_REGISTRY.v1.yaml"
INTELLIGENCE = EXEC / "MEOS_DECISION_INTELLIGENCE.v1.yaml"
INITIATIVES = EXEC / "MEOS_INITIATIVE_PORTFOLIO.v1.yaml"
DEBT = EXEC / "MEOS_TECHNICAL_DEBT_REGISTRY.v1.yaml"
PORTFOLIO = EXEC / "MEOS_PORTFOLIO_INTELLIGENCE.v1.yaml"
CONTEXTS = REPO / "backend" / "contexts"

FORBIDDEN_MATURITY = frozenset({"EXECUTING", "REALIZING", "CLOSED_LOOP", "ACTIONABLE"})
FORBIDDEN_ACTION = frozenset({"IN_PROGRESS", "COMPLETED", "READY"})
FORBIDDEN_BENEFIT = frozenset({"REALIZED", "PARTIALLY_REALIZED", "AT_RISK", "TRACKING"})


def _overlay() -> dict:
    return yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))


def test_overlay_is_inventoried_not_closed_loop():
    data = _overlay()
    assert data["overall_status"] == "DOCUMENTED"
    assert data["maturity"] == "INVENTORIED"
    assert data["maturity"] not in FORBIDDEN_MATURITY
    assert data["production_active"] is False
    assert data["closed_loop"] == "BLOCKED"
    assert data["authorized_action_count"] == 0
    assert data["in_progress_action_count"] == 0
    assert data["completed_action_count"] == 0
    assert data["failed_action_count"] == 0
    assert data["execution_readiness"] == "NOT_READY"
    assert data["benefit_count"] == 0
    assert data["realized_benefit_count"] == 0
    assert data["realized_value"] == "NOT_MEASURED"
    assert data["expected_value"] == "NOT_MEASURED"
    assert data["value_variance"] == "NOT_MEASURED"
    assert data["corrective_action_count"] == 0
    assert data["autonomous_execution"] == "BLOCKED"
    assert data["max_autonomy_level"] == "L0"
    assert data["ai_high_impact_approval"] == "FORBIDDEN"
    assert data["projects_context"] == "SCAFFOLDED"
    assert data["new_project_platform"] == "FORBIDDEN"
    assert data["new_workflow_engine"] == "FORBIDDEN"
    assert data["new_bpm_platform"] == "FORBIDDEN"
    assert data["new_pmo"] == "FORBIDDEN"
    assert data["actions"] == []
    assert data["benefits"] == []
    assert data["corrective_actions"] == []


def test_gate_decisions_have_no_authorized_actions():
    overlay = _overlay()
    registry = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    intel = yaml.safe_load(INTELLIGENCE.read_text(encoding="utf-8"))
    rows = overlay["decision_to_action"]
    assert overlay["decision_count"] == len(registry["decisions"]) == len(rows) == 4
    assert overlay["executed_decision_count"] == registry["executed_count"] == 0
    assert intel["executed_decision_count"] == 0
    assert overlay["workflow_task_binding"] == "NOT_AVAILABLE"
    for row in rows:
        assert row["authorized_action"] == "NONE"
        assert row["status"] == "BLOCKED"
        assert row["status"] not in FORBIDDEN_ACTION
        assert row["owner"] == "NOT_AVAILABLE"
        assert row["workflow_task_id"] == "NOT_AVAILABLE"
    for dec in registry["decisions"]:
        assert dec["lifecycle"] == "DECIDE"
        assert dec["workflow_task_id"] == "NOT_AVAILABLE"


def test_outcomes_remain_unmeasured_and_projects_scaffolded():
    overlay = _overlay()
    outcomes = yaml.safe_load(OUTCOMES.read_text(encoding="utf-8"))
    port = yaml.safe_load(PORTFOLIO.read_text(encoding="utf-8"))
    assert overlay["outcome_measured_count"] == outcomes["measured_count"] == 0
    assert overlay["kpi_trust"] == "NOT_MEASURED"
    assert port["projects_context"] == "SCAFFOLDED"
    assert port["realized_value_count"] == 0
    projects = CONTEXTS / "projects"
    assert projects.is_dir()
    assert not (projects / "application" / "service.py").exists()
    assert not (CONTEXTS / "pmo").exists()
    for row in overlay.get("benefits") or []:
        assert row.get("status") not in FORBIDDEN_BENEFIT


def test_p338_and_initiative_feed_reuses_existing():
    overlay = _overlay()
    intel = yaml.safe_load(INTELLIGENCE.read_text(encoding="utf-8"))
    initiatives = yaml.safe_load(INITIATIVES.read_text(encoding="utf-8"))
    debt = yaml.safe_load(DEBT.read_text(encoding="utf-8"))
    init_ids = {row["id"] for row in initiatives["initiatives"]}
    debt_ids = {item["id"] for item in debt["items"]}
    feed = overlay["p338_feed"]
    assert feed["maturity"] == intel["maturity"] == "FOUNDATION"
    assert feed["executed_decision_count"] == 0
    assert feed["workflow_task_binding"] == "NOT_AVAILABLE"
    p336 = overlay["p336_feed"]
    assert p336["new_execution_platform"] == "FORBIDDEN"
    assert p336["new_initiative"] == "FORBIDDEN"
    for iid in p336["initiative_ids"]:
        assert iid in init_ids
    for did in p336["debt_ids"]:
        assert did in debt_ids
    assert (CONTEXTS / "workflow").is_dir()
    assert not (CONTEXTS / "decision_execution").exists()
