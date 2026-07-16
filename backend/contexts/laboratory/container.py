"""Laboratory DI container — memory or Postgres."""
from __future__ import annotations

from contexts.laboratory.application.service import LaboratoryApplicationService
from contexts.laboratory.infrastructure.persistence.memory_store import (
    InMemorySampleRepository,
    InMemoryTestOrderRepository,
)
from contexts.laboratory.infrastructure.persistence.postgres_store import (
    PostgresSampleRepository,
    PostgresTestOrderRepository,
)
from shared.infrastructure.settings import use_postgres

_service: LaboratoryApplicationService | None = None


def get_laboratory_service() -> LaboratoryApplicationService:
    global _service
    if _service is None:
        if use_postgres():
            _service = LaboratoryApplicationService(
                orders=PostgresTestOrderRepository(),
                samples=PostgresSampleRepository(),
            )
        else:
            _service = LaboratoryApplicationService(
                orders=InMemoryTestOrderRepository(),
                samples=InMemorySampleRepository(),
            )
    return _service


def reset_laboratory_service() -> None:
    global _service
    _service = None
