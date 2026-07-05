"""Enterprise Treasury Risk Platform Engine."""
from __future__ import annotations

from datetime import UTC, datetime

from contexts.treasury.domain.aggregates.risk_engine import (
    AlertSeverity,
    LimitUnit,
    RiskType,
    STRESS_SCENARIOS,
)
from contexts.treasury.domain.aggregates.treasury_account import TreasuryAccount
from contexts.treasury.domain.services.treasury_engine import compute_liquidity

RISK_CATALOG: dict[str, dict] = {
    RiskType.LIQUIDITY_RISK.value: {"label": "Liquidity Risk", "supported": True},
    RiskType.INTEREST_RATE_RISK.value: {"label": "Interest Rate Risk", "supported": True},
    RiskType.FOREIGN_EXCHANGE_RISK.value: {"label": "Foreign Exchange Risk", "supported": True},
    RiskType.COUNTERPARTY_RISK.value: {"label": "Counterparty Risk", "supported": True},
    RiskType.OPERATIONAL_RISK.value: {"label": "Operational Risk", "supported": True},
    "limit_management": {"label": "Limit Management", "supported": True},
    "exposure_monitoring": {"label": "Exposure Monitoring", "supported": True},
    "stress_testing": {"label": "Stress Testing", "scenarios": list(STRESS_SCENARIOS.keys())},
    "risk_alerts": {"label": "Risk Alerts", "supported": True},
    "risk_dashboard": {"label": "Risk Dashboard", "supported": True},
    "ai_risk_scoring": {"label": "AI Risk Scoring", "autonomous_execution": False},
}

BASE_CURRENCY = "USD"


def list_risk_catalog() -> list[dict]:
    return [{"capability": k, **v} for k, v in RISK_CATALOG.items()]


def list_stress_scenarios() -> list[dict]:
    return [{"scenario": k, **v} for k, v in STRESS_SCENARIOS.items()]


def compute_liquidity_risk(*, accounts: list[TreasuryAccount], funding_gap: float = 0.0) -> dict:
    liquidity = compute_liquidity(accounts)
    total = liquidity["total_balance"] or 1
    liquid = liquidity["liquid_balance"]
    ratio = round(liquid / total * 100, 2) if total else 0
    coverage = round(liquid / funding_gap, 2) if funding_gap > 0 else None
    return {
        "risk_type": RiskType.LIQUIDITY_RISK.value,
        "liquid_balance": liquid,
        "total_balance": total,
        "liquidity_ratio_pct": ratio,
        "funding_gap": round(funding_gap, 2),
        "coverage_ratio": coverage,
        "exposure_value": ratio,
        "unit": LimitUnit.PERCENT.value,
    }


def compute_interest_rate_risk(*, investments: list[dict]) -> dict:
    bearing = [i for i in investments if i.get("interest_rate", 0) > 0 and i.get("status") == "active"]
    total_principal = sum(i.get("principal_amount", 0) for i in bearing)
    weighted_rate = 0.0
    duration_sensitivity = 0.0

    for inv in bearing:
        principal = inv.get("principal_amount", 0)
        rate = inv.get("interest_rate", 0)
        weight = principal / total_principal if total_principal else 0
        weighted_rate += rate * weight
        duration_sensitivity += principal * rate / 100

    rate_shock_impact = round(duration_sensitivity * 0.01, 2)
    return {
        "risk_type": RiskType.INTEREST_RATE_RISK.value,
        "bearing_instruments": len(bearing),
        "total_principal": round(total_principal, 2),
        "weighted_avg_rate_pct": round(weighted_rate, 4),
        "duration_sensitivity": round(duration_sensitivity, 2),
        "rate_shock_100bps_impact": rate_shock_impact,
        "exposure_value": rate_shock_impact,
        "unit": LimitUnit.AMOUNT.value,
    }


def compute_fx_risk(*, accounts: list[TreasuryAccount], investments: list[dict]) -> dict:
    by_currency: dict[str, float] = {}
    for a in accounts:
        if a.is_active:
            by_currency[a.currency] = by_currency.get(a.currency, 0) + a.balance
    for inv in investments:
        if inv.get("status") == "active":
            c = inv.get("currency", BASE_CURRENCY)
            by_currency[c] = by_currency.get(c, 0) + inv.get("current_value", 0)

    total = sum(by_currency.values()) or 1
    non_base = {c: v for c, v in by_currency.items() if c != BASE_CURRENCY}
    fx_exposure = sum(non_base.values())
    fx_pct = round(fx_exposure / total * 100, 2)

    return {
        "risk_type": RiskType.FOREIGN_EXCHANGE_RISK.value,
        "base_currency": BASE_CURRENCY,
        "by_currency": {k: round(v, 2) for k, v in by_currency.items()},
        "non_base_exposure": round(fx_exposure, 2),
        "non_base_pct": fx_pct,
        "exposure_value": fx_pct,
        "unit": LimitUnit.PERCENT.value,
    }


