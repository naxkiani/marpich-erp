"""Banking Payment Platform integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class BankingTransferPostedIntegration(IntegrationEvent):
    transfer_id: str
    transfer_ref: str
    transfer_type: str
    source_account_id: str
    destination_account_id: str | None
    amount: float
    currency: str
    source_gl_code: str | None
    destination_gl_code: str | None

    @property
    def event_name(self) -> str:
        return "banking.transfer.posted"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "transfer_id": self.transfer_id,
            "transfer_ref": self.transfer_ref,
            "transfer_type": self.transfer_type,
            "source_account_id": self.source_account_id,
            "destination_account_id": self.destination_account_id,
            "amount": self.amount,
            "currency": self.currency,
            "source_gl_code": self.source_gl_code,
            "destination_gl_code": self.destination_gl_code,
        }


@dataclass(frozen=True, kw_only=True)
class BankingTransactionPostedIntegration(IntegrationEvent):
    transfer_id: str
    transfer_ref: str
    transfer_type: str
    amount: float
    currency: str
    channel: str

    @property
    def event_name(self) -> str:
        return "banking.transaction.posted"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "transfer_id": self.transfer_id,
            "transfer_ref": self.transfer_ref,
            "transfer_type": self.transfer_type,
            "amount": self.amount,
            "currency": self.currency,
            "channel": self.channel,
        }


@dataclass(frozen=True, kw_only=True)
class BankingPaymentFraudFlaggedIntegration(IntegrationEvent):
    transfer_id: str
    fraud_check_id: str
    risk_score: float
    status: str

    @property
    def event_name(self) -> str:
        return "banking.payment.fraud.flagged"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "transfer_id": self.transfer_id,
            "fraud_check_id": self.fraud_check_id,
            "risk_score": self.risk_score,
            "status": self.status,
        }
