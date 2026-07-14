"""Federation protocol observability metrics."""
from __future__ import annotations

_metrics: dict[str, float] = {}


def increment(metric: str, value: float = 1.0) -> None:
    _metrics[metric] = _metrics.get(metric, 0.0) + value


def record_latency(metric: str, ms: float) -> None:
    _metrics[f"{metric}_ms_total"] = _metrics.get(f"{metric}_ms_total", 0.0) + ms
    _metrics[f"{metric}_count"] = _metrics.get(f"{metric}_count", 0.0) + 1.0


def snapshot() -> dict:
    login = int(_metrics.get("federation_login_total", 0))
    token = int(_metrics.get("federation_token_total", 0))
    sso = int(_metrics.get("federation_sso_total", 0))
    return {
        "federation_metrics": {"login_total": login, "token_total": token, "sso_total": sso},
        "sso_metrics": {"success_rate": round(sso / login, 4) if login else 0},
        "provisioning_metrics": {"scim_total": int(_metrics.get("federation_scim_total", 0))},
        "prometheus_format": [
            f"# TYPE marpich_{k} counter",
            *[f"marpich_{k} {v}" for k, v in sorted(_metrics.items())],
        ],
    }


def reset() -> None:
    _metrics.clear()
