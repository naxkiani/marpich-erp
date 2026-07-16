"""Session policy — pure domain helpers."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta


def session_expiry(days: int = 7) -> datetime:
    return datetime.now(UTC) + timedelta(days=days)


def remember_me_expiry(days: int = 30) -> datetime:
    return datetime.now(UTC) + timedelta(days=days)
