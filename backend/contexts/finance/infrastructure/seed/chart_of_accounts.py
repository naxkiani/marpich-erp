"""Backward-compatible re-export — use application.services.chart_seeder."""
from __future__ import annotations

from contexts.finance.application.services.chart_seeder import build_default_accounts as seed_default_accounts

__all__ = ["seed_default_accounts"]