def compute_counterparty_risk(*, accounts: list[TreasuryAccount]) -> dict:
    bank_accounts = [a for a in accounts if a.is_active and a.account_type == "bank"]
    total = sum(a.balance for a in bank_accounts) or 1
    by_bank: dict[str, float] = {}
    for a in bank_accounts:
        bank = a.bank_name or "Unknown Bank"
        by_bank[bank] = by_bank.get(bank, 0) + a.balance

    concentrations = [
        {"counterparty": bank, "balance": round(bal, 2), "concentration_pct": round(bal / total * 100, 2)}
        for bank, bal in sorted(by_bank.items(), key=lambda x: -x[1])
    ]
    max_conc = concentrations[0]["concentration_pct"] if concentrations else 0

    return {
        "risk_type": RiskType.COUNTERPARTY_RISK.value,
        "bank_accounts": len(bank_accounts),
        "total_bank_balance": round(total, 2),
        "concentrations": concentrations,
        "max_concentration_pct": max_conc,
        "exposure_value": max_conc,
        "unit": LimitUnit.PERCENT.value,
    }


def compute_operational_risk(
    *,
    open_alerts: int = 0,
    pending_approvals: int = 0,
    reconciliation_exceptions: int = 0,
) -> dict:
    score = open_alerts * 2 + pending_approvals + reconciliation_exceptions
    return {
        "risk_type": RiskType.OPERATIONAL_RISK.value,
        "open_alerts": open_alerts,
        "pending_approvals": pending_approvals,
        "reconciliation_exceptions": reconciliation_exceptions,
        "operational_score": score,
        "exposure_value": score,
        "unit": LimitUnit.COUNT.value,
    }


def compute_all_exposures(
    *,
    accounts: list[TreasuryAccount],
    investments: list[dict],
    funding_gap: float = 0.0,
    open_alerts: int = 0,
    pending_approvals: int = 0,
) -> dict:
    exposures = {
        RiskType.LIQUIDITY_RISK.value: compute_liquidity_risk(accounts=accounts, funding_gap=funding_gap),
        RiskType.INTEREST_RATE_RISK.value: compute_interest_rate_risk(investments=investments),
        RiskType.FOREIGN_EXCHANGE_RISK.value: compute_fx_risk(accounts=accounts, investments=investments),
        RiskType.COUNTERPARTY_RISK.value: compute_counterparty_risk(accounts=accounts),
        RiskType.OPERATIONAL_RISK.value: compute_operational_risk(
            open_alerts=open_alerts,
            pending_approvals=pending_approvals,
        ),
    }
    return exposures


def check_limit_breaches(
    *,
    exposures: dict[str, dict],
    limits: list[dict],
) -> list[dict]:
    breaches: list[dict] = []
    limit_by_type = {lim["risk_type"]: lim for lim in limits if lim.get("is_active", True)}

    for risk_type, exposure in exposures.items():
        limit = limit_by_type.get(risk_type)
        if not limit:
            continue
        exp_val = exposure.get("exposure_value", 0)
        threshold = limit["threshold_value"]
        unit = limit["threshold_unit"]

        breached = False
        if unit == LimitUnit.PERCENT.value:
            if risk_type == RiskType.LIQUIDITY_RISK.value:
                breached = exp_val < threshold
            else:
                breached = exp_val > threshold
        elif unit == LimitUnit.AMOUNT.value:
            breached = exp_val > threshold
        elif unit == LimitUnit.COUNT.value:
            breached = exp_val > threshold

        if breached:
            severity = _severity_for_breach(risk_type, exp_val, threshold, unit)
            breaches.append(
                {
                    "risk_type": risk_type,
                    "limit_id": limit["id"],
                    "limit_name": limit["name"],
                    "exposure_value": exp_val,
                    "limit_value": threshold,
                    "severity": severity,
                    "message": _breach_message(risk_type, exp_val, threshold, unit),
                }
            )
    return breaches


