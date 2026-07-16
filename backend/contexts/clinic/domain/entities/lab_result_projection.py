"""Clinic local projection of laboratory.result.available (peer IDs only)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class LabResultProjection:
    id: UniqueId
    tenant_id: str
    order_id: str
    patient_ref: str
    test_code: str
    result_value: str
    result_unit: str | None
    source_event_id: str
    projected_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def from_lab_event(
        cls,
        *,
        tenant_id: str,
        order_id: str,
        patient_ref: str,
        test_code: str,
        result_value: str,
        result_unit: str | None,
        source_event_id: str,
    ) -> LabResultProjection:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            order_id=order_id,
            patient_ref=patient_ref,
            test_code=test_code,
            result_value=result_value,
            result_unit=result_unit,
            source_event_id=source_event_id,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "order_id": self.order_id,
            "patient_ref": self.patient_ref,
            "test_code": self.test_code,
            "result_value": self.result_value,
            "result_unit": self.result_unit,
            "source_event_id": self.source_event_id,
            "projected_at": self.projected_at.isoformat(),
        }
