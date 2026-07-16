"""Hospital in-memory repositories."""
from __future__ import annotations

from contexts.hospital.domain.aggregates.admission import Admission
from contexts.hospital.domain.aggregates.encounter import Encounter
from contexts.hospital.domain.aggregates.patient import Patient
from contexts.hospital.domain.ports.repositories import (
    IAdmissionRepository,
    IEncounterRepository,
    IPatientRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class HospitalMemoryStore:
    patients: dict[str, Patient] = {}
    admissions: dict[str, Admission] = {}
    encounters: dict[str, Encounter] = {}

    @classmethod
    def reset(cls) -> None:
        cls.patients.clear()
        cls.admissions.clear()
        cls.encounters.clear()


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
