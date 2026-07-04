"""Currency Engine — rate resolution, conversion, gain/loss, revaluation."""
from __future__ import annotations

from datetime import date

from contexts.financial_kernel.domain.aggregates.currency import (
    ExchangeRate,
    ExchangeRateSnapshot,
    RateSource,
    RateType,
)

RATE_PRIORITY = [
    RateType.MANUAL,
    RateType.CENTRAL_BANK,
    RateType.SPOT,
    RateType.AVERAGE,
    RateType.HISTORICAL,
]


def convert_amount(amount: float, rate: float) -> float:
    return round(amount * rate, 2)


def resolve_rate_from_list(
    rates: list[ExchangeRate],
    *,
    from_currency: str,
    to_currency: str,
    rate_type: str | None = None,
    as_of_date: str | None = None,
) -> ExchangeRate | None:
    if from_currency == to_currency:
        return None
    target_date = as_of_date or date.today().isoformat()
    candidates = [
        r
        for r in rates
        if r.is_active
        and r.from_currency == from_currency
        and r.to_currency == to_currency
        and r.effective_date <= target_date
    ]
    if rate_type:
        typed = [r for r in candidates if r.rate_type == rate_type]
        if typed:
            candidates = typed
    if not candidates:
        inverse = [
            r
            for r in rates
            if r.is_active
            and r.from_currency == to_currency
            and r.to_currency == from_currency
            and r.effective_date <= target_date
        ]
        if rate_type:
            inverse = [r for r in inverse if r.rate_type == rate_type]
        if inverse:
            best = sorted(inverse, key=lambda r: (r.effective_date, r.created_at), reverse=True)[0]
            return ExchangeRate.create(
                tenant_id=best.tenant_id,
                from_currency=from_currency,
                to_currency=to_currency,
                rate=round(1 / best.rate, 8),
                rate_type=best.rate_type,
                rate_source=best.rate_source,
                effective_date=best.effective_date,
                provider=best.provider,
            )
        if rate_type:
            return None
        return _resolve_via_priority(rates, from_currency, to_currency, target_date)
    return sorted(candidates, key=lambda r: (r.effective_date, r.created_at), reverse=True)[0]


def _resolve_via_priority(
    rates: list[ExchangeRate], from_currency: str, to_currency: str, as_of_date: str
) -> ExchangeRate | None:
    for priority in RATE_PRIORITY:
        match = resolve_rate_from_list(
            rates,
            from_currency=from_currency,
            to_currency=to_currency,
            rate_type=priority.value,
            as_of_date=as_of_date,
        )
        if match:
            return match
    return None


def build_rate_snapshot(
    *,
    tenant_id: str,
    transaction_currency: str,
    base_currency: str,
    reporting_currency: str,
    transaction_to_base: ExchangeRate | None,
    transaction_to_reporting: ExchangeRate | None,
    journal_id: str | None = None,
    source_context: str | None = None,
    source_document_id: str | None = None,
) -> ExchangeRateSnapshot:
    base_rate = transaction_to_base.rate if transaction_to_base else 1.0
    reporting_rate = transaction_to_reporting.rate if transaction_to_reporting else base_rate
    rate_type = (
        transaction_to_base.rate_type
        if transaction_to_base
        else RateType.SPOT.value
    )
    rate_source = (
        transaction_to_base.rate_source
        if transaction_to_base
        else RateSource.SYSTEM.value
    )
    effective_date = (
        transaction_to_base.effective_date
        if transaction_to_base
        else date.today().isoformat()
    )
    return ExchangeRateSnapshot.from_rates(
        tenant_id=tenant_id,
        transaction_currency=transaction_currency,
        base_currency=base_currency,
        reporting_currency=reporting_currency,
        transaction_to_base_rate=base_rate,
        transaction_to_reporting_rate=reporting_rate,
        rate_type=rate_type,
        rate_source=rate_source,
        effective_date=effective_date,
        journal_id=journal_id,
        source_context=source_context,
        source_document_id=source_document_id,
    )


def compute_revaluation_lines(
    balances: list[dict],
    *,
    new_rates: dict[str, float],
    base_currency: str,
) -> list[dict]:
    """Compute unrealized gain/loss per foreign currency balance."""
    lines = []
    for row in balances:
        currency = row.get("currency", base_currency)
        if currency == base_currency:
            continue
        old_base = float(row.get("base_balance", 0))
        foreign_balance = float(row.get("foreign_balance", 0))
        new_rate = new_rates.get(currency)
        if new_rate is None:
            continue
        revalued_base = round(foreign_balance * new_rate, 2)
        diff = round(revalued_base - old_base, 2)
        lines.append(
            {
                "currency": currency,
                "foreign_balance": foreign_balance,
                "old_base_balance": old_base,
                "new_base_balance": revalued_base,
                "new_rate": new_rate,
                "gain": diff if diff > 0 else 0,
                "loss": abs(diff) if diff < 0 else 0,
                "net": diff,
            }
        )
    return lines
