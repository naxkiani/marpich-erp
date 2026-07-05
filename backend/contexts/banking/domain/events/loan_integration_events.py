"""Loan Management integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class BankingLoanDisbursedIntegration(IntegrationEvent):
    account_id: str
    loan_id: str
    transaction_id: str
    transaction_ref: str
    amount: float
    currency: str
    gl_account_code: str | None
    account_number: str = ""

    @property
    def event_name(self) -> str:
        return "banking.loan.disbursed"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "account_id": self.account_id,
            "loan_id": self.loan_id,
            "transaction_id": self.transaction_id,
            "transaction_ref": self.transaction_ref,
            "amount": self.amount,
            "currency": self.currency,
            "gl_account_code": self.gl_account_code,
            "account_number": self.account_number,
        }


@dataclass(frozen=True, kw_only=True)
class BankingLoanRepaymentPostedIntegration(IntegrationEvent):
    account_id: str
    loan_id: str
    transaction_id: str
    transaction_ref: str
    amount: float
    principal_part: float
    interest_part: float
    penalty_amount: float
    currency: str
    gl_account_code: str | None

    @property
    def event_name(self) -> str:
        return "banking.loan.repayment.posted"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "account_id": self.account_id,
            "loan_id": self.loan_id,
            "transaction_id": self.transaction_id,
            "transaction_ref": self.transaction_ref,
            "amount": self.amount,
            "principal_part": self.principal_part,
            "interest_part": self.interest_part,
            "penalty_amount": self.penalty_amount,
            "currency": self.currency,
            "gl_account_code": self.gl_account_code,
        }


@dataclass(frozen=True, kw_only=True)
class BankingLoanCreditRiskAnalyzedIntegration(IntegrationEvent):
    loan_id: str
    analysis_id: str
    risk_score: float
    risk_grade: str
    recommendation: str

    @property
    def event_name(self) -> str:
        return "banking.loan.credit_risk.analyzed"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "loan_id": self.loan_id,
            "analysis_id": self.analysis_id,
            "risk_score": self.risk_score,
            "risk_grade": self.risk_grade,
            "recommendation": self.recommendation,
        }
