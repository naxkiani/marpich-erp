"""Trust / mesh / risk observability metrics for federation C1."""
from __future__ import annotations

_metrics: dict[str, float] = {}


def increment(metric: str, value: float = 1.0) -> None:
    _metrics[metric] = _metrics.get(metric, 0.0) + value


def snapshot() -> dict:
    return {
        "trust_metrics": {
            "evaluations": int(_metrics.get("trust_eval_total", 0)),
            "propagations": int(_metrics.get("trust_propagate_total", 0)),
        },
        "federation_metrics": {
            "zt_decisions": int(_metrics.get("zt_decision_total", 0)),
            "mesh_routes": int(_metrics.get("mesh_route_total", 0)),
            "risk_decisions": int(_metrics.get("risk_decision_total", 0)),
        },
        "certificate_metrics": {
            "validations": int(_metrics.get("cert_validate_total", 0)),
        },
        "identity_metrics": {
            "broker_intel": int(_metrics.get("broker_intel_total", 0)),
        },
        "risk_metrics": {
            "high_risk": int(_metrics.get("high_risk_total", 0)),
        },
        "latency_metrics": {
            "zt_ms_total": _metrics.get("zt_ms_total", 0.0),
        },
        "prometheus_format": [
            *[f"# TYPE marpich_{k} counter\nmarpich_{k} {v}" for k, v in sorted(_metrics.items())],
        ],
    }


def reset() -> None:
    _metrics.clear()
