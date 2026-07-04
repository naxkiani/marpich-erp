"""Cash flow forecast aggregate."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class ForecastScenario(StrEnum):
    BASE = "base"
    OPTIMISTIC = "optimistic"
    PESSIMISTIC = "pessimistic"


@dataclass(eq=False, kw_only=True)
class CashForecast(AggregateRoot):
    tenant_id: str
    name: str
    period_start: str
    period_end: str
    scenario: str
    currency: str
    opening_balance: float
    lines: list[dict]
    total_inflow: float = 0.0
    total_outflow: float = 0.0
    closing_balance: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(
        cls,
        *,
        tenant_id: str,
        name: str,
        period_start: str,
        period_end: str,
        scenario: str,
        currency: str,
        opening_balance: float,
        projected_lines: list[dict],
    ) -> CashForecast:
        lines = _build_forecast_lines(opening_balance, projected_lines)
        total_inflow = round(sum(l["inflow"] for l in lines), 2)
        total_outflow = round(sum(l["outflow"] for l in lines), 2)
        closing = lines[-1]["closing_balance"] if lines else opening_balance
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            name=name,
            period_start=period_start,
            period_end=period_end,
            scenario=scenario,
            currency=currency.strip().upper(),
            opening_balance=round(opening_balance, 2),
            lines=lines,
            total_inflow=total_inflow,
            total_outflow=total_outflow,
            closing_balance=round(closing, 2),
        )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": self.tenant_id,
            "name": self.name,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "scenario": self.scenario,
            "currency": self.currency,
            "opening_balance": self.opening_balance,
            "lines": self.lines,
            "total_inflow": self.total_inflow,
            "total_outflow": self.total_outflow,
            "closing_balance": self.closing_balance,
            "created_at": self.created_at.isoformat(),
        }


def _build_forecast_lines(opening: float, projected: list[dict]) -> list[dict]:
    lines = []
    balance = opening
    for row in sorted(projected, key=lambda r: r.get("date", "")):
        inflow = round(float(row.get("inflow", 0)), 2)
        outflow = round(float(row.get("outflow", 0)), 2)
        balance = round(balance + inflow - outflow, 2)
        lines.append(
            {
                "date": row.get("date", ""),
                "label": row.get("label", ""),
                "inflow": inflow,
                "outflow": outflow,
                "opening_balance": round(balance - inflow + outflow, 2),
                "closing_balance": balance,
            }
        )
    return lines
