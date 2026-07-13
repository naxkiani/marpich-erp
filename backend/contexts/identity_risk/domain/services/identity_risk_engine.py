"""Identity risk scoring engine — explainable, rule-based."""
from __future__ import annotations

from contexts.identity_risk.domain.aggregates.identity_risk_platform import (
    IdentityRiskCapability,
    RiskLevel,
)

POLICY_KEYS = [
    "identity_risk.scoring.enabled",
    "identity_risk.score.threshold",
    "identity_risk.step_up.threshold",
    "identity_risk.directory.bulk_create_threshold",
]

CAPABILITY_LABELS = {
    IdentityRiskCapability.RISK_SIGNAL_CATALOG.value: "Risk Signal Catalog",
    IdentityRiskCapability.AUTHENTICATION_RISK_SCORING.value: "Authentication Risk Scoring",
    IdentityRiskCapability.DIRECTORY_SYNC_RISK_SCORING.value: "Directory Sync Risk Scoring",
    IdentityRiskCapability.FEDERATION_RISK_SCORING.value: "Federation Risk Scoring",
    IdentityRiskCapability.ANOMALY_DETECTION.value: "Anomaly Detection",
    IdentityRiskCapability.RISK_SCORE_REGISTRY.value: "Risk Score Registry",
    IdentityRiskCapability.STEP_UP_RECOMMENDATION.value: "Step-Up Recommendation",
    IdentityRiskCapability.POLICY_DRIVEN_RISK.value: "Policy-Driven Risk",
    IdentityRiskCapability.IDENTITY_RISK_DASHBOARD.value: "Identity Risk Dashboard",
    IdentityRiskCapability.IDENTITY_RISK_API.value: "Identity Risk API",
}

RISK_SIGNALS = [
    {"signal": "auth.login", "label": "Authentication Login", "source": "authentication"},
    {"signal": "auth.federation", "label": "Federation Login", "source": "authentication"},
    {"signal": "directory.sync", "label": "Directory Sync", "source": "directory"},
    {"signal": "directory.scim", "label": "SCIM Provisioning", "source": "scim"},
]

AUTH_METHOD_WEIGHTS = {
    "password": 10,
    "webauthn": 5,
    "oidc": 15,
    "saml": 20,
}


def list_capability_catalog() -> list[dict]:
    return [
        {"capability": c.value, "label": CAPABILITY_LABELS.get(c.value, c.name.replace("_", " ").title())}
        for c in IdentityRiskCapability
    ]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def list_risk_signals() -> list[dict]:
    return list(RISK_SIGNALS)


def dependency_map() -> dict:
    return {
        "nodes": [
            {"id": "identity_risk", "type": "platform", "label": "Identity Risk"},
            {"id": "authentication", "type": "platform", "label": "Authentication"},
            {"id": "directory", "type": "platform", "label": "Directory"},
            {"id": "authorization", "type": "platform", "label": "Authorization PDP"},
        ],
        "edges": [
            {"from": "authentication", "to": "identity_risk", "type": "risk_signal"},
            {"from": "directory", "to": "identity_risk", "type": "risk_signal"},
            {"from": "identity_risk", "to": "authorization", "type": "step_up_recommendation"},
        ],
        "explainable": True,
    }


def classify_risk_level(score: int, *, threshold: int) -> str:
    if score >= threshold + 40:
        return RiskLevel.CRITICAL.value
    if score >= threshold + 20:
        return RiskLevel.HIGH.value
    if score >= threshold:
        return RiskLevel.MEDIUM.value
    return RiskLevel.LOW.value


def score_authentication_event(
    *,
    auth_method: str,
    is_new_user: bool = False,
    failed_attempts_24h: int = 0,
) -> tuple[int, list[dict], str]:
    factors: list[dict] = []
    score = AUTH_METHOD_WEIGHTS.get(auth_method, 12)
    factors.append({"factor": "auth_method", "weight": score, "value": auth_method})
    if is_new_user:
        factors.append({"factor": "new_user_provisioned", "weight": 15, "value": True})
        score += 15
    if failed_attempts_24h > 5:
        bump = min(failed_attempts_24h * 2, 30)
        factors.append({"factor": "failed_logins_24h", "weight": bump, "value": failed_attempts_24h})
        score += bump
    explanation = f"Authentication via {auth_method} scored {score} based on {len(factors)} factor(s)."
    return score, factors, explanation


def score_directory_sync_event(
    *,
    users_synced: int,
    users_created: int,
    bulk_create_threshold: int,
) -> tuple[int, list[dict], str]:
    factors: list[dict] = []
    score = 5
    factors.append({"factor": "users_synced", "weight": 5, "value": users_synced})
    if users_created > 0:
        create_weight = min(users_created * 3, 45)
        factors.append({"factor": "users_created", "weight": create_weight, "value": users_created})
        score += create_weight
    if users_created >= bulk_create_threshold:
        bulk_weight = 25
        factors.append({"factor": "bulk_create_anomaly", "weight": bulk_weight, "value": users_created})
        score += bulk_weight
    explanation = (
        f"Directory sync scored {score}: {users_created} created of {users_synced} synced "
        f"(threshold {bulk_create_threshold})."
    )
    return score, factors, explanation


def score_scim_provision_event(*, is_new_user: bool) -> tuple[int, list[dict], str]:
    factors: list[dict] = []
    score = 8 if is_new_user else 3
    factors.append({"factor": "scim_provision", "weight": score, "value": is_new_user})
    explanation = f"SCIM provisioning scored {score} (new_user={is_new_user})."
    return score, factors, explanation


def build_dashboard(
    *,
    profile: dict | None,
    scores: list[dict],
    alerts: list[dict],
) -> dict:
    by_level: dict[str, int] = {}
    for item in scores:
        level = str(item.get("risk_level", "low"))
        by_level[level] = by_level.get(level, 0) + 1
    return {
        "summary": {
            "capabilities": len(list_capability_catalog()),
            "risk_scores": len(scores),
            "anomaly_alerts": len(alerts),
            "unacknowledged_alerts": len([a for a in alerts if not a.get("acknowledged")]),
            "risk_distribution": by_level,
        },
        "profile": profile,
    }
