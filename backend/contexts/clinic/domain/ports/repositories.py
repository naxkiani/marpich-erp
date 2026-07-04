"""Clinic repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from contexts.clinic.domain.aggregates.appointment import Appointment
from contexts.clinic.domain.aggregates.outpatient_encounter import OutpatientEncounter
from contexts.clinic.domain.aggregates.patient import ClinicPatient
from contexts.clinic.domain.aggregates.referral import Referral
from shared.domain.value_objects.unique_id import UniqueId


class IClinicPatientRepository(ABC):
    @abstractmethod
    async def save(self, patient: ClinicPatient) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, patient_id: UniqueId) -> ClinicPatient | None: ...

    @abstractmethod
    async def find_by_number(self, tenant_id: str, patient_number: str) -> ClinicPatient | None: ...

    @abstractmethod
    async def list_patients(self, tenant_id: str) -> list[ClinicPatient]: ...


class IAppointmentRepository(ABC):
    @abstractmethod
    async def save(self, appointment: Appointment) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, appointment_id: UniqueId) -> Appointment | None: ...

    @abstractmethod
    async def list_by_patient(self, tenant_id: str, patient_id: UniqueId) -> list[Appointment]: ...

    @abstractmethod
    async def list_scheduled(self, tenant_id: str, from_dt: datetime | None = None) -> list[Appointment]: ...


class IOutpatientEncounterRepository(ABC):
    @abstractmethod
    async def save(self, encounter: OutpatientEncounter) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, encounter_id: UniqueId) -> OutpatientEncounter | None: ...


class IReferralRepository(ABC):
    @abstractmethod
    async def save(self, referral: Referral) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, referral_id: UniqueId) -> Referral | None: ...
