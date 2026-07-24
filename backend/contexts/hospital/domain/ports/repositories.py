"""Hospital repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.hospital.domain.aggregates.admission import Admission
from contexts.hospital.domain.aggregates.bed import Bed
from contexts.hospital.domain.aggregates.care_event_projection import CareEventProjection
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

    @abstractmethod
    async def list_admissions(self, tenant_id: str) -> list[Admission]: ...


class IBedRepository(ABC):
    @abstractmethod
    async def save(self, bed: Bed) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, bed_id: UniqueId) -> Bed | None: ...

    @abstractmethod
    async def find_by_code(
        self, tenant_id: str, ward: str, room: str, bed_code: str
    ) -> Bed | None: ...

    @abstractmethod
    async def list_beds(self, tenant_id: str) -> list[Bed]: ...


class IEncounterRepository(ABC):
    @abstractmethod
    async def save(self, encounter: Encounter) -> None: ...

    @abstractmethod
    async def find_by_id(self, tenant_id: str, encounter_id: UniqueId) -> Encounter | None: ...

    @abstractmethod
    async def list_by_admission(self, tenant_id: str, admission_id: UniqueId) -> list[Encounter]: ...

    @abstractmethod
    async def list_encounters(self, tenant_id: str) -> list[Encounter]: ...


class ICareEventProjectionRepository(ABC):
    @abstractmethod
    async def save(self, event: CareEventProjection) -> None: ...

    @abstractmethod
    async def find_by_source_event(
        self, tenant_id: str, source_event_id: str
    ) -> CareEventProjection | None: ...

    @abstractmethod
    async def list_care_events(
        self,
        tenant_id: str,
        *,
        patient_id: str | None = None,
        admission_id: str | None = None,
        encounter_id: str | None = None,
        limit: int = 50,
    ) -> list[CareEventProjection]: ...
