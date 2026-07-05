"""Banking Settlement Engine domain logic."""
from __future__ import annotations

from contexts.banking.domain.aggregates.settlement_engine import SettlementType

SETTLEMENT_CATALOG: dict[str, dict] = {
    "internal_settlement": {"label": "Internal Settlement", "supported": True},
    "interbank_settlement": {"label": "Interbank Settlement", "supported": True},
    "clearing": {"label": "Clearing", "supported": True},
    "bank_reconciliation": {"label": "Bank Reconciliation", "supported": True},
    "settlement_reports": {"label": "Settlement Reports", "supported": True},
    "exception_management": {"label": "Exception Management", "supported": True},
    "difference_analysis": {"label": "Difference Analysis", "supported": True},
    "retry_mechanism": {"label": "Retry Mechanism", "supported": True},
    "automatic_matching": {"label": "Automatic Matching", "supported": True},
    "manual_adjustment_approval": {"label": "Manual Adjustment Approval", "supported": True},
    "settlement_dashboard": {"label": "Settlement Dashboard", "supported": True},
    "reconciliation_audit": {"label": "Reconciliation Audit", "supported": True},
}

SETTLEMENT_POLICY_KEYS: list[dict] = [
    {"key": "settlement.interbank.cutoff", "description": "Interbank settlement cutoff time"},
    {"key": "settlement.clearing.window", "description": "Clearing window parameters"},
    {"key": "settlement.match.tolerance", "description": "Reconciliation amount tolerance"},
    {"key": "settlement.retry.max_attempts", "description": "Exception retry limit"},
    {"key": "settlement.adjustment.approval_level", "description": "Manual adjustment approval levels"},
    {"key": "settlement.reconciliation.auto_match", "description": "Automatic matching rules"},
    {"key": "settlement.exception.escalation", "description": "Exception escalation thresholds"},
]

POSTING_RULE_BY_TYPE: dict[str, str] = {
    SettlementType.INTERNAL.value: "bank_settlement",
    SettlementType.INTERBANK.value: "interbank_settlement",
    SettlementType.CLEARING.value: "clearing_settlement",
}


def list_settlement_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in SETTLEMENT_CATALOG.items()]


def list_settlement_policy_keys() -> list[dict]:
    return list(SETTLEMENT_POLICY_KEYS)


def resolve_posting_rule(settlement_type: str) -> str:
    return POSTING_RULE_BY_TYPE.get(settlement_type, "bank_settlement")


def _normalize_ref(item: dict) -> str:
    return str(item.get("reference", "") or item.get("id", "")).strip().lower()


def _match_score(left: dict, right: dict) -> float:
    score = 0.5
    if _normalize_ref(left) and _normalize_ref(left) == _normalize_ref(right):
        score += 0.4
    if round(float(left.get("amount", 0)), 2) == round(float(right.get("amount", 0)), 2):
        score += 0.1
    return min(score, 1.0)


def automatic_match(
    statement_items: list[dict],
    book_items: list[dict],
    *,
    amount_tolerance: float = 0.01,
) -> tuple[list[dict], list[dict], list[dict]]:
    matched: list[dict] = []
    used_book: set[int] = set()
    unmatched_stmt: list[dict] = []

    for stmt in statement_items:
        stmt_amount = round(float(stmt.get("amount", 0)), 2)
        stmt_ref = _normalize_ref(stmt)
        found = False
        for idx, book in enumerate(book_items):
            if idx in used_book:
                continue
            book_amount = round(float(book.get("amount", 0)), 2)
            book_ref = _normalize_ref(book)
            if abs(stmt_amount - book_amount) <= amount_tolerance and (
                stmt_ref == book_ref or not stmt_ref or not book_ref
            ):
                matched.append(
                    {
                        "statement": stmt,
                        "book": book,
                        "match_type": "automatic",
                        "match_score": _match_score(stmt, book),
                    }
                )
                used_book.add(idx)
                found = True
                break
        if not found:
            for idx, book in enumerate(book_items):
                if idx in used_book:
                    continue
                book_amount = round(float(book.get("amount", 0)), 2)
                if abs(stmt_amount - book_amount) <= amount_tolerance:
                    matched.append(
                        {
                            "statement": stmt,
                            "book": book,
                            "match_type": "automatic",
                            "match_score": 0.7,
                            "match_note": "amount_only",
                        }
                    )
                    used_book.add(idx)
                    found = True
                    break
        if not found:
            unmatched_stmt.append(stmt)

    unmatched_book = [b for i, b in enumerate(book_items) if i not in used_book]
    return matched, unmatched_stmt, unmatched_book


