"""P334 change overlay must not invent IN_PROGRESS, COMPLETED, or adoption."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
EXEC = REPO / "docs" / "meos" / "execution"
CHANGES = EXEC / "MEOS_CHANGE_REGISTRY.v1.yaml"
INITIATIVES = EXEC / "MEOS_INITIATIVE_PORTFOLIO.v1.yaml"
RELEASES = EXEC / "MEOS_RELEASE_REGISTRY.v1.yaml"
READINESS = EXEC / "MEOS_CAPABILITY_READINESS.v1.yaml"
ADOPTION_DOC = EXEC / "MEOS_ADOPTION_STATUS.md"

FORBIDDEN_STATUS = frozenset(
    {"APPROVED", "PLANNED", "IN_PROGRESS", "VALIDATION", "COMPLETED", "ROLLED_BACK"}
)
ALLOWED_STATUS = frozenset({"PROPOSED", "ASSESSED", "CANCELLED"})


def test_change_registry_is_inventoried_not_executing():
    data = yaml.safe_load(CHANGES.read_text(encoding="utf-8"))
    assert data["overall_status"] == "INVENTORIED"
    assert data["maturity"] == "INVENTORIED"
    assert data["production_active"] is False
    assert data["production_change_count"] == 0
    assert data["approved_count"] == 0
    assert data["in_progress_count"] == 0
    assert data["completed_count"] == 0
    assert data["rolled_back_count"] == 0
    assert data["adopted"] is False
    assert data["adoption_metrics"] == "NOT_MEASURED"
    assert data["readiness"] == "NOT_MEASURED"
    assert data["training_completed_count"] == 0
    assert data["owners"] == "NOT_AVAILABLE"
    assert data["projects_context"] == "SCAFFOLDED"
    assert data["autonomous_change"] == "BLOCKED"
    assert data["max_autonomy_level"] == "L0"


def test_change_rows_map_initiatives_and_stay_pre_approval():
    overlay = yaml.safe_load(CHANGES.read_text(encoding="utf-8"))
    initiatives = yaml.safe_load(INITIATIVES.read_text(encoding="utf-8"))
    init_ids = {row["id"] for row in initiatives["initiatives"]}
    assert initiatives["in_progress_count"] == 0
    for row in overlay["changes"]:
        assert row["status"] in ALLOWED_STATUS
        assert row["status"] not in FORBIDDEN_STATUS
        assert row["owner"] == "NOT_AVAILABLE"
        assert row["sponsor"] == "NOT_AVAILABLE"
        assert row["start"] == "NOT_SET"
        assert row["target_date"] == "NOT_SET"
        assert row["adoption"] == "NOT_MEASURED"
        assert row["readiness"] == "BLOCKED"
        assert row["initiative_id"] in init_ids
        assert row["procedure_category"] in {"STANDARD", "NORMAL", "EMERGENCY"}


def test_no_production_release_to_attach():
    releases = yaml.safe_load(RELEASES.read_text(encoding="utf-8"))
    assert releases["production_release_count"] == 0


def test_readiness_and_adoption_sources_remain_honest():
    readiness = yaml.safe_load(READINESS.read_text(encoding="utf-8"))
    assert readiness["readiness"] == "NOT_MEASURED"
    assert readiness["training_assigned_count"] == 0
    text = ADOPTION_DOC.read_text(encoding="utf-8")
    assert "**ADOPTED:** **false**" in text
    assert "NOT_AVAILABLE" in text


def test_g26_blocks_all_production_changes():
    data = yaml.safe_load(CHANGES.read_text(encoding="utf-8"))
    blocker_ids = {b["id"] for b in data["blockers"]}
    assert "BLK-G26" in blocker_ids
    g26 = next(c for c in data["changes"] if c["id"] == "CHG-G26")
    assert g26["risk"] == "R-01"
    for row in data["changes"]:
        if row["id"] != "CHG-G26":
            assert "CHG-G26" in row.get("depends_on", [])
