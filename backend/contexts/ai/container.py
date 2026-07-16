"""AI DI container."""
from __future__ import annotations

from contexts.ai.application.service import AiApplicationService

_service: AiApplicationService | None = None


def get_ai_service() -> AiApplicationService:
    global _service
    if _service is None:
        _service = AiApplicationService()
    return _service


def reset_ai_service() -> None:
    global _service
    if _service is not None:
        _service.reset()
    _service = None
