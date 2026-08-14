"""Space DI container."""
from __future__ import annotations

from contexts.space.application.service import SpaceApplicationService

_service: SpaceApplicationService | None = None


def get_space_service() -> SpaceApplicationService:
    global _service
    if _service is None:
        _service = SpaceApplicationService()
    return _service


def reset_space_service() -> None:
    global _service
    _service = None
