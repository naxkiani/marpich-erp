"""Human Resources DI container."""
from __future__ import annotations

from contexts.human_resources.application.service import HumanResourcesApplicationService
from contexts.human_resources.infrastructure.persistence.memory_store import (
    InMemoryEmployeeRepository,
)
from contexts.human_resources.infrastructure.persistence.postgres_store import (
    PostgresEmployeeRepository,
)
from shared.infrastructure.settings import use_postgres

_service: HumanResourcesApplicationService | None = None


def get_human_resources_service() -> HumanResourcesApplicationService:
    global _service
    if _service is None:
        if use_postgres():
            _service = HumanResourcesApplicationService(employees=PostgresEmployeeRepository())
        else:
            _service = HumanResourcesApplicationService(employees=InMemoryEmployeeRepository())
    return _service


def reset_human_resources_service() -> None:
    global _service
    _service = None
