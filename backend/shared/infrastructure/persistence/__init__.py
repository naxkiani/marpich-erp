"""Repository backend selection — memory vs PostgreSQL."""
from __future__ import annotations

from shared.infrastructure.settings import use_postgres

__all__ = ["use_postgres"]
