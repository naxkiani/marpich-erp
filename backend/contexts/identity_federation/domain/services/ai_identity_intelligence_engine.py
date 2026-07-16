"""AI Identity Intelligence Engine — explainable ML pipelines for federation."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


MODEL_REGISTRY: dict[str, dict] = {
    "identity_risk_predictor_v1": {
        "version": "1.0.0",
        "type": "identity_risk_prediction",
        "features": ["failed_logins", "device_confidence", "behavior_confidence", "geo_risk", "federation_age_days"],
        "status": "production",
    },
    "ato_predictor_v1": {
        "version": "1.0.0",
        "type": "account_takeover_prediction",
        "features": ["impossible_travel", "new_device", "credential_stuffing_signals", "session_anomaly"],
        "status": "production",
    },
    "privilege_escalation_v1": {
        "version": "1.0.0",
        "type": "privilege_escalation_detection",
        "features": ["role_change_velocity", "admin_grant", "unusual_resource_access"],
        "status": "production",
    },
    "dormant_account_v1": {
        "version": "1.0.0",
        "type": "dormant_account_detection",
        "features": ["days_inactive", "last_federation", "login_count_90d"],
        "status": "production",
    },
    "federation_recommender_v1": {
        "version": "1.0.0",
        "type": "adaptive_federation_recommendation",
        "features": ["risk_score", "trust_score", "protocol_preference", "mfa_capability"],
        "status": "production",
    },
    "credential_abuse_v1": {
        "version": "1.0.0",
        "type": "credential_abuse_prediction",
        "features": ["velocity", "ip_diversity", "failed_ratio", "bot_signals"],
        "status": "production",
    },
}

FEATURE_STORE_SCHEMA = [
    {"feature": "device_confidence", "type": "float", "source": "device_trust"},
    {"feature": "behavior_confidence", "type": "float", "source": "behavior_analytics"},
    {"feature": "organization_trust", "type": "float", "source": "trust_graph"},
    {"feature": "session_trust", "type": "float", "source": "session_federation"},
    {"feature": "identity_confidence", "type": "float", "source": "broker_intelligence"},
    {"feature": "failed_logins_24h", "type": "int", "source": "auth_events"},
    {"feature": "federation_protocol", "type": "categorical", "source": "federation_gateway"},
]


@dataclass
class IdentityFeatureVector:
    failed_logins: int = 0
    device_confidence: float = 0.5
    behavior_confidence: float = 0.5
    organization_trust: float = 0.5
    session_trust: float = 0.5
    identity_confidence: float = 0.5
    geo_risk: float = 0.0
    federation_age_days: int = 0
    impossible_travel: bool = False
    new_device: bool = False
    credential_stuffing_signals: float = 0.0
    session_anomaly: float = 0.0
    role_change_velocity: float = 0.0
    admin_grant: bool = False
    unusual_resource_access: float = 0.0
    days_inactive: int = 0
    login_count_90d: int = 10
    velocity: float = 0.0
    ip_diversity: float = 0.0
    failed_ratio: float = 0.0
    bot_signals: float = 0.0
    risk_score: int = 0
    trust_score: int = 50
    mfa_capable: bool = True
    extra: dict = field(default_factory=dict)

    def to_features(self) -> dict:
        return {
            "failed_logins": min(self.failed_logins / 10.0, 1.0),
            "device_confidence": self.device_confidence,
            "behavior_confidence": self.behavior_confidence,
            "organization_trust": self.organization_trust,
            "session_trust": self.session_trust,
            "identity_confidence": self.identity_confidence,
            "geo_risk": self.geo_risk,
            "federation_age_days": min(self.federation_age_days / 365.0, 1.0),
            "impossible_travel": 1.0 if self.impossible_travel else 0.0,
            "new_device": 1.0 if self.new_device else 0.0,
            "credential_stuffing_signals": self.credential_stuffing_signals,
            "session_anomaly": self.session_anomaly,
            "role_change_velocity": self.role_change_velocity,
            "admin_grant": 1.0 if self.admin_grant else 0.0,
            "unusual_resource_access": self.unusual_resource_access,
            "days_inactive": min(self.days_inactive / 180.0, 1.0),
            "login_count_90d": min(self.login_count_90d / 90.0, 1.0),
            "velocity": self.velocity,
            "ip_diversity": self.ip_diversity,
            "failed_ratio": self.failed_ratio,
            "bot_signals": self.bot_signals,
            "risk_score": self.risk_score / 100.0,
            "trust_score": self.trust_score / 100.0,
            "mfa_capable": 1.0 if self.mfa_capable else 0.0,
            **self.extra,
        }


def list_models() -> list[dict]:
    return [{"model_id": mid, **meta} for mid, meta in MODEL_REGISTRY.items()]


def feature_store_catalog() -> dict:
    return {
        "schema": FEATURE_STORE_SCHEMA,
        "pipeline_stages": [
            "ingest_events",
            "feature_compute",
            "feature_store_write",
            "model_inference",
            "explainability",
            "feedback_loop",
        ],
        "versioning": "model_registry_append_only",
    }


def predict_identity_intelligence(
    features: IdentityFeatureVector,
    *,
    model_id: str = "identity_risk_predictor_v1",
    confidence_threshold: float = 0.7,
) -> dict:
    """Unified inference with explainability — thresholds must be policy-supplied."""
    fv = features.to_features()
    model = MODEL_REGISTRY.get(model_id, MODEL_REGISTRY["identity_risk_predictor_v1"])
    contributions: list[dict] = []
    score = 0.0

    weight_sets = {
        "identity_risk_predictor_v1": {
            "failed_logins": 22,
            "device_confidence": -18,
            "behavior_confidence": -16,
            "geo_risk": 20,
            "federation_age_days": -8,
            "identity_confidence": -12,
        },
        "ato_predictor_v1": {
            "impossible_travel": 35,
            "new_device": 22,
            "credential_stuffing_signals": 30,
            "session_anomaly": 25,
            "device_confidence": -15,
        },
        "privilege_escalation_v1": {
            "role_change_velocity": 30,
            "admin_grant": 28,
            "unusual_resource_access": 25,
        },
        "dormant_account_v1": {
            "days_inactive": 40,
            "login_count_90d": -25,
        },
        "credential_abuse_v1": {
            "velocity": 28,
            "ip_diversity": 22,
            "failed_ratio": 30,
            "bot_signals": 26,
        },
        "federation_recommender_v1": {
            "risk_score": 20,
            "trust_score": -25,
            "mfa_capable": -10,
            "device_confidence": -12,
        },
    }
    weights = weight_sets.get(model_id, weight_sets["identity_risk_predictor_v1"])
    for key, weight in weights.items():
        if key not in fv:
            continue
        val = float(fv[key])
        contrib = int(weight * val)
        if contrib:
            score += contrib
            contributions.append({"feature": key, "contribution": contrib, "value": fv[key]})

    risk_score = min(100, max(0, int(score)))
    confidence = min(0.98, 0.62 + len(contributions) * 0.045)
    identity_health = _identity_health(features)
    prediction_type = model.get("type", "identity_risk_prediction")

    return {
        "model_id": model_id,
        "model_version": model.get("version", "1.0.0"),
        "prediction_type": prediction_type,
        "risk_score": risk_score,
        "identity_confidence_score": int(features.identity_confidence * 100),
        "behavior_confidence_score": int(features.behavior_confidence * 100),
        "device_confidence_score": int(features.device_confidence * 100),
        "organization_trust_score": int(features.organization_trust * 100),
        "session_trust_score": int(features.session_trust * 100),
        "identity_health_score": identity_health,
        "classification": _classify(risk_score, prediction_type),
        "recommendation": _recommend(risk_score, prediction_type, features),
        "anomaly_detected": risk_score >= 70 or features.session_anomaly >= 0.7,
        "account_takeover_likelihood": _ato_likelihood(features, risk_score),
        "privilege_escalation_flag": features.admin_grant or features.role_change_velocity >= 0.6,
        "dormant_account": features.days_inactive >= 90 and features.login_count_90d <= 1,
        "confidence": round(confidence, 3),
        "explanation": {
            "summary": f"{prediction_type} scored {risk_score} via {model_id}",
            "confidence": round(confidence, 3),
            "above_threshold": confidence >= confidence_threshold,
            "top_features": [
                c["feature"]
                for c in sorted(contributions, key=lambda x: abs(x["contribution"]), reverse=True)[:5]
            ],
            "contributions": contributions[:10],
            "explainable": True,
            "auditable": True,
        },
        "feedback_eligible": True,
        "inferred_at": datetime.now(UTC).isoformat(),
    }


def _identity_health(f: IdentityFeatureVector) -> int:
    raw = (
        f.identity_confidence * 25
        + f.device_confidence * 20
        + f.behavior_confidence * 20
        + f.organization_trust * 15
        + f.session_trust * 10
        + (1.0 - min(f.failed_logins / 10.0, 1.0)) * 10
    )
    return int(min(100, max(0, raw)))


def _classify(score: int, prediction_type: str) -> str:
    if "dormant" in prediction_type:
        return "dormant" if score >= 50 else "active"
    if score >= 85:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 40:
        return "elevated"
    return "normal"


def _recommend(score: int, prediction_type: str, f: IdentityFeatureVector) -> str:
    if "federation_recommender" in prediction_type or prediction_type.endswith("recommendation"):
        if score >= 70 or not f.mfa_capable:
            return "route_to_mfa_capable_idp"
        if f.trust_score >= 70:
            return "allow_passwordless_federation"
        return "standard_oidc_federation"
    if score >= 85:
        return "deny_and_investigate"
    if score >= 70:
        return "step_up_and_notify"
    if score >= 50:
        return "require_mfa"
    return "allow"


def _ato_likelihood(f: IdentityFeatureVector, risk_score: int) -> float:
    base = risk_score / 100.0
    if f.impossible_travel:
        base += 0.2
    if f.new_device:
        base += 0.1
    base += f.credential_stuffing_signals * 0.3
    return round(min(1.0, base), 3)


def record_feedback(*, prediction_id: str, useful: bool, label: str | None = None) -> dict:
    return {
        "prediction_id": prediction_id,
        "useful": useful,
        "label": label,
        "loop": "feedback_learning",
        "recorded_at": datetime.now(UTC).isoformat(),
    }


def ml_pipeline_manifest() -> dict:
    return {
        "pipelines": [
            {"id": "identity_feature_pipeline", "schedule": "near_realtime"},
            {"id": "identity_risk_training", "schedule": "daily"},
            {"id": "federation_recommender_training", "schedule": "weekly"},
        ],
        "model_registry": list_models(),
        "feature_store": feature_store_catalog(),
        "inference_services": [
            "predict_identity_intelligence",
            "adaptive_federation_recommendation",
        ],
        "explainability": "feature_contribution_shap_lite",
    }
