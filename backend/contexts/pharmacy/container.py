"""Pharmacy DI container — memory or Postgres."""
from __future__ import annotations

from contexts.pharmacy.application.service import PharmacyApplicationService
from contexts.pharmacy.infrastructure.persistence.memory_store import (
    InMemoryDispenseRepository,
    InMemoryPrescriptionRepository,
)
from contexts.pharmacy.infrastructure.persistence.postgres_store import (
    PostgresDispenseRepository,
    PostgresPrescriptionRepository,
)
from shared.infrastructure.settings import use_postgres

_service: PharmacyApplicationService | None = None


def get_pharmacy_service() -> PharmacyApplicationService:
    global _service
    if _service is None:
        if use_postgres():
            _service = PharmacyApplicationService(
                prescriptions=PostgresPrescriptionRepository(),
                dispenses=PostgresDispenseRepository(),
            )
        else:
            _service = PharmacyApplicationService(
                prescriptions=InMemoryPrescriptionRepository(),
                dispenses=InMemoryDispenseRepository(),
            )
    return _service


def reset_pharmacy_service() -> None:
    global _service
    _service = None
