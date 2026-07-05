"""Enterprise Investment Management Engine."""
from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from contexts.treasury.domain.aggregates.investment_engine import (
    InvestmentStatus,
    InvestmentType,
    RiskRating,
)

INVESTMENT_CATALOG: dict[str, dict] = {
    InvestmentType.FIXED_DEPOSIT.value: {"label": "Fixed Deposit", "supported": True},
    InvestmentType.BONDS.value: {"label": "Bonds", "supported": True},
    InvestmentType.GOVERNMENT_SECURITIES.value: {"label": "Government Securities", "supported": True},
    InvestmentType.MUTUAL_FUNDS.value: {"label": "Mutual Funds", "supported": True},
    "investment_portfolio": {"label": "Investment Portfolio", "supported": True},
    "investment_income": {"label": "Investment Income", "supported": True},
    "interest_accrual": {"label": "Interest Accrual", "supported": True},
    "maturity_tracking": {"label": "Maturity Tracking", "supported": True},
    "risk_rating": {"label": "Risk Rating", "supported": True},
    "portfolio_performance": {"label": "Portfolio Performance", "supported": True},
    "investment_dashboard": {"label": "Investment Dashboard", "supported": True},
    "ai_investment_analysis": {"label": "AI Investment Analysis", "autonomous_execution": False},
}

RISK_SCORE: dict[str, int] = {
    RiskRating.AAA.value: 1,
    RiskRating.AA.value: 2,
    RiskRating.A.value: 3,
    RiskRating.BBB.value: 4,
    RiskRating.BB.value: 5,
    RiskRating.B.value: 6,
    RiskRating.UNRATED.value: 7,
}


def list_investment_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in INVESTMENT_CATALOG.items()]


def compute_daily_accrual(*, principal: float, annual_rate: float, days: int = 1) -> float:
    if annual_rate <= 0 or principal <= 0:
        return 0.0
    return round(principal * (annual_rate / 100) / 365 * days, 2)


def compute_maturity_tracking(*, investments: list[dict], horizon_days: int = 90) -> dict:
    today = date.today()
    horizon = today + timedelta(days=horizon_days)
    upcoming = []
    overdue = []
    no_maturity = []

    for inv in investments:
        if inv.get("status") != InvestmentStatus.ACTIVE.value:
            continue
        mat = inv.get("maturity_date")
        if not mat:
            no_maturity.append(inv)
            continue
        try:
            mat_date = date.fromisoformat(mat[:10])
        except ValueError:
            no_maturity.append(inv)
            continue
        entry = {
            **inv,
            "days_to_maturity": (mat_date - today).days,
        }
        if mat_date < today:
            overdue.append(entry)
        elif mat_date <= horizon:
            upcoming.append(entry)

    upcoming.sort(key=lambda x: x["days_to_maturity"])
    overdue.sort(key=lambda x: x["days_to_maturity"])
    return {
        "as_of": today.isoformat(),
        "horizon_days": horizon_days,
        "upcoming_maturities": upcoming,
        "overdue_maturities": overdue,
        "no_maturity_date": no_maturity,
        "upcoming_count": len(upcoming),
        "overdue_count": len(overdue),
    }


def compute_risk_ratings(*, investments: list[dict]) -> dict:
    by_rating: dict[str, dict] = {}
    weighted_score = 0.0
    total_value = 0.0

    for inv in investments:
        if inv.get("status") not in {InvestmentStatus.ACTIVE.value, InvestmentStatus.MATURED.value}:
            continue
        rating = inv.get("risk_rating", RiskRating.UNRATED.value)
        value = inv.get("current_value", 0)
        total_value += value
        weighted_score += value * RISK_SCORE.get(rating, 7)
        bucket = by_rating.setdefault(
            rating,
            {"rating": rating, "count": 0, "total_value": 0.0, "investments": []},
        )
        bucket["count"] += 1
        bucket["total_value"] = round(bucket["total_value"] + value, 2)
        bucket["investments"].append(inv["id"])

    portfolio_rating = RiskRating.UNRATED.value
    if total_value > 0:
        avg = weighted_score / total_value
        if avg <= 1.5:
            portfolio_rating = RiskRating.AAA.value
        elif avg <= 2.5:
            portfolio_rating = RiskRating.AA.value
        elif avg <= 3.5:
            portfolio_rating = RiskRating.A.value
        elif avg <= 4.5:
            portfolio_rating = RiskRating.BBB.value
        elif avg <= 5.5:
            portfolio_rating = RiskRating.BB.value
        else:
            portfolio_rating = RiskRating.B.value

    return {
        "portfolio_risk_rating": portfolio_rating,
        "by_rating": list(by_rating.values()),
        "total_exposure": round(total_value, 2),
    }


