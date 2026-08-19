"""P313 — offsite backup helper and script wiring."""
from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
S3 = ROOT / "scripts" / "meos_s3.py"
BACKUP = ROOT / "scripts" / "meos-postgres-backup.sh"


def test_parse_s3_uri():
    mod = runpy.run_path(str(S3))
    assert mod["parse_s3_uri"]("s3://meos-backups/postgres/a.sql.gz") == (
        "meos-backups",
        "postgres/a.sql.gz",
    )


def test_backup_script_uses_s3_helper_and_fail_closed():
    text = BACKUP.read_text(encoding="utf-8")
    assert "scripts/meos_s3.py" in text or "meos_s3.py" in text
    assert "MEOS_BACKUP_S3_URI" in text
    assert "MEOS_REQUIRE_OFFSITE" in text
