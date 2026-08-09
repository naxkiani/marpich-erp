"""Civilization DI container."""
from __future__ import annotations

from contexts.civilization.application.service import CivilizationApplicationService

_service: CivilizationApplicationService | None = None


def get_civilization_service() -> CivilizationApplicationService:
    global _service
    if _service is None:
        _service = CivilizationApplicationService()
    return _service


def reset_civilization_service() -> None:
    global _service
    _service = None
