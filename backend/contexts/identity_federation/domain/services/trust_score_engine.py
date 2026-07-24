"""Dynamic trust score engine with explainability (P200-B6)."""
from __future__ import annotations

from contexts.identity_federation.domain.value_objects.trust_levels import (
    level_from_score,
    level_name,
)

DEFAULT_WEIGHTS: dict[str, float] = {
    "identity_assurance": 0.14,
    "authentication_strength": 0.12,
    "behavior_analysis": 0.10,
    "risk_signals": 0.14,
    "compliance_status": 0.10,
    "device_security": 0.10,
    "network_context": 0.08,
    "historical_trust": 0.10,
    "threat_intelligence": 0.06,
    "ai_analysis": 0.06,
}


def compute_continuous_score(
    *,
    inputs: dict[str, float | int] | None = None,
    weights: dict[str, float] | None = None,
    prior_score: int | None = None,
) -> dict:
    """Weighted trust score — never a black box (factors always returned)."""
    raw = {k: float(v) for k, v in (inputs or {}).items()}
    w = dict(weights or DEFAULT_WEIGHTS)
    # Fill missing inputs with mid defaults; risk inverted (high risk lowers score)
    filled: dict[str, float] = {}
    factors: list[str] = []
    for key in w:
        if key == "risk_signals":
            risk = float(raw.get(key, 30.0))
            filled[key] = max(0.0, 100.0 - risk)
            if risk >= 70:
                factors.append("elevated_risk")
            elif risk <= 20:
                factors.append("low_risk")
        else:
            filled[key] = float(raw.get(key, 50.0))
            if filled[key] >= 80:
                factors.append(f"strong_{key}")
            elif filled[key] <= 30:
                factors.append(f"weak_{key}")

    composite = int(round(sum(filled[k] * w[k] for k in w)))
    composite = max(0, min(100, composite))
    # Weakest-link penalty
    weakest = min(filled, key=filled.get)
    if filled[weakest] < 40:
        composite = max(0, composite - int((40 - filled[weakest]) * 0.25))
        factors.append(f"weakest_link_penalty:{weakest}")

    if prior_score is not None:
        # Smooth drift for continuous adaptive behavior
        composite = int(round(0.7 * composite + 0.3 * prior_score))
        factors.append("historical_smoothing")

    level = level_from_score(composite)
    return {
        "trust_score": composite,
        "enterprise_level": level,
        "enterprise_level_name": level_name(level),
        "dimension_breakdown": filled,
        "weights": w,
        "weakest_link": weakest,
        "factors": factors,
        "explainable": True,
        "never_trust_automatically": True,
        "continuous": True,
    }
