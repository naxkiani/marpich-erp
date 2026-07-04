"""PostgreSQL repositories — Clinic bounded context."""
from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import select

from contexts.clinic.domain.aggregates.appointment import Appointment, AppointmentStatus
from contexts.clinic.domain.aggregates.outpatient_encounter import OutpatientEncounter, OutpatientEncounterStatus
from contexts.clinic.domain.aggregates.patient import ClinicPatient
from contexts.clinic.domain.aggregates.referral import Referral, ReferralStatus
from contexts.clinic.domain.ports.repositories import (
    IAppointmentRepository,
    IClinicPatientRepository,
    IOutpatientEncounterRepository,
    IReferralRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    ClinicAppointmentRow,
    ClinicEncounterRow,
    ClinicPatientRow,
    ClinicReferralRow,
)


class PostgresClinicPatientRepository(IClinicPatientRepository):
    async def save(self, patient: ClinicPatient) -> None:
        async with session_scope() as session:
            row = await session.get(ClinicPatientRow, UUID(str(patient.id)))
            if row is None:
                row = ClinicPatientRow(
                    id=UUID(str(patient.id)),
                    tenant_id=patient.tenant_id,
                    patient_number=patient.patient_number,
                    first_name=patient.first_name,
                    last_name=patient.last_name,
                    date_of_birth=date.fromisoformat(patient.date_of_birth),
                )
                session.add(row)
            else:
                row.first_name = patient.first_name
                row.last_name = patient.last_name

    async def find_by_id(self, tenant_id: str, patient_id: UniqueId) -> ClinicPatient | None:
        async with session_scope() as session:
            row = await session.get(ClinicPatientRow, UUID(str(patient_id)))
            return _patient_from_row(row) if row and row.tenant_id == tenant_id else None

    async def find_by_number(self, tenant_id: str, patient_number: str) -> ClinicPatient | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(ClinicPatientRow).where(
                    ClinicPatientRow.tenant_id == tenant_id,
                    ClinicPatientRow.patient_number == patient_number.upper(),
                )
            )
            return _patient_from_row(row) if row else None

    async def list_patients(self, tenant_id: str) -> list[ClinicPatient]:
        async with session_scope() as session:
            rows = (await session.scalars(select(ClinicPatientRow).where(ClinicPatientRow.tenant_id == tenant_id))).all()
        return [_patient_from_row(r) for r in rows]


class PostgresAppointmentRepository(IAppointmentRepository):
    async def save(self, appointment: Appointment) -> None:
        async with session_scope() as session:
            row = await session.get(ClinicAppointmentRow, UUID(str(appointment.id)))
            if row is None:
                row = ClinicAppointmentRow(
                    id=UUID(str(appointment.id)),
                    tenant_id=appointment.tenant_id,
                    patient_id=UUID(str(appointment.patient_id)),
                    provider_name=appointment.provider_name,
                    scheduled_at=appointment.scheduled_at,
                    status=appointment.status.value,
                )
                session.add(row)
            else:
                row.status = appointment.status.value

    async def find_by_id(self, tenant_id: str, appointment_id: UniqueId) -> Appointment | None:
        async with session_scope() as session:
            row = await session.get(ClinicAppointmentRow, UUID(str(appointment_id)))
            return _appointment_from_row(row) if row and row.tenant_id == tenant_id else None

    async def list_by_patient(self, tenant_id: str, patient_id: UniqueId) -> list[Appointment]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(ClinicAppointmentRow).where(
                        ClinicAppointmentRow.tenant_id == tenant_id,
                        ClinicAppointmentRow.patient_id == UUID(str(patient_id)),
                    )
                )
            ).all()
        return [_appointment_from_row(r) for r in rows]

    async def list_scheduled(self, tenant_id: str, from_dt: datetime | None = None) -> list[Appointment]:
        async with session_scope() as session:
            stmt = select(ClinicAppointmentRow).where(ClinicAppointmentRow.tenant_id == tenant_id)
            if from_dt:
                stmt = stmt.where(ClinicAppointmentRow.scheduled_at >= from_dt)
            rows = (await session.scalars(stmt)).all()
        return sorted([_appointment_from_row(r) for r in rows], key=lambda a: a.scheduled_at)


