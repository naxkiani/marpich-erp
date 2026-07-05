"""Interest Calculation Engine — catalog, calculators, rate resolution."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.banking.domain.aggregates.interest_calculation_engine import (
    CalcFrequency,
    InterestMethod,
    RateType,
)

INTEREST_CALCULATION_CATALOG: dict[str, dict] = {
    CalcFrequency.DAILY.value: {"label": "Daily Interest", "supported": True},
    CalcFrequency.MONTHLY.value: {"label": "Monthly Interest", "supported": True},
    CalcFrequency.ANNUAL.value: {"label": "Annual Interest", "supported": True},
    InterestMethod.SIMPLE.value: {"label": "Simple Interest", "supported": True},
    InterestMethod.COMPOUND.value: {"label": "Compound Interest", "supported": True},
    "profit_sharing": {"label": "Profit Sharing", "supported": True, "extension_ready": True},
    "grace_period": {"label": "Grace Period", "policy_key": "interest.grace.period"},
    "penalty_interest": {"label": "Penalty Interest", "policy_key": "interest.penalty.rate"},
    RateType.FIXED.value: {"label": "Fixed Rate", "supported": True},
    RateType.FLOATING.value: {"label": "Floating Rate", "supported": True},
    RateType.PROMOTIONAL.value: {"label": "Promotional Rate", "supported": True},
    "historical_rate_changes": {"label": "Historical Rate Changes", "supported": True},
    "calculation_audit_history": {"label": "Calculation Audit History", "supported": True},
    "simulation_mode": {"label": "Simulation Mode", "supported": True},
    "configurable_policies": {"label": "Configurable Policies", "supported": True},
}

INTEREST_POLICY_KEYS: list[dict] = [
    {"key": "interest.calculation.method", "description": "Default simple vs compound method"},
    {"key": "interest.compounding.frequency", "description": "Compounding periods per year"},
    {"key": "interest.rate.fixed", "description": "Fixed rate parameters by product context"},
    {"key": "interest.rate.floating", "description": "Floating rate index and spread"},
    {"key": "interest.rate.promotional", "description": "Promotional rate duration and override"},
    {"key": "interest.grace.period", "description": "Grace period days before interest accrues"},
    {"key": "interest.penalty.rate", "description": "Penalty interest on overdue balances"},
    {"key": "interest.profit_sharing", "description": "Profit sharing pool allocation (extension-ready)"},
    {"key": "deposit.interest.rate", "description": "Deposit product interest rate (delegated)"},
    {"key": "loan.interest.rate", "description": "Loan product interest rate (delegated)"},
]


def list_interest_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in INTEREST_CALCULATION_CATALOG.items()]


def list_interest_policy_keys() -> list[dict]:
    return INTEREST_POLICY_KEYS


def apply_grace_period(*, days: int, grace_days: int) -> tuple[int, int]:
    """Return (effective_days, grace_days_applied)."""
    if grace_days <= 0 or days <= 0:
        return days, 0
    applied = min(grace_days, days)
    return max(0, days - grace_days), applied


def calculate_simple_interest(
    *, principal: float, rate_annual: float, days: int, day_count_basis: int = 365
) -> float:
    if principal <= 0 or rate_annual <= 0 or days <= 0:
        return 0.0
    return round(principal * (rate_annual / 100) * (days / day_count_basis), 2)


def calculate_compound_interest(
    *,
    principal: float,
    rate_annual: float,
    periods: int,
    compounding_periods_per_year: int = 12,
) -> float:
    if principal <= 0 or rate_annual <= 0 or periods <= 0:
        return 0.0
    r = rate_annual / 100 / compounding_periods_per_year
    amount = principal * ((1 + r) ** periods)
    return round(amount - principal, 2)


def frequency_to_days(frequency: str, *, periods: int = 1) -> int:
    if frequency == CalcFrequency.DAILY.value:
        return periods
    if frequency == CalcFrequency.MONTHLY.value:
        return periods * 30
    if frequency == CalcFrequency.ANNUAL.value:
        return periods * 365
    return periods


def calculate_interest_by_frequency(
    *,
    principal: float,
    rate_annual: float,
    frequency: str,
    method: str,
    periods: int = 1,
    compounding_periods_per_year: int = 12,
    days_override: int | None = None,
) -> tuple[float, dict]:
    days = days_override if days_override is not None else frequency_to_days(frequency, periods=periods)
    detail: dict = {"frequency": frequency, "method": method, "days": days, "periods": periods}

    if method == InterestMethod.COMPOUND.value:
        compound_periods = periods
        if frequency == CalcFrequency.DAILY.value:
            compound_periods = days
            compounding_periods_per_year = 365
        elif frequency == CalcFrequency.ANNUAL.value:
            compound_periods = periods
            compounding_periods_per_year = 1
        amount = calculate_compound_interest(
            principal=principal,
            rate_annual=rate_annual,
            periods=compound_periods,
            compounding_periods_per_year=compounding_periods_per_year,
        )
        detail["compounding_periods_per_year"] = compounding_periods_per_year
        detail["compound_periods"] = compound_periods
        return amount, detail

    amount = calculate_simple_interest(principal=principal, rate_annual=rate_annual, days=days)
    detail["day_count_basis"] = 365
    return amount, detail


def calculate_penalty_interest(
    *,
    principal: float,
    rate_annual: float,
    days_overdue: int,
    penalty_multiplier: float,
    policy_outcome: str | None,
) -> float:
    if policy_outcome == "waive_penalty" or days_overdue <= 0 or penalty_multiplier <= 0:
        return 0.0
    effective_rate = rate_annual * penalty_multiplier
    return calculate_simple_interest(principal=principal, rate_annual=effective_rate, days=days_overdue)


def calculate_profit_share(*, profit_pool: float, share_pct: float) -> float:
    """Extension-ready profit sharing allocation."""
    if profit_pool <= 0 or share_pct <= 0:
        return 0.0
    return round(profit_pool * (share_pct / 100), 2)


def resolve_floating_rate(*, index_rate_annual: float, spread_bps: float) -> float:
    return round(index_rate_annual + (spread_bps / 100), 6)


def resolve_promotional_rate(
    *,
    base_rate_annual: float,
    promotional_rate_annual: float | None,
    promotional_until: datetime | None,
    as_of: datetime | None = None,
) -> tuple[float, str]:
    now = as_of or datetime.now(UTC)
    if promotional_rate_annual is not None and promotional_until and now <= promotional_until:
        return promotional_rate_annual, RateType.PROMOTIONAL.value
    return base_rate_annual, RateType.FIXED.value


def resolve_historical_rate(
    *,
    profile_rate_annual: float,
    rate_changes: list[dict],
    as_of: datetime | None = None,
) -> tuple[float, str | None]:
    """Pick the rate effective at as_of from ordered change history."""
    now = as_of or datetime.now(UTC)
    effective_rate = profile_rate_annual
    effective_type: str | None = None
    for change in sorted(rate_changes, key=lambda c: c.get("effective_from", "")):
        eff_from = change.get("effective_from")
        if not eff_from:
            continue
        change_dt = datetime.fromisoformat(eff_from.replace("Z", "+00:00"))
        if change_dt <= now:
            effective_rate = float(change.get("new_rate_annual", effective_rate))
            effective_type = change.get("rate_type")
    return effective_rate, effective_type


def run_interest_calculation(
    *,
    principal: float,
    rate_annual: float,
    rate_type: str,
    frequency: str,
    method: str,
    periods: int = 1,
    days: int | None = None,
    grace_days: int = 0,
    days_overdue: int = 0,
    penalty_multiplier: float = 1.0,
    penalty_outcome: str | None = None,
    profit_pool: float = 0.0,
    profit_share_pct: float = 0.0,
    compounding_periods_per_year: int = 12,
) -> dict:
    raw_days = days if days is not None else frequency_to_days(frequency, periods=periods)
    effective_days, grace_applied = apply_grace_period(days=raw_days, grace_days=grace_days)

    interest, calc_detail = calculate_interest_by_frequency(
        principal=principal,
        rate_annual=rate_annual,
        frequency=frequency,
        method=method,
        periods=periods,
        compounding_periods_per_year=compounding_periods_per_year,
        days_override=effective_days if effective_days != raw_days else None,
    )

    penalty = calculate_penalty_interest(
        principal=principal,
        rate_annual=rate_annual,
        days_overdue=days_overdue,
        penalty_multiplier=penalty_multiplier,
        policy_outcome=penalty_outcome,
    )
    profit_share = calculate_profit_share(profit_pool=profit_pool, share_pct=profit_share_pct)

    return {
        "principal": round(principal, 2),
        "rate_annual": round(rate_annual, 6),
        "rate_type": rate_type,
        "frequency": frequency,
        "method": method,
        "raw_days": raw_days,
        "effective_days": effective_days if effective_days > 0 else raw_days,
        "grace_days_applied": grace_applied,
        "interest_amount": interest,
        "penalty_interest": penalty,
        "profit_share_amount": profit_share,
        "total_amount": round(interest + penalty + profit_share, 2),
        "calculation_detail": calc_detail,
    }


def build_interest_dashboard(
    *,
    profiles: list[dict],
    audits: list[dict],
    rate_changes: list[dict],
) -> dict:
    by_rate_type: dict[str, int] = {}
    by_method: dict[str, int] = {}
    total_interest = 0.0
    simulations = 0

    for audit in audits:
        by_method[audit.get("method", "unknown")] = by_method.get(audit.get("method", "unknown"), 0) + 1
        if audit.get("mode") == "simulation":
            simulations += 1
        else:
            total_interest += audit.get("interest_amount", 0)

    for profile in profiles:
        rt = profile.get("rate_type", "unknown")
        by_rate_type[rt] = by_rate_type.get(rt, 0) + 1

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "summary": {
            "rate_profile_count": len(profiles),
            "calculation_count": len(audits),
            "simulation_count": simulations,
            "rate_change_count": len(rate_changes),
            "total_interest_calculated": round(total_interest, 2),
        },
        "by_rate_type": by_rate_type,
        "by_method": by_method,
        "policy_keys": list_interest_policy_keys(),
    }
