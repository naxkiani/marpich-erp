"""Enterprise Bank Reconciliation aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class BankReconStatus(StrEnum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    MATCHED = "matched"
    PARTIAL_MATCH = "partial_match"
    EXCEPTION = "exception"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"


class MatchType(StrEnum):
    AUTOMATIC = "automatic"
    MANUAL = "manual"


class StatementImportSource(StrEnum):
    FILE_IMPORT = "file_import"
    BANK_API = "bank_api"
    MANUAL = "manual"


@dataclass(eq=False, kw_only=True)
class BankStatementImport(AggregateRoot):
    tenant_id: str
    treasury_account_id: str
    source: str
    statement_date: str
    statement_balance: float
    items: list[dict]
    status: str
    imported_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        treasury_account_id: str,
        source: str,
        statement_date: str,
        statement_balance: float,
        items: list[dict],
    ) -> BankStatementImport:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            treasury_account_id=treasury_account_id,
            source=source,
            statement_date=statement_date,
            statement_balance=round(statement_balance, 2),
            items=items,
            status="imported",
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "treasury_account_id": self.treasury_account_id,
            "source": self.source,
            "statement_date": self.statement_date,
            "statement_balance": self.statement_balance,
            "item_count": len(self.items),
            "items": self.items,
            "status": self.status,
            "imported_at": self.imported_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class EnterpriseBankReconciliation(AggregateRoot):
    tenant_id: str
    treasury_account_id: str
    statement_import_id: str | None
    reconciliation_date: str
    statement_balance: float
    book_balance: float
    matched_pairs: list[dict]
    unmatched_statement: list[dict]
    unmatched_book: list[dict]
    duplicates: list[dict]
    exceptions: list[dict]
    outstanding_transactions: list[dict]
    ai_suggestions: list[dict]
    report_summary: dict
    variance: float
    status: str
    approval_status: str
    submitted_by: str | None = None
    approved_by: str | None = None
    rejection_reason: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        treasury_account_id: str,
        reconciliation_date: str,
        statement_balance: float,
        book_balance: float,
        matched_pairs: list[dict],
        unmatched_statement: list[dict],
        unmatched_book: list[dict],
        duplicates: list[dict],
        exceptions: list[dict],
        outstanding_transactions: list[dict],
        ai_suggestions: list[dict],
        report_summary: dict,
        statement_import_id: str | None = None,
    ) -> EnterpriseBankReconciliation:
        variance = round(statement_balance - book_balance, 2)
        if matched_pairs and not unmatched_statement and not unmatched_book and abs(variance) < 0.01:
            status = BankReconStatus.MATCHED.value
        elif matched_pairs:
            status = BankReconStatus.PARTIAL_MATCH.value
        elif unmatched_statement or unmatched_book or abs(variance) >= 0.01:
            status = BankReconStatus.EXCEPTION.value
        else:
            status = BankReconStatus.IN_PROGRESS.value
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            treasury_account_id=treasury_account_id,
            statement_import_id=statement_import_id,
            reconciliation_date=reconciliation_date,
            statement_balance=round(statement_balance, 2),
            book_balance=round(book_balance, 2),
            matched_pairs=matched_pairs,
            unmatched_statement=unmatched_statement,
            unmatched_book=unmatched_book,
            duplicates=duplicates,
            exceptions=exceptions,
            outstanding_transactions=outstanding_transactions,
            ai_suggestions=ai_suggestions,
            report_summary=report_summary,
            variance=variance,
            status=status,
            approval_status="none",
        )

    def submit_for_approval(self, actor_id: str) -> None:
        if self.status not in (
            BankReconStatus.MATCHED.value,
            BankReconStatus.PARTIAL_MATCH.value,
            BankReconStatus.EXCEPTION.value,
        ):
            raise ValueError("cannot_submit")
        self.status = BankReconStatus.PENDING_APPROVAL.value
        self.approval_status = "pending"
        self.submitted_by = actor_id
        self.updated_at = datetime.now(UTC)

    def approve(self, actor_id: str) -> None:
        if self.status != BankReconStatus.PENDING_APPROVAL.value:
            raise ValueError("not_pending_approval")
        self.status = BankReconStatus.APPROVED.value
        self.approval_status = "approved"
        self.approved_by = actor_id
        self.updated_at = datetime.now(UTC)

    def reject(self, actor_id: str, reason: str = "") -> None:
        if self.status != BankReconStatus.PENDING_APPROVAL.value:
            raise ValueError("not_pending_approval")
        self.status = BankReconStatus.REJECTED.value
        self.approval_status = "rejected"
        self.approved_by = actor_id
        self.rejection_reason = reason
        self.updated_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "treasury_account_id": self.treasury_account_id,
            "statement_import_id": self.statement_import_id,
            "reconciliation_date": self.reconciliation_date,
            "statement_balance": self.statement_balance,
            "book_balance": self.book_balance,
            "matched_pairs": self.matched_pairs,
            "unmatched_statement": self.unmatched_statement,
            "unmatched_book": self.unmatched_book,
            "duplicates": self.duplicates,
            "exceptions": self.exceptions,
            "outstanding_transactions": self.outstanding_transactions,
            "ai_suggestions": self.ai_suggestions,
            "report_summary": self.report_summary,
            "variance": self.variance,
            "status": self.status,
            "approval_status": self.approval_status,
            "submitted_by": self.submitted_by,
            "approved_by": self.approved_by,
            "rejection_reason": self.rejection_reason,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class ReconciliationAuditEntry(AggregateRoot):
    tenant_id: str
    reconciliation_id: str
    action: str
    actor_id: str | None
    detail: str
    payload: dict = field(default_factory=dict)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        reconciliation_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
        payload: dict | None = None,
    ) -> ReconciliationAuditEntry:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            reconciliation_id=reconciliation_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
            payload=payload or {},
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "reconciliation_id": self.reconciliation_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "detail": self.detail,
            "payload": self.payload,
            "occurred_at": self.occurred_at.isoformat(),
        }
