"""Bank reconciliation aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class ReconciliationStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RECONCILED = "reconciled"
    DISCREPANCY = "discrepancy"


@dataclass(eq=False, kw_only=True)
class BankReconciliation(AggregateRoot):
    tenant_id: str
    treasury_account_id: str
    statement_date: str
    statement_balance: float
    book_balance: float
    matched_items: list[dict]
    unmatched_statement: list[dict]
    unmatched_book: list[dict]
    status: str
    variance: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        treasury_account_id: str,
        statement_date: str,
        statement_balance: float,
        book_balance: float,
        statement_items: list[dict],
        book_items: list[dict],
    ) -> BankReconciliation:
        matched, unmatched_stmt, unmatched_book = _match_items(statement_items, book_items)
        variance = round(statement_balance - book_balance, 2)
        status = (
            ReconciliationStatus.RECONCILED
            if variance == 0 and not unmatched_stmt and not unmatched_book
            else ReconciliationStatus.DISCREPANCY
            if variance != 0 or unmatched_stmt or unmatched_book
            else ReconciliationStatus.IN_PROGRESS
        )
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            treasury_account_id=treasury_account_id,
            statement_date=statement_date,
            statement_balance=round(statement_balance, 2),
            book_balance=round(book_balance, 2),
            matched_items=matched,
            unmatched_statement=unmatched_stmt,
            unmatched_book=unmatched_book,
            status=status,
            variance=variance,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "treasury_account_id": self.treasury_account_id,
            "statement_date": self.statement_date,
            "statement_balance": self.statement_balance,
            "book_balance": self.book_balance,
            "matched_items": self.matched_items,
            "unmatched_statement": self.unmatched_statement,
            "unmatched_book": self.unmatched_book,
            "status": self.status,
            "variance": self.variance,
            "created_at": self.created_at.isoformat(),
        }


def _match_items(
    statement_items: list[dict], book_items: list[dict]
) -> tuple[list[dict], list[dict], list[dict]]:
    matched: list[dict] = []
    used_book: set[int] = set()
    unmatched_stmt: list[dict] = []

    for stmt in statement_items:
        stmt_amount = round(float(stmt.get("amount", 0)), 2)
        stmt_ref = stmt.get("reference", "")
        found = False
        for idx, book in enumerate(book_items):
            if idx in used_book:
                continue
            book_amount = round(float(book.get("amount", 0)), 2)
            book_ref = book.get("reference", "")
            if stmt_amount == book_amount and (stmt_ref == book_ref or not stmt_ref or not book_ref):
                matched.append({"statement": stmt, "book": book})
                used_book.add(idx)
                found = True
                break
        if not found:
            unmatched_stmt.append(stmt)

    unmatched_book = [b for i, b in enumerate(book_items) if i not in used_book]
    return matched, unmatched_stmt, unmatched_book
