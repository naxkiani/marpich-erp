"""Multi-Currency Treasury Engine."""
from __future__ import annotations

from datetime import UTC, date, datetime

from contexts.treasury.domain.aggregates.multi_currency_engine import (
    BASE_CURRENCY,
    FxTransactionType,
    RateType,
)
from contexts.treasury.domain.aggregates.treasury_account import TreasuryAccount

MULTI_CURRENCY_CATALOG: dict[str, dict] = {
    "currency_positions": {"label": "Currency Positions", "supported": True},
    "currency_conversion": {"label": "Currency Conversion", "supported": True},
    "exchange_gain": {"label": "Exchange Gain", "supported": True},
    "exchange_loss": {"label": "Exchange Loss", "supported": True},
    "revaluation": {"label": "Revaluation", "supported": True},
    "cross_currency_transfer": {"label": "Cross Currency Transfer", "supported": True},
    RateType.CENTRAL_BANK.value: {"label": "Central Bank Rates", "supported": True},
    RateType.MARKET.value: {"label": "Market Rates", "supported": True},
    RateType.MANUAL.value: {"label": "Manual Rates", "supported": True},
    RateType.HISTORICAL.value: {"label": "Historical Rates", "supported": True},
    "fx_reports": {"label": "FX Reports", "supported": True},
    "ai_fx_recommendations": {"label": "AI FX Recommendations", "autonomous_execution": False},
}

DEFAULT_MARKET_RATES: dict[str, float] = {
    "EUR": 0.92,
    "GBP": 0.79,
    "AED": 3.67,
    "SAR": 3.75,
    "JPY": 157.5,
}


def list_multi_currency_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in MULTI_CURRENCY_CATALOG.items()]


def _rate_lookup(
    rates: list[dict],
    quote_currency: str,
    rate_type: str | None = None,
) -> float | None:
    candidates = [r for r in rates if r["quote_currency"] == quote_currency]
    if rate_type:
        candidates = [r for r in candidates if r["rate_type"] == rate_type]
    if not candidates:
        return None
    candidates.sort(key=lambda x: x.get("effective_date", ""), reverse=True)
    return candidates[0]["rate"]


def convert_amount(
    *,
    amount: float,
    from_currency: str,
    to_currency: str,
    rates: list[dict],
    rate_type: str | None = None,
) -> tuple[float, float]:
    if from_currency == to_currency:
        return amount, 1.0

    if from_currency == BASE_CURRENCY:
        rate = _rate_lookup(rates, to_currency, rate_type)
        if not rate:
            raise ValueError("rate_not_found")
        return round(amount * rate, 2), rate

    if to_currency == BASE_CURRENCY:
        rate = _rate_lookup(rates, from_currency, rate_type)
        if not rate or rate == 0:
            raise ValueError("rate_not_found")
        return round(amount / rate, 2), rate

    via_base = convert_amount(
        amount=amount, from_currency=from_currency, to_currency=BASE_CURRENCY, rates=rates, rate_type=rate_type
    )
    final = convert_amount(
        amount=via_base[0], from_currency=BASE_CURRENCY, to_currency=to_currency, rates=rates, rate_type=rate_type
    )
    cross_rate = round(final[0] / amount, 6) if amount else 0
    return final[0], cross_rate


def compute_currency_positions(
    *,
    accounts: list[TreasuryAccount],
    investments: list[dict],
    rates: list[dict],
) -> dict:
    by_currency: dict[str, dict] = {}

    for account in accounts:
        if not account.is_active:
            continue
        c = account.currency
        bucket = by_currency.setdefault(
            c,
            {"currency": c, "local_balance": 0.0, "account_count": 0, "base_equivalent": 0.0},
        )
        bucket["local_balance"] = round(bucket["local_balance"] + account.balance, 2)
        bucket["account_count"] += 1

    for inv in investments:
        if inv.get("status") not in {"active", "matured"}:
            continue
        c = inv.get("currency", BASE_CURRENCY)
        bucket = by_currency.setdefault(
            c,
            {"currency": c, "local_balance": 0.0, "account_count": 0, "base_equivalent": 0.0},
        )
        bucket["local_balance"] = round(bucket["local_balance"] + inv.get("current_value", 0), 2)

    total_base = 0.0
    positions = []
    for c, data in sorted(by_currency.items()):
        local = data["local_balance"]
        if c == BASE_CURRENCY:
            base_eq = local
        else:
            try:
                base_eq, _ = convert_amount(
                    amount=local, from_currency=c, to_currency=BASE_CURRENCY, rates=rates, rate_type=RateType.MARKET.value
                )
            except ValueError:
                base_eq = 0.0
        data["base_equivalent"] = base_eq
        total_base += base_eq
        positions.append(data)

    for pos in positions:
        pos["portfolio_pct"] = round(pos["base_equivalent"] / total_base * 100, 2) if total_base else 0

    return {
        "base_currency": BASE_CURRENCY,
        "as_of": datetime.now(UTC).isoformat(),
        "total_base_equivalent": round(total_base, 2),
        "positions": positions,
        "currency_count": len(positions),
    }


