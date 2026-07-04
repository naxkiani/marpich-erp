"""General ledger journal entry — Finance local model."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


@dataclass(eq=False, kw_only=True)
class JournalEntry(AggregateRoot):
    tenant_id: str
    external_journal_id: str
    source_type: str
    source_id: str
    currency: str
    lines: list[dict]
    correlation_id: str = ""
    posted_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def from_accounting_event(
        cls,
        *,
        tenant_id: str,
        correlation_id: str,
        external_journal_id: str,
        source_type: str,
        source_id: str,
        currency: str,
        lines: list[dict],
    ) -> JournalEntry:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            external_journal_id=external_journal_id,
            source_type=source_type,
            source_id=source_id,
            currency=currency,
            lines=lines,
            correlation_id=correlation_id,
        )

    @property
    def total_debits(self) -> float:
        return round(sum(line.get("debit", 0.0) for line in self.lines), 2)

    @property
    def total_credits(self) -> float:
        return round(sum(line.get("credit", 0.0) for line in self.lines), 2)

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "external_journal_id": self.external_journal_id,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "currency": self.currency,
            "lines": self.lines,
            "total_debits": self.total_debits,
            "total_credits": self.total_credits,
            "correlation_id": self.correlation_id,
            "posted_at": self.posted_at.isoformat(),
        }
