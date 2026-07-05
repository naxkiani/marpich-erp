"""Enterprise Bank Reconciliation Engine."""
from __future__ import annotations

from contexts.treasury.domain.aggregates.bank_reconciliation_engine import BankReconStatus

BANK_RECONCILIATION_CATALOG: dict[str, dict] = {
    "automatic_matching": {"label": "Automatic Matching", "supported": True},
    "manual_matching": {"label": "Manual Matching", "supported": True},
    "statement_import": {"label": "Statement Import", "sources": ["file_import", "manual"]},
    "bank_api_integration": {"label": "Bank API Integration", "source": "bank_api"},
    "duplicate_detection": {"label": "Duplicate Detection", "supported": True},
    "exception_queue": {"label": "Exception Queue", "supported": True},
    "outstanding_transactions": {"label": "Outstanding Transactions", "supported": True},
    "ai_matching_suggestions": {"label": "AI Matching Suggestions", "autonomous_execution": False},
    "reconciliation_workflow": {"label": "Reconciliation Workflow", "supported": True},
    "reconciliation_reports": {"label": "Reconciliation Reports", "supported": True},
    "reconciliation_audit": {"label": "Reconciliation Audit", "supported": True},
}

WORKFLOW_TRANSITIONS: dict[str, list[str]] = {
    BankReconStatus.DRAFT.value: [BankReconStatus.IN_PROGRESS.value],
    BankReconStatus.IN_PROGRESS.value: [
        BankReconStatus.MATCHED.value,
        BankReconStatus.PARTIAL_MATCH.value,
        BankReconStatus.EXCEPTION.value,
    ],
    BankReconStatus.MATCHED.value: [BankReconStatus.PENDING_APPROVAL.value],
    BankReconStatus.PARTIAL_MATCH.value: [BankReconStatus.PENDING_APPROVAL.value],
    BankReconStatus.EXCEPTION.value: [BankReconStatus.PENDING_APPROVAL.value],
    BankReconStatus.PENDING_APPROVAL.value: [
        BankReconStatus.APPROVED.value,
        BankReconStatus.REJECTED.value,
    ],
}


def list_bank_reconciliation_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in BANK_RECONCILIATION_CATALOG.items()]


def list_workflow_states() -> list[dict]:
    terminal = [BankReconStatus.APPROVED.value, BankReconStatus.REJECTED.value]
    states = [
        {"status": s, "allowed_transitions": t} for s, t in WORKFLOW_TRANSITIONS.items()
    ]
    states.extend({"status": s, "allowed_transitions": []} for s in terminal)
    return states


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


def manual_match(
    *,
    matched_pairs: list[dict],
    unmatched_statement: list[dict],
    unmatched_book: list[dict],
    statement_item: dict,
    book_item: dict,
    actor_id: str,
) -> tuple[list[dict], list[dict], list[dict]]:
    pairs = list(matched_pairs)
    stmt = list(unmatched_statement)
    book = list(unmatched_book)
    pairs.append(
        {
            "statement": statement_item,
            "book": book_item,
            "match_type": "manual",
            "matched_by": actor_id,
            "match_score": 1.0,
        }
    )
    stmt = [s for s in stmt if s != statement_item]
    book = [b for b in book if b != book_item]
    return pairs, stmt, book


def detect_duplicates(items: list[dict], *, side: str) -> list[dict]:
    seen: dict[str, int] = {}
    duplicates: list[dict] = []
    for item in items:
        key = f"{_normalize_ref(item)}:{round(float(item.get('amount', 0)), 2)}"
        if key in seen:
            duplicates.append(
                {
                    "side": side,
                    "item": item,
                    "duplicate_of_index": seen[key],
                    "reason": "duplicate_reference_amount",
                }
            )
        else:
            seen[key] = len(seen)
    return duplicates


def build_exception_queue(
    *,
    unmatched_statement: list[dict],
    unmatched_book: list[dict],
    variance: float,
    duplicates: list[dict],
) -> list[dict]:
    exceptions: list[dict] = []
    for item in unmatched_statement:
        exceptions.append(
            {
                "side": "statement",
                "item": item,
                "reason": "unmatched_statement_item",
                "amount": item.get("amount", 0),
                "reference": item.get("reference", ""),
            }
        )
    for item in unmatched_book:
        exceptions.append(
            {
                "side": "book",
                "item": item,
                "reason": "unmatched_book_item",
                "amount": item.get("amount", 0),
                "reference": item.get("reference", ""),
            }
        )
    for dup in duplicates:
        exceptions.append(
            {
                "side": dup["side"],
                "reason": "duplicate_detected",
                "item": dup["item"],
            }
        )
    if abs(variance) >= 0.01:
        exceptions.append(
            {"side": "balance", "reason": "variance_detected", "variance": variance}
        )
    return exceptions


def build_outstanding_transactions(
    unmatched_statement: list[dict],
    unmatched_book: list[dict],
) -> list[dict]:
    outstanding: list[dict] = []
    for item in unmatched_statement:
        outstanding.append(
            {
                "source": "statement",
                "reference": item.get("reference", ""),
                "amount": item.get("amount", 0),
                "date": item.get("date", ""),
                "status": "outstanding",
            }
        )
    for item in unmatched_book:
        outstanding.append(
            {
                "source": "book",
                "reference": item.get("reference", ""),
                "amount": item.get("amount", 0),
                "date": item.get("date", ""),
                "status": "outstanding",
            }
        )
    return outstanding


