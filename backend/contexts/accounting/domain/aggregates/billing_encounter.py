"""Billing encounter — Accounting local aggregate (not Hospital Encounter)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class BillingStatus(StrEnum):
    PENDING = "pending"
    POSTED = "posted"
    PAID = "paid"
    VOID = "void"


# Simple fee schedule for demo
FEE_SCHEDULE: dict[str, float] = {
    "99213": 150.0,
    "99214": 200.0,
    "99215": 275.0,
    "80053": 85.0,
    "85025": 45.0,
}


@dataclass(eq=False, kw_only=True)
class BillingEncounter(AggregateRoot):
    tenant_id: str
    external_encounter_id: str
    patient_ref: str
    procedure_codes: list[str]
    line_items: list[dict]
    total_amount: float
    currency: str = "USD"
    status: BillingStatus = BillingStatus.PENDING
    correlation_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def from_hospital_event(
        cls,
        *,
        tenant_id: str,
        correlation_id: str,
        external_encounter_id: str,
        patient_ref: str,
        procedure_codes: list[str],
    ) -> BillingEncounter:
        line_items = []
        total = 0.0
        for code in procedure_codes:
            amount = FEE_SCHEDULE.get(code, 100.0)
            line_items.append({"code": code, "description": f"Procedure {code}", "amount": amount})
            total += amount
        if not line_items:
            line_items.append({"code": "DEFAULT", "description": "Clinical encounter", "amount": 100.0})
            total = 100.0

        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            external_encounter_id=external_encounter_id,
            patient_ref=patient_ref,
            procedure_codes=procedure_codes,
            line_items=line_items,
            total_amount=round(total, 2),
            correlation_id=correlation_id,
        )

    def post(self) -> None:
        if self.status != BillingStatus.PENDING:
            raise ValueError("Billing already processed")
        self.status = BillingStatus.POSTED

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "external_encounter_id": self.external_encounter_id,
            "patient_ref": self.patient_ref,
            "procedure_codes": self.procedure_codes,
            "line_items": self.line_items,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "status": self.status.value,
            "correlation_id": self.correlation_id,
            "created_at": self.created_at.isoformat(),
        }
