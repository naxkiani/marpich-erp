"""Municipality DI container."""
from __future__ import annotations

from contexts.municipality.application.service import MunicipalityApplicationService
from contexts.municipality.infrastructure.persistence.memory_store import (
    InMemoryPermitRepository,
    InMemoryServiceRequestRepository,
    InMemoryUtilityAccountRepository,
)
from contexts.municipality.infrastructure.persistence.postgres_store import (
    PostgresPermitRepository,
    PostgresServiceRequestRepository,
    PostgresUtilityAccountRepository,
)
from shared.infrastructure.settings import use_postgres

_service: MunicipalityApplicationService | None = None


def get_municipality_service() -> MunicipalityApplicationService:
    global _service
    if _service is None:
        if use_postgres():
            _service = MunicipalityApplicationService(
                permits=PostgresPermitRepository(),
                service_requests=PostgresServiceRequestRepository(),
                utility_accounts=PostgresUtilityAccountRepository(),
            )
        else:
            _service = MunicipalityApplicationService(
                permits=InMemoryPermitRepository(),
                service_requests=InMemoryServiceRequestRepository(),
                utility_accounts=InMemoryUtilityAccountRepository(),
            )
    return _service


def reset_municipality_service() -> None:
    global _service
    _service = None
