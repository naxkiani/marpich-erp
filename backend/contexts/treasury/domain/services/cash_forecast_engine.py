"""Enterprise Cash Forecast Engine — periods, categories, AI, scenarios."""
from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from contexts.treasury.domain.aggregates.cash_forecast_engine import (
    INFLOW_CATEGORIES,
    OUTFLOW_CATEGORIES,
    ForecastLineCategory,
    ForecastPeriodType,
    ForecastScenarioType,
)
from contexts.treasury.domain.aggregates.treasury_account import TreasuryAccount
from contexts.treasury.domain.services.treasury_engine import compute_liquidity

CASH_FORECAST_CATALOG: dict[str, dict] = {
    ForecastPeriodType.DAILY.value: {"label": "Daily Cash", "period": "daily"},
    ForecastPeriodType.WEEKLY.value: {"label": "Weekly Cash", "period": "weekly"},
    ForecastPeriodType.MONTHLY.value: {"label": "Monthly Cash", "period": "monthly"},
    ForecastPeriodType.QUARTERLY.value: {"label": "Quarterly Cash", "period": "quarterly"},
    ForecastPeriodType.ANNUAL.value: {"label": "Annual Cash", "period": "annual"},
    ForecastLineCategory.INCOMING_PAYMENTS.value: {"label": "Incoming Payments", "flow": "inflow"},
    ForecastLineCategory.OUTGOING_PAYMENTS.value: {"label": "Outgoing Payments", "flow": "outflow"},
    ForecastLineCategory.PAYROLL.value: {"label": "Payroll", "flow": "outflow"},
    ForecastLineCategory.TAX.value: {"label": "Tax", "flow": "outflow"},
    ForecastLineCategory.LOAN_PAYMENTS.value: {"label": "Loan Payments", "flow": "outflow"},
    ForecastLineCategory.STUDENT_TUITION.value: {"label": "Student Tuition", "flow": "inflow"},
    ForecastLineCategory.HOSPITAL_REVENUE.value: {"label": "Hospital Revenue", "flow": "inflow"},
    ForecastLineCategory.CONSTRUCTION_EXPENSES.value: {"label": "Construction Expenses", "flow": "outflow"},
    ForecastLineCategory.INVENTORY_PURCHASES.value: {"label": "Inventory Purchases", "flow": "outflow"},
    "ai_forecast": {"label": "AI Forecast", "autonomous_execution": False},
    "forecast_confidence_score": {"label": "Forecast Confidence Score", "supported": True},
    "scenario_simulation": {"label": "Scenario Simulation", "scenarios": ["base", "optimistic", "pessimistic"]},
}

SCENARIO_MULTIPLIERS: dict[str, dict[str, float]] = {
    ForecastScenarioType.BASE.value: {"inflow": 1.0, "outflow": 1.0},
    ForecastScenarioType.OPTIMISTIC.value: {"inflow": 1.15, "outflow": 0.9},
    ForecastScenarioType.PESSIMISTIC.value: {"inflow": 0.85, "outflow": 1.1},
}

DEFAULT_CATEGORY_WEIGHTS: dict[str, float] = {
    ForecastLineCategory.INCOMING_PAYMENTS.value: 0.25,
    ForecastLineCategory.HOSPITAL_REVENUE.value: 0.20,
    ForecastLineCategory.STUDENT_TUITION.value: 0.10,
    ForecastLineCategory.PAYROLL.value: 0.18,
    ForecastLineCategory.TAX.value: 0.08,
    ForecastLineCategory.LOAN_PAYMENTS.value: 0.07,
    ForecastLineCategory.CONSTRUCTION_EXPENSES.value: 0.05,
    ForecastLineCategory.INVENTORY_PURCHASES.value: 0.04,
    ForecastLineCategory.OUTGOING_PAYMENTS.value: 0.03,
}


def list_cash_forecast_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in CASH_FORECAST_CATALOG.items()]


def list_line_categories() -> list[dict]:
    return [
        {"category": c.value, "label": CASH_FORECAST_CATALOG[c.value]["label"], "flow": CASH_FORECAST_CATALOG[c.value]["flow"]}
        for c in ForecastLineCategory
    ]


def _apply_scenario(amount: float, category: str, scenario: str) -> float:
    mult = SCENARIO_MULTIPLIERS.get(scenario, SCENARIO_MULTIPLIERS["base"])
    if category in INFLOW_CATEGORIES:
        return round(amount * mult["inflow"], 2)
    return round(amount * mult["outflow"], 2)


