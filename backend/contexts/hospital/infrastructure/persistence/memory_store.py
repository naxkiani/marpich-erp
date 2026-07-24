"""Hospital in-memory repositories."""
from __future__ import annotations

from contexts.hospital.domain.aggregates.admission import Admission
from contexts.hospital.domain.aggregates.bed import Bed
from contexts.hospital.domain.aggregates.care_event_projection import CareEventProjection
from contexts.hospital.domain.aggregates.encounter import Encounter
from contexts.hospital.domain.aggregates.patient import Patient
from contexts.hospital.domain.ports.repositories import (
    IAdmissionRepository,
    IBedRepository,
    ICareEventProjectionRepository,
    IEncounterRepository,
    IPatientRepository,
)
from shared.domain.value_objects.unique_id import UniqueId


class HospitalMemoryStore:
    patients: dict[str, Patient] = {}
    admissions: dict[str, Admission] = {}
    encounters: dict[str, Encounter] = {}
    beds: dict[str, Bed] = {}
    care_events: dict[str, object] = {}

    @classmethod
    def reset(cls) -> None:
        cls.patients.clear()
        cls.admissions.clear()
        cls.encounters.clear()
        cls.beds.clear()
        cls.care_events.clear()


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


class InMemoryBedRepository(IBedRepository):
    async def save(self, bed: Bed) -> None:
        HospitalMemoryStore.beds[str(bed.id)] = bed

    async def find_by_id(self, tenant_id: str, bed_id: UniqueId) -> Bed | None:
        b = HospitalMemoryStore.beds.get(str(bed_id))
        return b if b and b.tenant_id == tenant_id else None

    async def find_by_code(
        self, tenant_id: str, ward: str, room: str, bed_code: str
    ) -> Bed | None:
        for b in HospitalMemoryStore.beds.values():
            if (
                b.tenant_id == tenant_id
                and b.ward == ward
                and b.room == room
                and b.bed_code == bed_code.upper()
            ):
                return b
        return None

    async def list_beds(self, tenant_id: str) -> list[Bed]:
        items = [b for b in HospitalMemoryStore.beds.values() if b.tenant_id == tenant_id]
        return sorted(items, key=lambda b: (b.ward, b.room, b.bed_code))


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


class InMemoryCareEventProjectionRepository(ICareEventProjectionRepository):
    async def save(self, event: CareEventProjection) -> None:
        HospitalMemoryStore.care_events[str(event.id)] = event

    async def find_by_source_event(
        self, tenant_id: str, source_event_id: str
    ) -> CareEventProjection | None:
        for event in HospitalMemoryStore.care_events.values():
            if event.tenant_id == tenant_id and event.source_event_id == source_event_id:
                return event
        return None

    async def list_care_events(
        self,
        tenant_id: str,
        *,
        patient_id: str | None = None,
        admission_id: str | None = None,
        encounter_id: str | None = None,
        limit: int = 50,
    ) -> list[CareEventProjection]:
        items = [
            e for e in HospitalMemoryStore.care_events.values() if e.tenant_id == tenant_id
        ]
        if patient_id:
            items = [e for e in items if e.patient_id == patient_id]
        if admission_id:
            items = [e for e in items if e.admission_id == admission_id]
        if encounter_id:
            items = [e for e in items if e.encounter_id == encounter_id]
        items.sort(key=lambda e: e.occurred_at, reverse=True)
        return items[: max(1, min(limit, 100))]

