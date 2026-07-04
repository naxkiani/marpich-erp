"""Payment engine — allocation, matching, installments, splits."""
from __future__ import annotations


def auto_allocate(
    paid_amount: float,
    open_items: list[dict],
) -> list[dict]:
    """FIFO allocation of payment amount across open documents."""
    remaining = round(paid_amount, 2)
    allocations: list[dict] = []
    for item in sorted(open_items, key=lambda x: x.get("due_date", "")):
        if remaining <= 0:
            break
        due = round(float(item.get("amount_due", 0)), 2)
        if due <= 0:
            continue
        alloc = min(remaining, due)
        allocations.append(
            {
                "document_type": item.get("document_type", "invoice"),
                "document_id": item["document_id"],
                "amount": alloc,
                "allocated": True,
            }
        )
        remaining = round(remaining - alloc, 2)
    return allocations


def build_installment_schedule(
    total_amount: float,
    installment_count: int,
    due_dates: list[str],
) -> list[dict]:
    if installment_count <= 0 or len(due_dates) != installment_count:
        raise ValueError("invalid_installment_schedule")
    base = round(total_amount / installment_count, 2)
    installments = []
    allocated = 0.0
    for i, due in enumerate(due_dates):
        amount = base if i < installment_count - 1 else round(total_amount - allocated, 2)
        allocated = round(allocated + amount, 2)
        installments.append(
            {
                "installment_number": i + 1,
                "due_date": due,
                "amount": amount,
                "status": "pending",
                "payment_id": None,
            }
        )
    return installments


def validate_split_amounts(splits: list[dict], total_amount: float) -> tuple[bool, str | None]:
    if not splits:
        return False, "empty_splits"
    split_total = round(sum(float(s.get("amount", 0)) for s in splits), 2)
    if split_total != round(total_amount, 2):
        return False, "split_total_mismatch"
    return True, None


def match_payments_to_bank(
    payments: list[dict], bank_items: list[dict]
) -> dict:
    matched: list[dict] = []
    used_bank: set[int] = set()
    unmatched_payments: list[dict] = []

    for pay in payments:
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
            unmatched_payments.append(pay)

    unmatched_bank = [b for i, b in enumerate(bank_items) if i not in used_bank]
    return {
        "matched_pairs": matched,
        "unmatched_payments": unmatched_payments,
        "unmatched_bank": unmatched_bank,
        "match_rate": round(len(matched) / max(len(payments), 1), 4),
    }
