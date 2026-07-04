"""Default marketplace seed listings."""
from __future__ import annotations

SEED_LISTINGS: list[tuple] = [
    (
        "com.marpich.demo-sales-widget",
        "widget",
        "Demo Sales KPI Widget",
        "Sample dashboard widget for sales metrics",
        "com.marpich",
        "Marpich Labs",
        "1.0.0",
        ["analytics.read", "sales.orders.read"],
        ["ui.dashboard.widget"],
        "strict",
        "community",
        "sha256:demo-widget-checksum-001",
        "sha256:demo-publisher-key-001",
    ),
    (
        "com.marpich.demo-report-pack",
        "report",
        "Demo Financial Reports",
        "Sample P&L and balance sheet templates",
        "com.marpich",
        "Marpich Labs",
        "2.1.0",
        ["finance.reports.read"],
        ["analytics.report.template"],
        "standard",
        "verified",
        "sha256:demo-report-checksum-002",
        "sha256:demo-publisher-key-002",
    ),
]
