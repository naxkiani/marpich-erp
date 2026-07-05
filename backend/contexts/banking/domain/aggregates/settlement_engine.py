"""Banking Settlement Engine aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class SettlementType(StrEnum):
    INTERNAL = "internal_settlement"
    INTERBANK = "interbank_settlement"
    CLEARING = "clearing"


class SettlementStatus(StrEnum):
    DRAFT = "draft"
    PENDING_CLEARING = "pending_clearing"
    CLEARING = "clearing"
    CLEARED = "cleared"
    PENDING_SETTLEMENT = "pending_settlement"
    SETTLING = "settling"
    COMPLETED = "completed"
    FAILED = "failed"
    EXCEPTION = "exception"


class ReconciliationStatus(StrEnum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    MATCHED = "matched"
    PARTIAL_MATCH = "partial_match"
    EXCEPTION = "exception"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"


class ExceptionStatus(StrEnum):
    OPEN = "open"
    RETRYING = "retrying"
    RESOLVED = "resolved"
    ESCALATED = "escalated"


class AdjustmentStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    POSTED = "posted"


@dataclass(eq=False, kw_only=True)
class SettlementBatch(AggregateRoot):
    tenant_id: str
    batch_ref: str
    settlement_type: str
    status: str = SettlementStatus.DRAFT.value
    currency: str = "USD"
    total_amount: float = 0.0
    item_count: int = 0
    clearing_ref: str = ""
    journal_id: str | None = None
    failure_reason: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    cleared_at: datetime | None = None
    settled_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        batch_ref: str,
        settlement_type: str,
        currency: str = "USD",
    ) -> SettlementBatch:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            batch_ref=batch_ref,
            settlement_type=settlement_type,
            currency=currency,
        )

    def add_items(self, *, count: int, total_amount: float) -> None:
        self.item_count = count
        self.total_amount = round(total_amount, 2)

    def submit(self) -> None:
        if self.status != SettlementStatus.DRAFT.value:
            raise ValueError("not_draft")
        if self.item_count == 0:
            raise ValueError("empty_batch")
        if self.settlement_type == SettlementType.CLEARING.value:
            self.status = SettlementStatus.PENDING_CLEARING.value
        else:
            self.status = SettlementStatus.PENDING_SETTLEMENT.value

    def start_clearing(self) -> None:
        if self.status != SettlementStatus.PENDING_CLEARING.value:
            raise ValueError("not_pending_clearing")
        self.status = SettlementStatus.CLEARING.value

    def complete_clearing(self, clearing_ref: str) -> None:
        if self.status != SettlementStatus.CLEARING.value:
            raise ValueError("not_clearing")
        self.clearing_ref = clearing_ref
        self.cleared_at = datetime.now(UTC)
        self.status = SettlementStatus.CLEARED.value

    def start_settlement(self) -> None:
        allowed = {
            SettlementStatus.PENDING_SETTLEMENT.value,
            SettlementStatus.CLEARED.value,
        }
        if self.status not in allowed:
            raise ValueError("cannot_settle")
        self.status = SettlementStatus.SETTLING.value

    def complete(self, journal_id: str | None = None) -> None:
        if self.status != SettlementStatus.SETTLING.value:
            raise ValueError("not_settling")
        self.journal_id = journal_id
        self.settled_at = datetime.now(UTC)
        self.status = SettlementStatus.COMPLETED.value

    def fail(self, reason: str) -> None:
        self.failure_reason = reason
        self.status = SettlementStatus.FAILED.value

    def mark_exception(self) -> None:
        self.status = SettlementStatus.EXCEPTION.value

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "batch_ref": self.batch_ref,
            "settlement_type": self.settlement_type,
            "status": self.status,
            "currency": self.currency,
            "total_amount": self.total_amount,
            "item_count": self.item_count,
            "clearing_ref": self.clearing_ref,
            "journal_id": self.journal_id,
            "failure_reason": self.failure_reason,
            "created_at": self.created_at.isoformat(),
            "cleared_at": self.cleared_at.isoformat() if self.cleared_at else None,
            "settled_at": self.settled_at.isoformat() if self.settled_at else None,
        }


@dataclass(eq=False, kw_only=True)
class SettlementItem(AggregateRoot):
    tenant_id: str
    batch_id: str
    item_ref: str
    source_ref: str
    amount: float
    currency: str = "USD"
    counterparty: str = ""
    narrative: str = ""
    status: str = "pending"
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        batch_id: str,
        item_ref: str,
        source_ref: str,
        amount: float,
        currency: str = "USD",
        counterparty: str = "",
        narrative: str = "",
    ) -> SettlementItem:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            batch_id=batch_id,
            item_ref=item_ref,
            source_ref=source_ref,
            amount=round(amount, 2),
            currency=currency,
            counterparty=counterparty,
            narrative=narrative,
        )

    def settle(self) -> None:
        self.status = "settled"

    def fail(self) -> None:
        self.status = "failed"

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "batch_id": self.batch_id,
            "item_ref": self.item_ref,
            "source_ref": self.source_ref,
            "amount": self.amount,
            "currency": self.currency,
            "counterparty": self.counterparty,
            "narrative": self.narrative,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class BankReconciliationRun(AggregateRoot):
    tenant_id: str
    run_ref: str
    status: str = ReconciliationStatus.DRAFT.value
    settlement_account: str = ""
    statement_items: list[dict] = field(default_factory=list)
    book_items: list[dict] = field(default_factory=list)
    matched_count: int = 0
    unmatched_statement_count: int = 0
    unmatched_book_count: int = 0
    difference_amount: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    completed_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        run_ref: str,
        settlement_account: str = "",
        statement_items: list[dict] | None = None,
        book_items: list[dict] | None = None,
    ) -> BankReconciliationRun:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            run_ref=run_ref,
            settlement_account=settlement_account,
            statement_items=list(statement_items or []),
            book_items=list(book_items or []),
        )

    def start(self) -> None:
        if self.status != ReconciliationStatus.DRAFT.value:
            raise ValueError("not_draft")
        self.status = ReconciliationStatus.IN_PROGRESS.value

    def apply_match_results(
        self,
        *,
        matched_count: int,
        unmatched_stmt: int,
        unmatched_book: int,
        difference_amount: float,
    ) -> None:
        self.matched_count = matched_count
        self.unmatched_statement_count = unmatched_stmt
        self.unmatched_book_count = unmatched_book
        self.difference_amount = round(difference_amount, 2)
        if unmatched_stmt == 0 and unmatched_book == 0:
            self.status = ReconciliationStatus.MATCHED.value
        elif matched_count > 0:
            self.status = ReconciliationStatus.PARTIAL_MATCH.value
        else:
            self.status = ReconciliationStatus.EXCEPTION.value

    def request_approval(self) -> None:
        allowed = {
            ReconciliationStatus.MATCHED.value,
            ReconciliationStatus.PARTIAL_MATCH.value,
            ReconciliationStatus.EXCEPTION.value,
        }
        if self.status not in allowed:
            raise ValueError("cannot_request_approval")
        self.status = ReconciliationStatus.PENDING_APPROVAL.value

    def approve(self) -> None:
        if self.status != ReconciliationStatus.PENDING_APPROVAL.value:
            raise ValueError("not_pending_approval")
        self.status = ReconciliationStatus.APPROVED.value
        self.completed_at = datetime.now(UTC)

    def reject(self) -> None:
        if self.status != ReconciliationStatus.PENDING_APPROVAL.value:
            raise ValueError("not_pending_approval")
        self.status = ReconciliationStatus.REJECTED.value

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "run_ref": self.run_ref,
            "status": self.status,
            "settlement_account": self.settlement_account,
            "statement_item_count": len(self.statement_items),
            "book_item_count": len(self.book_items),
            "matched_count": self.matched_count,
            "unmatched_statement_count": self.unmatched_statement_count,
            "unmatched_book_count": self.unmatched_book_count,
            "difference_amount": self.difference_amount,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


@dataclass(eq=False, kw_only=True)
class ReconciliationMatch(AggregateRoot):
    tenant_id: str
    run_id: str
    statement_item: dict
    book_item: dict
    match_type: str
    match_score: float
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        run_id: str,
        statement_item: dict,
        book_item: dict,
        match_type: str,
        match_score: float,
    ) -> ReconciliationMatch:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            run_id=run_id,
            statement_item=statement_item,
            book_item=book_item,
            match_type=match_type,
            match_score=match_score,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "run_id": self.run_id,
            "statement_item": self.statement_item,
            "book_item": self.book_item,
            "match_type": self.match_type,
            "match_score": self.match_score,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class SettlementException(AggregateRoot):
    tenant_id: str
    exception_ref: str
    source_type: str
    source_id: str
    reason: str
    status: str = ExceptionStatus.OPEN.value
    retry_count: int = 0
    max_retries: int = 3
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    resolved_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        exception_ref: str,
        source_type: str,
        source_id: str,
        reason: str,
        max_retries: int = 3,
    ) -> SettlementException:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            exception_ref=exception_ref,
            source_type=source_type,
            source_id=source_id,
            reason=reason,
            max_retries=max_retries,
        )

    def retry(self) -> None:
        if self.status not in {ExceptionStatus.OPEN.value, ExceptionStatus.RETRYING.value}:
            raise ValueError("cannot_retry")
        if self.retry_count >= self.max_retries:
            self.status = ExceptionStatus.ESCALATED.value
            raise ValueError("max_retries_exceeded")
        self.retry_count += 1
        self.status = ExceptionStatus.RETRYING.value

    def resolve(self) -> None:
        self.status = ExceptionStatus.RESOLVED.value
        self.resolved_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "exception_ref": self.exception_ref,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "reason": self.reason,
            "status": self.status,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "created_at": self.created_at.isoformat(),
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
        }


@dataclass(eq=False, kw_only=True)
class SettlementDifference(AggregateRoot):
    tenant_id: str
    run_id: str
    difference_ref: str
    statement_total: float
    book_total: float
    difference_amount: float
    unmatched_statement: list[dict] = field(default_factory=list)
    unmatched_book: list[dict] = field(default_factory=list)
    analysis: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        run_id: str,
        difference_ref: str,
        statement_total: float,
        book_total: float,
        difference_amount: float,
        unmatched_statement: list[dict],
        unmatched_book: list[dict],
        analysis: list[dict],
    ) -> SettlementDifference:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            run_id=run_id,
            difference_ref=difference_ref,
            statement_total=round(statement_total, 2),
            book_total=round(book_total, 2),
            difference_amount=round(difference_amount, 2),
            unmatched_statement=unmatched_statement,
            unmatched_book=unmatched_book,
            analysis=analysis,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "run_id": self.run_id,
            "difference_ref": self.difference_ref,
            "statement_total": self.statement_total,
            "book_total": self.book_total,
            "difference_amount": self.difference_amount,
            "unmatched_statement": self.unmatched_statement,
            "unmatched_book": self.unmatched_book,
            "analysis": self.analysis,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class SettlementAdjustment(AggregateRoot):
    tenant_id: str
    adjustment_ref: str
    run_id: str
    amount: float
    currency: str = "USD"
    reason: str = ""
    status: str = AdjustmentStatus.DRAFT.value
    approver_id: str | None = None
    journal_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        adjustment_ref: str,
        run_id: str,
        amount: float,
        currency: str = "USD",
        reason: str = "",
    ) -> SettlementAdjustment:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            adjustment_ref=adjustment_ref,
            run_id=run_id,
            amount=round(amount, 2),
            currency=currency,
            reason=reason,
        )

    def submit(self) -> None:
        if self.status != AdjustmentStatus.DRAFT.value:
            raise ValueError("not_draft")
        self.status = AdjustmentStatus.PENDING_APPROVAL.value

    def approve(self, approver_id: str) -> None:
        if self.status != AdjustmentStatus.PENDING_APPROVAL.value:
            raise ValueError("not_pending_approval")
        self.approver_id = approver_id
        self.status = AdjustmentStatus.APPROVED.value

    def reject(self) -> None:
        if self.status != AdjustmentStatus.PENDING_APPROVAL.value:
            raise ValueError("not_pending_approval")
        self.status = AdjustmentStatus.REJECTED.value

    def post(self, journal_id: str | None = None) -> None:
        if self.status != AdjustmentStatus.APPROVED.value:
            raise ValueError("not_approved")
        self.journal_id = journal_id
        self.status = AdjustmentStatus.POSTED.value

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "adjustment_ref": self.adjustment_ref,
            "run_id": self.run_id,
            "amount": self.amount,
            "currency": self.currency,
            "reason": self.reason,
            "status": self.status,
            "approver_id": self.approver_id,
            "journal_id": self.journal_id,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class SettlementAuditEntry(AggregateRoot):
    tenant_id: str
    source_type: str
    source_id: str
    action: str
    actor_id: str | None = None
    detail: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        source_type: str,
        source_id: str,
        action: str,
        actor_id: str | None = None,
        detail: str = "",
    ) -> SettlementAuditEntry:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            source_type=source_type,
            source_id=source_id,
            action=action,
            actor_id=actor_id,
            detail=detail,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "action": self.action,
            "actor_id": self.actor_id,
            "detail": self.detail,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class SettlementReport(AggregateRoot):
    tenant_id: str
    report_ref: str
    report_type: str
    summary: dict
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        report_ref: str,
        report_type: str,
        summary: dict,
    ) -> SettlementReport:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            report_ref=report_ref,
            report_type=report_type,
            summary=summary,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "report_ref": self.report_ref,
            "report_type": self.report_type,
            "summary": self.summary,
            "created_at": self.created_at.isoformat(),
        }
