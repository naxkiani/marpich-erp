"""Lessons must stay DRAFT; no invented validated learning."""
from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
LESSONS = REPO / "docs" / "meos" / "execution" / "MEOS_LESSONS_LEARNED.v1.yaml"
FORBIDDEN = frozenset({"VALIDATED", "PUBLISHED", "IMPLEMENTED", "APPLIED"})


def test_lessons_are_draft_not_validated():
    data = yaml.safe_load(LESSONS.read_text(encoding="utf-8"))
    assert data["validated_count"] == 0
    assert data["applied_count"] == 0
    assert data["reused_count"] == 0
    assert data["production_pir_count"] == 0
    for row in data["lessons"]:
        assert row["status"] not in FORBIDDEN
        assert row["validation"] == "NOT_COMPLETE"
        assert row["owner"] == "NOT_AVAILABLE"
        assert row["authority"] == "PROGRAM_DOCUMENT"
        assert row["status"] == "DRAFT"
