"""Command from hospital.encounter.completed integration event."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateBillingFromEncounterCommand:
    tenant_id: str
    correlation_id: str
    external_encounter_id: str
    patient_ref: str
    procedure_codes: list[str]
