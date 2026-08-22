"""Home pulse is catalog counts with DATA_QUALITY_WARNING — never invented KPIs."""
from __future__ import annotations

from contexts.analytics.application.home_pulse import (
    DATA_NOT_AVAILABLE,
    DATA_QUALITY_WARNING,
    SIGNAL_CLASS_CATALOG_COUNT,
    build_home_pulse,
)


def test_home_pulse_catalog_counts_are_not_business_kpis() -> None:
    pulse = build_home_pulse(
        tenant_id="t-demo",
        metrics=[{}, {}],
        dashboards=[{}],
        alerts=[],
    )
    assert pulse["metrics_count"] == 2
    assert pulse["dashboards_count"] == 1
    assert pulse["alerts_count"] == 0
    assert pulse["tenant_id"] == "t-demo"
    assert pulse["signal_class"] == SIGNAL_CLASS_CATALOG_COUNT
    assert pulse["production_kpis"] == DATA_NOT_AVAILABLE
    assert pulse["data_quality"]["status"] == DATA_QUALITY_WARNING
    assert pulse["data_quality"]["freshness"] == DATA_NOT_AVAILABLE
    assert pulse["data_quality"]["confidence"] == DATA_NOT_AVAILABLE
    assert pulse["provenance"]["source_system"] == "analytics"
    assert pulse["provenance"]["tenant_id"] == "t-demo"
    assert "revenue" not in pulse
    assert "customers" not in pulse
    assert "prediction" not in pulse
