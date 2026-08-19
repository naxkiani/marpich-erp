"""Autonomy overlay must not claim L3/L4 or healthy production observe."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
LEVELS = REPO / "docs" / "meos" / "execution" / "MEOS_AUTONOMY_LEVELS.v1.yaml"


def test_production_autonomy_is_l0_and_block_automation():
    data = yaml.safe_load(LEVELS.read_text(encoding="utf-8"))
    assert data["block_automation"] is True
    assert data["max_authorized_level"] == "L0"
    assert data["production_level"] == "L0"
    assert data["observe_operational"] is False
    assert data["l1_recommendations_authoritative"] is False
    assert data["l2_hitl_active"] is False
    assert data["l3_policy_automation_active"] is False
    assert data["l4_controlled_autonomous_active"] is False
    assert data["levels"]["L3"]["production"] == "NOT_ACTIVE"
    assert data["levels"]["L4"]["production"] == "NOT_ACTIVE"
    assert data["levels"]["L0"]["production"] == "AUTHORIZED_BUT_BLOCKED"
