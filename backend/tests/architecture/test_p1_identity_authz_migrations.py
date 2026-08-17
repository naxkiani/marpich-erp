"""P1 — identity/authz SQL migrations are on disk and listed in the runner."""
from __future__ import annotations

from pathlib import Path

P1_MIGRATIONS = (
    "018_enterprise_directory_service.sql",
    "020_enterprise_organization_directory.sql",
    "021_enterprise_identity_graph.sql",
    "022_enterprise_authentication_platform.sql",
    "023_enterprise_password_authentication_engine.sql",
    "024_security_trusted_devices.sql",
    "025_enterprise_passkey_webauthn_platform.sql",
    "026_enterprise_adaptive_mfa_platform.sql",
    "027_enterprise_adaptive_risk_auth_engine.sql",
    "030_enterprise_authorization_platform.sql",
    "037_identity_governance.sql",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def test_p1_migrations_exist_on_disk():
    migrations = _repo_root() / "infrastructure" / "docker" / "migrations"
    for name in P1_MIGRATIONS:
        path = migrations / name
        assert path.is_file(), f"missing {name}"
        text = path.read_text()
        assert "tenant_id" in text
        assert "ROW LEVEL SECURITY" in text


def test_p1_migrations_listed_in_runner():
    runner = (_repo_root() / "scripts" / "run-migrations.sh").read_text()
    for name in P1_MIGRATIONS:
        assert name in runner, f"{name} not in POST_WAVE01_MIGRATIONS"


def test_deferred_catalog_no_longer_lists_missing_files():
    catalog = (
        _repo_root() / "infrastructure" / "docker" / "migrations" / "DEFERRED_MIGRATIONS.md"
    ).read_text()
    lowered = catalog.lower()
    assert "on disk" in lowered
    assert "no longer skipped" in lowered
    assert "missing as of" not in catalog
