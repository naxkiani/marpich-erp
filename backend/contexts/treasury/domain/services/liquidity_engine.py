"""Enterprise Liquidity Engine — analytics, forecasting, AI, optimization."""
from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from contexts.treasury.domain.aggregates.liquidity_engine import LiquidityPeriod
from contexts.treasury.domain.aggregates.treasury_account import TreasuryAccount
from contexts.treasury.domain.services.treasury_engine import compute_liquidity

LIQUIDITY_ENGINE_CATALOG: dict[str, dict] = {
    "cash_position": {"label": "Cash Position", "supported": True},
    "daily_liquidity": {"label": "Daily Liquidity", "period": LiquidityPeriod.DAILY.value},
    "weekly_liquidity": {"label": "Weekly Liquidity", "period": LiquidityPeriod.WEEKLY.value},
    "monthly_liquidity": {"label": "Monthly Liquidity", "period": LiquidityPeriod.MONTHLY.value},
    "rolling_forecast": {"label": "Rolling Forecast", "horizon_weeks": 13},
    "cash_pools": {"label": "Cash Pools", "supported": True},
    "funding_needs": {"label": "Funding Needs", "supported": True},
    "liquidity_gap": {"label": "Liquidity Gap", "supported": True},
    "working_capital": {"label": "Working Capital", "supported": True},
    "liquidity_dashboard": {"label": "Liquidity Dashboard", "supported": True},
    "ai_liquidity_prediction": {"label": "AI Liquidity Prediction", "autonomous_execution": False},
    "optimization_recommendations": {"label": "Optimization Recommendations", "autonomous_execution": False},
}


def list_liquidity_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in LIQUIDITY_ENGINE_CATALOG.items()]


def _liquid_accounts(accounts: list[TreasuryAccount]) -> list[TreasuryAccount]:
    liquid_types = {"cash", "bank", "petty_cash"}
    return [a for a in accounts if a.is_active and a.account_type in liquid_types]


def compute_cash_position(*, accounts: list[TreasuryAccount]) -> dict:
    liquidity = compute_liquidity(accounts)
    positions = [
        {
            "account_id": str(a.id),
            "code": a.code,
            "name": a.name,
            "account_type": a.account_type,
            "currency": a.currency,
            "balance": a.balance,
        }
        for a in accounts
        if a.is_active
    ]
    return {
        "as_of": datetime.now(UTC).isoformat(),
        "total_balance": liquidity["total_balance"],
        "liquid_balance": liquidity["liquid_balance"],
        "restricted_balance": liquidity["restricted_balance"],
        "by_currency": liquidity["by_currency"],
        "by_account_type": liquidity["by_account_type"],
        "positions": positions,
    }


def _forecast_lines_from_forecasts(forecasts: list[dict]) -> list[dict]:
    lines: list[dict] = []
    for forecast in forecasts:
        for line in forecast.get("lines", []):
            lines.append(
                {
                    "date": line.get("date", ""),
                    "label": line.get("label", forecast.get("name", "")),
                    "inflow": float(line.get("inflow", 0)),
                    "outflow": float(line.get("outflow", 0)),
                    "scenario": forecast.get("scenario", "base"),
                }
            )
    return sorted(lines, key=lambda x: x["date"])


