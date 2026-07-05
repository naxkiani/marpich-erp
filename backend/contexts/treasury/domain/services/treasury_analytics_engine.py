"""Treasury Analytics Engine."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.treasury.domain.aggregates.treasury_analytics_engine import AnalyticsCapability
from contexts.treasury.domain.services.investment_engine import compute_portfolio_performance
from contexts.treasury.domain.services.liquidity_engine import (
    compute_cash_position,
    compute_funding_needs,
    compute_liquidity_gap,
    compute_period_liquidity,
    compute_working_capital,
    optimization_recommendations,
)
from contexts.treasury.domain.services.multi_currency_engine import (
    BASE_CURRENCY,
    build_fx_report,
    compute_currency_positions,
)
from contexts.treasury.domain.services.risk_engine import compute_all_exposures
from contexts.treasury.domain.services.treasury_engine import compute_liquidity

ANALYTICS_CATALOG: dict[str, dict] = {
    AnalyticsCapability.CASH_FLOW_ANALYSIS.value: {"label": "Cash Flow Analysis", "supported": True},
    AnalyticsCapability.LIQUIDITY_TRENDS.value: {"label": "Liquidity Trends", "supported": True},
    AnalyticsCapability.TREASURY_KPIS.value: {"label": "Treasury KPIs", "supported": True},
    AnalyticsCapability.BANK_BALANCE_ANALYSIS.value: {"label": "Bank Balance Analysis", "supported": True},
    AnalyticsCapability.FORECAST_ACCURACY.value: {"label": "Forecast Accuracy", "supported": True},
    AnalyticsCapability.INVESTMENT_PERFORMANCE.value: {"label": "Investment Performance", "supported": True},
    AnalyticsCapability.FUNDING_ANALYSIS.value: {"label": "Funding Analysis", "supported": True},
    AnalyticsCapability.CURRENCY_EXPOSURE.value: {"label": "Currency Exposure", "supported": True},
    AnalyticsCapability.WORKING_CAPITAL_KPIS.value: {"label": "Working Capital KPIs", "supported": True},
    AnalyticsCapability.EXECUTIVE_DASHBOARD.value: {"label": "Executive Dashboard", "supported": True},
    AnalyticsCapability.CFO_DASHBOARD.value: {"label": "CFO Dashboard", "supported": True},
    AnalyticsCapability.AI_TREASURY_ASSISTANT.value: {
        "label": "AI Treasury Assistant",
        "autonomous_execution": False,
    },
    AnalyticsCapability.LIQUIDITY_OPTIMIZATION.value: {"label": "Liquidity Optimization", "supported": True},
    AnalyticsCapability.FUNDING_STRATEGY.value: {"label": "Funding Strategy", "supported": True},
    AnalyticsCapability.CASH_CONCENTRATION.value: {"label": "Cash Concentration", "supported": True},
    AnalyticsCapability.OPERATIONAL_EFFICIENCY.value: {"label": "Operational Efficiency", "supported": True},
}


def list_analytics_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in ANALYTICS_CATALOG.items()]


def _rec(
    *,
    priority: str,
    category: str,
    action: str,
    detail: str,
    explanation: str,
    confidence: float = 0.8,
) -> dict:
    return {
        "priority": priority,
        "category": category,
        "action": action,
        "detail": detail,
        "explanation": explanation,
        "confidence": round(confidence, 2),
        "autonomous_execution": False,
    }


def build_cash_flow_analysis(*, accounts, forecasts: list[dict]) -> dict:
    liquidity = compute_liquidity(accounts)
    daily = compute_period_liquidity(
        accounts=accounts, forecasts=forecasts, period="daily", periods=30
    )
    monthly = compute_period_liquidity(
        accounts=accounts, forecasts=forecasts, period="monthly", periods=12
    )
    total_inflow = round(sum(l["inflow"] for l in daily["lines"]), 2)
    total_outflow = round(sum(l["outflow"] for l in daily["lines"]), 2)
    net_flow = round(total_inflow - total_outflow, 2)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "opening_balance": daily["opening_balance"],
        "total_inflow_30d": total_inflow,
        "total_outflow_30d": total_outflow,
        "net_cash_flow_30d": net_flow,
        "closing_balance": daily["closing_balance"],
        "daily_lines": daily["lines"][-14:],
        "monthly_summary": monthly["lines"][-6:],
        "by_currency": liquidity["by_currency"],
        "cash_flow_ratio": round(total_inflow / total_outflow, 4) if total_outflow else 0,
    }


def build_liquidity_trends(*, accounts, forecasts: list[dict]) -> dict:
    daily = compute_period_liquidity(
        accounts=accounts, forecasts=forecasts, period="daily", periods=30
    )
    weekly = compute_period_liquidity(
        accounts=accounts, forecasts=forecasts, period="weekly", periods=12
    )
    monthly = compute_period_liquidity(
        accounts=accounts, forecasts=forecasts, period="monthly", periods=12
    )
    gap = compute_liquidity_gap(accounts=accounts, forecasts=forecasts)

    balances = [l["closing_balance"] for l in daily["lines"]]
    trend = 0.0
    if len(balances) >= 2:
        trend = round((balances[-1] - balances[0]) / len(balances), 2)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "trend_per_day": trend,
        "trend_direction": "improving" if trend >= 0 else "declining",
        "liquidity_gap": gap,
        "daily": daily["lines"][-14:],
        "weekly": weekly["lines"][-8:],
        "monthly": monthly["lines"][-6:],
        "minimum_balance": min(balances) if balances else 0,
        "maximum_balance": max(balances) if balances else 0,
    }


def build_treasury_kpis(*, ctx: dict) -> dict:
    accounts = ctx["accounts"]
    liquidity = compute_liquidity(accounts)
    gap = compute_liquidity_gap(accounts=accounts, forecasts=ctx["forecasts"])
    wc = compute_working_capital(accounts=accounts)
    funding = compute_funding_needs(
        accounts=accounts,
        forecasts=ctx["forecasts"],
        funding_needs=ctx["funding_needs"],
    )
    performance = compute_portfolio_performance(investments=ctx["investments"])
    exposures = ctx["exposures"]

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "kpis": {
            "total_cash": liquidity["total_balance"],
            "liquid_ratio": liquidity["liquidity_ratio"],
            "liquidity_gap": gap["liquidity_gap"],
            "working_capital": wc["working_capital"],
            "current_ratio": wc["current_ratio"],
            "funding_gap": funding["total_funding_gap"],
            "investment_return_pct": performance["return_pct"],
            "fx_net_impact": ctx.get("fx_net_impact", 0),
            "open_risk_alerts": ctx.get("open_alerts", 0),
            "portfolio_value": performance["total_current_value"],
        },
        "risk_exposures": exposures,
    }


def build_bank_balance_analysis(*, accounts) -> dict:
    bank_accounts = [a for a in accounts if a.is_active and a.account_type == "bank"]
    by_bank: dict[str, dict] = {}
    total = 0.0

    for acct in bank_accounts:
        bank_key = acct.name.split("-")[0].strip() if "-" in acct.name else acct.name
        bucket = by_bank.setdefault(
            bank_key,
            {"bank": bank_key, "account_count": 0, "balance": 0.0, "currencies": {}},
        )
        bucket["account_count"] += 1
        bucket["balance"] = round(bucket["balance"] + acct.balance, 2)
        bucket["currencies"][acct.currency] = round(
            bucket["currencies"].get(acct.currency, 0) + acct.balance, 2
        )
        total += acct.balance

    ranked = sorted(by_bank.values(), key=lambda x: x["balance"], reverse=True)
    concentration = 0.0
    if ranked and total:
        concentration = round(ranked[0]["balance"] / total * 100, 2)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "total_bank_balance": round(total, 2),
        "bank_count": len(by_bank),
        "account_count": len(bank_accounts),
        "top_bank_concentration_pct": concentration,
        "by_bank": ranked,
        "by_currency": compute_liquidity(accounts)["by_currency"],
    }


def build_forecast_accuracy(*, forecast_plans: list[dict], accounts) -> dict:
    liquidity = compute_liquidity(accounts)
    actual_balance = liquidity["liquid_balance"]

    plans_with_confidence = [p for p in forecast_plans if p.get("confidence_score")]
    avg_confidence = 0.0
    if plans_with_confidence:
        avg_confidence = round(
            sum(p["confidence_score"] for p in plans_with_confidence) / len(plans_with_confidence),
            4,
        )

    variances: list[dict] = []
    for plan in forecast_plans[-10:]:
        projected = plan.get("projected_closing", plan.get("closing_balance", 0))
        if projected:
            variance = round(actual_balance - projected, 2)
            accuracy = round(max(0, 1 - abs(variance) / max(abs(projected), 1)) * 100, 2)
            variances.append(
                {
                    "plan_id": plan.get("id"),
                    "plan_name": plan.get("name", "unnamed"),
                    "projected_closing": projected,
                    "actual_balance": actual_balance,
                    "variance": variance,
                    "accuracy_pct": accuracy,
                    "confidence_score": plan.get("confidence_score", 0),
                }
            )

    avg_accuracy = 0.0
    if variances:
        avg_accuracy = round(sum(v["accuracy_pct"] for v in variances) / len(variances), 2)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "plan_count": len(forecast_plans),
        "avg_confidence_score": avg_confidence,
        "avg_forecast_accuracy_pct": avg_accuracy,
        "actual_liquid_balance": actual_balance,
        "plan_variances": variances,
        "accuracy_rating": (
            "high" if avg_accuracy >= 85 else "medium" if avg_accuracy >= 70 else "low"
        ),
    }


def build_funding_analysis(*, accounts, forecasts: list[dict], funding_needs: list[dict]) -> dict:
    funding = compute_funding_needs(
        accounts=accounts, forecasts=forecasts, funding_needs=funding_needs
    )
    gap = compute_liquidity_gap(accounts=accounts, forecasts=forecasts)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "funding_needs": funding,
        "liquidity_gap": gap,
        "funding_priority": "high" if funding["total_funding_gap"] > 0 else "low",
        "open_needs": [n for n in funding_needs if n.get("status") != "fulfilled"],
    }


def build_currency_exposure(*, accounts, investments: list[dict], rates: list[dict], fx_transactions: list[dict]) -> dict:
    positions = compute_currency_positions(accounts=accounts, investments=investments, rates=rates)
    report = build_fx_report(positions=positions, transactions=fx_transactions, rates=rates)

    concentrations = []
    for pos in positions.get("positions", []):
        if pos.get("portfolio_pct", 0) > 25:
            concentrations.append(pos)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "base_currency": BASE_CURRENCY,
        "positions": positions,
        "fx_report": report,
        "high_concentration_currencies": concentrations,
        "net_fx_impact": report["summary"]["net_fx_impact"],
    }


def build_working_capital_kpis(*, accounts) -> dict:
    wc = compute_working_capital(accounts=accounts)
    cash_position = compute_cash_position(accounts=accounts)
    liquidity = compute_liquidity(accounts)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "working_capital": wc,
        "cash_position": cash_position,
        "quick_ratio_proxy": round(
            cash_position["liquid_balance"] / wc["current_liabilities_proxy"], 4
        )
        if wc["current_liabilities_proxy"]
        else 0,
        "cash_to_total_ratio": round(
            cash_position["liquid_balance"] / liquidity["total_balance"], 4
        )
        if liquidity["total_balance"]
        else 0,
    }


def build_executive_dashboard(*, ctx: dict) -> dict:
    kpis = build_treasury_kpis(ctx=ctx)
    cash_flow = build_cash_flow_analysis(accounts=ctx["accounts"], forecasts=ctx["forecasts"])
    liquidity_trends = build_liquidity_trends(accounts=ctx["accounts"], forecasts=ctx["forecasts"])
    investment = compute_portfolio_performance(investments=ctx["investments"])
    funding = build_funding_analysis(
        accounts=ctx["accounts"],
        forecasts=ctx["forecasts"],
        funding_needs=ctx["funding_needs"],
    )

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "audience": "executive",
        "headline": {
            "total_cash": kpis["kpis"]["total_cash"],
            "liquidity_gap": kpis["kpis"]["liquidity_gap"],
            "working_capital": kpis["kpis"]["working_capital"],
            "investment_return_pct": kpis["kpis"]["investment_return_pct"],
            "funding_gap": kpis["kpis"]["funding_gap"],
            "open_risk_alerts": kpis["kpis"]["open_risk_alerts"],
        },
        "cash_flow_summary": {
            "net_cash_flow_30d": cash_flow["net_cash_flow_30d"],
            "cash_flow_ratio": cash_flow["cash_flow_ratio"],
        },
        "liquidity_trend": liquidity_trends["trend_direction"],
        "investment_summary": {
            "portfolio_value": investment["total_current_value"],
            "return_pct": investment["return_pct"],
        },
        "funding_status": funding["funding_priority"],
        "risk_exposures": kpis["risk_exposures"],
        "recommendations_count": len(ctx.get("recommendations", [])),
    }


def build_cfo_dashboard(*, ctx: dict) -> dict:
    kpis = build_treasury_kpis(ctx=ctx)
    bank = build_bank_balance_analysis(accounts=ctx["accounts"])
    forecast = build_forecast_accuracy(
        forecast_plans=ctx["forecast_plans"], accounts=ctx["accounts"]
    )
    fx = build_currency_exposure(
        accounts=ctx["accounts"],
        investments=ctx["investments"],
        rates=ctx["rates"],
        fx_transactions=ctx["fx_transactions"],
    )
    wc = build_working_capital_kpis(accounts=ctx["accounts"])
    funding = build_funding_analysis(
        accounts=ctx["accounts"],
        forecasts=ctx["forecasts"],
        funding_needs=ctx["funding_needs"],
    )

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "audience": "cfo",
        "treasury_kpis": kpis["kpis"],
        "bank_balance_analysis": bank,
        "forecast_accuracy": forecast,
        "currency_exposure": {
            "net_fx_impact": fx["net_fx_impact"],
            "high_concentration": fx["high_concentration_currencies"],
        },
        "working_capital_kpis": wc,
        "funding_analysis": funding,
        "investment_performance": compute_portfolio_performance(
            investments=ctx["investments"]
        ),
        "liquidity_trends": build_liquidity_trends(
            accounts=ctx["accounts"], forecasts=ctx["forecasts"]
        ),
    }


def build_analytics_dashboard(*, ctx: dict) -> dict:
    return {
        "as_of": datetime.now(UTC).isoformat(),
        "summary": {
            "total_cash": compute_liquidity(ctx["accounts"])["total_balance"],
            "capability_count": len(ANALYTICS_CATALOG),
            "recommendation_count": len(ctx.get("recommendations", [])),
            "forecast_plan_count": len(ctx["forecast_plans"]),
            "investment_count": len(ctx["investments"]),
        },
        "treasury_kpis": build_treasury_kpis(ctx=ctx)["kpis"],
        "executive_headline": build_executive_dashboard(ctx=ctx)["headline"],
        "cfo_highlights": {
            "bank_concentration_pct": build_bank_balance_analysis(accounts=ctx["accounts"])[
                "top_bank_concentration_pct"
            ],
            "forecast_accuracy_pct": build_forecast_accuracy(
                forecast_plans=ctx["forecast_plans"], accounts=ctx["accounts"]
            )["avg_forecast_accuracy_pct"],
            "working_capital": build_working_capital_kpis(accounts=ctx["accounts"])[
                "working_capital"
            ]["working_capital"],
        },
    }


def generate_treasury_recommendations(*, ctx: dict) -> dict:
    accounts = ctx["accounts"]
    forecasts = ctx["forecasts"]
    pools = ctx["pools"]
    liquidity_opts = optimization_recommendations(
        accounts=accounts, forecasts=forecasts, pools=pools
    )

    recommendations: list[dict] = list(liquidity_opts.get("recommendations", []))

    bank = build_bank_balance_analysis(accounts=accounts)
    if bank["top_bank_concentration_pct"] > 60:
        recommendations.append(
            _rec(
                priority="medium",
                category="cash_concentration",
                action="diversify_bank_deposits",
                detail=f"Top bank holds {bank['top_bank_concentration_pct']}% of balances",
                explanation="High bank concentration increases counterparty risk.",
                confidence=0.87,
            )
        )

    funding = compute_funding_needs(
        accounts=accounts, forecasts=forecasts, funding_needs=ctx["funding_needs"]
    )
    if funding["total_funding_gap"] > 0:
        recommendations.append(
            _rec(
                priority="high",
                category="funding_strategy",
                action="establish_credit_facility",
                detail=f"Funding gap of {funding['total_funding_gap']:.2f} identified",
                explanation="Secure committed funding lines before shortfall materializes.",
                confidence=0.91,
            )
        )

    fx = build_currency_exposure(
        accounts=accounts,
        investments=ctx["investments"],
        rates=ctx["rates"],
        fx_transactions=ctx["fx_transactions"],
    )
    for pos in fx["high_concentration_currencies"]:
        recommendations.append(
            _rec(
                priority="medium",
                category="currency_exposure",
                action="hedge_or_rebalance_fx",
                detail=f"{pos['currency']} at {pos.get('portfolio_pct', 0)}% of portfolio",
                explanation="Reduce FX concentration through hedging or conversion.",
                confidence=0.84,
            )
        )

    gap = compute_liquidity_gap(accounts=accounts, forecasts=forecasts)
    if gap["coverage_ratio"] < 1.0:
        recommendations.append(
            _rec(
                priority="high",
                category="operational_efficiency",
                action="accelerate_collections",
                detail=f"Coverage ratio {gap['coverage_ratio']:.2f} below 1.0",
                explanation="Improve receivables collection to strengthen cash coverage.",
                confidence=0.86,
            )
        )

    by_category: dict[str, list[dict]] = {}
    for rec in recommendations:
        by_category.setdefault(rec["category"], []).append(rec)

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "recommendation_count": len(recommendations),
        "by_category": by_category,
        "liquidity_optimization": [r for r in recommendations if r["category"] in {"funding", "cash_pool", "liquidity"}],
        "funding_strategy": [r for r in recommendations if r["category"] == "funding_strategy"],
        "cash_concentration": [r for r in recommendations if r["category"] == "cash_concentration"],
        "operational_efficiency": [r for r in recommendations if r["category"] == "operational_efficiency"],
        "recommendations": recommendations,
        "autonomous_execution": False,
    }


def generate_ai_treasury_assistant(*, ctx: dict) -> dict:
    kpis = build_treasury_kpis(ctx=ctx)
    trends = build_liquidity_trends(accounts=ctx["accounts"], forecasts=ctx["forecasts"])
    recs = generate_treasury_recommendations(ctx=ctx)
    forecast_acc = build_forecast_accuracy(
        forecast_plans=ctx["forecast_plans"], accounts=ctx["accounts"]
    )

    insights: list[str] = []
    if kpis["kpis"]["liquidity_gap"] < 0:
        insights.append(
            f"Liquidity gap of {abs(kpis['kpis']['liquidity_gap']):.2f} — prioritize funding actions."
        )
    if trends["trend_direction"] == "declining":
        insights.append("Daily liquidity trend is declining — review outflow commitments.")
    if forecast_acc["accuracy_rating"] == "low":
        insights.append("Forecast accuracy is low — recalibrate cash forecast assumptions.")
    if kpis["kpis"]["open_risk_alerts"] > 0:
        insights.append(
            f"{kpis['kpis']['open_risk_alerts']} open risk alert(s) require treasury attention."
        )
    if not insights:
        insights.append("Treasury position is stable — monitor concentration and funding runway.")

    top_recs = sorted(recs["recommendations"], key=lambda r: r["priority"] == "high", reverse=True)[:5]

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "assistant": "treasury_ai",
        "insights": insights,
        "top_recommendations": top_recs,
        "kpi_snapshot": kpis["kpis"],
        "recommendation_summary": {
            "total": recs["recommendation_count"],
            "liquidity_optimization": len(recs["liquidity_optimization"]),
            "funding_strategy": len(recs["funding_strategy"]),
            "cash_concentration": len(recs["cash_concentration"]),
            "operational_efficiency": len(recs["operational_efficiency"]),
        },
        "explanation": (
            f"AI assistant analyzed {len(ctx['accounts'])} accounts, "
            f"{len(ctx['investments'])} investments, and {len(ctx['forecast_plans'])} forecast plans. "
            f"Generated {len(insights)} insight(s) and {recs['recommendation_count']} recommendation(s)."
        ),
        "autonomous_execution": False,
    }
