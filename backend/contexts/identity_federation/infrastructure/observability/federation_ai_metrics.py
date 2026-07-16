"""AI / intelligence observability metrics (P198-C2)."""
from __future__ import annotations

_metrics: dict[str, float] = {}


def increment(metric: str, value: float = 1.0) -> None:
    _metrics[metric] = _metrics.get(metric, 0.0) + value


def snapshot() -> dict:
    return {
        "ai_metrics": {
            "inference_total": int(_metrics.get("ai_inference_total", 0)),
            "high_risk_total": int(_metrics.get("ai_high_risk_total", 0)),
            "insight_total": int(_metrics.get("ai_insight_total", 0)),
            "copilot_total": int(_metrics.get("ai_copilot_total", 0)),
            "feedback_total": int(_metrics.get("ai_feedback_total", 0)),
        },
        "identity_metrics": {
            "predictions": int(_metrics.get("ai_inference_total", 0)),
        },
        "trust_metrics": {},
        "risk_metrics": {
            "ai_high_risk": int(_metrics.get("ai_high_risk_total", 0)),
        },
        "prometheus_format": [
            *[f"# TYPE marpich_{k} counter\nmarpich_{k} {v}" for k, v in sorted(_metrics.items())],
        ],
    }


def reset() -> None:
    _metrics.clear()
