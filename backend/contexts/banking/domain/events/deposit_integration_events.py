"""Deposit Management integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class BankingDepositPostedIntegration(IntegrationEvent):
    account_id: str
    deposit_id: str
    transaction_id: str
    transaction_ref: str
    amount: float
    currency: str
    gl_account_code: str | None
    account_number: str = ""

    @property
    def event_name(self) -> str:
        return "banking.deposit.posted"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "account_id": self.account_id,
            "deposit_id": self.deposit_id,
            "transaction_id": self.transaction_id,
            "transaction_ref": self.transaction_ref,
            "amount": self.amount,
            "currency": self.currency,
            "gl_account_code": self.gl_account_code,
            "account_number": self.account_number,
        }


@dataclass(frozen=True, kw_only=True)
class BankingWithdrawalPostedIntegration(IntegrationEvent):
    account_id: str
    deposit_id: str
    transaction_id: str
    transaction_ref: str
    amount: float
    currency: str
    gl_account_code: str | None
    penalty_amount: float = 0.0

    @property
    def event_name(self) -> str:
        return "banking.withdrawal.posted"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "account_id": self.account_id,
            "deposit_id": self.deposit_id,
            "transaction_id": self.transaction_id,
            "transaction_ref": self.transaction_ref,
            "amount": self.amount,
            "currency": self.currency,
            "gl_account_code": self.gl_account_code,
            "penalty_amount": self.penalty_amount,
        }


@dataclass(frozen=True, kw_only=True)
class BankingInterestAccruedIntegration(IntegrationEvent):
    deposit_id: str
    accrual_id: str
    accrual_ref: str
    accrued_amount: float
    currency: str
    gl_account_code: str | None

    @property
    def event_name(self) -> str:
        return "banking.interest.accrued"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "deposit_id": self.deposit_id,
            "accrual_id": self.accrual_id,
            "accrual_ref": self.accrual_ref,
            "accrued_amount": self.accrued_amount,
            "currency": self.currency,
            "gl_account_code": self.gl_account_code,
        }


@dataclass(frozen=True, kw_only=True)
class BankingDepositMaturedIntegration(IntegrationEvent):
    deposit_id: str
    account_id: str
    principal: float
    auto_renew: bool

    @property
    def event_name(self) -> str:
        return "banking.deposit.matured"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "deposit_id": self.deposit_id,
            "account_id": self.account_id,
            "principal": self.principal,
            "auto_renew": self.auto_renew,
        }
