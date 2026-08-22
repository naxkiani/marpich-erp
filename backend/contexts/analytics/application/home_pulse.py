"""Home pulse — catalog counts with provenance. Not enterprise business KPIs."""
from __future__ import annotations

from typing import Any


SIGNAL_CLASS_CATALOG_COUNT = "CATALOG_COUNT"
DATA_QUALITY_WARNING = "DATA_QUALITY_WARNING"
DATA_NOT_AVAILABLE = "DATA_NOT_AVAILABLE"


def _count(value: Any) -> int:
    return len(value) if isinstance(value, list) else 0


def build_home_pulse(
    *,
    tenant_id: str,
    metrics: Any,
    dashboards: Any,
    alerts: Any,
) -> dict[str, Any]:
    """Tenant-scoped catalog sizes. Never revenue, customers, risk, or predictions."""
    return {
        "metrics_count": _count(metrics),
        "dashboards_count": _count(dashboards),
        "alerts_count": _count(alerts),
        "tenant_id": tenant_id,
        "signal_class": SIGNAL_CLASS_CATALOG_COUNT,
        "production_kpis": DATA_NOT_AVAILABLE,
        "data_quality": {
            "status": DATA_QUALITY_WARNING,
            "reason": "catalog_counts_are_not_enterprise_kpis",
            "freshness": DATA_NOT_AVAILABLE,
            "confidence": DATA_NOT_AVAILABLE,
        },
        "provenance": {
            "source_system": "analytics",
            "dataset": "metric_definitions,dashboards,alert_rules",
            "calculation": "len(list_by_tenant)",
            "tenant_id": tenant_id,
        },
    }