def analyze_differences(
    *,
    statement_items: list[dict],
    book_items: list[dict],
    unmatched_statement: list[dict],
    unmatched_book: list[dict],
) -> list[dict]:
    stmt_total = round(sum(float(i.get("amount", 0)) for i in statement_items), 2)
    book_total = round(sum(float(i.get("amount", 0)) for i in book_items), 2)
    diff = round(stmt_total - book_total, 2)
    analysis: list[dict] = [
        {
            "factor": "statement_total",
            "value": stmt_total,
            "impact": stmt_total,
        },
        {
            "factor": "book_total",
            "value": book_total,
            "impact": book_total,
        },
        {
            "factor": "net_difference",
            "value": diff,
            "impact": diff,
        },
    ]
    if unmatched_statement:
        analysis.append(
            {
                "factor": "unmatched_statement_items",
                "value": len(unmatched_statement),
                "impact": round(sum(float(i.get("amount", 0)) for i in unmatched_statement), 2),
            }
        )
    if unmatched_book:
        analysis.append(
            {
                "factor": "unmatched_book_items",
                "value": len(unmatched_book),
                "impact": round(sum(float(i.get("amount", 0)) for i in unmatched_book), 2),
            }
        )
    return analysis


def build_settlement_dashboard(
    *,
    batches: list[dict],
    reconciliations: list[dict],
    exceptions: list[dict],
    adjustments: list[dict],
    reports: list[dict],
) -> dict:
    by_status: dict[str, int] = {}
    by_type: dict[str, int] = {}
    total_settled = 0.0
    for b in batches:
        by_status[b.get("status", "unknown")] = by_status.get(b.get("status", "unknown"), 0) + 1
        by_type[b.get("settlement_type", "unknown")] = by_type.get(b.get("settlement_type", "unknown"), 0) + 1
        if b.get("status") == "completed":
            total_settled += float(b.get("total_amount", 0))

    open_exceptions = sum(1 for e in exceptions if e.get("status") in {"open", "retrying"})
    pending_adjustments = sum(1 for a in adjustments if a.get("status") == "pending_approval")
    recon_matched = sum(1 for r in reconciliations if r.get("status") == "matched")

    return {
        "batch_count": len(batches),
        "batches_by_status": by_status,
        "batches_by_type": by_type,
        "total_settled_amount": round(total_settled, 2),
        "reconciliation_count": len(reconciliations),
        "reconciliations_matched": recon_matched,
        "open_exceptions": open_exceptions,
        "pending_adjustments": pending_adjustments,
        "report_count": len(reports),
    }


def build_settlement_report(
    *,
    batches: list[dict],
    reconciliations: list[dict],
    exceptions: list[dict],
) -> dict:
    completed = [b for b in batches if b.get("status") == "completed"]
    failed = [b for b in batches if b.get("status") == "failed"]
    return {
        "completed_batches": len(completed),
        "failed_batches": len(failed),
        "total_settled": round(sum(float(b.get("total_amount", 0)) for b in completed), 2),
        "reconciliation_runs": len(reconciliations),
        "approved_reconciliations": sum(1 for r in reconciliations if r.get("status") == "approved"),
        "open_exceptions": sum(1 for e in exceptions if e.get("status") in {"open", "retrying", "escalated"}),
        "by_settlement_type": {
            t: sum(1 for b in batches if b.get("settlement_type") == t)
            for t in {b.get("settlement_type") for b in batches}
        },
    }
