"""Laboratory test order — CAP-HLT-007.

Stores patient_ref only (peer hospital/clinic id) — never shared patient tables.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class TestOrder(AggregateRoot):
    tenant_id: str
    order_number: str
    patient_ref: str
    test_code: str
    status: str = "ordered"
    result_value: str | None = None
    result_unit: str | None = None
    source_encounter_ref: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    finalized_at: datetime | None = None

    @classmethod
    def place(
        cls,
        *,
        tenant_id: str,
        order_number: str,
        patient_ref: str,
        test_code: str,
        source_encounter_ref: str | None = None,
    ) -> TestOrder:
        ref = patient_ref.strip()
        if not ref:
            raise ValueError("laboratory.errors.patient_ref_required")
        code = test_code.strip().upper()
        if not code:
            raise ValueError("laboratory.errors.test_code_required")
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            order_number=order_number.strip().upper(),
            patient_ref=ref,
            test_code=code,
            status="ordered",
            source_encounter_ref=source_encounter_ref,
        )

    def mark_sample_received(self) -> None:
        if self.status in ("finalized",):
            raise ValueError("laboratory.errors.order_finalized")
        self.status = "sample_received"

    def finalize_result(self, *, result_value: str, result_unit: str | None = None) -> None:
        if self.status == "finalized":
            raise ValueError("laboratory.errors.already_finalized")
        if self.status != "sample_received":
            raise ValueError("laboratory.errors.sample_required_before_result")
        value = result_value.strip()
        if not value:
            raise ValueError("laboratory.errors.result_required")
        self.result_value = value
        self.result_unit = (result_unit or "").strip() or None
        self.status = "finalized"
        self.finalized_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "order_number": self.order_number,
            "patient_ref": self.patient_ref,
            "test_code": self.test_code,
            "status": self.status,
            "result_value": self.result_value,
            "result_unit": self.result_unit,
            "source_encounter_ref": self.source_encounter_ref,
            "created_at": self.created_at.isoformat(),
            "finalized_at": self.finalized_at.isoformat() if self.finalized_at else None,
        }
