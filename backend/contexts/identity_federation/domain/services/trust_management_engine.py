"""Trust management engine — trust hierarchy, scoring, lifecycle."""
from __future__ import annotations

TRUST_ENTITY_TYPES = (
    "organization", "partner", "tenant", "identity", "device",
    "application", "service", "certificate",
)

TRUST_LIFECYCLE = ("pending", "active", "suspended", "revoked", "expired")


def compute_trust_score(
    *,
    base_score: int = 50,
    certificate_valid: bool = True,
    mfa_enforced: bool = False,
    federation_history_days: int = 0,
    prior_incidents: int = 0,
    partner_verified: bool = False,
) -> dict:
    score = base_score
    factors: list[str] = []
    if certificate_valid:
        score += 10
        factors.append("valid_certificate")
    else:
        score -= 30
        factors.append("invalid_certificate")
    if mfa_enforced:
        score += 15
        factors.append("mfa_enforced")
    if federation_history_days > 365:
        score += 10
        factors.append("long_federation_history")
    if prior_incidents > 0:
        score -= min(40, prior_incidents * 10)
        factors.append("prior_incidents")
    if partner_verified:
        score += 20
        factors.append("partner_verified")
    score = max(0, min(100, score))
    level = _score_to_level(score)
    return {"trust_score": score, "trust_level": level, "factors": factors}


def _score_to_level(score: int) -> str:
    if score >= 85:
        return "verified"
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def evaluate_trust_hierarchy(
    *,
    organization_trust: int,
    partner_trust: int,
    identity_trust: int,
    device_trust: int,
) -> dict:
    """Aggregate trust across hierarchy — weighted minimum (weakest link)."""
    weights = {"organization": 0.25, "partner": 0.25, "identity": 0.30, "device": 0.20}
    scores = {
        "organization": organization_trust,
        "partner": partner_trust,
        "identity": identity_trust,
        "device": device_trust,
    }
    composite = sum(scores[k] * weights[k] for k in weights)
    return {
        "composite_trust_score": int(composite),
        "trust_level": _score_to_level(int(composite)),
        "hierarchy": scores,
        "weakest_link": min(scores, key=scores.get),
    }


def trust_lifecycle_transition(current_status: str, event: str) -> str | None:
    transitions = {
        ("pending", "verify"): "active",
        ("active", "suspend"): "suspended",
        ("suspended", "reactivate"): "active",
        ("active", "revoke"): "revoked",
        ("active", "expire"): "expired",
        ("suspended", "revoke"): "revoked",
    }
    return transitions.get((current_status, event))


TRUST_DIMENSIONS = (
    "identity",
    "organization",
    "partner",
    "device",
    "session",
    "behavior",
    "application",
    "network",
    "certificate",
    "token",
)


def evaluate_enterprise_trust(
    *,
    identity: int = 50,
    organization: int = 50,
    partner: int = 50,
    device: int = 50,
    session: int = 50,
    behavior: int = 50,
    application: int = 50,
    network: int = 50,
    certificate: int = 50,
    token: int = 50,
) -> dict:
    """Multi-dimensional enterprise trust score with weakest-link detection."""
    dims = {
        "identity": identity,
        "organization": organization,
        "partner": partner,
        "device": device,
        "session": session,
        "behavior": behavior,
        "application": application,
        "network": network,
        "certificate": certificate,
        "token": token,
    }
    weights = {
        "identity": 0.14,
        "organization": 0.12,
        "partner": 0.10,
        "device": 0.12,
        "session": 0.10,
        "behavior": 0.10,
        "application": 0.08,
        "network": 0.08,
        "certificate": 0.08,
        "token": 0.08,
    }
    composite = int(sum(dims[k] * weights[k] for k in dims))
    return {
        "trust_score": composite,
        "trust_level": _score_to_level(composite),
        "dimensions": dims,
        "weakest_link": min(dims, key=dims.get),
        "lifecycle": TRUST_LIFECYCLE,
    }


def append_trust_history(history: list[dict], *, score: int, level: str, reason: str) -> list[dict]:
    from datetime import UTC, datetime

    entry = {
        "score": score,
        "level": level,
        "reason": reason,
        "at": datetime.now(UTC).isoformat(),
    }
    history = list(history) + [entry]
    return history[-100:]


def recalculate_trust(*, prior_score: int, delta: int, reason: str) -> dict:
    score = max(0, min(100, prior_score + delta))
    return {
        "prior_score": prior_score,
        "delta": delta,
        "trust_score": score,
        "trust_level": _score_to_level(score),
        "reason": reason,
        "recalculated": True,
    }


def cross_organization_trust_contract(
    *,
    partner_type: str,
    source_org: str,
    target_org: str,
    legal_policy_ref: str | None = None,
) -> dict:
    """Federation agreement / legal trust policy template (config-driven)."""
    templates = {
        "government": {"assurance": "high", "loa": "substantial", "retention_years": 10},
        "bank": {"assurance": "high", "loa": "high", "retention_years": 7},
        "university": {"assurance": "medium", "loa": "substantial", "retention_years": 5},
        "hospital": {"assurance": "high", "loa": "high", "retention_years": 10},
        "tax_authority": {"assurance": "high", "loa": "high", "retention_years": 10},
        "insurance": {"assurance": "medium", "loa": "substantial", "retention_years": 7},
        "holding": {"assurance": "medium", "loa": "substantial", "retention_years": 5},
        "international": {"assurance": "medium", "loa": "substantial", "retention_years": 5},
        "partner": {"assurance": "medium", "loa": "low", "retention_years": 3},
    }
    tmpl = templates.get(partner_type, templates["partner"])
    return {
        "contract_type": "federation_agreement",
        "partner_type": partner_type,
        "source_org": source_org,
        "target_org": target_org,
        "legal_policy_ref": legal_policy_ref or f"policy.trust.{partner_type}",
        "terms": tmpl,
        "status": "draft",
    }