def _rollup_period_lines(
    *,
    opening_balance: float,
    forecast_lines: list[dict],
    period: str,
    periods: int,
) -> list[dict]:
    today = date.today()
    rows: list[dict] = []
    balance = opening_balance

    if period == LiquidityPeriod.DAILY.value:
        for i in range(periods):
            d = today + timedelta(days=i)
            day_key = d.isoformat()
            day_lines = [l for l in forecast_lines if l["date"] == day_key]
            inflow = round(sum(l["inflow"] for l in day_lines), 2)
            outflow = round(sum(l["outflow"] for l in day_lines), 2)
            if not day_lines and i > 0:
                inflow = round(balance * 0.002, 2)
                outflow = round(balance * 0.003, 2)
            opening = balance
            balance = round(balance + inflow - outflow, 2)
            rows.append(
                {
                    "period": day_key,
                    "label": d.strftime("%a %d %b"),
                    "opening_balance": opening,
                    "inflow": inflow,
                    "outflow": outflow,
                    "closing_balance": balance,
                    "net_flow": round(inflow - outflow, 2),
                }
            )
    elif period == LiquidityPeriod.WEEKLY.value:
        for i in range(periods):
            start = today + timedelta(weeks=i)
            end = start + timedelta(days=6)
            week_lines = [
                l
                for l in forecast_lines
                if l["date"] and start.isoformat() <= l["date"] <= end.isoformat()
            ]
            inflow = round(sum(l["inflow"] for l in week_lines), 2)
            outflow = round(sum(l["outflow"] for l in week_lines), 2)
            if not week_lines:
                inflow = round(balance * 0.01, 2)
                outflow = round(balance * 0.012, 2)
            opening = balance
            balance = round(balance + inflow - outflow, 2)
            rows.append(
                {
                    "period": f"W{i + 1}",
                    "label": f"{start.isoformat()} – {end.isoformat()}",
                    "opening_balance": opening,
                    "inflow": inflow,
                    "outflow": outflow,
                    "closing_balance": balance,
                    "net_flow": round(inflow - outflow, 2),
                }
            )
    else:
        for i in range(periods):
            month = (today.replace(day=1) + timedelta(days=32 * i)).replace(day=1)
            month_key = month.strftime("%Y-%m")
            month_lines = [l for l in forecast_lines if l["date"].startswith(month_key)]
            inflow = round(sum(l["inflow"] for l in month_lines), 2)
            outflow = round(sum(l["outflow"] for l in month_lines), 2)
            if not month_lines:
                inflow = round(balance * 0.04, 2)
                outflow = round(balance * 0.045, 2)
            opening = balance
            balance = round(balance + inflow - outflow, 2)
            rows.append(
                {
                    "period": month_key,
                    "label": month.strftime("%B %Y"),
                    "opening_balance": opening,
                    "inflow": inflow,
                    "outflow": outflow,
                    "closing_balance": balance,
                    "net_flow": round(inflow - outflow, 2),
                }
            )
    return rows


def compute_period_liquidity(
    *,
    accounts: list[TreasuryAccount],
    forecasts: list[dict],
    period: str,
    periods: int,
) -> dict:
    liquidity = compute_liquidity(accounts)
    opening = liquidity["liquid_balance"]
    forecast_lines = _forecast_lines_from_forecasts(forecasts)
    lines = _rollup_period_lines(
        opening_balance=opening,
        forecast_lines=forecast_lines,
        period=period,
        periods=periods,
    )
    total_inflow = round(sum(l["inflow"] for l in lines), 2)
    total_outflow = round(sum(l["outflow"] for l in lines), 2)
    closing = lines[-1]["closing_balance"] if lines else opening
    return {
        "period_type": period,
        "opening_balance": opening,
        "closing_balance": closing,
        "total_inflow": total_inflow,
        "total_outflow": total_outflow,
        "net_flow": round(total_inflow - total_outflow, 2),
        "lines": lines,
    }


def compute_rolling_forecast(
    *,
    accounts: list[TreasuryAccount],
    forecasts: list[dict],
    horizon_weeks: int = 13,
) -> dict:
    weekly = compute_period_liquidity(
        accounts=accounts,
        forecasts=forecasts,
        period=LiquidityPeriod.WEEKLY.value,
        periods=horizon_weeks,
    )
    min_balance = min((l["closing_balance"] for l in weekly["lines"]), default=0)
    return {
        "horizon_weeks": horizon_weeks,
        "opening_balance": weekly["opening_balance"],
        "projected_closing": weekly["closing_balance"],
        "minimum_balance": round(min_balance, 2),
        "weeks": weekly["lines"],
    }


def compute_cash_pools_view(
    *,
    pools: list[dict],
    accounts: list[TreasuryAccount],
) -> dict:
    account_map = {str(a.id): a for a in accounts}
    pool_views = []
    for pool in pools:
        members = []
        total = 0.0
        for acc_id in pool.get("member_account_ids", []):
            acc = account_map.get(acc_id)
            if acc:
                members.append(acc.to_dict())
                total += acc.balance
        pool_views.append(
            {
                **pool,
                "current_balance": round(total, 2),
                "surplus": round(total - pool.get("target_balance", 0), 2),
                "deficit": round(max(pool.get("minimum_balance", 0) - total, 0), 2),
                "members": members,
            }
        )
    return {
        "pool_count": len(pool_views),
        "total_pooled_balance": round(sum(p["current_balance"] for p in pool_views), 2),
        "pools": pool_views,
    }


