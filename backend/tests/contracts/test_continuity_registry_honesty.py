"""Continuity overlay must not invent crises, active playbooks, or production validation."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
CRISIS = EXEC / "MEOS_CRISIS_REGISTRY.v1.yaml"
PLAYBOOKS = EXEC / "MEOS_CRISIS_PLAYBOOKS.v1.yaml"
TESTS = EXEC / "MEOS_CONTINUITY_TESTING.v1.yaml"


def test_no_declared_crisis_or_staffed_command():
    data = yaml.safe_load(CRISIS.read_text(encoding="utf-8"))
    assert data["declared_count"] == 0
    assert data["active_count"] == 0
    assert data["production_ir_active"] is False
    assert data["command_staffed"] is False
    assert data["resilience_score"] == "NOT_SCORED"
    assert data["continuity_mode"] == "NOT_IN_FORCE"
    for key in (
        "incident_commander",
        "technical_lead",
        "business_lead",
        "security_lead",
        "communication_lead",
        "recovery_lead",
    ):
        assert data["roles"][key] == "NOT_AVAILABLE"


def test_playbooks_not_active():
    data = yaml.safe_load(PLAYBOOKS.read_text(encoding="utf-8"))
    assert data["active_count"] == 0
    for row in data["playbooks"]:
        assert row["production"] in {
            "NOT_ACTIVE",
            "NOT_VERIFIED",
            "BLOCKED",
            "NOT_CERTIFIED_CLUSTER",
            "NOT_APPLICABLE",
            "NOT_MEASURED",
        }
        assert row["status"] in {"DOCUMENTED", "NOT_IMPLEMENTED"}


def test_continuity_tests_not_production_validated():
    data = yaml.safe_load(TESTS.read_text(encoding="utf-8"))
    assert data["production_validated"] is False
    assert data["simulation_count"] == 0
    for row in data["tests"]:
        assert row["production"] in {"NOT_VERIFIED", "BLOCKED"}
        if row["id"] == "CT-G09-OFFSITE":
            assert row["geographic_failover"] == "NOT_DEMONSTRATED"
        if row["id"] == "CT-SIM-CRISIS":
            assert row["result"] == "NOT_CREATED"
            assert row["label"] == "SIMULATION"
        if row["environment"] == "PRODUCTION":
            assert row["result"] == "BLOCKED"
