"""Clinic application service."""
from __future__ import annotations

import json
from datetime import UTC, datetime

from contexts.clinic.domain.aggregates.appointment import Appointment
from contexts.clinic.domain.aggregates.outpatient_encounter import OutpatientEncounter
from contexts.clinic.domain.aggregates.patient import ClinicPatient
from contexts.clinic.domain.aggregates.referral import Referral
from contexts.clinic.domain.ports.repositories import (
    IAppointmentRepository,
    IClinicPatientRepository,
    IOutpatientEncounterRepository,
    IReferralRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class ConsoleClinicAudit:
    async def log(self, **kwargs: object) -> None:
        entry = {"type": "audit", "context": "clinic", **kwargs, "occurred_at": datetime.now(UTC).isoformat()}
        print(json.dumps(entry, default=str))


class ClinicApplicationService:
    def __init__(
        self,
        patients: IClinicPatientRepository,
        appointments: IAppointmentRepository,
        encounters: IOutpatientEncounterRepository,
        referrals: IReferralRepository,
        audit: ConsoleClinicAudit | None = None,
    ) -> None:
        self._patients = patients
        self._appointments = appointments
        self._encounters = encounters
        self._referrals = referrals
        self._audit = audit or ConsoleClinicAudit()

    async def register_patient(
        self,
        *,
        tenant_id: str,
        patient_number: str,
        first_name: str,
        last_name: str,
        date_of_birth: str,
        correlation_id: str,
    ) -> Result[dict]:
        if await self._patients.find_by_number(tenant_id, patient_number):
            return Result.fail("clinic.errors.patient_number_exists")

        patient = ClinicPatient.register(
            tenant_id=tenant_id,
            patient_number=patient_number,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
        await self._patients.save(patient)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="clinic.patient.registered",
            resource_type="patient",
            resource_id=str(patient.id),
        )
        return Result.ok(patient.to_dict())

    async def list_patients(self, tenant_id: str) -> Result[list[dict]]:
        patients = await self._patients.list_patients(tenant_id)
        return Result.ok([p.to_dict() for p in patients])

    async def schedule_appointment(
        self,
        *,
        tenant_id: str,
        patient_id: str,
        provider_name: str,
        scheduled_at: datetime,
        correlation_id: str,
    ) -> Result[dict]:
        patient = await self._patients.find_by_id(tenant_id, UniqueId.from_string(patient_id))
        if not patient:
            return Result.fail("clinic.errors.patient_not_found")

        appointment, event = Appointment.schedule(
            tenant_id=tenant_id,
            patient_id=patient.id,
            provider_name=provider_name,
            scheduled_at=scheduled_at,
            correlation_id=correlation_id,
        )
        await self._appointments.save(appointment)
        await publish_integration_event(event)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="clinic.appointment.scheduled",
            resource_type="appointment",
            resource_id=str(appointment.id),
        )
        return Result.ok(appointment.to_dict())

    async def list_appointments(self, tenant_id: str) -> Result[list[dict]]:
        appointments = await self._appointments.list_scheduled(tenant_id)
        return Result.ok([a.to_dict() for a in appointments])

    async def start_encounter(
        self,
        *,
        tenant_id: str,
        appointment_id: str,
        correlation_id: str,
    ) -> Result[dict]:
        appointment = await self._appointments.find_by_id(tenant_id, UniqueId.from_string(appointment_id))
        if not appointment:
            return Result.fail("clinic.errors.appointment_not_found")

        encounter = OutpatientEncounter.start(
            tenant_id=tenant_id,
            patient_id=appointment.patient_id,
            appointment_id=appointment.id,
        )
        await self._encounters.save(encounter)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="clinic.encounter.started",
            resource_type="encounter",
            resource_id=str(encounter.id),
        )
        return Result.ok(encounter.to_dict())

    async def complete_encounter(
        self,
        *,
        tenant_id: str,
        encounter_id: str,
        diagnosis_codes: list[str] | None,
        correlation_id: str,
    ) -> Result[dict]:
        encounter = await self._encounters.find_by_id(tenant_id, UniqueId.from_string(encounter_id))
        if not encounter:
            return Result.fail("clinic.errors.encounter_not_found")

        try:
            event = encounter.complete(correlation_id=correlation_id, diagnosis_codes=diagnosis_codes)
        except ValueError as exc:
            return Result.fail(str(exc))

        await self._encounters.save(encounter)
        await publish_integration_event(event)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="clinic.encounter.completed",
            resource_type="encounter",
            resource_id=str(encounter.id),
        )
        return Result.ok(encounter.to_dict())

    async def create_referral(
        self,
        *,
        tenant_id: str,
        encounter_id: str,
        target_specialty: str,
        reason: str,
        correlation_id: str,
        send: bool = False,
    ) -> Result[dict]:
        encounter = await self._encounters.find_by_id(tenant_id, UniqueId.from_string(encounter_id))
        if not encounter:
            return Result.fail("clinic.errors.encounter_not_found")

        referral = Referral.create(
            tenant_id=tenant_id,
            encounter_id=encounter.id,
            patient_id=encounter.patient_id,
            target_specialty=target_specialty,
            reason=reason,
        )
        if send:
            try:
                event = referral.send(correlation_id=correlation_id)
            except ValueError as exc:
                return Result.fail(str(exc))
            await publish_integration_event(event)

        await self._referrals.save(referral)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="clinic.referral.sent" if send else "clinic.referral.created",
            resource_type="referral",
            resource_id=str(referral.id),
        )
        return Result.ok(referral.to_dict())
