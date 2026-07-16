"""Pharmacy DI container — memory-only P0 stub."""
from __future__ import annotations

from contexts.pharmacy.application.service import PharmacyApplicationService
from contexts.pharmacy.infrastructure.persistence.memory_store import (
    InMemoryDispenseRepository,
    InMemoryPrescriptionRepository,
)

_service: PharmacyApplicationService | None = None


def get_pharmacy_service() -> PharmacyApplicationService:
    global _service
    if _service is None:
        _service = PharmacyApplicationService(
            prescriptions=InMemoryPrescriptionRepository(),
            dispenses=InMemoryDispenseRepository(),
        )
    return _service


def reset_pharmacy_service() -> None:
    global _service
    _service = None
