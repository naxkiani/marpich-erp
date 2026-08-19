"""P336 architecture overlay must not invent ACTIVE apps, usage, cost, or retirements."""
from __future__ import annotations

from pathlib import Path

import yaml

from core.presentation.api.startup_registry import (
    BLUEPRINT_CONTEXT_IDS,
    EMPTY_INDUSTRY_SCAFFOLD_IDS,
)

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
OVERLAY = EXEC / "MEOS_ARCHITECTURE_RATIONALIZATION.v1.yaml"
REGISTRY = EXEC / "MEOS_APPLICATION_REGISTRY.v1.yaml"
PORTFOLIO = EXEC / "MEOS_PORTFOLIO_INTELLIGENCE.v1.yaml"
CONTEXTS = REPO / "backend" / "contexts"


def _overlay() -> dict:
    return yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))


def _apps() -> list[dict]:
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    return list(data.get("applications") or [])


def test_overlay_is_inventoried_not_operating():
    data = _overlay()
    assert data["overall_status"] == "INVENTORIED"
    assert data["maturity"] == "INVENTORIED"
    assert data["production_active"] is False
    assert data["active_application_count"] == 0
    assert data["utilization"] == "NOT_MEASURED"
    assert data["cost"] == "NOT_MEASURED"
    assert data["realized_value"] == "NOT_MEASURED"
    assert data["cmdb"] == "NOT_IMPLEMENTED"
    assert data["itsm_product"] == "NOT_IMPLEMENTED"
    assert data["autonomous_architecture"] == "BLOCKED"
    assert data["max_autonomy_level"] == "L0"
    assert data["retirement_candidates"] == []
    assert data["graphql_runtime"] == "NOT_AVAILABLE"
    assert data["frontend_modules_dir"] == "ABSENT"
    assert data["frontend_deployable_apps"] == 1


def test_counts_match_registry_and_filesystem():
    data = _overlay()
    apps = _apps()
    by_status: dict[str, int] = {}
    for app in apps:
        by_status[app["status"]] = by_status.get(app["status"], 0) + 1
    assert data["registry_application_count"] == len(apps)
    assert data["status_counts"]["ACTIVE"] == by_status.get("ACTIVE", 0) == 0
    assert data["status_counts"]["SCAFFOLDED"] == by_status.get("SCAFFOLDED", 0) == len(
        EMPTY_INDUSTRY_SCAFFOLD_IDS
    )
    assert data["status_counts"]["BLUEPRINT"] == by_status.get("BLUEPRINT", 0) == len(
        BLUEPRINT_CONTEXT_IDS
    )
    assert data["empty_scaffold_count"] == 12
    ctx = [
        p.name
        for p in CONTEXTS.iterdir()
        if p.is_dir() and not p.name.startswith("_") and p.name != "__pycache__"
    ]
    assert data["backend_context_count"] == len(ctx)
    assert data["backend_context_count"] > data["registry_application_count"]


def test_lifecycle_does_not_retire_production():
    data = _overlay()
    recs = {row["class_id"]: row["recommendation"] for row in data["lifecycle_classes"]}
    assert recs["FUNCTIONAL_SLICE"] == "RETAIN"
    assert recs["EMPTY_SCAFFOLD"] == "FREEZE"
    assert recs["BLUEPRINT_FABRIC"] == "MONITOR"
    assert recs["DESIGNED_MISSING_PACKAGE"] == "DO_NOT_PROMOTE"
    assert recs["LEGACY_TYPESCRIPT_SERVICES"] == "CONSOLIDATE"
    for row in data["lifecycle_classes"]:
        assert row["recommendation"] != "RETIRE"
        assert row["expected_value"] == "NOT_MEASURED"


def test_redundancy_does_not_eliminate_on_names():
    data = _overlay()
    by_id = {row["id"]: row for row in data["redundancy"]}
    assert by_id["RD-INV-WH"]["class"] == "PARTIAL_OVERLAP"
    assert by_id["RD-EDU"]["class"] == "COMPLEMENTARY"
    assert by_id["RD-FINANCE-SURFACE"]["action"] == "DO_NOT_ELIMINATE"
    assert by_id["RD-TS-PYTHON-IDENTITY"]["class"] == "FULL_DUPLICATION"
    assert by_id["RD-TS-PYTHON-IDENTITY"]["retire_production"] == "FORBIDDEN"


def test_p335_feed_reuses_existing_initiatives():
    overlay = _overlay()
    port = yaml.safe_load(PORTFOLIO.read_text(encoding="utf-8"))
    debt = yaml.safe_load((EXEC / "MEOS_TECHNICAL_DEBT_REGISTRY.v1.yaml").read_text())
    init_ids = {row["initiative_id"] for row in port["items"]}
    debt_ids = {item["id"] for item in debt["items"]}
    rows = overlay["modernization_into_p335"]
    assert any(r.get("new_initiative") == "FORBIDDEN" for r in rows)
    for row in rows:
        assert row.get("new_initiative") is not True
        if "initiative_id" in row:
            assert row["initiative_id"] in init_ids
        if "debt_id" in row:
            assert row["debt_id"] in debt_ids
