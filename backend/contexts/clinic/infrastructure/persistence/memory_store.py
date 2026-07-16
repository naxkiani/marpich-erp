"""Clinic in-memory repositories."""
from __future__ import annotations

from datetime import datetime

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
from shared.domain.value_objects.unique_id import UniqueId


class ClinicMemoryStore:
    patients: dict[str, ClinicPatient] = {}
    appointments: dict[str, Appointment] = {}
    encounters: dict[str, OutpatientEncounter] = {}
    referrals: dict[str, Referral] = {}

    @classmethod
    def reset(cls) -> None:
        cls.patients.clear()
        cls.appointments.clear()
        cls.encounters.clear()
        cls.referrals.clear()


class InMemoryClinicPatientRepository(IClinicPatientRepository):
    async def save(self, patient: ClinicPatient) -> None:
        ClinicMemoryStore.patients[str(patient.id)] = patient

    async def find_by_id(self, tenant_id: str, patient_id: UniqueId) -> ClinicPatient | None:
        p = ClinicMemoryStore.patients.get(str(patient_id))
        return p if p and p.tenant_id == tenant_id else None

    async def find_by_number(self, tenant_id: str, patient_number: str) -> ClinicPatient | None:
        for p in ClinicMemoryStore.patients.values():
            if p.tenant_id == tenant_id and p.patient_number == patient_number.upper():
                return p
        return None

    async def list_patients(self, tenant_id: str) -> list[ClinicPatient]:
        return [p for p in ClinicMemoryStore.patients.values() if p.tenant_id == tenant_id]


class InMemoryAppointmentRepository(IAppointmentRepository):
    async def save(self, appointment: Appointment) -> None:
        ClinicMemoryStore.appointments[str(appointment.id)] = appointment

    async def find_by_id(self, tenant_id: str, appointment_id: UniqueId) -> Appointment | None:
        a = ClinicMemoryStore.appointments.get(str(appointment_id))
        return a if a and a.tenant_id == tenant_id else None

    async def list_by_patient(self, tenant_id: str, patient_id: UniqueId) -> list[Appointment]:
        return [
            a
            for a in ClinicMemoryStore.appointments.values()
            if a.tenant_id == tenant_id and str(a.patient_id) == str(patient_id)
        ]

    async def list_scheduled(self, tenant_id: str, from_dt: datetime | None = None) -> list[Appointment]:
        items = [a for a in ClinicMemoryStore.appointments.values() if a.tenant_id == tenant_id]
        if from_dt:
            items = [a for a in items if a.scheduled_at >= from_dt]
        return sorted(items, key=lambda a: a.scheduled_at)


class InMemoryOutpatientEncounterRepository(IOutpatientEncounterRepository):
    async def save(self, encounter: OutpatientEncounter) -> None:
        ClinicMemoryStore.encounters[str(encounter.id)] = encounter

    async def find_by_id(self, tenant_id: str, encounter_id: UniqueId) -> OutpatientEncounter | None:
        e = ClinicMemoryStore.encounters.get(str(encounter_id))
        return e if e and e.tenant_id == tenant_id else None

    async def list_encounters(self, tenant_id: str) -> list[OutpatientEncounter]:
        items = [e for e in ClinicMemoryStore.encounters.values() if e.tenant_id == tenant_id]
        return sorted(items, key=lambda e: e.started_at, reverse=True)


class InMemoryReferralRepository(IReferralRepository):
    async def save(self, referral: Referral) -> None:
        ClinicMemoryStore.referrals[str(referral.id)] = referral

    async def find_by_id(self, tenant_id: str, referral_id: UniqueId) -> Referral | None:
        r = ClinicMemoryStore.referrals.get(str(referral_id))
        return r if r and r.tenant_id == tenant_id else None