def compute_funding_needs(
    *,
    accounts: list[TreasuryAccount],
    forecasts: list[dict],
    funding_needs: list[dict],
) -> dict:
    liquidity = compute_liquidity(accounts)
    available = liquidity["liquid_balance"]
    identified: list[dict] = list(funding_needs)

    rolling = compute_rolling_forecast(accounts=accounts, forecasts=forecasts)
    min_balance = rolling["minimum_balance"]
    if min_balance < 0:
        identified.append(
            {
                "label": "Rolling forecast shortfall",
                "required_amount": round(abs(min_balance) + available * 0.1, 2),
                "available_amount": available,
                "gap_amount": round(abs(min_balance), 2),
                "due_date": rolling["weeks"][-1]["label"] if rolling["weeks"] else "",
                "status": "open",
                "source": "rolling_forecast",
            }
        )

    total_gap = round(sum(n.get("gap_amount", 0) for n in identified), 2)
    return {
        "available_liquidity": available,
        "total_funding_gap": total_gap,
        "open_needs_count": len([n for n in identified if n.get("status") == "open"]),
        "needs": identified,
    }


def compute_liquidity_gap(
    *,
    accounts: list[TreasuryAccount],
    forecasts: list[dict],
) -> dict:
    liquidity = compute_liquidity(accounts)
    forecast_lines = _forecast_lines_from_forecasts(forecasts)
    projected_inflow = round(sum(l["inflow"] for l in forecast_lines), 2)
    projected_outflow = round(sum(l["outflow"] for l in forecast_lines), 2)
    position = liquidity["liquid_balance"]
    gap = round(position + projected_inflow - projected_outflow, 2)
    return {
        "cash_position": position,
        "projected_inflow": projected_inflow,
        "projected_outflow": projected_outflow,
        "liquidity_gap": gap,
        "surplus": gap if gap >= 0 else 0,
        "shortfall": abs(gap) if gap < 0 else 0,
        "coverage_ratio": round(position / projected_outflow, 4) if projected_outflow else 0,
    }


def compute_working_capital(*, accounts: list[TreasuryAccount]) -> dict:
    current_assets = round(
        sum(a.balance for a in accounts if a.is_active and a.account_type in {"cash", "bank", "petty_cash"}),
        2,
    )
    restricted = round(
        sum(a.balance for a in accounts if a.is_active and a.account_type in {"vault", "safe"}),
        2,
    )
    current_liabilities_proxy = round(current_assets * 0.35, 2)
    working_capital = round(current_assets - current_liabilities_proxy, 2)
    ratio = round(current_assets / current_liabilities_proxy, 4) if current_liabilities_proxy else 0
    return {
        "current_assets": current_assets,
        "restricted_assets": restricted,
        "current_liabilities_proxy": current_liabilities_proxy,
        "working_capital": working_capital,
        "current_ratio": ratio,
    }


def build_liquidity_dashboard(
    *,
    accounts: list[TreasuryAccount],
    forecasts: list[dict],
    pools: list[dict],
    funding_needs: list[dict],
) -> dict:
    cash_position = compute_cash_position(accounts=accounts)
    daily = compute_period_liquidity(
        accounts=accounts, forecasts=forecasts, period=LiquidityPeriod.DAILY.value, periods=30
    )
    weekly = compute_period_liquidity(
        accounts=accounts, forecasts=forecasts, period=LiquidityPeriod.WEEKLY.value, periods=12
    )
    monthly = compute_period_liquidity(
        accounts=accounts, forecasts=forecasts, period=LiquidityPeriod.MONTHLY.value, periods=12
    )
    rolling = compute_rolling_forecast(accounts=accounts, forecasts=forecasts)
    pools_view = compute_cash_pools_view(pools=pools, accounts=accounts)
    funding = compute_funding_needs(accounts=accounts, forecasts=forecasts, funding_needs=funding_needs)
    gap = compute_liquidity_gap(accounts=accounts, forecasts=forecasts)
    wc = compute_working_capital(accounts=accounts)

    return {
        "summary": {
            "cash_position": cash_position["liquid_balance"],
            "total_balance": cash_position["total_balance"],
            "liquidity_gap": gap["liquidity_gap"],
            "working_capital": wc["working_capital"],
            "funding_gap": funding["total_funding_gap"],
            "pool_count": pools_view["pool_count"],
            "rolling_minimum": rolling["minimum_balance"],
        },
        "cash_position": cash_position,
        "daily_liquidity": daily,
        "weekly_liquidity": weekly,
        "monthly_liquidity": monthly,
        "rolling_forecast": rolling,
        "cash_pools": pools_view,
        "funding_needs": funding,
        "liquidity_gap": gap,
        "working_capital": wc,
    }


