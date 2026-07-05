"""Branch Banking Platform integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class BankingBranchOpenedIntegration(IntegrationEvent):
    office_id: str
    office_ref: str
    office_type: str
    operator_id: str

    @property
    def event_name(self) -> str:
        return "banking.branch.opened"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "office_id": self.office_id,
            "office_ref": self.office_ref,
            "office_type": self.office_type,
            "operator_id": self.operator_id,
        }


@dataclass(frozen=True, kw_only=True)
class BankingBranchClosedIntegration(IntegrationEvent):
    office_id: str
    office_ref: str
    closing_balance: float
    operator_id: str

    @property
    def event_name(self) -> str:
        return "banking.branch.closed"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "office_id": self.office_id,
            "office_ref": self.office_ref,
            "closing_balance": self.closing_balance,
            "operator_id": self.operator_id,
        }


@dataclass(frozen=True, kw_only=True)
class BankingVaultMovementIntegration(IntegrationEvent):
    vault_id: str
    office_id: str
    movement_type: str
    amount: float
    currency: str

    @property
    def event_name(self) -> str:
        return "banking.vault.movement"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "vault_id": self.vault_id,
            "office_id": self.office_id,
            "movement_type": self.movement_type,
            "amount": self.amount,
            "currency": self.currency,
        }


@dataclass(frozen=True, kw_only=True)
class BankingBranchKPIRecordedIntegration(IntegrationEvent):
    office_id: str
    metric_key: str
    metric_value: float
    target_value: float

    @property
    def event_name(self) -> str:
        return "banking.branch.kpi.recorded"

    @property
    def source_context(self) -> str:
        return "banking"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "office_id": self.office_id,
            "metric_key": self.metric_key,
            "metric_value": self.metric_value,
            "target_value": self.target_value,
        }
