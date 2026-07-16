"""Banking Settlement Engine integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class BankingSettlementPostedIntegration(IntegrationEvent):
    batch_id: str
    batch_ref: str
    settlement_type: str
    amount: float
    currency: str
    debit_gl_code: str | None
    credit_gl_code: str | None

    @property
    def event_name(self) -> str:
        return "banking.settlement.posted"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "batch_id": self.batch_id,
            "batch_ref": self.batch_ref,
            "settlement_type": self.settlement_type,
            "amount": self.amount,
            "currency": self.currency,
            "debit_gl_code": self.debit_gl_code,
            "credit_gl_code": self.credit_gl_code,
        }


@dataclass(frozen=True, kw_only=True)
class BankingReconciliationCompletedIntegration(IntegrationEvent):
    run_id: str
    run_ref: str
    status: str
    matched_count: int
    difference_amount: float

    @property
    def event_name(self) -> str:
        return "banking.reconciliation.completed"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "run_id": self.run_id,
            "run_ref": self.run_ref,
            "status": self.status,
            "matched_count": self.matched_count,
            "difference_amount": self.difference_amount,
        }


@dataclass(frozen=True, kw_only=True)
class BankingSettlementExceptionRaisedIntegration(IntegrationEvent):
    exception_id: str
    exception_ref: str
    source_type: str
    source_id: str
    reason: str

    @property
    def event_name(self) -> str:
        return "banking.settlement.exception.raised"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "exception_id": self.exception_id,
            "exception_ref": self.exception_ref,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "reason": self.reason,
        }
