"""PostgreSQL repositories — Hospital bounded context."""
from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import select

from contexts.hospital.domain.aggregates.admission import Admission, AdmissionStatus
from contexts.hospital.domain.aggregates.encounter import Encounter, EncounterStatus
from contexts.hospital.domain.aggregates.patient import Patient
from contexts.hospital.domain.ports.repositories import (
    IAdmissionRepository,
    IEncounterRepository,
    IPatientRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import AdmissionRow, EncounterRow, PatientRow


class PostgresPatientRepository(IPatientRepository):
    async def save(self, patient: Patient) -> None:
        async with session_scope() as session:
            row = await session.get(PatientRow, UUID(str(patient.id)))
            if row is None:
                row = PatientRow(
                    id=UUID(str(patient.id)),
                    tenant_id=patient.tenant_id,
                    mrn=patient.mrn,
                    first_name=patient.first_name,
                    last_name=patient.last_name,
                    date_of_birth=date.fromisoformat(patient.date_of_birth),
                )
                session.add(row)
            else:
                row.mrn = patient.mrn
                row.first_name = patient.first_name
                row.last_name = patient.last_name

    async def find_by_id(self, tenant_id: str, patient_id: UniqueId) -> Patient | None:
        async with session_scope() as session:
            row = await session.get(PatientRow, UUID(str(patient_id)))
            if row and row.tenant_id == tenant_id:
                return _patient_from_row(row)
            return None

    async def find_by_mrn(self, tenant_id: str, mrn: str) -> Patient | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(PatientRow).where(PatientRow.tenant_id == tenant_id, PatientRow.mrn == mrn.upper())
            )
            return _patient_from_row(row) if row else None

    async def list_patients(self, tenant_id: str) -> list[Patient]:
        async with session_scope() as session:
            rows = (await session.scalars(select(PatientRow).where(PatientRow.tenant_id == tenant_id))).all()
        return [_patient_from_row(r) for r in rows]


class PostgresAdmissionRepository(IAdmissionRepository):
    async def save(self, admission: Admission) -> None:
        async with session_scope() as session:
            row = await session.get(AdmissionRow, UUID(str(admission.id)))
            if row is None:
                row = AdmissionRow(
                    id=UUID(str(admission.id)),
                    tenant_id=admission.tenant_id,
                    patient_id=UUID(str(admission.patient_id)),
                    ward=admission.ward,
                    status=admission.status.value,
                    admitted_at=admission.admitted_at,
                )
                session.add(row)
            else:
                row.status = admission.status.value
                row.ward = admission.ward

    async def find_by_id(self, tenant_id: str, admission_id: UniqueId) -> Admission | None:
        async with session_scope() as session:
            row = await session.get(AdmissionRow, UUID(str(admission_id)))
            if row and row.tenant_id == tenant_id:
                return _admission_from_row(row)
            return None

    async def list_admissions(self, tenant_id: str) -> list[Admission]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(AdmissionRow)
                    .where(AdmissionRow.tenant_id == tenant_id)
                    .order_by(AdmissionRow.admitted_at.desc())
                )
            ).all()
        return [_admission_from_row(r) for r in rows]


class PostgresEncounterRepository(IEncounterRepository):
    async def save(self, encounter: Encounter) -> None:
        async with session_scope() as session:
            row = await session.get(EncounterRow, UUID(str(encounter.id)))
            if row is None:
                row = EncounterRow(
                    id=UUID(str(encounter.id)),
                    tenant_id=encounter.tenant_id,
                    patient_id=UUID(str(encounter.patient_id)),
                    admission_id=UUID(str(encounter.admission_id)),
                    status=encounter.status.value,
                    procedure_codes=list(encounter.procedure_codes),
                    diagnosis_codes=list(encounter.diagnosis_codes),
                    started_at=encounter.started_at,
                    completed_at=encounter.completed_at,
                )
                session.add(row)
            else:
                row.status = encounter.status.value
                row.procedure_codes = list(encounter.procedure_codes)
                row.diagnosis_codes = list(encounter.diagnosis_codes)
                row.completed_at = encounter.completed_at

    async def find_by_id(self, tenant_id: str, encounter_id: UniqueId) -> Encounter | None:
        async with session_scope() as session:
            row = await session.get(EncounterRow, UUID(str(encounter_id)))
            if row and row.tenant_id == tenant_id:
                return _encounter_from_row(row)
            return None

    async def list_by_admission(self, tenant_id: str, admission_id: UniqueId) -> list[Encounter]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(EncounterRow).where(
                        EncounterRow.tenant_id == tenant_id,
                        EncounterRow.admission_id == UUID(str(admission_id)),
                    )
                )
            ).all()
        return [_encounter_from_row(r) for r in rows]

    async def list_encounters(self, tenant_id: str) -> list[Encounter]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(EncounterRow)
                    .where(EncounterRow.tenant_id == tenant_id)
                    .order_by(EncounterRow.started_at.desc())
                )
            ).all()
        return [_encounter_from_row(r) for r in rows]


def _patient_from_row(row: PatientRow) -> Patient:
    return Patient(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        mrn=row.mrn,
        first_name=row.first_name,
        last_name=row.last_name,
        date_of_birth=row.date_of_birth.isoformat(),
        created_at=row.created_at,
    )


def _admission_from_row(row: AdmissionRow) -> Admission:
    return Admission(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        patient_id=UniqueId.from_string(str(row.patient_id)),
        ward=row.ward,
        status=AdmissionStatus(row.status),
        admitted_at=row.admitted_at,
    )


def _encounter_from_row(row: EncounterRow) -> Encounter:
    return Encounter(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        patient_id=UniqueId.from_string(str(row.patient_id)),
        admission_id=UniqueId.from_string(str(row.admission_id)),
        status=EncounterStatus(row.status),
        procedure_codes=list(row.procedure_codes or []),
        diagnosis_codes=list(row.diagnosis_codes or []),
        started_at=row.started_at,
        completed_at=row.completed_at,
    )
