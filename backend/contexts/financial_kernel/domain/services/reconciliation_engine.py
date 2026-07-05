"""Enterprise reconciliation engine — matching, analysis, AI, reports."""
from __future__ import annotations

from contexts.financial_kernel.domain.aggregates.reconciliation import (
    ApprovalAction,
    MatchType,
    ReconciliationStatus,
    ReconciliationType,
)

RECONCILIATION_CATALOG: dict[str, dict] = {
    ReconciliationType.BANK.value: {
        "label": "Bank Reconciliation",
        "left_label": "Bank Statement",
        "right_label": "Book Balance",
        "description": "Match bank statement lines to book transactions",
        "approval_required": True,
    },
    ReconciliationType.CASH.value: {
        "label": "Cash Reconciliation",
        "left_label": "Physical Cash Count",
        "right_label": "Cash Book",
        "description": "Reconcile petty cash and cash drawer counts",
        "approval_required": True,
    },
    ReconciliationType.INTERCOMPANY.value: {
        "label": "Intercompany Reconciliation",
        "left_label": "Entity A Balance",
        "right_label": "Entity B Balance",
        "description": "Match intercompany due-to/due-from balances",
        "approval_required": True,
    },
    ReconciliationType.SUBLEDGER.value: {
        "label": "Subledger Reconciliation",
        "left_label": "Subledger Balance",
        "right_label": "GL Control Account",
        "description": "Reconcile subledger totals to control accounts",
        "approval_required": True,
    },
    ReconciliationType.GENERAL_LEDGER.value: {
        "label": "General Ledger Reconciliation",
        "left_label": "Trial Balance",
        "right_label": "Account Balances",
        "description": "Reconcile GL trial balance to account ledger",
        "approval_required": True,
    },
}


def list_reconciliation_catalog() -> list[dict]:
    return [{"reconciliation_type": key, **meta} for key, meta in RECONCILIATION_CATALOG.items()]


def get_reconciliation_definition(reconciliation_type: str) -> dict:
    definition = RECONCILIATION_CATALOG.get(reconciliation_type)
    if not definition:
        raise KeyError(f"unknown_reconciliation_type:{reconciliation_type}")
    return definition


def sum_item_amounts(items: list[dict]) -> float:
    return round(sum(float(i.get("amount", 0)) for i in items), 2)


def automatic_match_items(
    left_items: list[dict],
    right_items: list[dict],
    *,
    amount_tolerance: float = 0.01,
    match_by_reference: bool = True,
) -> tuple[list[dict], list[dict], list[dict]]:
    matched: list[dict] = []
    used_right: set[int] = set()
    unmatched_left: list[dict] = []

    for left in left_items:
        left_amount = round(float(left.get("amount", 0)), 2)
        left_ref = _normalize_ref(left)
        found = False

        for idx, right in enumerate(right_items):
            if idx in used_right:
                continue
            right_amount = round(float(right.get("amount", 0)), 2)
            right_ref = _normalize_ref(right)
            amount_ok = abs(left_amount - right_amount) <= amount_tolerance
            ref_ok = (
                not match_by_reference
                or left_ref == right_ref
                or not left_ref
                or not right_ref
            )
            if amount_ok and ref_ok:
                matched.append(
                    {
                        "left": left,
                        "right": right,
                        "match_type": MatchType.AUTOMATIC.value,
                        "match_score": _match_score(left, right),
                    }
                )
                used_right.add(idx)
                found = True
                break

        if not found:
            for idx, right in enumerate(right_items):
                if idx in used_right:
                    continue
                right_amount = round(float(right.get("amount", 0)), 2)
                if abs(left_amount - right_amount) <= amount_tolerance:
                    matched.append(
                        {
                            "left": left,
                            "right": right,
                            "match_type": MatchType.AUTOMATIC.value,
                            "match_score": 0.7,
                            "match_note": "amount_only",
                        }
                    )
                    used_right.add(idx)
                    found = True
                    break

        if not found:
            unmatched_left.append(left)

    unmatched_right = [r for i, r in enumerate(right_items) if i not in used_right]
    return matched, unmatched_left, unmatched_right


