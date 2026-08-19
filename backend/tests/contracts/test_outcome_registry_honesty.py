"""Outcome registry must not claim measured business value."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
REGISTRY = REPO / "docs" / "meos" / "execution" / "MEOS_OUTCOME_REGISTRY.v1.yaml"
FORBIDDEN = frozenset({"MEASURED", "BASELINED", "IMPROVING", "ACHIEVED", "STABLE"})


def test_outcomes_are_identified_not_measured():
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert data["measured_count"] == 0
    assert data["achieved_count"] == 0
    assert data["overall_status"] == "NOT_MEASURED"
    for row in data["outcomes"]:
        assert row["state"] not in FORBIDDEN
        assert row["baseline"] == "NOT_MEASURED"
        assert row["current"] == "NOT_MEASURED"
        assert row["target"] == "NOT_SET"