def run_stress_test(
    *,
    scenario: str,
    exposures: dict[str, dict],
    accounts: list[TreasuryAccount],
    investments: list[dict],
) -> dict:
    spec = STRESS_SCENARIOS.get(scenario)
    if not spec:
        raise ValueError("invalid_stress_scenario")

    liquidity = exposures[RiskType.LIQUIDITY_RISK.value]
    rate_risk = exposures[RiskType.INTEREST_RATE_RISK.value]
    fx_risk = exposures[RiskType.FOREIGN_EXCHANGE_RISK.value]
    counterparty = exposures[RiskType.COUNTERPARTY_RISK.value]
    operational = exposures[RiskType.OPERATIONAL_RISK.value]

    if scenario == "liquidity_shock":
        shock = spec["shock_pct"] / 100
        stressed_liquid = round(liquidity["liquid_balance"] * (1 + shock), 2)
        impact = round(liquidity["liquid_balance"] - stressed_liquid, 2)
        result = {
            "baseline_liquid_balance": liquidity["liquid_balance"],
            "stressed_liquid_balance": stressed_liquid,
            "impact_amount": abs(impact),
            "survives": stressed_liquid > 0,
        }
    elif scenario == "rate_shock_up":
        bps = spec["rate_bps"]
        impact = round(rate_risk["duration_sensitivity"] * bps / 10000, 2)
        result = {
            "baseline_rate_exposure": rate_risk["duration_sensitivity"],
            "rate_shock_bps": bps,
            "mark_to_market_impact": impact,
            "survives": impact < rate_risk["total_principal"] * 0.1,
        }
    elif scenario == "fx_depreciation":
        shock = spec["fx_shock_pct"] / 100
        impact = round(fx_risk["non_base_exposure"] * abs(shock), 2)
        result = {
            "non_base_exposure": fx_risk["non_base_exposure"],
            "fx_shock_pct": spec["fx_shock_pct"],
            "valuation_impact": impact,
            "survives": impact < fx_risk["non_base_exposure"] * 0.15,
        }
    elif scenario == "counterparty_default":
        top = counterparty["concentrations"][0] if counterparty["concentrations"] else {}
        loss = top.get("balance", 0)
        result = {
            "counterparty": top.get("counterparty", "N/A"),
            "exposure_at_risk": loss,
            "survives": loss < counterparty["total_bank_balance"] * 0.5,
        }
    else:
        mult = spec["exception_multiplier"]
        stressed_score = operational["operational_score"] * mult
        result = {
            "baseline_operational_score": operational["operational_score"],
            "stressed_score": stressed_score,
            "survives": stressed_score < 50,
        }

    impact_score = _stress_impact_score(result)
    return {
        "scenario": scenario,
        "label": spec["label"],
        "risk_type": spec["risk_type"],
        "parameters": {k: v for k, v in spec.items() if k not in {"label", "risk_type"}},
        "results": result,
        "impact_score": impact_score,
    }


def build_risk_dashboard(
    *,
    exposures: dict[str, dict],
    limits: list[dict],
    alerts: list[dict],
    stress_runs: list[dict],
) -> dict:
    breaches = check_limit_breaches(exposures=exposures, limits=limits)
    open_alerts = [a for a in alerts if a.get("status") == "open"]
    composite = compute_composite_risk_score(exposures=exposures, limits=limits, alerts=alerts)

    return {
        "as_of": datetime.now(UTC).isoformat(),
        "summary": {
            "composite_risk_score": composite["score"],
            "risk_level": composite["level"],
            "active_limits": len([l for l in limits if l.get("is_active")]),
            "open_alerts": len(open_alerts),
            "limit_breaches": len(breaches),
            "stress_tests_run": len(stress_runs),
        },
        "exposures": exposures,
        "limit_breaches": breaches,
        "open_alerts": open_alerts[:10],
        "recent_stress_tests": stress_runs[:5],
        "by_risk_type": {rt: exposures[rt] for rt in exposures},
    }


