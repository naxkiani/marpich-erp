"""Laboratory DI container — memory-only P0 stub."""
from __future__ import annotations

from contexts.laboratory.application.service import LaboratoryApplicationService
from contexts.laboratory.infrastructure.persistence.memory_store import (
    InMemorySampleRepository,
    InMemoryTestOrderRepository,
)

_service: LaboratoryApplicationService | None = None


def get_laboratory_service() -> LaboratoryApplicationService:
    global _service
    if _service is None:
        _service = LaboratoryApplicationService(
            orders=InMemoryTestOrderRepository(),
            samples=InMemorySampleRepository(),
        )
    return _service


def reset_laboratory_service() -> None:
    global _service
    _service = None
