"""Enterprise Treasury Platform — capability catalog and domain enums."""
from __future__ import annotations

from enum import StrEnum


class TreasuryCapability(StrEnum):
    BANK_ACCOUNTS = "bank_accounts"
    CASH_POOLS = "cash_pools"
    LIQUIDITY_MANAGEMENT = "liquidity_management"
    TREASURY_OPERATIONS = "treasury_operations"
    FINANCIAL_RISK = "financial_risk"
    INVESTMENTS = "investments"
    BORROWING = "borrowing"
    FUNDING = "funding"
    CASH_FORECASTING = "cash_forecasting"
    TREASURY_DASHBOARD = "treasury_dashboard"
    TREASURY_ANALYTICS = "treasury_analytics"
    TREASURY_AI_ASSISTANT = "treasury_ai_assistant"


class TreasuryOperationType(StrEnum):
    TRANSFER = "transfer"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    POOL_SWEEP = "pool_sweep"
    INVESTMENT_PURCHASE = "investment_purchase"
    INVESTMENT_MATURITY = "investment_maturity"
    BORROWING_DRAWDOWN = "borrowing_drawdown"
    BORROWING_REPAYMENT = "borrowing_repayment"
    FUNDING_RECEIPT = "funding_receipt"
    FX_SETTLEMENT = "fx_settlement"


class ImplementationStatus(StrEnum):
    IMPLEMENTED = "implemented"
    PLANNED = "planned"


TREASURY_PLATFORM_CATALOG: dict[str, dict] = {
    TreasuryCapability.BANK_ACCOUNTS.value: {
        "label": "Bank Accounts",
        "status": ImplementationStatus.IMPLEMENTED.value,
        "aggregates": ["TreasuryAccount"],
        "gl_rules": ["bank_deposit"],
    },
    TreasuryCapability.CASH_POOLS.value: {
        "label": "Cash Pools",
        "status": ImplementationStatus.PLANNED.value,
        "aggregates": ["CashPool", "PoolSweep"],
        "gl_rules": ["pool_sweep"],
    },
    TreasuryCapability.LIQUIDITY_MANAGEMENT.value: {
        "label": "Liquidity Management",
        "status": ImplementationStatus.IMPLEMENTED.value,
        "aggregates": ["LiquiditySnapshot"],
        "gl_rules": [],
    },
    TreasuryCapability.TREASURY_OPERATIONS.value: {
        "label": "Treasury Operations",
        "status": ImplementationStatus.IMPLEMENTED.value,
        "aggregates": ["TreasuryTransfer", "TreasuryOperation"],
        "gl_rules": ["treasury_transfer", "bank_deposit"],
    },
    TreasuryCapability.FINANCIAL_RISK.value: {
        "label": "Financial Risk",
        "status": ImplementationStatus.IMPLEMENTED.value,
        "aggregates": ["TreasuryRiskLimit", "RiskAlert", "StressTestRun"],
        "gl_rules": [],
    },
    TreasuryCapability.INVESTMENTS.value: {
        "label": "Investments",
        "status": ImplementationStatus.IMPLEMENTED.value,
        "aggregates": ["Investment", "InvestmentTransaction"],
        "gl_rules": ["investment_purchase", "investment_maturity"],
    },
    TreasuryCapability.BORROWING.value: {
        "label": "Borrowing",
        "status": ImplementationStatus.PLANNED.value,
        "aggregates": ["BorrowingFacility", "LoanDrawdown", "LoanRepayment"],
        "gl_rules": ["borrowing_drawdown", "borrowing_repayment", "loan"],
    },
    TreasuryCapability.FUNDING.value: {
        "label": "Funding",
        "status": ImplementationStatus.PLANNED.value,
        "aggregates": ["FundingPlan", "FundingEvent"],
        "gl_rules": ["funding_received"],
    },
    TreasuryCapability.CASH_FORECASTING.value: {
        "label": "Cash Forecasting",
        "status": ImplementationStatus.IMPLEMENTED.value,
        "aggregates": ["CashForecast"],
        "gl_rules": [],
    },
    TreasuryCapability.TREASURY_DASHBOARD.value: {
        "label": "Treasury Dashboard",
        "status": ImplementationStatus.IMPLEMENTED.value,
        "aggregates": [],
        "gl_rules": [],
    },
    TreasuryCapability.TREASURY_ANALYTICS.value: {
        "label": "Treasury Analytics",
        "status": ImplementationStatus.IMPLEMENTED.value,
        "aggregates": [],
        "gl_rules": [],
    },
    TreasuryCapability.TREASURY_AI_ASSISTANT.value: {
        "label": "Treasury AI Assistant",
        "status": ImplementationStatus.IMPLEMENTED.value,
        "aggregates": [],
        "gl_rules": [],
    },
}

OPERATION_GL_RULE_MAP: dict[str, str] = {
    TreasuryOperationType.TRANSFER.value: "treasury_transfer",
    TreasuryOperationType.DEPOSIT.value: "bank_deposit",
    TreasuryOperationType.POOL_SWEEP.value: "pool_sweep",
    TreasuryOperationType.INVESTMENT_PURCHASE.value: "investment_purchase",
    TreasuryOperationType.INVESTMENT_MATURITY.value: "investment_maturity",
    TreasuryOperationType.BORROWING_DRAWDOWN.value: "borrowing_drawdown",
    TreasuryOperationType.BORROWING_REPAYMENT.value: "borrowing_repayment",
    TreasuryOperationType.FUNDING_RECEIPT.value: "funding_received",
    TreasuryOperationType.FX_SETTLEMENT.value: "exchange_transaction",
}

EVENT_GL_RULE_MAP: dict[str, str] = {
    "treasury.transfer.executed": "treasury_transfer",
    "treasury.deposit.executed": "bank_deposit",
    "treasury.pool.sweep.executed": "pool_sweep",
    "treasury.investment.purchased": "investment_purchase",
    "treasury.investment.matured": "investment_maturity",
    "treasury.borrowing.drawdown": "borrowing_drawdown",
    "treasury.borrowing.repayment": "borrowing_repayment",
    "treasury.funding.received": "funding_received",
    "currency_exchange.deal.settled": "exchange_transaction",
}
