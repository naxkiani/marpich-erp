"""Hospital application service — CAP-HLT-001/004/005 acute lifecycle.

Audit via integration events → Audit Platform (no console / local audit tables).
Admission required before encounter (no clinic-style walk-in).
Beds stay in hospital schema — never merge with clinic.
"""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.hospital.domain.aggregates.admission import Admission, AdmissionStatus
from contexts.hospital.domain.aggregates.bed import Bed
from contexts.hospital.domain.aggregates.care_event_projection import (
    CareEventKind,
    CareEventProjection,
)
from contexts.hospital.domain.aggregates.encounter import Encounter
from contexts.hospital.domain.aggregates.patient import Patient
from contexts.hospital.domain.events.integration_events import (
    EncounterStartedIntegration,
    PatientRegisteredIntegration,
)
from contexts.hospital.application.commands.record_care_event import (
    RecordLabResultCareEventCommand,
    RecordPharmacyDispenseCareEventCommand,
)
from contexts.hospital.application.ports.peer_care_events import (
    ILaboratoryEventAdapter,
    IPharmacyEventAdapter,
)
from contexts.hospital.domain.ports.repositories import (
    IAdmissionRepository,
    IBedRepository,
    ICareEventProjectionRepository,
    IEncounterRepository,
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
        beds: IBedRepository,
        care_events: ICareEventProjectionRepository | None = None,
        laboratory_events: ILaboratoryEventAdapter | None = None,
        pharmacy_events: IPharmacyEventAdapter | None = None,
    ) -> None:
        self._patients = patients
        self._admissions = admissions
        self._encounters = encounters
        self._beds = beds
        self._care_events = care_events
        self._laboratory_events = laboratory_events
        self._pharmacy_events = pharmacy_events

    async def handle_laboratory_result_available(self, envelope: dict) -> None:
        """ACL entry — never imports laboratory.domain."""
        if self._laboratory_events is None:
            return
        command = self._laboratory_events.parse_result_available(envelope)
        await self.record_lab_result_care_event(command)

    async def handle_pharmacy_dispense_completed(self, envelope: dict) -> None:
        """ACL entry — never imports pharmacy.domain."""
        if self._pharmacy_events is None:
            return
        command = self._pharmacy_events.parse_dispense_completed(envelope)
        await self.record_pharmacy_dispense_care_event(command)

    async def _resolve_care_context(
        self, tenant_id: str, patient_ref: str
    ) -> tuple[str, str, str] | None:
        """Return (patient_id, admission_id, encounter_id) or None if patient unknown."""
        try:
            patient = await self._patients.find_by_id(
                tenant_id, UniqueId.from_string(patient_ref)
            )
        except ValueError:
            return None
        if not patient:
            return None
        admissions = await self._admissions.list_admissions(tenant_id)
        patient_admissions = [
            a for a in admissions if str(a.patient_id) == str(patient.id)
        ]
        admission = next(
            (a for a in patient_admissions if a.status == AdmissionStatus.ACTIVE),
            patient_admissions[0] if patient_admissions else None,
        )
        admission_id = str(admission.id) if admission else ""
        encounter_id = ""
        if admission:
            encs = await self._encounters.list_by_admission(tenant_id, admission.id)
            if encs:
                encounter_id = str(encs[0].id)
        return str(patient.id), admission_id, encounter_id

    async def record_lab_result_care_event(
        self, command: RecordLabResultCareEventCommand
    ) -> Result[dict]:
        if self._care_events is None:
            return Result.fail("hospital.errors.care_events_unavailable")
        if not command.source_event_id:
            return Result.fail("hospital.errors.care_event_source_required")
        existing = await self._care_events.find_by_source_event(
            command.tenant_id, command.source_event_id
        )
        if existing:
            return Result.ok(existing.to_dict())
        resolved = await self._resolve_care_context(
            command.tenant_id, command.patient_ref
        )
        if not resolved:
            return Result.fail("hospital.errors.patient_not_found")
        patient_id, admission_id, encounter_id = resolved
        try:
            event = CareEventProjection.record(
                tenant_id=command.tenant_id,
                source_event_id=command.source_event_id,
                source_context="laboratory",
                event_kind=CareEventKind.LAB_RESULT,
                peer_id=command.peer_order_id,
                patient_id=patient_id,
                admission_id=admission_id,
                encounter_id=encounter_id,
                correlation_id=command.correlation_id,
                summary={
                    "test_code": command.test_code,
                    "result_value": command.result_value,
                    "result_unit": command.result_unit,
                    "order_id": command.peer_order_id,
                },
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._care_events.save(event)
        return Result.ok(event.to_dict())

    async def record_pharmacy_dispense_care_event(
        self, command: RecordPharmacyDispenseCareEventCommand
    ) -> Result[dict]:
        if self._care_events is None:
            return Result.fail("hospital.errors.care_events_unavailable")
        if not command.source_event_id:
            return Result.fail("hospital.errors.care_event_source_required")
        existing = await self._care_events.find_by_source_event(
            command.tenant_id, command.source_event_id
        )
        if existing:
            return Result.ok(existing.to_dict())
        resolved = await self._resolve_care_context(
            command.tenant_id, command.patient_ref
        )
        if not resolved:
            return Result.fail("hospital.errors.patient_not_found")
        patient_id, admission_id, encounter_id = resolved
        try:
            event = CareEventProjection.record(
                tenant_id=command.tenant_id,
                source_event_id=command.source_event_id,
                source_context="pharmacy",
                event_kind=CareEventKind.PHARMACY_DISPENSE,
                peer_id=command.peer_dispense_id,
                patient_id=patient_id,
                admission_id=admission_id,
                encounter_id=encounter_id,
                correlation_id=command.correlation_id,
                summary={
                    "drug_code": command.drug_code,
                    "quantity_dispensed": command.quantity_dispensed,
                    "dispense_id": command.peer_dispense_id,
                    "prescription_id": command.peer_prescription_id,
                },
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._care_events.save(event)
        return Result.ok(event.to_dict())

    async def list_care_events(
        self,
        tenant_id: str,
        *,
        patient_id: str | None = None,
        admission_id: str | None = None,
        encounter_id: str | None = None,
        limit: int = 50,
    ) -> Result[dict]:
        if self._care_events is None:
            return Result.fail("hospital.errors.care_events_unavailable")
        limit = max(1, min(limit, 100))
        items = await self._care_events.list_care_events(
            tenant_id,
            patient_id=patient_id,
            admission_id=admission_id,
            encounter_id=encounter_id,
            limit=limit,
        )
        return Result.ok(
            {
                "items": [e.to_dict() for e in items],
                "total": len(items),
                "limit": limit,
            }
        )

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

    async def create_bed(
        self,
        *,
        tenant_id: str,
        ward: str,
        room: str,
        bed_code: str,
    ) -> Result[dict]:
        try:
            bed = Bed.create(tenant_id=tenant_id, ward=ward, room=room, bed_code=bed_code)
        except ValueError as exc:
            return Result.fail(str(exc))
        existing = await self._beds.find_by_code(
            tenant_id, bed.ward, bed.room, bed.bed_code
        )
        if existing:
            return Result.fail("hospital.errors.bed_exists")
        await self._beds.save(bed)
        return Result.ok(bed.to_dict())

    async def list_beds(
        self, tenant_id: str, *, limit: int = 50, offset: int = 0
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        beds = await self._beds.list_beds(tenant_id)
        page = beds[offset : offset + limit]
        return Result.ok(
            {
                "items": [b.to_dict() for b in page],
                "total": len(beds),
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
        bed_id: str | None = None,
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

        if bed_id:
            assigned = await self.assign_bed(
                tenant_id=tenant_id,
                admission_id=str(admission.id),
                bed_id=bed_id,
                correlation_id=correlation_id,
            )
            if not assigned.succeeded:
                return assigned
            return Result.ok(assigned.unwrap())

        return Result.ok(admission.to_dict())

    async def assign_bed(
        self,
        *,
        tenant_id: str,
        admission_id: str,
        bed_id: str,
        correlation_id: str,
    ) -> Result[dict]:
        admission = await self._admissions.find_by_id(
            tenant_id, UniqueId.from_string(admission_id)
        )
        if not admission:
            return Result.fail("hospital.errors.admission_not_found")
        bed = await self._beds.find_by_id(tenant_id, UniqueId.from_string(bed_id))
        if not bed:
            return Result.fail("hospital.errors.bed_not_found")

        previous_bed = None
        if admission.bed_id:
            previous_bed = await self._beds.find_by_id(tenant_id, admission.bed_id)

        try:
            if previous_bed and str(previous_bed.id) != str(bed.id):
                previous_bed.release()
            bed.occupy(admission.id)
            event = admission.assign_bed(
                bed_id=bed.id, ward=bed.ward, correlation_id=correlation_id
            )
        except ValueError as exc:
            return Result.fail(str(exc))

        if previous_bed and str(previous_bed.id) != str(bed.id):
            await self._beds.save(previous_bed)
        await self._beds.save(bed)
        await self._admissions.save(admission)
        await publish_integration_event(event)
        return Result.ok(admission.to_dict())

    async def transfer_admission(
        self,
        *,
        tenant_id: str,
        admission_id: str,
        to_ward: str,
        correlation_id: str,
        to_bed_id: str | None = None,
    ) -> Result[dict]:
        admission = await self._admissions.find_by_id(
            tenant_id, UniqueId.from_string(admission_id)
        )
        if not admission:
            return Result.fail("hospital.errors.admission_not_found")

        previous_bed = None
        if admission.bed_id:
            previous_bed = await self._beds.find_by_id(tenant_id, admission.bed_id)

        new_bed = None
        target_bed_id = None
        if to_bed_id:
            new_bed = await self._beds.find_by_id(tenant_id, UniqueId.from_string(to_bed_id))
            if not new_bed:
                return Result.fail("hospital.errors.bed_not_found")
            if new_bed.ward.strip() != to_ward.strip():
                return Result.fail("hospital.errors.bed_ward_mismatch")
            target_bed_id = new_bed.id

        try:
            if previous_bed and (
                new_bed is None or str(previous_bed.id) != str(new_bed.id)
            ):
                previous_bed.release()
            if new_bed is not None:
                new_bed.occupy(admission.id)
            event = admission.transfer(
                to_ward=to_ward,
                to_bed_id=target_bed_id,
                correlation_id=correlation_id,
            )
        except ValueError as exc:
            return Result.fail(str(exc))

        if previous_bed and (
            new_bed is None or str(previous_bed.id) != str(new_bed.id)
        ):
            await self._beds.save(previous_bed)
        if new_bed is not None:
            await self._beds.save(new_bed)
        await self._admissions.save(admission)
        await publish_integration_event(event)
        return Result.ok(admission.to_dict())

    async def discharge_admission(
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

        bed = None
        if admission.bed_id:
            bed = await self._beds.find_by_id(tenant_id, admission.bed_id)

        try:
            event = admission.discharge(correlation_id=correlation_id)
            if bed is not None:
                bed.release()
        except ValueError as exc:
            return Result.fail(str(exc))

        if bed is not None:
            await self._beds.save(bed)
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
        if admission.status != AdmissionStatus.ACTIVE:
            return Result.fail("hospital.errors.admission_not_active")

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
        self,
        tenant_id: str,
        *,
        limit: int = 50,
        offset: int = 0,
        admission_id: str | None = None,
        status: str | None = None,
    ) -> Result[dict]:
        limit = max(1, min(limit, 100))
        offset = max(0, offset)
        encounters = await self._encounters.list_encounters(tenant_id)
        if admission_id:
            encounters = [e for e in encounters if str(e.admission_id) == admission_id]
        if status:
            status_n = status.strip().lower()
            encounters = [e for e in encounters if e.status.value == status_n]
        page = encounters[offset : offset + limit]
        return Result.ok(
            {
                "items": [e.to_dict() for e in page],
                "total": len(encounters),
                "limit": limit,
                "offset": offset,
            }
        )

    async def document_encounter(
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
        try:
            event = encounter.document(
                procedure_codes=procedure_codes,
                diagnosis_codes=diagnosis_codes,
                correlation_id=correlation_id,
            )
        except ValueError as exc:
            return Result.fail(str(exc))
        await self._encounters.save(encounter)
        await publish_integration_event(event)
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
        encounter = await self._encounters.find_by_id(
            tenant_id, UniqueId.from_string(encounter_id)
        )
        if not encounter:
            return Result.fail("hospital.errors.encounter_not_found")

        try:
            if procedure_codes:
                for code in procedure_codes:
                    encounter.add_procedure(code)
            if diagnosis_codes:
                for code in diagnosis_codes:
                    encounter.add_diagnosis(code)
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

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        patients = await self._patients.list_patients(tenant_id)
        beds = await self._beds.list_beds(tenant_id)
        admissions = await self._admissions.list_admissions(tenant_id)
        encounters = await self._encounters.list_encounters(tenant_id)
        available_beds = sum(1 for b in beds if b.status.value == "available")
        occupied_beds = sum(1 for b in beds if b.status.value == "occupied")
        active_admissions = sum(1 for a in admissions if a.status == AdmissionStatus.ACTIVE)
        open_encounters = sum(1 for e in encounters if e.status.value == "in_progress")
        completed = sum(1 for e in encounters if e.status.value == "completed")
        return Result.ok(
            {
                "as_of": datetime.now(UTC).isoformat(),
                "summary": {
                    "patient_count": len(patients),
                    "bed_count": len(beds),
                    "available_beds": available_beds,
                    "occupied_beds": occupied_beds,
                    "active_admissions": active_admissions,
                    "admission_count": len(admissions),
                    "encounter_count": len(encounters),
                    "open_encounters": open_encounters,
                    "completed_encounters": completed,
                },
                "headline": {
                    "patients": len(patients),
                    "available_beds": available_beds,
                    "occupied_beds": occupied_beds,
                    "active_admissions": active_admissions,
                    "open_encounters": open_encounters,
                },
            }
        )

    async def ensure_demo_catalog(self, tenant_id: str, *, correlation_id: str) -> Result[dict]:
        """Idempotent demo acute-care book so Hospital Care is never empty."""
        existing = await self._patients.list_patients(tenant_id)
        if existing:
            dash = await self.get_dashboard(tenant_id)
            return Result.ok({"seeded": False, "dashboard": dash.unwrap()})

        patients_spec = [
            ("MRN-1001", "Ali", "Rezaei", "1975-01-20"),
            ("MRN-1002", "Maryam", "Hosseini", "1988-06-15"),
            ("MRN-1003", "Hassan", "Karimi", "1962-03-08"),
            ("MRN-1004", "Zahra", "Ahmadi", "1990-11-22"),
        ]
        patient_ids: list[str] = []
        for mrn, first, last, dob in patients_spec:
            registered = await self.register_patient(
                tenant_id=tenant_id,
                mrn=mrn,
                first_name=first,
                last_name=last,
                date_of_birth=dob,
                correlation_id=correlation_id,
            )
            if registered.succeeded:
                patient_ids.append(registered.unwrap()["id"])

        beds_spec = [
            ("ICU-1", "101", "A"),
            ("ICU-1", "101", "B"),
            ("Ward-A", "201", "A"),
            ("Ward-A", "201", "B"),
        ]
        bed_ids: list[str] = []
        for ward, room, code in beds_spec:
            created = await self.create_bed(
                tenant_id=tenant_id, ward=ward, room=room, bed_code=code
            )
            if created.succeeded:
                bed_ids.append(created.unwrap()["id"])

        admission_ids: list[str] = []
        admit_pairs = [
            (0, 0, "ICU-1"),
            (1, 1, "ICU-1"),
            (2, 2, "Ward-A"),
        ]
        for patient_idx, bed_idx, ward in admit_pairs:
            if patient_idx >= len(patient_ids) or bed_idx >= len(bed_ids):
                continue
            admitted = await self.admit_patient(
                tenant_id=tenant_id,
                patient_id=patient_ids[patient_idx],
                ward=ward,
                bed_id=bed_ids[bed_idx],
                correlation_id=correlation_id,
            )
            if admitted.succeeded:
                admission_ids.append(admitted.unwrap()["id"])

        encounter_ids: list[str] = []
        for index, admission_id in enumerate(admission_ids[:2]):
            started = await self.start_encounter(
                tenant_id=tenant_id,
                admission_id=admission_id,
                correlation_id=correlation_id,
            )
            if not started.succeeded:
                continue
            eid = started.unwrap()["id"]
            encounter_ids.append(eid)
            if index == 0:
                await self.complete_encounter(
                    tenant_id=tenant_id,
                    encounter_id=eid,
                    procedure_codes=["99223"],
                    diagnosis_codes=["J18.9"],
                    correlation_id=correlation_id,
                )

        dash = await self.get_dashboard(tenant_id)
        return Result.ok(
            {
                "seeded": True,
                "patients": len(patient_ids),
                "beds": len(bed_ids),
                "admissions": len(admission_ids),
                "encounters": len(encounter_ids),
                "dashboard": dash.unwrap(),
            }
        )
