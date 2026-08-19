"""P313 — federation migration 017 must be re-runnable (CREATE POLICY idempotent)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SQL = ROOT / "infrastructure/docker/migrations/017_eif_fabric_schema.sql"


def test_017_create_policy_is_idempotent():
    text = SQL.read_text(encoding="utf-8")
    assert "FROM pg_policies" in text
    assert "CREATE POLICY tenant_isolation_" in text
    assert text.index("FROM pg_policies") < text.index(
        "'CREATE POLICY tenant_isolation_%s ON %I.%I USING (tenant_id = identity.current_tenant_id())'"
    )
