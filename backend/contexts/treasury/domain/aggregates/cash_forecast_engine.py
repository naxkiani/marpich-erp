"""Enterprise Cash Forecast aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class ForecastPeriodType(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"


class ForecastLineCategory(StrEnum):
    INCOMING_PAYMENTS = "incoming_payments"
    OUTGOING_PAYMENTS = "outgoing_payments"
    PAYROLL = "payroll"
    TAX = "tax"
    LOAN_PAYMENTS = "loan_payments"
    STUDENT_TUITION = "student_tuition"
    HOSPITAL_REVENUE = "hospital_revenue"
    CONSTRUCTION_EXPENSES = "construction_expenses"
    INVENTORY_PURCHASES = "inventory_purchases"


class ForecastScenarioType(StrEnum):
    BASE = "base"
    OPTIMISTIC = "optimistic"
    PESSIMISTIC = "pessimistic"


INFLOW_CATEGORIES = {
    ForecastLineCategory.INCOMING_PAYMENTS.value,
    ForecastLineCategory.STUDENT_TUITION.value,
    ForecastLineCategory.HOSPITAL_REVENUE.value,
}

OUTFLOW_CATEGORIES = {
    ForecastLineCategory.OUTGOING_PAYMENTS.value,
    ForecastLineCategory.PAYROLL.value,
    ForecastLineCategory.TAX.value,
    ForecastLineCategory.LOAN_PAYMENTS.value,
    ForecastLineCategory.CONSTRUCTION_EXPENSES.value,
    ForecastLineCategory.INVENTORY_PURCHASES.value,
}


@dataclass(eq=False, kw_only=True)
class CashForecastPlan(AggregateRoot):
    tenant_id: str
    name: str
    period_type: str
    period_start: str
    period_end: str
    scenario: str
    currency: str
    opening_balance: float
    lines: list[dict]
    category_totals: dict
    total_inflow: float
    total_outflow: float
    closing_balance: float
    confidence_score: float
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        name: str,
        period_type: str,
        period_start: str,
        period_end: str,
        scenario: str,
        currency: str,
        opening_balance: float,
        projected_lines: list[dict],
        confidence_score: float = 0.0,
    ) -> CashForecastPlan:
        from contexts.treasury.domain.services.cash_forecast_engine import build_forecast_lines

        built = build_forecast_lines(opening_balance, projected_lines, scenario)
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            name=name,
            period_type=period_type,
            period_start=period_start,
            period_end=period_end,
            scenario=scenario,
            currency=currency.strip().upper(),
            opening_balance=round(opening_balance, 2),
            lines=built["lines"],
            category_totals=built["category_totals"],
            total_inflow=built["total_inflow"],
            total_outflow=built["total_outflow"],
            closing_balance=built["closing_balance"],
            confidence_score=round(confidence_score, 4),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "name": self.name,
            "period_type": self.period_type,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "scenario": self.scenario,
            "currency": self.currency,
            "opening_balance": self.opening_balance,
            "lines": self.lines,
            "category_totals": self.category_totals,
            "total_inflow": self.total_inflow,
            "total_outflow": self.total_outflow,
            "closing_balance": self.closing_balance,
            "confidence_score": self.confidence_score,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class ForecastSimulation(AggregateRoot):
    tenant_id: str
    name: str
    base_forecast_id: str
    scenarios: list[dict]
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        name: str,
        base_forecast_id: str,
        scenarios: list[dict],
    ) -> ForecastSimulation:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            name=name,
            base_forecast_id=base_forecast_id,
            scenarios=scenarios,
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "name": self.name,
            "base_forecast_id": self.base_forecast_id,
            "scenarios": self.scenarios,
            "created_at": self.created_at.isoformat(),
        }
