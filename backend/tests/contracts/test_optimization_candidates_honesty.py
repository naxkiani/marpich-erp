"""Optimization overlay must not invent verified gains or reuse local p95 as prod."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
CAND = REPO / "docs" / "meos" / "execution" / "MEOS_OPTIMIZATION_CANDIDATES.v1.yaml"


def test_no_production_verified_optimizations_or_forecasts():
    data = yaml.safe_load(CAND.read_text(encoding="utf-8"))
    assert data["production_verified_count"] == 0
    assert data["forecast_count"] == 0
    assert data["implemented_this_phase"] == 0
    assert data["autonomy_max"] == "L0"
    by_id = {row["id"]: row for row in data["candidates"]}
    local = by_id["OPT-LOCAL-P95"]
    assert local["status"] == "REJECTED"
    assert local["expected_gain"] == "NOT_MEASURED"
    for row in data["candidates"]:
        assert row["expected_gain"] == "NOT_MEASURED"
        assert row["owner"] == "NOT_AVAILABLE"
        assert row["status"] in {"IDENTIFIED", "ASSESSED", "APPROVED", "IMPLEMENTED", "VERIFIED", "REJECTED"}
        assert row["status"] not in {"IMPLEMENTED", "VERIFIED"}
