"""Treasury Analytics aggregates and enums."""
from __future__ import annotations

from enum import StrEnum


class AnalyticsCapability(StrEnum):
    CASH_FLOW_ANALYSIS = "cash_flow_analysis"
    LIQUIDITY_TRENDS = "liquidity_trends"
    TREASURY_KPIS = "treasury_kpis"
    BANK_BALANCE_ANALYSIS = "bank_balance_analysis"
    FORECAST_ACCURACY = "forecast_accuracy"
    INVESTMENT_PERFORMANCE = "investment_performance"
    FUNDING_ANALYSIS = "funding_analysis"
    CURRENCY_EXPOSURE = "currency_exposure"
    WORKING_CAPITAL_KPIS = "working_capital_kpis"
    EXECUTIVE_DASHBOARD = "executive_dashboard"
    CFO_DASHBOARD = "cfo_dashboard"
    AI_TREASURY_ASSISTANT = "ai_treasury_assistant"
    LIQUIDITY_OPTIMIZATION = "liquidity_optimization"
    FUNDING_STRATEGY = "funding_strategy"
    CASH_CONCENTRATION = "cash_concentration"
    OPERATIONAL_EFFICIENCY = "operational_efficiency"
