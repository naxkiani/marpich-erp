"""P338 decision overlay must not invent KPI values, signals, or a new intelligence platform."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OVERLAY = EXEC / "MEOS_DECISION_INTELLIGENCE.v1.yaml"
DECISIONS = EXEC / "MEOS_DECISION_REGISTRY.v1.yaml"
DATA = EXEC / "MEOS_DATA_ARCHITECTURE.v1.yaml"
INITIATIVES = EXEC / "MEOS_INITIATIVE_PORTFOLIO.v1.yaml"
DEBT = EXEC / "MEOS_TECHNICAL_DEBT_REGISTRY.v1.yaml"
CONTEXTS = REPO / "backend" / "contexts"

FORBIDDEN_MATURITY = frozenset(
    {"DECISION_READY", "DECISION_INTELLIGENT", "ACTIONABLE", "PREDICTIVE", "CONNECTED"}
)
FORBIDDEN_KPI_TRUST = frozenset({"VERIFIED"})


def _overlay() -> dict:
    return yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))


def test_overlay_is_foundation_not_operating():
    data = _overlay()
    assert data["overall_status"] == "DOCUMENTED"
    assert data["maturity"] == "FOUNDATION"
    assert data["maturity"] not in FORBIDDEN_MATURITY
    assert data["production_active"] is False
    assert data["executed_decision_count"] == 0
    assert data["measured_outcome_count"] == 0
    assert data["kpi_governed_business_count"] == 0
    assert data["kpi_trust"] == "NOT_MEASURED"
    assert data["executive_signals_count"] == 0
    assert data["early_warning_state"] == "NOT_AVAILABLE"
    assert data["scenario_count"] == 0
    assert data["forecast_count"] == 0
    assert data["ai_decision_support"] == "STUB"
    assert data["ai_confidence"] == "NOT_AVAILABLE"
    assert data["ai_autonomous_approval"] == "FORBIDDEN"
    assert data["max_autonomy_level"] == "L0"
    assert data["business_value"] == "NOT_MEASURED"
    assert data["decision_queue_implemented"] is False
    assert data["runtime_decision_registry"] == "NOT_IMPLEMENTED"
    assert data["new_bi_platform"] == "FORBIDDEN"
    assert data["new_analytics_engine"] == "FORBIDDEN"
    assert data["new_ai_platform"] == "FORBIDDEN"
    assert data["new_kpi_engine"] == "FORBIDDEN"
    assert data["new_executive_erp_module"] == "FORBIDDEN"
    assert data["signals"] == []
    assert data["early_warnings"] == []
    assert data["scenarios"] == "NOT_CREATED"


def test_decision_count_matches_registry():
    overlay = _overlay()
    registry = yaml.safe_load(DECISIONS.read_text(encoding="utf-8"))
    assert overlay["decision_count"] == len(registry["decisions"]) == 4
    assert registry["executed_count"] == 0
    assert registry["measured_followup_count"] == 0
    assert overlay["executed_decision_count"] == registry["executed_count"]
    for row in registry["decisions"]:
        assert row["lifecycle"] == "DECIDE"
        assert row["workflow_task_id"] == "NOT_AVAILABLE"


def test_home_pulse_not_authoritative_kpi():
    data = _overlay()
    pulse = data["home_pulse"]
    assert pulse["signal_class"] == "CATALOG_COUNT"
    assert pulse["production_kpis"] == "DATA_NOT_AVAILABLE"
    assert pulse["data_quality_status"] == "DATA_QUALITY_WARNING"
    assert data["kpi_trust_summary"]["verified"] == 0
    assert data["kpi_trust_summary"]["not_measured"] == data["kpi_catalog_count"] == 12


def test_does_not_create_duplicate_intelligence_platforms():
    data = _overlay()
    assert (CONTEXTS / "analytics").is_dir()
    assert not (CONTEXTS / "decision_intelligence").exists()
    forbidden = data["forbidden_without_evidence"]
    assert "VERIFIED_KPI" in forbidden
    assert "RECOMMENDATION" in forbidden
    assert data["kpi_trust"] not in FORBIDDEN_KPI_TRUST


def test_p337_and_initiative_feed_reuses_existing():
    overlay = _overlay()
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    initiatives = yaml.safe_load(INITIATIVES.read_text(encoding="utf-8"))
    debt = yaml.safe_load(DEBT.read_text(encoding="utf-8"))
    init_ids = {row["id"] for row in initiatives["initiatives"]}
    debt_ids = {item["id"] for item in debt["items"]}
    feed = overlay["p337_feed"]
    assert feed["published_data_product_count"] == 0
    assert feed["lineage"] == "LINEAGE_INCOMPLETE"
    assert feed["quality"] == "NOT_MEASURED"
    assert data["published_data_product_count"] == 0
    p336 = overlay["p336_feed"]
    assert p336["new_decision_platform"] == "FORBIDDEN"
    assert p336["new_initiative"] == "FORBIDDEN"
    for iid in p336["initiative_ids"]:
        assert iid in init_ids
    for did in p336["debt_ids"]:
        assert did in debt_ids
