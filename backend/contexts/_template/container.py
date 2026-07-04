"""DI container — wire ports to adapters and expose use cases."""
from __future__ import annotations

from contexts.module_id.application.use_cases.example_use_case import ExampleUseCase
from contexts.module_id.infrastructure.persistence.memory_store import (
    InMemoryExampleRepository,
)
from contexts.module_id.infrastructure.persistence.postgres_store import (
    PostgresExampleRepository,
)
from shared.infrastructure.settings import use_postgres

_use_case: ExampleUseCase | None = None


def get_example_use_case() -> ExampleUseCase:
    global _use_case
    if _use_case is None:
        repo = (
            PostgresExampleRepository()
            if use_postgres()
            else InMemoryExampleRepository()
        )
        _use_case = ExampleUseCase(repository=repo)
    return _use_case


def reset_module_service() -> None:
    global _use_case
    _use_case = None
