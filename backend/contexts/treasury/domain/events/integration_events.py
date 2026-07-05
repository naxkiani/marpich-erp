"""Treasury integration events."""
from __future__ import annotations

from dataclasses import dataclass

from shared.domain.events.integration_event import IntegrationEvent


@dataclass(frozen=True, kw_only=True)
class TreasuryTransferExecutedIntegration(IntegrationEvent):
    transfer_id: str
    from_account_id: str
    to_account_id: str
    from_account_type: str
    to_account_type: str
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
            "from_account_type": self.from_account_type,
            "to_account_type": self.to_account_type,
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


@dataclass(frozen=True, kw_only=True)
class BankAccountApprovalRequestedIntegration(IntegrationEvent):
    bank_account_id: str
    code: str
    account_type: str

    @property
    def event_name(self) -> str:
        return "treasury.bank_account.approval.requested"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "bank_account_id": self.bank_account_id,
            "code": self.code,
            "account_type": self.account_type,
        }


@dataclass(frozen=True, kw_only=True)
class BankAccountActivatedIntegration(IntegrationEvent):
    bank_account_id: str
    code: str
    currency: str

    @property
    def event_name(self) -> str:
        return "treasury.bank_account.activated"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "bank_account_id": self.bank_account_id,
            "code": self.code,
            "currency": self.currency,
        }


@dataclass(frozen=True, kw_only=True)
class TreasuryTransactionApprovalRequestedIntegration(IntegrationEvent):
    transaction_id: str
    transaction_type: str
    amount: float
    currency: str
    required_approval_levels: int

    @property
    def event_name(self) -> str:
        return "treasury.transaction.approval.requested"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "currency": self.currency,
            "required_approval_levels": self.required_approval_levels,
        }


@dataclass(frozen=True, kw_only=True)
class TreasuryTransactionExecutedIntegration(IntegrationEvent):
    transaction_id: str
    transaction_type: str
    posting_rule_id: str
    from_account_id: str | None
    to_account_id: str | None
    from_account_type: str | None
    to_account_type: str | None
    amount: float
    currency: str

    @property
    def event_name(self) -> str:
        return "treasury.transaction.executed"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type,
            "posting_rule_id": self.posting_rule_id,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
            "from_account_type": self.from_account_type,
            "to_account_type": self.to_account_type,
            "amount": self.amount,
            "currency": self.currency,
        }


@dataclass(frozen=True, kw_only=True)
class TreasuryAIAnalysisCompletedIntegration(IntegrationEvent):
    capability: str
    result_summary: str

    @property
    def event_name(self) -> str:
        return "treasury.ai.analysis.completed"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "capability": self.capability,
            "result_summary": self.result_summary,
        }


@dataclass(frozen=True, kw_only=True)
class TreasuryInvestmentPurchasedIntegration(IntegrationEvent):
    investment_id: str
    investment_type: str
    principal_amount: float
    currency: str
    portfolio_name: str

    @property
    def event_name(self) -> str:
        return "treasury.investment.purchased"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "investment_id": self.investment_id,
            "investment_type": self.investment_type,
            "principal_amount": self.principal_amount,
            "currency": self.currency,
            "portfolio_name": self.portfolio_name,
        }


@dataclass(frozen=True, kw_only=True)
class TreasuryInvestmentMaturedIntegration(IntegrationEvent):
    investment_id: str
    investment_type: str
    maturity_proceeds: float
    currency: str

    @property
    def event_name(self) -> str:
        return "treasury.investment.matured"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "investment_id": self.investment_id,
            "investment_type": self.investment_type,
            "maturity_proceeds": self.maturity_proceeds,
            "currency": self.currency,
        }


@dataclass(frozen=True, kw_only=True)
class TreasuryFxDealSettledIntegration(IntegrationEvent):
    transaction_id: str
    from_currency: str
    to_currency: str
    from_amount: float
    to_amount: float
    exchange_rate: float
    gain_loss: float

    @property
    def event_name(self) -> str:
        return "currency_exchange.deal.settled"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "from_currency": self.from_currency,
            "to_currency": self.to_currency,
            "from_amount": self.from_amount,
            "to_amount": self.to_amount,
            "exchange_rate": self.exchange_rate,
            "gain_loss": self.gain_loss,
        }


@dataclass(frozen=True, kw_only=True)
class TreasuryRiskBreachIntegration(IntegrationEvent):
    alert_id: str
    risk_type: str
    exposure_value: float
    limit_value: float
    severity: str

    @property
    def event_name(self) -> str:
        return "treasury.risk.breach"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "alert_id": self.alert_id,
            "risk_type": self.risk_type,
            "exposure_value": self.exposure_value,
            "limit_value": self.limit_value,
            "severity": self.severity,
        }


@dataclass(frozen=True, kw_only=True)
class TreasurySecurityAccessDeniedIntegration(IntegrationEvent):
    operation_type: str
    reason: str
    actor_id: str

    @property
    def event_name(self) -> str:
        return "treasury.security.access.denied"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "operation_type": self.operation_type,
            "reason": self.reason,
            "actor_id": self.actor_id,
        }


@dataclass(frozen=True, kw_only=True)
class TreasurySecurityPolicyViolationIntegration(IntegrationEvent):
    operation_type: str
    violation_type: str
    actor_id: str

    @property
    def event_name(self) -> str:
        return "treasury.security.policy.violated"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "operation_type": self.operation_type,
            "violation_type": self.violation_type,
            "actor_id": self.actor_id,
        }


@dataclass(frozen=True, kw_only=True)
class TreasurySecurityFreezeActivatedIntegration(IntegrationEvent):
    reason: str
    activated_by: str

    @property
    def event_name(self) -> str:
        return "treasury.security.freeze.activated"

    @property
    def source_context(self) -> str:
        return "treasury"

    @property
    def event_version(self) -> int:
        return 1

    def to_payload(self) -> dict:
        return {
            "reason": self.reason,
            "activated_by": self.activated_by,
        }
