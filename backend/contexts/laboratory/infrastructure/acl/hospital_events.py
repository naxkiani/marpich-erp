"""ACL — Hospital encounter envelopes → Laboratory commands (peer IDs only)."""
from __future__ import annotations

from contexts.laboratory.application.commands.link_hospital_encounter import (
    LinkHospitalEncounterCommand,
)


class HospitalEventAdapter:
    def parse_encounter_started(self, envelope: dict) -> LinkHospitalEncounterCommand:
        return self._parse(envelope, phase="started")

    def parse_encounter_completed(self, envelope: dict) -> LinkHospitalEncounterCommand:
        return self._parse(envelope, phase="completed")

    def _parse(self, envelope: dict, *, phase: str) -> LinkHospitalEncounterCommand:
        payload = envelope.get("payload") if isinstance(envelope.get("payload"), dict) else {}
        return LinkHospitalEncounterCommand(
            tenant_id=str(envelope.get("tenant_id") or ""),
            correlation_id=str(envelope.get("correlation_id") or envelope.get("event_id") or ""),
            encounter_ref=str(payload.get("encounter_id") or ""),
            patient_ref=str(payload.get("patient_id") or ""),
            phase=phase,
        )


async def handle_hospital_encounter_started(envelope: dict) -> None:
    if str(envelope.get("event_name") or "") != "hospital.encounter.started":
        return
    from contexts.laboratory.container import get_laboratory_service

    cmd = HospitalEventAdapter().parse_encounter_started(envelope)
    await get_laboratory_service().link_hospital_encounter(cmd)


async def handle_hospital_encounter_completed(envelope: dict) -> None:
    if str(envelope.get("event_name") or "") != "hospital.encounter.completed":
        return
    from contexts.laboratory.container import get_laboratory_service

    cmd = HospitalEventAdapter().parse_encounter_completed(envelope)
    await get_laboratory_service().link_hospital_encounter(cmd)
