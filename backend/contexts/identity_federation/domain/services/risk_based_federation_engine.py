"""Risk-based adaptive federation — dynamic trust, step-up, conditional access."""
from __future__ import annotations


RISK_SIGNALS = (
    "device",
    "behavior",
    "network",
    "organization",
    "certificate",
    "country",
    "transaction",
)


def score_federation_risk(
    *,
    device_risk: int = 0,
    behavior_risk: int = 0,
    network_risk: int = 0,
    organization_risk: int = 0,
    certificate_risk: int = 0,
    country_risk: int = 0,
    transaction_risk: int = 0,
) -> dict:
    weights = {
        "device": 0.20,
        "behavior": 0.20,
        "network": 0.15,
        "organization": 0.15,
        "certificate": 0.10,
        "country": 0.10,
        "transaction": 0.10,
    }
    scores = {
        "device": device_risk,
        "behavior": behavior_risk,
        "network": network_risk,
        "organization": organization_risk,
        "certificate": certificate_risk,
        "country": country_risk,
        "transaction": transaction_risk,
    }
    composite = int(sum(scores[k] * weights[k] for k in weights))
    return {
        "risk_score": min(100, composite),
        "signals": scores,
        "signal_catalog": list(RISK_SIGNALS),
        "level": _level(composite),
    }


def _level(score: int) -> str:
    if score >= 85:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def adaptive_federation_decision(
    *,
    risk_score: int,
    trust_score: int,
    step_up_threshold: int = 70,
    deny_threshold: int = 90,
    conditional_access_required: bool = False,
) -> dict:
    dynamic_trust = max(0, min(100, int((trust_score * 0.6) + ((100 - risk_score) * 0.4))))
    if risk_score >= deny_threshold or dynamic_trust < 20:
        action = "deny"
        approval = "rejected"
    elif risk_score >= step_up_threshold or conditional_access_required or dynamic_trust < 50:
        action = "step_up"
        approval = "conditional"
    else:
        action = "allow"
        approval = "auto_approved"
    return {
        "action": action,
        "dynamic_trust_level": _trust_label(dynamic_trust),
        "dynamic_trust_score": dynamic_trust,
        "dynamic_federation_approval": approval,
        "step_up_authentication": action == "step_up",
        "conditional_access": conditional_access_required or action == "step_up",
        "risk_score": risk_score,
        "trust_score": trust_score,
    }


def _trust_label(score: int) -> str:
    if score >= 85:
        return "verified"
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"