def _recommendation(
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


def predict_liquidity_ai(
    *,
    accounts: list[TreasuryAccount],
    forecasts: list[dict],
    horizon_days: int = 30,
) -> dict:
    daily = compute_period_liquidity(
        accounts=accounts,
        forecasts=forecasts,
        period=LiquidityPeriod.DAILY.value,
        periods=horizon_days,
    )
    lines = daily["lines"]
    balances = [l["closing_balance"] for l in lines]
    if len(balances) >= 2:
        trend = (balances[-1] - balances[0]) / len(balances)
    else:
        trend = 0.0

    predictions = []
    last = balances[-1] if balances else daily["opening_balance"]
    for i in range(1, 8):
        predicted = round(last + trend * i, 2)
        predictions.append(
            {
                "day_offset": i,
                "predicted_balance": predicted,
                "confidence": round(max(0.55, 0.9 - i * 0.04), 2),
            }
        )

    risk_level = "low"
    if any(p["predicted_balance"] < 0 for p in predictions):
        risk_level = "high"
    elif any(p["predicted_balance"] < daily["opening_balance"] * 0.2 for p in predictions):
        risk_level = "medium"

    return {
        "horizon_days": horizon_days,
        "current_balance": daily["opening_balance"],
        "trend_per_day": round(trend, 2),
        "risk_level": risk_level,
        "predictions": predictions,
        "explanation": (
            f"Based on {len(lines)} daily liquidity periods, projected trend is "
            f"{'positive' if trend >= 0 else 'negative'} at {trend:+.2f}/day. "
            f"Risk assessed as {risk_level}."
        ),
        "autonomous_execution": False,
    }


def optimization_recommendations(
    *,
    accounts: list[TreasuryAccount],
    forecasts: list[dict],
    pools: list[dict],
) -> dict:
    recommendations: list[dict] = []
    liquidity = compute_liquidity(accounts)
    gap = compute_liquidity_gap(accounts=accounts, forecasts=forecasts)
    pools_view = compute_cash_pools_view(pools=pools, accounts=accounts)
    rolling = compute_rolling_forecast(accounts=accounts, forecasts=forecasts)

    if gap["shortfall"] > 0:
        recommendations.append(
            _recommendation(
                priority="high",
                category="funding",
                action="secure_funding",
                detail=f"Address liquidity shortfall of {gap['shortfall']:.2f}",
                explanation="Projected outflows exceed available cash plus inflows.",
                confidence=0.92,
            )
        )

    for pool in pools_view["pools"]:
        if pool["surplus"] > pool.get("target_balance", 0) * 0.1:
            recommendations.append(
                _recommendation(
                    priority="medium",
                    category="cash_pool",
                    action="sweep_surplus",
                    detail=f"Sweep {pool['surplus']:.2f} from pool {pool['code']}",
                    explanation="Pool balance exceeds target — sweep to operating account.",
                    confidence=0.85,
                )
            )
        if pool["deficit"] > 0:
            recommendations.append(
                _recommendation(
                    priority="high",
                    category="cash_pool",
                    action="fund_pool",
                    detail=f"Fund pool {pool['code']} by {pool['deficit']:.2f}",
                    explanation="Pool balance below minimum threshold.",
                    confidence=0.88,
                )
            )

    if liquidity["restricted_balance"] > liquidity["liquid_balance"] * 0.3:
        recommendations.append(
            _recommendation(
                priority="low",
                category="allocation",
                action="rebalance_restricted",
                detail="Reduce vault/safe concentration",
                explanation="Restricted cash exceeds 30% of liquid balance — consider reallocation.",
                confidence=0.75,
            )
        )

    if rolling["minimum_balance"] < rolling["opening_balance"] * 0.15:
        recommendations.append(
            _recommendation(
                priority="medium",
                category="forecast",
                action="build_buffer",
                detail="Maintain 15%+ liquidity buffer over rolling horizon",
                explanation="Rolling 13-week minimum balance drops below 15% of opening.",
                confidence=0.82,
            )
        )

    return {
        "recommendation_count": len(recommendations),
        "recommendations": recommendations,
        "autonomous_execution": False,
        "explainable": True,
    }
