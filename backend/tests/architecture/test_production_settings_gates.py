"""P0 — production settings hard gates."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from shared.infrastructure.settings import Settings, _DEFAULT_JWT_SECRET


def test_development_allows_default_jwt():
    s = Settings(marpich_environment="development", jwt_secret=_DEFAULT_JWT_SECRET)
    assert s.jwt_secret == _DEFAULT_JWT_SECRET
    assert s.event_bus_mode == "direct"


def test_production_rejects_default_jwt():
    with pytest.raises(ValidationError):
        Settings(
            marpich_environment="production",
            jwt_secret=_DEFAULT_JWT_SECRET,
            persistence_backend="postgres",
        )


def test_production_forces_outbox_and_requires_postgres():
    s = Settings(
        marpich_environment="production",
        jwt_secret="a" * 40,
        persistence_backend="postgres",
        database_url="postgresql+asyncpg://app:strong-secret@db.internal:5432/marpich",
        event_bus_mode="direct",
        otel_enabled=True,
        document_signing_secret="doc-secret",
    )
    assert s.event_bus_mode == "outbox"


def test_production_rejects_default_database_credentials():
    with pytest.raises(ValidationError):
        Settings(
            marpich_environment="production",
            jwt_secret="a" * 40,
            persistence_backend="postgres",
            database_url="postgresql+asyncpg://marpich:marpich@127.0.0.1:5432/marpich_platform",
        )


def test_production_rejects_memory_persistence():
    with pytest.raises(ValidationError):
        Settings(
            marpich_environment="production",
            jwt_secret="a" * 40,
            persistence_backend="memory",
            database_url="postgresql+asyncpg://app:strong-secret@db.internal:5432/marpich",
        )
