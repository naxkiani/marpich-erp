"""Treasury integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class TreasuryTransferExecutedIntegration(IntegrationEvent):
    transfer_id: str
    from_account_id: str
    to_account_id: str
    amount: float
    currency: str
    instrument: str

    @property
    def event_name(self) -> str:
        return "treasury.transfer.executed"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "transfer_id": self.transfer_id,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
            "amount": self.amount,
            "currency": self.currency,
            "instrument": self.instrument,
        }


@dataclass(frozen=True, kw_only=True)
class TreasuryLiquidityUpdatedIntegration(IntegrationEvent):
    total_balance: float
    liquid_balance: float
    liquidity_ratio: float

    @property
    def event_name(self) -> str:
        return "treasury.liquidity.updated"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "total_balance": self.total_balance,
            "liquid_balance": self.liquid_balance,
            "liquidity_ratio": self.liquidity_ratio,
        }


@dataclass(frozen=True, kw_only=True)
class TreasuryTransferApprovalRequestedIntegration(IntegrationEvent):
    transfer_id: str
    amount: float
    instrument: str

    @property
    def event_name(self) -> str:
        return "treasury.transfer.approval.requested"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "transfer_id": self.transfer_id,
            "amount": self.amount,
            "instrument": self.instrument,
        }
