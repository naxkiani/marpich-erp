"""Payment reconciliation aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class PaymentReconciliationStatus(StrEnum):
    OPEN = "open"
    MATCHED = "matched"
    PARTIAL_MATCH = "partial_match"
    UNMATCHED = "unmatched"


@dataclass(eq=False, kw_only=True)
class PaymentReconciliation(AggregateRoot):
    tenant_id: str
    reconciliation_date: str
    bank_reference: str | None
    payment_items: list[dict]
    bank_items: list[dict]
    matched_pairs: list[dict]
    unmatched_payments: list[dict]
    unmatched_bank: list[dict]
    status: str
    matched_amount: float = 0.0
    variance: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        reconciliation_date: str,
        payment_items: list[dict],
        bank_items: list[dict],
        bank_reference: str | None = None,
    ) -> PaymentReconciliation:
        matched, unmatched_pay, unmatched_bank = _match_payment_items(payment_items, bank_items)
        matched_amount = round(sum(p["payment"].get("amount", 0) for p in matched), 2)
        pay_total = round(sum(p.get("amount", 0) for p in payment_items), 2)
        bank_total = round(sum(b.get("amount", 0) for b in bank_items), 2)
        variance = round(bank_total - pay_total, 2)
        if matched and not unmatched_pay and not unmatched_bank:
            status = PaymentReconciliationStatus.MATCHED
        elif matched:
            status = PaymentReconciliationStatus.PARTIAL_MATCH
        else:
            status = PaymentReconciliationStatus.UNMATCHED
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            reconciliation_date=reconciliation_date,
            bank_reference=bank_reference,
            payment_items=payment_items,
            bank_items=bank_items,
            matched_pairs=matched,
            unmatched_payments=unmatched_pay,
            unmatched_bank=unmatched_bank,
            status=status,
            matched_amount=matched_amount,
            variance=variance,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "reconciliation_date": self.reconciliation_date,
            "bank_reference": self.bank_reference,
            "payment_items": self.payment_items,
            "bank_items": self.bank_items,
            "matched_pairs": self.matched_pairs,
            "unmatched_payments": self.unmatched_payments,
            "unmatched_bank": self.unmatched_bank,
            "status": self.status,
            "matched_amount": self.matched_amount,
            "variance": self.variance,
            "created_at": self.created_at.isoformat(),
        }


def _match_payment_items(
    payment_items: list[dict], bank_items: list[dict]
) -> tuple[list[dict], list[dict], list[dict]]:
    matched: list[dict] = []
    used_bank: set[int] = set()
    unmatched_pay: list[dict] = []

    for pay in payment_items:
        pay_amount = round(float(pay.get("amount", 0)), 2)
        pay_ref = pay.get("reference", "")
        found = False
        for idx, bank in enumerate(bank_items):
            if idx in used_bank:
                continue
            bank_amount = round(float(bank.get("amount", 0)), 2)
            bank_ref = bank.get("reference", "")
            if pay_amount == bank_amount and (pay_ref == bank_ref or not pay_ref or not bank_ref):
                matched.append({"payment": pay, "bank": bank})
                used_bank.add(idx)
                found = True
                break
        if not found:
            unmatched_pay.append(pay)

    unmatched_bank = [b for i, b in enumerate(bank_items) if i not in used_bank]
    return matched, unmatched_pay, unmatched_bank