def apply_manual_match(
    *,
    matched_pairs: list[dict],
    unmatched_left: list[dict],
    unmatched_right: list[dict],
    left_item: dict,
    right_item: dict,
    actor_id: str,
) -> tuple[list[dict], list[dict], list[dict]]:
    pairs = list(matched_pairs)
    left = list(unmatched_left)
    right = list(unmatched_right)
    pairs.append(
        {
            "left": left_item,
            "right": right_item,
            "match_type": MatchType.MANUAL.value,
            "matched_by": actor_id,
        }
    )
    left = [i for i in left if i != left_item]
    right = [i for i in right if i != right_item]
    return pairs, left, right


def build_exception_queue(
    *,
    unmatched_left: list[dict],
    unmatched_right: list[dict],
    variance: float,
) -> list[dict]:
    exceptions: list[dict] = []
    for item in unmatched_left:
        exceptions.append(
            {
                "side": "left",
                "item": item,
                "reason": "unmatched_left_item",
                "amount": item.get("amount", 0),
                "reference": item.get("reference", ""),
            }
        )
    for item in unmatched_right:
        exceptions.append(
            {
                "side": "right",
                "item": item,
                "reason": "unmatched_right_item",
                "amount": item.get("amount", 0),
                "reference": item.get("reference", ""),
            }
        )
    if abs(variance) >= 0.01:
        exceptions.append(
            {
                "side": "balance",
                "reason": "variance_detected",
                "variance": variance,
            }
        )
    return exceptions


def build_difference_analysis(
    *,
    left_total: float,
    right_total: float,
    matched_pairs: list[dict],
    unmatched_left: list[dict],
    unmatched_right: list[dict],
) -> dict:
    variance = round(right_total - left_total, 2)
    unmatched_left_total = sum_item_amounts(unmatched_left)
    unmatched_right_total = sum_item_amounts(unmatched_right)
    matched_left_total = sum_item_amounts([p["left"] for p in matched_pairs])
    matched_right_total = sum_item_amounts([p["right"] for p in matched_pairs])
    return {
        "left_total": left_total,
        "right_total": right_total,
        "variance": variance,
        "balanced": abs(variance) < 0.01,
        "matched_count": len(matched_pairs),
        "unmatched_left_count": len(unmatched_left),
        "unmatched_right_count": len(unmatched_right),
        "matched_left_total": matched_left_total,
        "matched_right_total": matched_right_total,
        "unmatched_left_total": unmatched_left_total,
        "unmatched_right_total": unmatched_right_total,
        "match_rate": round(
            len(matched_pairs) / max(len(matched_pairs) + len(unmatched_left) + len(unmatched_right), 1),
            4,
        ),
    }


def generate_ai_suggestions(
    *,
    reconciliation_type: str,
    difference_analysis: dict,
    exceptions: list[dict],
    unmatched_left: list[dict],
    unmatched_right: list[dict],
) -> list[dict]:
    suggestions: list[dict] = []
    variance = difference_analysis.get("variance", 0)
    match_rate = difference_analysis.get("match_rate", 0)

    if abs(variance) >= 0.01:
        suggestions.append(
            {
                "priority": "high",
                "category": "variance",
                "message": f"Balance variance of {variance} requires investigation before approval.",
                "action": "review_unmatched_items",
            }
        )

    if unmatched_left and unmatched_right:
        near_matches = _find_near_matches(unmatched_left, unmatched_right)
        for pair in near_matches[:5]:
            suggestions.append(
                {
                    "priority": "medium",
                    "category": "near_match",
                    "message": "Potential manual match — amounts close with similar references.",
                    "left_item": pair["left"],
                    "right_item": pair["right"],
                    "action": "manual_match",
                }
            )

    if match_rate < 0.8 and (unmatched_left or unmatched_right):
        suggestions.append(
            {
                "priority": "medium",
                "category": "low_match_rate",
                "message": f"Match rate {match_rate:.0%} is below 80%; review reference formatting.",
                "action": "normalize_references",
            }
        )

    if reconciliation_type == ReconciliationType.BANK.value and len(exceptions) > 3:
        suggestions.append(
            {
                "priority": "low",
                "category": "bank_timing",
                "message": "Multiple bank exceptions may indicate timing differences; check statement date range.",
                "action": "expand_date_window",
            }
        )

    if reconciliation_type == ReconciliationType.INTERCOMPANY.value and abs(variance) >= 0.01:
        suggestions.append(
            {
                "priority": "high",
                "category": "intercompany",
                "message": "Intercompany imbalance detected; verify elimination entries and FX rates.",
                "action": "review_ic_eliminations",
            }
        )

    if not suggestions:
        suggestions.append(
            {
                "priority": "low",
                "category": "optimal",
                "message": "Reconciliation is balanced; proceed to approval.",
                "action": "submit_for_approval",
            }
        )
    return suggestions


