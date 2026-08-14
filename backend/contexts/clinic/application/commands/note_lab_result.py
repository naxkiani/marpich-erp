"""Command from laboratory.result.available — Clinic ACL (no Laboratory imports)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NoteLabResultCommand:
    tenant_id: str
    correlation_id: str
    order_ref: str
    patient_ref: str
    test_code: str
    result_value: str
    result_unit: str
