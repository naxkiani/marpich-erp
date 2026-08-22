"""P333 capability overlay must not invent OPERATIONAL/MATURE, skills, or readiness scores."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
OVERLAY = REPO / "docs" / "meos" / "execution" / "MEOS_CAPABILITY_READINESS.v1.yaml"
OBJECTIVES = REPO / "docs" / "meos" / "execution" / "MEOS_STRATEGIC_OBJECTIVES.v1.yaml"
LESSONS = REPO / "docs" / "meos" / "execution" / "MEOS_LESSONS_LEARNED.v1.yaml"
CATALOG = REPO / "backend" / "shared" / "contracts" / "business_capabilities.json"

FORBIDDEN_STATUS = frozenset({"OPERATIONAL", "MATURE", "DEPRECATED"})
FORBIDDEN_CMMI = frozenset({"MEASURED", "OPTIMIZED"})
KNOWN_CAP_PREFIX = ("CAP-",)
PLATFORM_IDS = frozenset(
    {
        "identity",
        "organization",
        "analytics",
        "search",
        "workflow",
        "secrets",
        "observability",
        "audit",
        "privacy_dsar",
        "production_cluster",
        "outcome_measurement",
    }
)


def test_readiness_overlay_is_mapped_not_operational():
    data = yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))
    assert data["overall_status"] == "MAPPED"
    assert data["maturity"] == "MAPPED"
    assert data["production_active"] is False
    assert data["operational_count"] == 0
    assert data["mature_count"] == 0
    assert data["skill_record_count"] == 0
    assert data["validated_capability_count"] == 0
    assert data["training_assigned_count"] == 0
    assert data["readiness"] == "NOT_MEASURED"
    assert data["workforce_capacity"] == "NOT_MEASURED"
    assert data["expertise_discovery"] == "NOT_IMPLEMENTED"
    assert data["owners"] == "NOT_AVAILABLE"


def test_capability_rows_are_not_inflated():
    data = yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))
    for row in data["capabilities"]:
        assert row["status"] not in FORBIDDEN_STATUS
        assert row["cmmi"] not in FORBIDDEN_CMMI
        assert row["owner"] == "NOT_AVAILABLE"
        assert row["status"] in {"DEFINED", "PARTIAL", "AT_RISK"}
        assert row["id"].startswith(KNOWN_CAP_PREFIX) or row["id"] in PLATFORM_IDS


def test_strategic_mappings_stay_blocked_and_draft():
    overlay = yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))
    objectives = yaml.safe_load(OBJECTIVES.read_text(encoding="utf-8"))
    obj_by_id = {row["id"]: row for row in objectives["objectives"]}
    assert objectives["active_count"] == 0
    for mapping in overlay["strategic_mappings"]:
        assert mapping["objective_status"] == "DRAFT"
        assert mapping["readiness"] == "BLOCKED"
        src = obj_by_id[mapping["objective_id"]]
        assert src["status"] == "DRAFT"
        assert src["class"] == "PLATFORM_GATE"


def test_gaps_have_owners_not_invented_and_no_pii_fields():
    data = yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))
    assert {g["id"] for g in data["gaps"]} >= {
        "GAP-PROD-CLUSTER",
        "GAP-SKILL-MODEL",
        "GAP-CRISIS-ROLES",
    }
    for gap in data["gaps"]:
        assert gap["owner"] == "NOT_AVAILABLE"
        assert "employee_id" not in gap
        assert "email" not in gap
        assert "full_name" not in gap


def test_lessons_still_unvalidated_so_knowledge_cannot_prove_capability():
    lessons = yaml.safe_load(LESSONS.read_text(encoding="utf-8"))
    assert lessons["validated_count"] == 0


def test_taxonomy_sor_file_exists():
    assert CATALOG.is_file()
    overlay = yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))
    assert "BUSINESS_CAPABILITIES_REGISTRY.md" in overlay["capability_taxonomy_sor"]
