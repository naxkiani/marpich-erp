"""Hospital in-memory repositories."""
from __future__ import annotations

from contexts.hospital.domain.aggregates.admission import Admission
from contexts.hospital.domain.aggregates.encounter import Encounter
from contexts.hospital.domain.aggregates.patient import Patient
from contexts.hospital.domain.entities.lab_result_projection import LabResultProjection
from contexts.hospital.domain.ports.repositories import (
    IAdmissionRepository,
    IEncounterRepository,
    ILabResultProjectionRepository,
    IPatientRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class HospitalMemoryStore:
    patients: dict[str, Patient] = {}
    admissions: dict[str, Admission] = {}
    encounters: dict[str, Encounter] = {}
    lab_projections: dict[str, LabResultProjection] = {}

    @classmethod
    def reset(cls) -> None:
        cls.patients.clear()
        cls.admissions.clear()
        cls.encounters.clear()
        cls.lab_projections.clear()


class InMemoryPatientRepository(IPatientRepository):
    async def save(self, patient: Patient) -> None:
        HospitalMemoryStore.patients[str(patient.id)] = patient

    async def find_by_id(self, tenant_id: str, patient_id: UniqueId) -> Patient | None:
        p = HospitalMemoryStore.patients.get(str(patient_id))
        return p if p and p.tenant_id == tenant_id else None

    async def find_by_mrn(self, tenant_id: str, mrn: str) -> Patient | None:
        for p in HospitalMemoryStore.patients.values():
            if p.tenant_id == tenant_id and p.mrn == mrn.upper():
                return p
        return None

    async def list_patients(self, tenant_id: str) -> list[Patient]:
        return [p for p in HospitalMemoryStore.patients.values() if p.tenant_id == tenant_id]


class InMemoryAdmissionRepository(IAdmissionRepository):
    async def save(self, admission: Admission) -> None:
        HospitalMemoryStore.admissions[str(admission.id)] = admission

    async def find_by_id(self, tenant_id: str, admission_id: UniqueId) -> Admission | None:
        a = HospitalMemoryStore.admissions.get(str(admission_id))
        return a if a and a.tenant_id == tenant_id else None

    async def list_admissions(self, tenant_id: str) -> list[Admission]:
        items = [a for a in HospitalMemoryStore.admissions.values() if a.tenant_id == tenant_id]
        return sorted(items, key=lambda a: a.admitted_at, reverse=True)


class InMemoryEncounterRepository(IEncounterRepository):
    async def save(self, encounter: Encounter) -> None:
        HospitalMemoryStore.encounters[str(encounter.id)] = encounter

    async def find_by_id(self, tenant_id: str, encounter_id: UniqueId) -> Encounter | None:
        e = HospitalMemoryStore.encounters.get(str(encounter_id))
        return e if e and e.tenant_id == tenant_id else None

    async def list_by_admission(self, tenant_id: str, admission_id: UniqueId) -> list[Encounter]:
        return [
            e
            for e in HospitalMemoryStore.encounters.values()
            if e.tenant_id == tenant_id and str(e.admission_id) == str(admission_id)
        ]

    async def list_encounters(self, tenant_id: str) -> list[Encounter]:
        items = [e for e in HospitalMemoryStore.encounters.values() if e.tenant_id == tenant_id]
        return sorted(items, key=lambda e: e.started_at, reverse=True)


class InMemoryLabResultProjectionRepository(ILabResultProjectionRepository):
    async def save(self, projection: LabResultProjection) -> None:
        HospitalMemoryStore.lab_projections[str(projection.id)] = projection

    async def find_by_event_id(
        self, tenant_id: str, source_event_id: str
    ) -> LabResultProjection | None:
        for row in HospitalMemoryStore.lab_projections.values():
            if row.tenant_id == tenant_id and row.source_event_id == source_event_id:
                return row
        return None

    async def list_projections(self, tenant_id: str) -> list[LabResultProjection]:
        rows = [r for r in HospitalMemoryStore.lab_projections.values() if r.tenant_id == tenant_id]
        return sorted(rows, key=lambda r: r.projected_at, reverse=True)
