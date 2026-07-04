"""Clinic DI container."""
from __future__ import annotations

from contexts.clinic.application.service import ClinicApplicationService
from contexts.clinic.infrastructure.persistence.memory_store import (
    InMemoryAppointmentRepository,
    InMemoryClinicPatientRepository,
    InMemoryOutpatientEncounterRepository,
    InMemoryReferralRepository,
)
from contexts.clinic.infrastructure.persistence.postgres_store import (
    PostgresAppointmentRepository,
    PostgresClinicPatientRepository,
    PostgresOutpatientEncounterRepository,
    PostgresReferralRepository,
)
from shared.infrastructure.settings import use_postgres

_service: ClinicApplicationService | None = None


def get_clinic_service() -> ClinicApplicationService:
    global _service
    if _service is None:
        if use_postgres():
            _service = ClinicApplicationService(
                patients=PostgresClinicPatientRepository(),
                appointments=PostgresAppointmentRepository(),
                encounters=PostgresOutpatientEncounterRepository(),
                referrals=PostgresReferralRepository(),
            )
        else:
            _service = ClinicApplicationService(
                patients=InMemoryClinicPatientRepository(),
                appointments=InMemoryAppointmentRepository(),
                encounters=InMemoryOutpatientEncounterRepository(),
                referrals=InMemoryReferralRepository(),
            )
    return _service


def reset_clinic_service() -> None:
    global _service
    _service = None
