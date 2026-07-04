"""Immutable General Ledger journal entry."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class PostingMode(StrEnum):
    AUTOMATIC = "automatic"
    MANUAL = "manual"
    RECURRING = "recurring"
    REVERSING = "reversing"


class JournalStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    POSTED = "posted"
    REVERSED = "reversed"
    REJECTED = "rejected"


@dataclass(eq=False, kw_only=True)
class Journal(AggregateRoot):
    tenant_id: str
    organization_id: str | None
    branch_id: str | None
    fiscal_year_id: str | None
    period_id: str | None
    source_context: str
    source_document_id: str
    idempotency_key: str
    currency: str
    base_currency: str
    exchange_rate: float
    lines: list[dict]
    posting_mode: str
    status: str
    reporting_currency: str = ""
    reporting_exchange_rate: float = 1.0
    rate_snapshot_id: str | None = None
    rate_type: str = "spot"
    correlation_id: str = ""
    reverses_journal_id: str | None = None
    reversed_by_journal_id: str | None = None
    recurring_template_id: str | None = None
    immutable_hash: str = ""
    posted_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create_draft(
        cls,
        *,
        tenant_id: str,
        organization_id: str | None,
        branch_id: str | None,
        fiscal_year_id: str | None,
        period_id: str | None,
        source_context: str,
        source_document_id: str,
        idempotency_key: str,
        currency: str,
        base_currency: str,
        exchange_rate: float,
        lines: list[dict],
        posting_mode: str,
        correlation_id: str,
        reporting_currency: str = "",
        reporting_exchange_rate: float = 1.0,
        rate_snapshot_id: str | None = None,
        rate_type: str = "spot",
        recurring_template_id: str | None = None,
        reverses_journal_id: str | None = None,
    ) -> Journal:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            organization_id=organization_id,
            branch_id=branch_id,
            fiscal_year_id=fiscal_year_id,
            period_id=period_id,
            source_context=source_context,
            source_document_id=source_document_id,
            idempotency_key=idempotency_key,
            currency=currency,
            base_currency=base_currency,
            exchange_rate=exchange_rate,
            reporting_currency=reporting_currency or base_currency,
            reporting_exchange_rate=reporting_exchange_rate,
            rate_snapshot_id=rate_snapshot_id,
            rate_type=rate_type,
            lines=lines,
            posting_mode=posting_mode,
            status=JournalStatus.DRAFT if posting_mode == PostingMode.MANUAL else JournalStatus.POSTED,
            correlation_id=correlation_id,
            recurring_template_id=recurring_template_id,
            reverses_journal_id=reverses_journal_id,
            posted_at=None if posting_mode == PostingMode.MANUAL else datetime.now(UTC),
        )

    def submit_for_approval(self) -> None:
        if self.status != JournalStatus.DRAFT:
            raise ValueError("Only draft journals can be submitted")
        self.status = JournalStatus.PENDING_APPROVAL

    def approve_and_post(self) -> None:
        if self.status != JournalStatus.PENDING_APPROVAL:
            raise ValueError("Only pending journals can be approved")
        self.status = JournalStatus.POSTED
        self.posted_at = datetime.now(UTC)
        self.immutable_hash = self._compute_hash()

    def mark_posted(self) -> None:
        self.status = JournalStatus.POSTED
        self.posted_at = datetime.now(UTC)
        self.immutable_hash = self._compute_hash()

    def mark_reversed(self, reversal_journal_id: str) -> None:
        if self.status != JournalStatus.POSTED:
            raise ValueError("Only posted journals can be reversed")
        self.status = JournalStatus.REVERSED
        self.reversed_by_journal_id = reversal_journal_id

    def _compute_hash(self) -> str:
        import hashlib
        payload = f"{self.tenant_id}:{self.id}:{self.lines}:{self.posted_at}"
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    @property
    def is_immutable(self) -> bool:
        return self.status in (JournalStatus.POSTED, JournalStatus.REVERSED)

    @property
    def total_debits(self) -> float:
        return round(sum(float(line.get("debit", 0)) for line in self.lines), 2)

    @property
    def total_credits(self) -> float:
        return round(sum(float(line.get("credit", 0)) for line in self.lines), 2)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "organization_id": self.organization_id,
            "branch_id": self.branch_id,
            "fiscal_year_id": self.fiscal_year_id,
            "period_id": self.period_id,
            "source_context": self.source_context,
            "source_document_id": self.source_document_id,
            "idempotency_key": self.idempotency_key,
            "currency": self.currency,
            "base_currency": self.base_currency,
            "exchange_rate": self.exchange_rate,
            "reporting_currency": self.reporting_currency,
            "reporting_exchange_rate": self.reporting_exchange_rate,
            "rate_snapshot_id": self.rate_snapshot_id,
            "rate_type": self.rate_type,
            "lines": self.lines,
            "posting_mode": self.posting_mode,
            "status": self.status,
            "total_debits": self.total_debits,
            "total_credits": self.total_credits,
            "reverses_journal_id": self.reverses_journal_id,
            "reversed_by_journal_id": self.reversed_by_journal_id,
            "recurring_template_id": self.recurring_template_id,
            "immutable_hash": self.immutable_hash,
            "is_immutable": self.is_immutable,
            "correlation_id": self.correlation_id,
            "posted_at": self.posted_at.isoformat() if self.posted_at else None,
            "created_at": self.created_at.isoformat(),
        }