def build_forecast_lines(
    opening: float,
    projected: list[dict],
    scenario: str = ForecastScenarioType.BASE.value,
) -> dict:
    lines = []
    balance = opening
    category_totals: dict[str, dict] = {}

    for row in sorted(projected, key=lambda r: r.get("date", "")):
        category = row.get("category", ForecastLineCategory.INCOMING_PAYMENTS.value)
        raw_inflow = round(float(row.get("inflow", 0)), 2)
        raw_outflow = round(float(row.get("outflow", 0)), 2)

        if category in INFLOW_CATEGORIES and raw_inflow == 0 and raw_outflow == 0:
            raw_inflow = round(float(row.get("amount", 0)), 2)
        if category in OUTFLOW_CATEGORIES and raw_inflow == 0 and raw_outflow == 0:
            raw_outflow = round(float(row.get("amount", 0)), 2)

        inflow = _apply_scenario(raw_inflow, category, scenario) if raw_inflow else 0.0
        outflow = _apply_scenario(raw_outflow, category, scenario) if raw_outflow else 0.0
        balance = round(balance + inflow - outflow, 2)

        if category not in category_totals:
            category_totals[category] = {"inflow": 0.0, "outflow": 0.0, "net": 0.0}
        category_totals[category]["inflow"] = round(category_totals[category]["inflow"] + inflow, 2)
        category_totals[category]["outflow"] = round(category_totals[category]["outflow"] + outflow, 2)
        category_totals[category]["net"] = round(
            category_totals[category]["inflow"] - category_totals[category]["outflow"], 2
        )

        lines.append(
            {
                "date": row.get("date", ""),
                "label": row.get("label", ""),
                "category": category,
                "inflow": inflow,
                "outflow": outflow,
                "opening_balance": round(balance - inflow + outflow, 2),
                "closing_balance": balance,
            }
        )

    total_inflow = round(sum(l["inflow"] for l in lines), 2)
    total_outflow = round(sum(l["outflow"] for l in lines), 2)
    return {
        "lines": lines,
        "category_totals": category_totals,
        "total_inflow": total_inflow,
        "total_outflow": total_outflow,
        "closing_balance": balance,
    }


def compute_confidence_score(*, lines: list[dict], scenario: str, has_historical: bool) -> float:
    if not lines:
        return 0.3
    dated = sum(1 for l in lines if l.get("date"))
    categorized = sum(1 for l in lines if l.get("category"))
    date_score = dated / len(lines)
    category_score = categorized / len(lines)
    scenario_penalty = 0.0 if scenario == ForecastScenarioType.BASE.value else 0.05
    historical_bonus = 0.1 if has_historical else 0.0
    score = 0.5 + date_score * 0.2 + category_score * 0.2 + historical_bonus - scenario_penalty
    return round(min(max(score, 0.35), 0.98), 4)


