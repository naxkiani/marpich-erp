"""Command from hospital.encounter.* — Laboratory ACL (no Hospital imports)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LinkHospitalEncounterCommand:
    tenant_id: str
    correlation_id: str
    encounter_ref: str
    patient_ref: str
    phase: str  # started | completed
