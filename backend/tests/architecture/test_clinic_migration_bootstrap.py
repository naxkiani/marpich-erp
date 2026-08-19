"""P313 — clinic migration must create schema before ALTER walk-in encounters."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SQL = ROOT / "infrastructure/docker/migrations/033_clinic_walkin_encounters.sql"


def test_033_bootstraps_clinic_schema_before_alter():
    text = SQL.read_text(encoding="utf-8")
    assert "CREATE SCHEMA IF NOT EXISTS clinic" in text
    assert "CREATE TABLE IF NOT EXISTS clinic.encounters" in text
    assert "ALTER TABLE clinic.encounters" in text
    assert text.index("CREATE SCHEMA IF NOT EXISTS clinic") < text.index(
        "ALTER TABLE clinic.encounters"
    )
