"""Hospital application service — CAP-HLT-001 acute patient lifecycle.

Audit via integration events → Audit Platform (no console / local audit tables).
Admission required before encounter (no clinic-style walk-in).
"""
from __future__ import annotations

from contexts.hospital.domain.aggregates.admission import Admission
from contexts.hospital.domain.aggregates.encounter import Encounter
from contexts.hospital.domain.aggregates.patient import Patient
from contexts.hospital.domain.entities.lab_result_projection import LabResultProjection
from contexts.hospital.domain.events.integration_events import (
    EncounterStartedIntegration,
    PatientRegisteredIntegration,
)
from contexts.hospital.domain.ports.repositories import (
    IAdmissionRepository,
    IEncounterRepository,
    ILabResultProjectionRepository,
    IPatientRepository,
)
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.domain.value_objects.unique_id import UniqueId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class HospitalApplicationService:
    def __init__(
        self,
        patients: IPatientRepository,
        admissions: IAdmissionRepository,
        encounters: IEncounterRepository,
        lab_projections: ILabResultProjectionRepository,
    ) -> None:
        self._patients = patients
        self._admissions = admissions
        self._encounters = encounters
        self._lab_projections = lab_projections

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
        await publish_integration_event(
            PatientRegisteredIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                patient_id=patient.id,
                mrn=patient.mrn,
                full_name=patient.full_name,
            )
        )
        return Result.ok(patient.to_dict())

    async def list_patients(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        patients = await self._patients.list_patients(tenant_id)
        page = patients[offset : offset + limit]
        return Result.ok(
            {
                "items": [p.to_dict() for p in page],
                "total": len(patients),
                "limit": limit,
                "offset": offset,
            }
        )

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
        return Result.ok(admission.to_dict())

    async def list_admissions(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        admissions = await self._admissions.list_admissions(tenant_id)
        page = admissions[offset : offset + limit]
        return Result.ok(
            {
                "items": [a.to_dict() for a in page],
                "total": len(admissions),
                "limit": limit,
                "offset": offset,
            }
        )

    async def start_encounter(
        self,
        *,
        tenant_id: str,
        admission_id: str,
        correlation_id: str,
    ) -> Result[dict]:
        admission = await self._admissions.find_by_id(
            tenant_id, UniqueId.from_string(admission_id)
        )
        if not admission:
            return Result.fail("hospital.errors.admission_not_found")

        encounter = Encounter.start(
            tenant_id=tenant_id,
            patient_id=admission.patient_id,
            admission_id=admission.id,
        )
        await self._encounters.save(encounter)
        await publish_integration_event(
            EncounterStartedIntegration(
                tenant_id=TenantId.create(tenant_id),
                correlation_id=correlation_id,
                encounter_id=encounter.id,
                patient_id=encounter.patient_id,
                admission_id=encounter.admission_id,
            )
        )
        return Result.ok(encounter.to_dict())

    async def list_encounters(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        encounters = await self._encounters.list_encounters(tenant_id)
        page = encounters[offset : offset + limit]
        return Result.ok(
            {
                "items": [e.to_dict() for e in page],
                "total": len(encounters),
                "limit": limit,
                "offset": offset,
            }
        )

    async def complete_encounter(
        self,
        *,
        tenant_id: str,
        encounter_id: str,
        procedure_codes: list[str] | None,
        diagnosis_codes: list[str] | None,
        correlation_id: str,
    ) -> Result[dict]:
        encounter = await self._encounters.find_by_id(
            tenant_id, UniqueId.from_string(encounter_id)
        )
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
        return Result.ok(encounter.to_dict())

    async def get_encounter(self, tenant_id: str, encounter_id: str) -> Result[dict]:
        encounter = await self._encounters.find_by_id(
            tenant_id, UniqueId.from_string(encounter_id)
        )
        if not encounter:
            return Result.fail("hospital.errors.encounter_not_found")
        return Result.ok(encounter.to_dict())

    async def project_laboratory_result(
        self,
        *,
        tenant_id: str,
        order_id: str,
        patient_ref: str,
        test_code: str,
        result_value: str,
        result_unit: str | None,
        source_event_id: str,
    ) -> Result[dict]:
        """Idempotent ACL projection of laboratory.result.available (peer IDs only)."""
        existing = await self._lab_projections.find_by_event_id(tenant_id, source_event_id)
        if existing:
            return Result.ok(existing.to_dict())
        if not order_id or not patient_ref or not test_code or not source_event_id:
            return Result.fail("hospital.errors.invalid_lab_result_projection")

        projection = LabResultProjection.from_lab_event(
            tenant_id=tenant_id,
            order_id=order_id,
            patient_ref=patient_ref,
            test_code=test_code,
            result_value=result_value,
            result_unit=result_unit,
            source_event_id=source_event_id,
        )
        await self._lab_projections.save(projection)
        return Result.ok(projection.to_dict())

    async def list_lab_result_projections(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        rows = await self._lab_projections.list_projections(tenant_id)
        page = rows[offset : offset + limit]
        return Result.ok(
            {
                "items": [r.to_dict() for r in page],
                "total": len(rows),
                "limit": limit,
                "offset": offset,
            }
        )