def generate_ai_matching_suggestions(
    *,
    unmatched_statement: list[dict],
    unmatched_book: list[dict],
    variance: float,
    match_rate: float,
) -> list[dict]:
    suggestions: list[dict] = []
    if abs(variance) >= 0.01:
        suggestions.append(
            {
                "priority": "high",
                "category": "variance",
                "message": f"Balance variance of {variance} requires review.",
                "action": "review_exceptions",
                "autonomous_execution": False,
            }
        )
    for stmt in unmatched_statement[:3]:
        stmt_amt = float(stmt.get("amount", 0))
        for book in unmatched_book[:5]:
            book_amt = float(book.get("amount", 0))
            if abs(stmt_amt - book_amt) <= max(abs(stmt_amt) * 0.05, 1.0):
                suggestions.append(
                    {
                        "priority": "medium",
                        "category": "near_match",
                        "message": "Potential manual match — similar amounts.",
                        "statement_item": stmt,
                        "book_item": book,
                        "action": "manual_match",
                        "confidence": 0.75,
                        "autonomous_execution": False,
                    }
                )
                break
    if match_rate < 0.8:
        suggestions.append(
            {
                "priority": "medium",
                "category": "low_match_rate",
                "message": f"Match rate {match_rate:.0%} below 80%; normalize references.",
                "action": "normalize_references",
                "autonomous_execution": False,
            }
        )
    if not suggestions:
        suggestions.append(
            {
                "priority": "low",
                "category": "ready",
                "message": "Reconciliation balanced; submit for approval.",
                "action": "submit_for_approval",
                "autonomous_execution": False,
            }
        )
    return suggestions


def build_reconciliation_report(
    *,
    reconciliation_date: str,
    treasury_account_id: str,
    statement_balance: float,
    book_balance: float,
    matched_pairs: list[dict],
    exceptions: list[dict],
    outstanding: list[dict],
    status: str,
    variance: float,
) -> dict:
    match_rate = round(
        len(matched_pairs) / max(len(matched_pairs) + len(exceptions), 1), 4
    )
    return {
        "reconciliation_date": reconciliation_date,
        "treasury_account_id": treasury_account_id,
        "statement_balance": statement_balance,
        "book_balance": book_balance,
        "variance": variance,
        "balanced": abs(variance) < 0.01,
        "status": status,
        "matched_count": len(matched_pairs),
        "exception_count": len(exceptions),
        "outstanding_count": len(outstanding),
        "match_rate": match_rate,
        "ready_for_approval": status in (
            BankReconStatus.MATCHED.value,
            BankReconStatus.PARTIAL_MATCH.value,
        )
        and abs(variance) < 0.01,
        "sections": [
            {"name": "matched", "count": len(matched_pairs)},
            {"name": "exceptions", "count": len(exceptions)},
            {"name": "outstanding", "count": len(outstanding)},
        ],
    }


def run_reconciliation(
    *,
    statement_items: list[dict],
    book_items: list[dict],
    statement_balance: float,
    book_balance: float,
) -> dict:
    matched, unmatched_stmt, unmatched_book = automatic_match(statement_items, book_items)
    stmt_dups = detect_duplicates(statement_items, side="statement")
    book_dups = detect_duplicates(book_items, side="book")
    duplicates = stmt_dups + book_dups
    variance = round(statement_balance - book_balance, 2)
    exceptions = build_exception_queue(
        unmatched_statement=unmatched_stmt,
        unmatched_book=unmatched_book,
        variance=variance,
        duplicates=duplicates,
    )
    outstanding = build_outstanding_transactions(unmatched_stmt, unmatched_book)
    match_rate = round(
        len(matched) / max(len(matched) + len(unmatched_stmt) + len(unmatched_book), 1),
        4,
    )
    ai_suggestions = generate_ai_matching_suggestions(
        unmatched_statement=unmatched_stmt,
        unmatched_book=unmatched_book,
        variance=variance,
        match_rate=match_rate,
    )
    return {
        "matched_pairs": matched,
        "unmatched_statement": unmatched_stmt,
        "unmatched_book": unmatched_book,
        "duplicates": duplicates,
        "exceptions": exceptions,
        "outstanding_transactions": outstanding,
        "ai_suggestions": ai_suggestions,
        "variance": variance,
        "match_rate": match_rate,
    }


def build_reconciliation_dashboard(*, reconciliations: list[dict]) -> dict:
    by_status: dict[str, int] = {}
    open_exceptions = 0
    for r in reconciliations:
        status = r.get("status", "unknown")
        by_status[status] = by_status.get(status, 0) + 1
        if status in (BankReconStatus.EXCEPTION.value, BankReconStatus.PARTIAL_MATCH.value):
            open_exceptions += len(r.get("exceptions", []))

    return {
        "summary": {
            "reconciliation_count": len(reconciliations),
            "open_exceptions": open_exceptions,
            "pending_approval": by_status.get(BankReconStatus.PENDING_APPROVAL.value, 0),
            "approved": by_status.get(BankReconStatus.APPROVED.value, 0),
        },
        "by_status": by_status,
        "recent_reconciliations": reconciliations[:10],
        "workflow_states": list_workflow_states(),
    }