def _rollup_by_period(
    *,
    opening_balance: float,
    forecast_lines: list[dict],
    period: str,
    periods: int,
    scenario: str,
) -> list[dict]:
    today = date.today()
    rows: list[dict] = []
    balance = opening_balance

    for i in range(periods):
        if period == ForecastPeriodType.DAILY.value:
            d = today + timedelta(days=i)
            period_key = d.isoformat()
            period_lines = [l for l in forecast_lines if l.get("date") == period_key]
            label = d.strftime("%a %d %b")
        elif period == ForecastPeriodType.WEEKLY.value:
            start = today + timedelta(weeks=i)
            end = start + timedelta(days=6)
            period_key = f"W{i + 1}"
            period_lines = [
                l for l in forecast_lines
                if l.get("date") and start.isoformat() <= l["date"] <= end.isoformat()
            ]
            label = f"{start.isoformat()} – {end.isoformat()}"
        elif period == ForecastPeriodType.MONTHLY.value:
            month = (today.replace(day=1) + timedelta(days=32 * i)).replace(day=1)
            period_key = month.strftime("%Y-%m")
            period_lines = [l for l in forecast_lines if l.get("date", "").startswith(period_key)]
            label = month.strftime("%B %Y")
        elif period == ForecastPeriodType.QUARTERLY.value:
            q_start_month = ((today.month - 1) // 3) * 3 + 1 + (i * 3)
            year = today.year + (q_start_month - 1) // 12
            month = ((q_start_month - 1) % 12) + 1
            period_key = f"{year}-Q{((month - 1) // 3) + 1}"
            period_lines = [
                l for l in forecast_lines
                if l.get("date", "").startswith(str(year))
                and (int(l["date"][5:7]) - 1) // 3 == (month - 1) // 3
            ]
            label = period_key
        else:
            year = today.year + i
            period_key = str(year)
            period_lines = [l for l in forecast_lines if l.get("date", "").startswith(period_key)]
            label = f"FY {year}"

        inflow = round(sum(l.get("inflow", 0) for l in period_lines), 2)
        outflow = round(sum(l.get("outflow", 0) for l in period_lines), 2)
        if not period_lines and i > 0:
            inflow = round(balance * 0.02 * SCENARIO_MULTIPLIERS[scenario]["inflow"], 2)
            outflow = round(balance * 0.018 * SCENARIO_MULTIPLIERS[scenario]["outflow"], 2)

        opening = balance
        balance = round(balance + inflow - outflow, 2)
        rows.append(
            {
                "period": period_key,
                "label": label,
                "opening_balance": opening,
                "inflow": inflow,
                "outflow": outflow,
                "closing_balance": balance,
                "net_flow": round(inflow - outflow, 2),
            }
        )
    return rows


def compute_period_forecast(
    *,
    accounts: list[TreasuryAccount],
    forecast_plans: list[dict],
    period: str,
    periods: int,
    scenario: str = ForecastScenarioType.BASE.value,
) -> dict:
    liquidity = compute_liquidity(accounts)
    opening = liquidity["liquid_balance"]
    all_lines: list[dict] = []
    for plan in forecast_plans:
        if plan.get("scenario") == scenario or scenario == ForecastScenarioType.BASE.value:
            all_lines.extend(plan.get("lines", []))

    lines = _rollup_by_period(
        opening_balance=opening,
        forecast_lines=all_lines,
        period=period,
        periods=periods,
        scenario=scenario,
    )
    confidence = compute_confidence_score(
        lines=all_lines, scenario=scenario, has_historical=len(forecast_plans) > 0
    )
    return {
        "period_type": period,
        "scenario": scenario,
        "opening_balance": opening,
        "closing_balance": lines[-1]["closing_balance"] if lines else opening,
        "confidence_score": confidence,
        "lines": lines,
    }


def compute_category_breakdown(*, forecast_plans: list[dict]) -> dict:
    totals: dict[str, dict] = {}
    for plan in forecast_plans:
        for cat, data in plan.get("category_totals", {}).items():
            if cat not in totals:
                totals[cat] = {"inflow": 0.0, "outflow": 0.0, "net": 0.0}
            totals[cat]["inflow"] = round(totals[cat]["inflow"] + data.get("inflow", 0), 2)
            totals[cat]["outflow"] = round(totals[cat]["outflow"] + data.get("outflow", 0), 2)
            totals[cat]["net"] = round(totals[cat]["net"] + data.get("net", 0), 2)

    inflows = {k: v for k, v in totals.items() if k in INFLOW_CATEGORIES}
    outflows = {k: v for k, v in totals.items() if k in OUTFLOW_CATEGORIES}
    return {
        "incoming_payments": inflows,
        "outgoing_payments": outflows,
        "all_categories": totals,
        "total_inflow": round(sum(v["inflow"] for v in totals.values()), 2),
        "total_outflow": round(sum(v["outflow"] for v in totals.values()), 2),
    }


def run_scenario_simulation(*, base_plan: dict) -> list[dict]:
    scenarios = []
    for scenario in ForecastScenarioType:
        built = build_forecast_lines(
            base_plan["opening_balance"],
            [
                {
                    "date": l["date"],
                    "label": l["label"],
                    "category": l.get("category", ""),
                    "inflow": l["inflow"],
                    "outflow": l["outflow"],
                }
                for l in base_plan.get("lines", [])
            ],
            scenario.value,
        )
        confidence = compute_confidence_score(
            lines=base_plan.get("lines", []),
            scenario=scenario.value,
            has_historical=True,
        )
        scenarios.append(
            {
                "scenario": scenario.value,
                "total_inflow": built["total_inflow"],
                "total_outflow": built["total_outflow"],
                "closing_balance": built["closing_balance"],
                "category_totals": built["category_totals"],
                "confidence_score": confidence,
                "multipliers": SCENARIO_MULTIPLIERS[scenario.value],
            }
        )
    return scenarios


def generate_ai_forecast(
    *,
    accounts: list[TreasuryAccount],
    forecast_plans: list[dict],
    horizon_days: int = 90,
) -> dict:
    liquidity = compute_liquidity(accounts)
    opening = liquidity["liquid_balance"]
    monthly_burn = opening * 0.04 if opening else 1000.0

    if forecast_plans:
        avg_inflow = sum(p.get("total_inflow", 0) for p in forecast_plans) / len(forecast_plans)
        avg_outflow = sum(p.get("total_outflow", 0) for p in forecast_plans) / len(forecast_plans)
    else:
        avg_inflow = monthly_burn * 1.2
        avg_outflow = monthly_burn

    projected: list[dict] = []
    today = date.today()
    for i in range(0, horizon_days, 7):
        d = (today + timedelta(days=i)).isoformat()
        for category, weight in DEFAULT_CATEGORY_WEIGHTS.items():
            amount = round((avg_inflow if category in INFLOW_CATEGORIES else avg_outflow) * weight, 2)
            if amount <= 0:
                continue
            projected.append(
                {
                    "date": d,
                    "label": f"AI projected {category}",
                    "category": category,
                    "inflow": amount if category in INFLOW_CATEGORIES else 0,
                    "outflow": amount if category in OUTFLOW_CATEGORIES else 0,
                }
            )

    built = build_forecast_lines(opening, projected, ForecastScenarioType.BASE.value)
    confidence = compute_confidence_score(
        lines=projected,
        scenario=ForecastScenarioType.BASE.value,
        has_historical=bool(forecast_plans),
    )

    return {
        "horizon_days": horizon_days,
        "opening_balance": opening,
        "projected_closing": built["closing_balance"],
        "total_inflow": built["total_inflow"],
        "total_outflow": built["total_outflow"],
        "category_totals": built["category_totals"],
        "confidence_score": confidence,
        "lines": built["lines"][:20],
        "explanation": (
            f"AI forecast generated from {len(forecast_plans)} historical plan(s) "
            f"with {horizon_days}-day horizon. Confidence: {confidence:.0%}."
        ),
        "autonomous_execution": False,
    }


def build_forecast_dashboard(
    *,
    accounts: list[TreasuryAccount],
    forecast_plans: list[dict],
) -> dict:
    daily = compute_period_forecast(
        accounts=accounts, forecast_plans=forecast_plans,
        period=ForecastPeriodType.DAILY.value, periods=30,
    )
    weekly = compute_period_forecast(
        accounts=accounts, forecast_plans=forecast_plans,
        period=ForecastPeriodType.WEEKLY.value, periods=12,
    )
    monthly = compute_period_forecast(
        accounts=accounts, forecast_plans=forecast_plans,
        period=ForecastPeriodType.MONTHLY.value, periods=12,
    )
    quarterly = compute_period_forecast(
        accounts=accounts, forecast_plans=forecast_plans,
        period=ForecastPeriodType.QUARTERLY.value, periods=4,
    )
    annual = compute_period_forecast(
        accounts=accounts, forecast_plans=forecast_plans,
        period=ForecastPeriodType.ANNUAL.value, periods=3,
    )
    categories = compute_category_breakdown(forecast_plans=forecast_plans)
    ai = generate_ai_forecast(accounts=accounts, forecast_plans=forecast_plans)

    avg_confidence = 0.0
    if forecast_plans:
        avg_confidence = round(
            sum(p.get("confidence_score", 0.5) for p in forecast_plans) / len(forecast_plans), 4
        )

    return {
        "summary": {
            "plan_count": len(forecast_plans),
            "opening_balance": daily["opening_balance"],
            "projected_monthly_closing": monthly["closing_balance"],
            "avg_confidence_score": avg_confidence,
            "ai_confidence_score": ai["confidence_score"],
            "total_inflow": categories["total_inflow"],
            "total_outflow": categories["total_outflow"],
        },
        "daily_cash": daily,
        "weekly_cash": weekly,
        "monthly_cash": monthly,
        "quarterly_cash": quarterly,
        "annual_cash": annual,
        "category_breakdown": categories,
        "ai_forecast": ai,
        "recent_plans": forecast_plans[:10],
    }
