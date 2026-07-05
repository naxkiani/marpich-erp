"""Banking integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class BankingAccountOpenedIntegration(IntegrationEvent):
    account_id: str
    customer_id: str
    account_type: str
    account_number: str
    currency: str
    gl_account_code: str | None
    kernel_linked: bool

    @property
    def event_name(self) -> str:
        return "banking.account.opened"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "account_id": self.account_id,
            "customer_id": self.customer_id,
            "account_type": self.account_type,
            "account_number": self.account_number,
            "currency": self.currency,
            "gl_account_code": self.gl_account_code,
            "kernel_linked": self.kernel_linked,
        }


@dataclass(frozen=True, kw_only=True)
class BankingCustomerCreatedIntegration(IntegrationEvent):
    customer_id: str
    customer_type: str
    display_name: str
    kyc_status: str
    risk_rating: str

    @property
    def event_name(self) -> str:
        return "banking.customer.created"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "customer_id": self.customer_id,
            "customer_type": self.customer_type,
            "display_name": self.display_name,
            "kyc_status": self.kyc_status,
            "risk_rating": self.risk_rating,
        }


@dataclass(frozen=True, kw_only=True)
class BankingKycVerifiedIntegration(IntegrationEvent):
    customer_id: str
    kyc_id: str
    tier: str

    @property
    def event_name(self) -> str:
        return "banking.kyc.verified"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "customer_id": self.customer_id,
            "kyc_id": self.kyc_id,
            "tier": self.tier,
        }


@dataclass(frozen=True, kw_only=True)
class BankingAccountStatusChangedIntegration(IntegrationEvent):
    account_id: str
    previous_status: str
    new_status: str
    actor_id: str | None

    @property
    def event_name(self) -> str:
        return "banking.account.status.changed"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "account_id": self.account_id,
            "previous_status": self.previous_status,
            "new_status": self.new_status,
            "actor_id": self.actor_id,
        }
