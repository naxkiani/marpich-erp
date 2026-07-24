"""PostgreSQL repositories — Hospital bounded context."""
from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import select

from contexts.hospital.domain.aggregates.admission import Admission, AdmissionStatus
from contexts.hospital.domain.aggregates.bed import Bed, BedStatus
from contexts.hospital.domain.aggregates.care_event_projection import (
    CareEventKind,
    CareEventProjection,
)
from contexts.hospital.domain.aggregates.encounter import Encounter, EncounterStatus
from contexts.hospital.domain.aggregates.patient import Patient
from contexts.hospital.domain.ports.repositories import (
    IAdmissionRepository,
    IBedRepository,
    ICareEventProjectionRepository,
    IEncounterRepository,
    IPatientRepository,
)
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.database.engine import session_scope
from shared.infrastructure.database.orm import (
    AdmissionRow,
    BedRow,
    CareEventProjectionRow,
    EncounterRow,
    PatientRow,
)


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
                    bed_id=UUID(str(admission.bed_id)) if admission.bed_id else None,
                    admitted_at=admission.admitted_at,
                    discharged_at=admission.discharged_at,
                )
                session.add(row)
            else:
                row.status = admission.status.value
                row.ward = admission.ward
                row.bed_id = UUID(str(admission.bed_id)) if admission.bed_id else None
                row.discharged_at = admission.discharged_at

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


class PostgresBedRepository(IBedRepository):
    async def save(self, bed: Bed) -> None:
        async with session_scope() as session:
            row = await session.get(BedRow, UUID(str(bed.id)))
            if row is None:
                session.add(
                    BedRow(
                        id=UUID(str(bed.id)),
                        tenant_id=bed.tenant_id,
                        ward=bed.ward,
                        room=bed.room,
                        bed_code=bed.bed_code,
                        status=bed.status.value,
                        current_admission_id=(
                            UUID(str(bed.current_admission_id))
                            if bed.current_admission_id
                            else None
                        ),
                        created_at=bed.created_at,
                    )
                )
            else:
                row.ward = bed.ward
                row.room = bed.room
                row.bed_code = bed.bed_code
                row.status = bed.status.value
                row.current_admission_id = (
                    UUID(str(bed.current_admission_id)) if bed.current_admission_id else None
                )

    async def find_by_id(self, tenant_id: str, bed_id: UniqueId) -> Bed | None:
        async with session_scope() as session:
            row = await session.get(BedRow, UUID(str(bed_id)))
            if row and row.tenant_id == tenant_id:
                return _bed_from_row(row)
            return None

    async def find_by_code(
        self, tenant_id: str, ward: str, room: str, bed_code: str
    ) -> Bed | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(BedRow).where(
                    BedRow.tenant_id == tenant_id,
                    BedRow.ward == ward,
                    BedRow.room == room,
                    BedRow.bed_code == bed_code.upper(),
                )
            )
            return _bed_from_row(row) if row else None

    async def list_beds(self, tenant_id: str) -> list[Bed]:
        async with session_scope() as session:
            rows = (
                await session.scalars(
                    select(BedRow)
                    .where(BedRow.tenant_id == tenant_id)
                    .order_by(BedRow.ward, BedRow.room, BedRow.bed_code)
                )
            ).all()
        return [_bed_from_row(r) for r in rows]


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


class PostgresCareEventProjectionRepository(ICareEventProjectionRepository):
    async def save(self, event: CareEventProjection) -> None:
        async with session_scope() as session:
            row = await session.get(CareEventProjectionRow, UUID(str(event.id)))
            if row is None:
                session.add(
                    CareEventProjectionRow(
                        id=UUID(str(event.id)),
                        tenant_id=event.tenant_id,
                        source_event_id=event.source_event_id,
                        source_context=event.source_context,
                        event_kind=event.event_kind.value,
                        peer_id=event.peer_id,
                        patient_id=UUID(event.patient_id),
                        admission_id=UUID(event.admission_id) if event.admission_id else None,
                        encounter_id=UUID(event.encounter_id) if event.encounter_id else None,
                        summary=dict(event.summary or {}),
                        correlation_id=event.correlation_id or "",
                        occurred_at=event.occurred_at,
                    )
                )
            else:
                row.summary = dict(event.summary or {})
                row.correlation_id = event.correlation_id or ""
                row.admission_id = UUID(event.admission_id) if event.admission_id else None
                row.encounter_id = UUID(event.encounter_id) if event.encounter_id else None

    async def find_by_source_event(
        self, tenant_id: str, source_event_id: str
    ) -> CareEventProjection | None:
        async with session_scope() as session:
            row = await session.scalar(
                select(CareEventProjectionRow).where(
                    CareEventProjectionRow.tenant_id == tenant_id,
                    CareEventProjectionRow.source_event_id == source_event_id,
                )
            )
            return _care_event_from_row(row) if row else None

    async def list_care_events(
        self,
        tenant_id: str,
        *,
        patient_id: str | None = None,
        admission_id: str | None = None,
        encounter_id: str | None = None,
        limit: int = 50,
    ) -> list[CareEventProjection]:
        limit = max(1, min(limit, 100))
        async with session_scope() as session:
            stmt = select(CareEventProjectionRow).where(
                CareEventProjectionRow.tenant_id == tenant_id
            )
            if patient_id:
                stmt = stmt.where(CareEventProjectionRow.patient_id == UUID(patient_id))
            if admission_id:
                stmt = stmt.where(CareEventProjectionRow.admission_id == UUID(admission_id))
            if encounter_id:
                stmt = stmt.where(CareEventProjectionRow.encounter_id == UUID(encounter_id))
            stmt = stmt.order_by(CareEventProjectionRow.occurred_at.desc()).limit(limit)
            rows = (await session.scalars(stmt)).all()
        return [_care_event_from_row(r) for r in rows]


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
        bed_id=UniqueId.from_string(str(row.bed_id)) if row.bed_id else None,
        admitted_at=row.admitted_at,
        discharged_at=row.discharged_at,
    )


def _bed_from_row(row: BedRow) -> Bed:
    return Bed(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        ward=row.ward,
        room=row.room,
        bed_code=row.bed_code,
        status=BedStatus(row.status),
        current_admission_id=(
            UniqueId.from_string(str(row.current_admission_id))
            if row.current_admission_id
            else None
        ),
        created_at=row.created_at,
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


def _care_event_from_row(row: CareEventProjectionRow) -> CareEventProjection:
    return CareEventProjection(
        id=UniqueId.from_string(str(row.id)),
        tenant_id=row.tenant_id,
        source_event_id=row.source_event_id,
        source_context=row.source_context,
        event_kind=CareEventKind(row.event_kind),
        peer_id=row.peer_id,
        patient_id=str(row.patient_id),
        admission_id=str(row.admission_id) if row.admission_id else "",
        encounter_id=str(row.encounter_id) if row.encounter_id else "",
        summary=dict(row.summary or {}),
        correlation_id=row.correlation_id or "",
        occurred_at=row.occurred_at,
    )
