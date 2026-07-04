"""Hospital repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.hospital.domain.aggregates.admission import Admission
from contexts.hospital.domain.aggregates.encounter import Encounter
from contexts.hospital.domain.aggregates.patient import Patient
from shared.domain.value_objects.unique_id import UniqueId


class IPatientRepository(ABC):
    @abstractmethod
    async def save(self, patient: Patient) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, patient_id: UniqueId) -> Patient | None: ...

    @abstractmethod
    async def find_by_mrn(self, tenant_id: str, mrn: str) -> Patient | None: ...

    @abstractmethod
    async def list_patients(self, tenant_id: str) -> list[Patient]: ...


class IAdmissionRepository(ABC):
    @abstractmethod
    async def save(self, admission: Admission) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, admission_id: UniqueId) -> Admission | None: ...


class IEncounterRepository(ABC):
    @abstractmethod
    async def save(self, encounter: Encounter) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, encounter_id: UniqueId) -> Encounter | None: ...

    @abstractmethod
    async def list_by_admission(self, tenant_id: str, admission_id: UniqueId) -> list[Encounter]: ...