def compute_revaluation(
    *,
    currency: str,
    book_balance: float,
    prior_rate: float,
    new_rate: float,
) -> dict:
    if currency == BASE_CURRENCY:
        return {
            "currency": currency,
            "book_balance": book_balance,
            "prior_rate": prior_rate,
            "new_rate": new_rate,
            "prior_base_value": book_balance,
            "new_base_value": book_balance,
            "gain_loss": 0.0,
            "result_type": None,
        }

    prior_base = round(book_balance / prior_rate, 2) if prior_rate else 0
    new_base = round(book_balance / new_rate, 2) if new_rate else 0
    gain_loss = round(new_base - prior_base, 2)
    result_type = None
    if gain_loss > 0:
        result_type = FxTransactionType.EXCHANGE_GAIN.value
    elif gain_loss < 0:
        result_type = FxTransactionType.EXCHANGE_LOSS.value

    return {
        "currency": currency,
        "book_balance": book_balance,
        "prior_rate": prior_rate,
        "new_rate": new_rate,
        "prior_base_value": prior_base,
        "new_base_value": new_base,
        "gain_loss": gain_loss,
        "result_type": result_type,
    }


def build_fx_report(
    *,
    positions: dict,
    transactions: list[dict],
    rates: list[dict],
) -> dict:
    gains = sum(t.get("gain_loss", 0) for t in transactions if t.get("gain_loss", 0) > 0)
    losses = sum(abs(t.get("gain_loss", 0)) for t in transactions if t.get("gain_loss", 0) < 0)
    conversions = [t for t in transactions if t.get("transaction_type") == FxTransactionType.CONVERSION.value]
    revaluations = [t for t in transactions if t.get("transaction_type") == FxTransactionType.REVALUATION.value]
    transfers = [
        t for t in transactions if t.get("transaction_type") == FxTransactionType.CROSS_CURRENCY_TRANSFER.value
    ]

    by_rate_type: dict[str, int] = {}
    for r in rates:
        rt = r.get("rate_type", "unknown")
        by_rate_type[rt] = by_rate_type.get(rt, 0) + 1

    return {
        "report_date": date.today().isoformat(),
        "base_currency": BASE_CURRENCY,
        "summary": {
            "total_positions": positions.get("currency_count", 0),
            "total_base_equivalent": positions.get("total_base_equivalent", 0),
            "total_exchange_gains": round(gains, 2),
            "total_exchange_losses": round(losses, 2),
            "net_fx_impact": round(gains - losses, 2),
            "conversion_count": len(conversions),
            "revaluation_count": len(revaluations),
            "cross_currency_transfer_count": len(transfers),
        },
        "positions": positions.get("positions", []),
        "rates_by_type": by_rate_type,
        "recent_transactions": transactions[:15],
    }


def build_fx_dashboard(
    *,
    positions: dict,
    transactions: list[dict],
    rates: list[dict],
) -> dict:
    report = build_fx_report(positions=positions, transactions=transactions, rates=rates)
    market_rates = [r for r in rates if r.get("rate_type") == RateType.MARKET.value]
    return {
        "as_of": datetime.now(UTC).isoformat(),
        "summary": report["summary"],
        "positions": positions,
        "market_rates": market_rates[:10],
        "recent_transactions": transactions[:10],
        "fx_report": report,
    }


def generate_ai_fx_recommendations(
    *,
    positions: dict,
    rates: list[dict],
    transactions: list[dict],
) -> dict:
    recommendations: list[dict] = []
    pos_list = positions.get("positions", [])
    non_base = [p for p in pos_list if p["currency"] != BASE_CURRENCY]

    if non_base:
        largest = max(non_base, key=lambda p: p.get("portfolio_pct", 0))
        if largest.get("portfolio_pct", 0) > 40:
            recommendations.append(
                {
                    "priority": "high",
                    "category": "concentration",
                    "message": f"{largest['currency']} is {largest['portfolio_pct']}% of portfolio — consider rebalancing.",
                    "autonomous_execution": False,
                }
            )

    eur_rate = _rate_lookup(rates, "EUR", RateType.MARKET.value)
    eur_hist = _rate_lookup(rates, "EUR", RateType.HISTORICAL.value)
    if eur_rate and eur_hist and eur_rate > eur_hist * 1.05:
        recommendations.append(
            {
                "priority": "medium",
                "category": "rate_movement",
                "message": f"EUR market rate {eur_rate} is 5%+ above historical {eur_hist} — favorable conversion window.",
                "autonomous_execution": False,
            }
        )

    recent_losses = [t for t in transactions if t.get("gain_loss", 0) < 0][-5:]
    if len(recent_losses) >= 3:
        recommendations.append(
            {
                "priority": "high",
                "category": "exchange_loss",
                "message": f"{len(recent_losses)} recent exchange losses — review rate sources and timing.",
                "autonomous_execution": False,
            }
        )

    if len(pos_list) < 2:
        recommendations.append(
            {
                "priority": "low",
                "category": "diversification",
                "message": "Single-currency exposure — consider multi-currency accounts for natural hedging.",
                "autonomous_execution": False,
            }
        )

    if not recommendations:
        recommendations.append(
            {
                "priority": "low",
                "category": "balanced",
                "message": "FX position appears balanced — no immediate action required.",
                "autonomous_execution": False,
            }
        )

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "position_summary": positions.get("summary", positions),
        "recommendations": recommendations,
        "autonomous_execution": False,
    }
