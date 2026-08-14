"""Biotechnology DI container."""
from __future__ import annotations

from contexts.biotechnology.application.service import BiotechnologyApplicationService

_service: BiotechnologyApplicationService | None = None


def get_biotechnology_service() -> BiotechnologyApplicationService:
    global _service
    if _service is None:
        _service = BiotechnologyApplicationService()
    return _service


def reset_biotechnology_service() -> None:
    global _service
    _service = None
