"""CRM DI container."""
from __future__ import annotations

from contexts.crm.application.service import CrmApplicationService
from contexts.crm.infrastructure.persistence.memory_store import (
    InMemoryContactRepository,
    InMemoryOpportunityRepository,
)
from contexts.crm.infrastructure.persistence.postgres_store import (
    PostgresContactRepository,
    PostgresOpportunityRepository,
)
from shared.infrastructure.settings import use_postgres

_service: CrmApplicationService | None = None


def get_crm_service() -> CrmApplicationService:
    global _service
    if _service is None:
        if use_postgres():
            _service = CrmApplicationService(
                contacts=PostgresContactRepository(),
                opportunities=PostgresOpportunityRepository(),
            )
        else:
            _service = CrmApplicationService(
                contacts=InMemoryContactRepository(),
                opportunities=InMemoryOpportunityRepository(),
            )
    return _service


def reset_crm_service() -> None:
    global _service
    _service = None
