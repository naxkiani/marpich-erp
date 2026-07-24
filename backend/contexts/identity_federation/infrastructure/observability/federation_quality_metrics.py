"""Federation quality / DoD observability metrics (P200-B12)."""
from __future__ import annotations

_metrics: dict[str, float] = {}


def increment(metric: str, value: float = 1.0) -> None:
    _metrics[metric] = _metrics.get(metric, 0.0) + value


def record_latency(metric: str, ms: float) -> None:
    _metrics[f"{metric}_ms_total"] = _metrics.get(f"{metric}_ms_total", 0.0) + ms
    _metrics[f"{metric}_count"] = _metrics.get(f"{metric}_count", 0.0) + 1.0


def snapshot() -> dict:
    return {
        "quality_metrics": {
            "assessment_total": int(_metrics.get("qa_assessment_total", 0)),
            "gate_evaluate_total": int(_metrics.get("qa_gate_evaluate_total", 0)),
            "gate_blocked_total": int(_metrics.get("qa_gate_blocked_total", 0)),
            "release_certify_total": int(_metrics.get("qa_release_certify_total", 0)),
            "release_certify_passed_total": int(
                _metrics.get("qa_release_certify_passed_total", 0)
            ),
        },
        "prometheus_format": [
            f"# TYPE marpich_{k} counter",
            *[f"marpich_{k} {v}" for k, v in sorted(_metrics.items())],
        ],
    }


def reset() -> None:
    _metrics.clear()
