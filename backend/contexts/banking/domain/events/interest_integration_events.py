"""Interest Calculation Engine integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class BankingInterestCalculatedIntegration(IntegrationEvent):
    audit_id: str
    calc_ref: str
    product_context: str
    principal: float
    interest_amount: float
    penalty_interest: float
    currency: str
    mode: str

    @property
    def event_name(self) -> str:
        return "banking.interest.calculated"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "audit_id": self.audit_id,
            "calc_ref": self.calc_ref,
            "product_context": self.product_context,
            "principal": self.principal,
            "interest_amount": self.interest_amount,
            "penalty_interest": self.penalty_interest,
            "currency": self.currency,
            "mode": self.mode,
        }


@dataclass(frozen=True, kw_only=True)
class BankingInterestSimulatedIntegration(IntegrationEvent):
    audit_id: str
    calc_ref: str
    product_context: str
    interest_amount: float
    currency: str

    @property
    def event_name(self) -> str:
        return "banking.interest.simulated"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "audit_id": self.audit_id,
            "calc_ref": self.calc_ref,
            "product_context": self.product_context,
            "interest_amount": self.interest_amount,
            "currency": self.currency,
        }


@dataclass(frozen=True, kw_only=True)
class BankingInterestRateChangedIntegration(IntegrationEvent):
    profile_id: str
    profile_ref: str
    previous_rate_annual: float
    new_rate_annual: float
    rate_type: str
    effective_from: str

    @property
    def event_name(self) -> str:
        return "banking.interest.rate.changed"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "profile_id": self.profile_id,
            "profile_ref": self.profile_ref,
            "previous_rate_annual": self.previous_rate_annual,
            "new_rate_annual": self.new_rate_annual,
            "rate_type": self.rate_type,
            "effective_from": self.effective_from,
        }