class PostgresOutpatientEncounterRepository(IOutpatientEncounterRepository):
    async def save(self, encounter: OutpatientEncounter) -> None:
        async with session_scope() as session:
            row = await session.get(ClinicEncounterRow, UUID(str(encounter.id)))
            if row is None:
                row = ClinicEncounterRow(
                    id=UUID(str(encounter.id)),
                    tenant_id=encounter.tenant_id,
                    patient_id=UUID(str(encounter.patient_id)),
                    appointment_id=UUID(str(encounter.appointment_id)),
                    status=encounter.status.value,
                    diagnosis_codes=list(encounter.diagnosis_codes),
                    started_at=encounter.started_at,
                    completed_at=encounter.completed_at,
                )
                session.add(row)
            else:
                row.status = encounter.status.value
                row.diagnosis_codes = list(encounter.diagnosis_codes)
                row.completed_at = encounter.completed_at

    async def find_by_id(self, tenant_id: str, encounter_id: UniqueId) -> OutpatientEncounter | None:
        async with session_scope() as session:
            row = await session.get(ClinicEncounterRow, UUID(str(encounter_id)))
            return _encounter_from_row(row) if row and row.tenant_id == tenant_id else None


class PostgresReferralRepository(IReferralRepository):
    async def save(self, referral: Referral) -> None:
        async with session_scope() as session:
            row = await session.get(ClinicReferralRow, UUID(str(referral.id)))
            if row is None:
                row = ClinicReferralRow(
                    id=UUID(str(referral.id)),
                    tenant_id=referral.tenant_id,
                    encounter_id=UUID(str(referral.encounter_id)),
                    patient_id=UUID(str(referral.patient_id)),
                    target_specialty=referral.target_specialty,
                    reason=referral.reason,
                    status=referral.status.value,
                    sent_at=referral.sent_at,
                )
                session.add(row)
            else:
                row.status = referral.status.value
                row.sent_at = referral.sent_at

    async def find_by_id(self, tenant_id: str, referral_id: UniqueId) -> Referral | None:
        async with session_scope() as session:
            row = await session.get(ClinicReferralRow, UUID(str(referral_id)))
            return _referral_from_row(row) if row and row.tenant_id == tenant_id else None


def _patient_from_row(row: ClinicPatientRow) -> ClinicPatient:
    return ClinicPatient(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        patient_number=row.patient_number,
        first_name=row.first_name,
        last_name=row.last_name,
        date_of_birth=row.date_of_birth.isoformat(),
        created_at=row.created_at,
    )


def _appointment_from_row(row: ClinicAppointmentRow) -> Appointment:
    return Appointment(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        patient_id=UniqueId.from_string(str(row.patient_id)),
        provider_name=row.provider_name,
        scheduled_at=row.scheduled_at,
        status=AppointmentStatus(row.status),
        created_at=row.created_at,
    )


def _encounter_from_row(row: ClinicEncounterRow) -> OutpatientEncounter:
    return OutpatientEncounter(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        patient_id=UniqueId.from_string(str(row.patient_id)),
        appointment_id=UniqueId.from_string(str(row.appointment_id)),
        status=OutpatientEncounterStatus(row.status),
        diagnosis_codes=list(row.diagnosis_codes or []),
        started_at=row.started_at,
        completed_at=row.completed_at,
    )


def _referral_from_row(row: ClinicReferralRow) -> Referral:
    return Referral(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        encounter_id=UniqueId.from_string(str(row.encounter_id)),
        patient_id=UniqueId.from_string(str(row.patient_id)),
        target_specialty=row.target_specialty,
        reason=row.reason,
        status=ReferralStatus(row.status),
        created_at=row.created_at,
        sent_at=row.sent_at,
    )