def generate_ai_risk_scoring(
    *,
    exposures: dict[str, dict],
    limits: list[dict],
    alerts: list[dict],
) -> dict:
    composite = compute_composite_risk_score(exposures=exposures, limits=limits, alerts=alerts)
    breaches = check_limit_breaches(exposures=exposures, limits=limits)
    recommendations: list[dict] = []

    liq = exposures[RiskType.LIQUIDITY_RISK.value]
    if liq["liquidity_ratio_pct"] < 30:
        recommendations.append(
            {
                "priority": "high",
                "category": "liquidity_risk",
                "message": f"Liquidity ratio {liq['liquidity_ratio_pct']}% below 30% — increase liquid reserves.",
                "autonomous_execution": False,
            }
        )

    fx = exposures[RiskType.FOREIGN_EXCHANGE_RISK.value]
    if fx["non_base_pct"] > 20:
        recommendations.append(
            {
                "priority": "medium",
                "category": "foreign_exchange_risk",
                "message": f"Non-base currency exposure {fx['non_base_pct']}% — consider hedging.",
                "autonomous_execution": False,
            }
        )

    cp = exposures[RiskType.COUNTERPARTY_RISK.value]
    if cp["max_concentration_pct"] > 35:
        recommendations.append(
            {
                "priority": "high",
                "category": "counterparty_risk",
                "message": f"Bank concentration {cp['max_concentration_pct']}% — diversify counterparties.",
                "autonomous_execution": False,
            }
        )

    rate = exposures[RiskType.INTEREST_RATE_RISK.value]
    if rate["rate_shock_100bps_impact"] > 50000:
        recommendations.append(
            {
                "priority": "medium",
                "category": "interest_rate_risk",
                "message": f"100bps rate shock impact ${rate['rate_shock_100bps_impact']:,.0f} — review duration.",
                "autonomous_execution": False,
            }
        )

    if breaches:
        recommendations.append(
            {
                "priority": "critical",
                "category": "limit_breach",
                "message": f"{len(breaches)} active limit breach(es) — immediate review required.",
                "autonomous_execution": False,
            }
        )

    if not recommendations:
        recommendations.append(
            {
                "priority": "low",
                "category": "balanced",
                "message": "Risk profile within acceptable bounds.",
                "autonomous_execution": False,
            }
        )

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "composite_score": composite,
        "exposure_summary": {rt: e.get("exposure_value") for rt, e in exposures.items()},
        "breach_count": len(breaches),
        "recommendations": recommendations,
        "autonomous_execution": False,
    }


def compute_composite_risk_score(
    *,
    exposures: dict[str, dict],
    limits: list[dict],
    alerts: list[dict],
) -> dict:
    breaches = check_limit_breaches(exposures=exposures, limits=limits)
    open_alerts = [a for a in alerts if a.get("status") == "open"]

    score = 20.0
    score += len(breaches) * 15
    score += len(open_alerts) * 5

    liq = exposures[RiskType.LIQUIDITY_RISK.value]["liquidity_ratio_pct"]
    if liq < 20:
        score += 20
    elif liq < 40:
        score += 10

    fx_pct = exposures[RiskType.FOREIGN_EXCHANGE_RISK.value]["non_base_pct"]
    score += min(fx_pct * 0.5, 15)

    cp_pct = exposures[RiskType.COUNTERPARTY_RISK.value]["max_concentration_pct"]
    score += min(cp_pct * 0.3, 15)

    score = min(round(score, 1), 100)
    level = "low"
    if score >= 70:
        level = "critical"
    elif score >= 50:
        level = "high"
    elif score >= 30:
        level = "medium"

    return {"score": score, "level": level, "breach_count": len(breaches), "open_alert_count": len(open_alerts)}


def _severity_for_breach(risk_type: str, exposure: float, threshold: float, unit: str) -> str:
    if unit == LimitUnit.PERCENT.value and risk_type == RiskType.LIQUIDITY_RISK.value:
        gap = threshold - exposure
        if gap > 20:
            return AlertSeverity.CRITICAL.value
        if gap > 10:
            return AlertSeverity.HIGH.value
        return AlertSeverity.MEDIUM.value
    ratio = exposure / threshold if threshold else 2
    if ratio >= 2:
        return AlertSeverity.CRITICAL.value
    if ratio >= 1.5:
        return AlertSeverity.HIGH.value
    if ratio >= 1.2:
        return AlertSeverity.MEDIUM.value
    return AlertSeverity.LOW.value


def _breach_message(risk_type: str, exposure: float, threshold: float, unit: str) -> str:
    label = RISK_CATALOG.get(risk_type, {}).get("label", risk_type)
    if risk_type == RiskType.LIQUIDITY_RISK.value:
        return f"{label}: liquidity ratio {exposure}% below minimum {threshold}%"
    return f"{label}: exposure {exposure} {unit} exceeds limit {threshold} {unit}"


def _stress_impact_score(result: dict) -> float:
    if not result.get("survives", True):
        return 85.0
    if "impact_amount" in result:
        return min(round(result["impact_amount"] / 10000, 2), 75.0)
    if "mark_to_market_impact" in result:
        return min(round(result["mark_to_market_impact"] / 5000, 2), 75.0)
    if "valuation_impact" in result:
        return min(round(result["valuation_impact"] / 5000, 2), 75.0)
    if "exposure_at_risk" in result:
        return min(round(result["exposure_at_risk"] / 10000, 2), 75.0)
    return min(result.get("stressed_score", 20), 75.0)
