"""ACL — Clinic encounter envelopes → Pharmacy commands (peer IDs only)."""
from __future__ import annotations

from contexts.pharmacy.application.commands.link_hospital_encounter import (
    LinkHospitalEncounterCommand,
)


class ClinicEventAdapter:
    def parse_encounter_completed(self, envelope: dict) -> LinkHospitalEncounterCommand:
        payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
        return LinkHospitalEncounterCommand(
            tenant_id=str(envelope.get("tenant_id") or ""),
            correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
            encounter_ref=str(payload.get("encounter_id") or ""),
            patient_ref=str(payload.get("patient_id") or ""),
        )


async def handle_clinic_encounter_completed(envelope: dict) -> None:
    if str(envelope.get("event_name") or "") != "clinic.encounter.completed":
        return
    from contexts.pharmacy.container import get_pharmacy_service

    cmd = ClinicEventAdapter().parse_encounter_completed(envelope)
    await get_pharmacy_service().link_clinic_encounter(cmd)