def compute_portfolio_performance(*, investments: list[dict]) -> dict:
    portfolios: dict[str, dict] = {}
    total_principal = 0.0
    total_current = 0.0
    total_income = 0.0
    total_accrued = 0.0

    for inv in investments:
        if inv.get("status") == InvestmentStatus.SOLD.value:
            continue
        pname = inv.get("portfolio_name", "Default")
        principal = inv.get("principal_amount", 0)
        current = inv.get("current_value", 0)
        income = inv.get("total_income", 0)
        accrued = inv.get("accrued_interest", 0)

        total_principal += principal
        total_current += current
        total_income += income
        total_accrued += accrued

        bucket = portfolios.setdefault(
            pname,
            {
                "portfolio_name": pname,
                "investment_count": 0,
                "principal": 0.0,
                "current_value": 0.0,
                "total_income": 0.0,
                "accrued_interest": 0.0,
                "by_type": {},
            },
        )
        bucket["investment_count"] += 1
        bucket["principal"] = round(bucket["principal"] + principal, 2)
        bucket["current_value"] = round(bucket["current_value"] + current, 2)
        bucket["total_income"] = round(bucket["total_income"] + income, 2)
        bucket["accrued_interest"] = round(bucket["accrued_interest"] + accrued, 2)
        itype = inv.get("investment_type", "unknown")
        bucket["by_type"][itype] = bucket["by_type"].get(itype, 0) + 1

    unrealized = round(total_current - total_principal, 2)
    return_pct = round((unrealized / total_principal * 100) if total_principal else 0, 2)
    return {
        "total_principal": round(total_principal, 2),
        "total_current_value": round(total_current, 2),
        "total_income": round(total_income, 2),
        "total_accrued_interest": round(total_accrued, 2),
        "unrealized_gain_loss": unrealized,
        "return_pct": return_pct,
        "portfolios": list(portfolios.values()),
    }


def build_investment_dashboard(
    *,
    investments: list[dict],
    transactions: list[dict],
) -> dict:
    active = [i for i in investments if i.get("status") == InvestmentStatus.ACTIVE.value]
    performance = compute_portfolio_performance(investments=investments)
    maturity = compute_maturity_tracking(investments=investments)
    risk = compute_risk_ratings(investments=investments)

    by_type: dict[str, int] = {}
    for inv in active:
        t = inv.get("investment_type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1

    recent_income = [
        t for t in transactions if t.get("transaction_type") in {"income", "interest_accrual", "maturity"}
    ][-10:]

    return {
        "summary": {
            "total_investments": len(investments),
            "active_investments": len(active),
            "total_current_value": performance["total_current_value"],
            "total_income": performance["total_income"],
            "portfolio_risk_rating": risk["portfolio_risk_rating"],
            "upcoming_maturities": maturity["upcoming_count"],
        },
        "by_type": by_type,
        "by_status": _count_by_field(investments, "status"),
        "performance": performance,
        "maturity_tracking": maturity,
        "risk_ratings": risk,
        "recent_income_transactions": recent_income,
    }


def generate_ai_investment_analysis(
    *,
    investments: list[dict],
    liquid_balance: float = 0.0,
) -> dict:
    performance = compute_portfolio_performance(investments=investments)
    maturity = compute_maturity_tracking(investments=investments)
    risk = compute_risk_ratings(investments=investments)
    recommendations: list[dict] = []

    if performance["return_pct"] < 2:
        recommendations.append(
            {
                "priority": "medium",
                "category": "yield_optimization",
                "message": "Portfolio yield below 2% — consider higher-yield government securities or bonds.",
                "autonomous_execution": False,
            }
        )

    if maturity["overdue_count"] > 0:
        recommendations.append(
            {
                "priority": "high",
                "category": "maturity_action",
                "message": f"{maturity['overdue_count']} investment(s) past maturity — process redemption.",
                "autonomous_execution": False,
            }
        )

    if maturity["upcoming_count"] > 0:
        recommendations.append(
            {
                "priority": "medium",
                "category": "maturity_planning",
                "message": f"{maturity['upcoming_count']} maturity(ies) within 90 days — plan reinvestment.",
                "autonomous_execution": False,
            }
        )

    gov_pct = _type_allocation_pct(investments, InvestmentType.GOVERNMENT_SECURITIES.value)
    if gov_pct < 20 and liquid_balance > 100000:
        recommendations.append(
            {
                "priority": "low",
                "category": "allocation",
                "message": "Low government securities allocation with excess liquidity — diversify into sovereign instruments.",
                "autonomous_execution": False,
            }
        )

    if risk["portfolio_risk_rating"] in {RiskRating.BB.value, RiskRating.B.value}:
        recommendations.append(
            {
                "priority": "high",
                "category": "risk",
                "message": "Portfolio risk rating elevated — review bond and mutual fund exposure.",
                "autonomous_execution": False,
            }
        )

    if not recommendations:
        recommendations.append(
            {
                "priority": "low",
                "category": "balanced",
                "message": "Portfolio appears balanced — no immediate action required.",
                "autonomous_execution": False,
            }
        )

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "portfolio_performance": performance,
        "risk_summary": risk,
        "maturity_outlook": {
            "upcoming": maturity["upcoming_count"],
            "overdue": maturity["overdue_count"],
        },
        "recommendations": recommendations,
        "autonomous_execution": False,
    }


def _count_by_field(items: list[dict], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        key = item.get(field, "unknown")
        counts[key] = counts.get(key, 0) + 1
    return counts


def _type_allocation_pct(investments: list[dict], investment_type: str) -> float:
    active = [i for i in investments if i.get("status") == InvestmentStatus.ACTIVE.value]
    if not active:
        return 0.0
    total = sum(i.get("current_value", 0) for i in active)
    if not total:
        return 0.0
    typed = sum(i.get("current_value", 0) for i in active if i.get("investment_type") == investment_type)
    return round(typed / total * 100, 2)
