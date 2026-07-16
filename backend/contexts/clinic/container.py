"""Clinic DI container + laboratory result ACL subscription."""
from __future__ import annotations

from contexts.clinic.application.service import ClinicApplicationService
from contexts.clinic.infrastructure.acl.laboratory_events import (
    make_laboratory_result_handler,
)
from contexts.clinic.infrastructure.persistence.lab_result_postgres import (
    PostgresLabResultProjectionRepository,
)
from contexts.clinic.infrastructure.persistence.memory_store import (
    InMemoryAppointmentRepository,
    InMemoryClinicPatientRepository,
    InMemoryLabResultProjectionRepository,
    InMemoryOutpatientEncounterRepository,
    InMemoryReferralRepository,
)
from contexts.clinic.infrastructure.persistence.postgres_store import (
    PostgresAppointmentRepository,
    PostgresClinicPatientRepository,
    PostgresOutpatientEncounterRepository,
    PostgresReferralRepository,
)
from shared.infrastructure.messaging.event_bus import InProcessEventBus
from shared.infrastructure.settings import use_postgres

_service: ClinicApplicationService | None = None
_registered = False


def get_clinic_service() -> ClinicApplicationService:
    global _service, _registered
    if _service is None:
        if use_postgres():
            _service = ClinicApplicationService(
                patients=PostgresClinicPatientRepository(),
                appointments=PostgresAppointmentRepository(),
                encounters=PostgresOutpatientEncounterRepository(),
                referrals=PostgresReferralRepository(),
                lab_projections=PostgresLabResultProjectionRepository(),
            )
        else:
            _service = ClinicApplicationService(
                patients=InMemoryClinicPatientRepository(),
                appointments=InMemoryAppointmentRepository(),
                encounters=InMemoryOutpatientEncounterRepository(),
                referrals=InMemoryReferralRepository(),
                lab_projections=InMemoryLabResultProjectionRepository(),
            )
    if not _registered:
        InProcessEventBus.subscribe(
            "laboratory.result.available",
            make_laboratory_result_handler(get_clinic_service),
        )
        _registered = True
    return _service


def reset_clinic_service() -> None:
    global _service, _registered
    _service = None
    _registered = False
