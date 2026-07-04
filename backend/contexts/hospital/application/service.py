"""Hospital application service."""
from __future__ import annotations

import json
from datetime import UTC, datetime

from contexts.hospital.domain.aggregates.admission import Admission
from contexts.hospital.domain.aggregates.encounter import Encounter
from contexts.hospital.domain.aggregates.patient import Patient
from contexts.hospital.domain.ports.repositories import (
    IAdmissionRepository,
    IEncounterRepository,
    IPatientRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class ConsoleHospitalAudit:
    async def log(self, **kwargs: object) -> None:
        entry = {"type": "audit", "context": "hospital", **kwargs, "occurred_at": datetime.now(UTC).isoformat()}
        print(json.dumps(entry, default=str))


class HospitalApplicationService:
    def __init__(
        self,
        patients: IPatientRepository,
        admissions: IAdmissionRepository,
        encounters: IEncounterRepository,
        audit: ConsoleHospitalAudit | None = None,
    ) -> None:
        self._patients = patients
        self._admissions = admissions
        self._encounters = encounters
        self._audit = audit or ConsoleHospitalAudit()

    async def register_patient(
        self,
        *,
        tenant_id: str,
        mrn: str,
        first_name: str,
        last_name: str,
        date_of_birth: str,
        correlation_id: str,
    ) -> Result[dict]:
        existing = await self._patients.find_by_mrn(tenant_id, mrn)
        if existing:
            return Result.fail("hospital.errors.mrn_exists")

        patient = Patient.register(
            tenant_id=tenant_id,
            mrn=mrn,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
        await self._patients.save(patient)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="hospital.patient.registered",
            resource_type="patient",
            resource_id=str(patient.id),
        )
        return Result.ok(patient.to_dict())

    async def admit_patient(
        self,
        *,
        tenant_id: str,
        patient_id: str,
        ward: str,
        correlation_id: str,
    ) -> Result[dict]:
        patient = await self._patients.find_by_id(tenant_id, UniqueId.from_string(patient_id))
        if not patient:
            return Result.fail("hospital.errors.patient_not_found")

        admission, event = Admission.register(
            tenant_id=tenant_id,
            patient_id=patient.id,
            ward=ward,
            correlation_id=correlation_id,
        )
        await self._admissions.save(admission)
        await publish_integration_event(event)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="hospital.admission.registered",
            resource_type="admission",
            resource_id=str(admission.id),
        )
        return Result.ok(admission.to_dict())

    async def start_encounter(
        self,
        *,
        tenant_id: str,
        admission_id: str,
        correlation_id: str,
    ) -> Result[dict]:
        admission = await self._admissions.find_by_id(tenant_id, UniqueId.from_string(admission_id))
        if not admission:
            return Result.fail("hospital.errors.admission_not_found")

        encounter = Encounter.start(
            tenant_id=tenant_id,
            patient_id=admission.patient_id,
            admission_id=admission.id,
        )
        await self._encounters.save(encounter)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="hospital.encounter.started",
            resource_type="encounter",
            resource_id=str(encounter.id),
        )
        return Result.ok(encounter.to_dict())

    async def complete_encounter(
        self,
        *,
        tenant_id: str,
        encounter_id: str,
        procedure_codes: list[str] | None,
        diagnosis_codes: list[str] | None,
        correlation_id: str,
    ) -> Result[dict]:
        encounter = await self._encounters.find_by_id(tenant_id, UniqueId.from_string(encounter_id))
        if not encounter:
            return Result.fail("hospital.errors.encounter_not_found")

        if procedure_codes:
            for code in procedure_codes:
                encounter.add_procedure(code)
        if diagnosis_codes:
            encounter.diagnosis_codes.extend(diagnosis_codes)

        try:
            event = encounter.complete(correlation_id=correlation_id)
        except ValueError as exc:
            return Result.fail(str(exc))

        await self._encounters.save(encounter)
        await publish_integration_event(event)
        await self._audit.log(
            tenant_id=tenant_id,
            correlation_id=correlation_id,
            action="hospital.encounter.completed",
            resource_type="encounter",
            resource_id=str(encounter.id),
            payload={"procedure_codes": encounter.procedure_codes},
        )
        return Result.ok(encounter.to_dict())

    async def get_encounter(self, tenant_id: str, encounter_id: str) -> Result[dict]:
        encounter = await self._encounters.find_by_id(tenant_id, UniqueId.from_string(encounter_id))
        if not encounter:
            return Result.fail("hospital.errors.encounter_not_found")
        return Result.ok(encounter.to_dict())

    async def list_patients(self, tenant_id: str) -> Result[list[dict]]:
        patients = await self._patients.list_patients(tenant_id)
        return Result.ok([p.to_dict() for p in patients])