def build_reconciliation_report(
    *,
    reconciliation_type: str,
    reference_label: str,
    reconciliation_date: str,
    difference_analysis: dict,
    matched_pairs: list[dict],
    exceptions: list[dict],
    status: str,
) -> dict:
    return {
        "reconciliation_type": reconciliation_type,
        "reference_label": reference_label,
        "reconciliation_date": reconciliation_date,
        "status": status,
        "summary": difference_analysis,
        "matched_count": len(matched_pairs),
        "exception_count": len(exceptions),
        "ready_for_approval": (
            status in (ReconciliationStatus.MATCHED.value, ReconciliationStatus.PARTIAL_MATCH.value)
            and difference_analysis.get("balanced", False)
        ),
        "sections": [
            {"name": "matched", "count": len(matched_pairs)},
            {"name": "exceptions", "count": len(exceptions)},
        ],
    }


def validate_approval_action(
    *,
    current_status: str,
    action: str,
) -> tuple[bool, str]:
    if action == ApprovalAction.SUBMIT.value:
        if current_status in (
            ReconciliationStatus.PENDING_APPROVAL.value,
            ReconciliationStatus.APPROVED.value,
        ):
            return False, "already_submitted"
        return True, ""
    if action == ApprovalAction.APPROVE.value:
        if current_status != ReconciliationStatus.PENDING_APPROVAL.value:
            return False, "not_pending_approval"
        return True, ""
    if action == ApprovalAction.REJECT.value:
        if current_status != ReconciliationStatus.PENDING_APPROVAL.value:
            return False, "not_pending_approval"
        return True, ""
    if action == ApprovalAction.REOPEN.value:
        if current_status not in (
            ReconciliationStatus.APPROVED.value,
            ReconciliationStatus.REJECTED.value,
        ):
            return False, "cannot_reopen"
        return True, ""
    return False, "unknown_action"


def _normalize_ref(item: dict) -> str:
    return str(
        item.get("reference", "")
        or item.get("source_document_id", "")
        or item.get("journal_id", "")
        or ""
    ).strip().lower()


def _match_score(left: dict, right: dict) -> float:
    score = 0.5
    left_ref = _normalize_ref(left)
    right_ref = _normalize_ref(right)
    if left_ref and right_ref and left_ref == right_ref:
        score += 0.4
    left_amt = round(float(left.get("amount", 0)), 2)
    right_amt = round(float(right.get("amount", 0)), 2)
    if left_amt == right_amt:
        score += 0.1
    return min(score, 1.0)


def _find_near_matches(
    left_items: list[dict], right_items: list[dict]
) -> list[dict]:
    near: list[dict] = []
    for left in left_items:
        left_amount = float(left.get("amount", 0))
        for right in right_items:
            right_amount = float(right.get("amount", 0))
            if abs(left_amount - right_amount) <= max(abs(left_amount) * 0.05, 1.0):
                near.append({"left": left, "right": right, "amount_delta": round(right_amount - left_amount, 2)})
    return near
