"""Enterprise Observability engine — telemetry synthesis, dependency graph, dashboards."""
from __future__ import annotations

from pathlib import Path

import yaml

from contexts.enterprise_observability.domain.aggregates.enterprise_observability_platform import (
    AlertSeverity,
    HealthStatus,
    ObservabilityCapability,
)

POLICY_KEYS = [
    "enterprise_observability.tracing.enabled",
    "enterprise_observability.tracing.sampling_rate",
    "enterprise_observability.logging.retention_days",
    "enterprise_observability.metrics.enabled",
    "enterprise_observability.health_checks.enabled",
    "enterprise_observability.alerting.enabled",
    "enterprise_observability.incident.auto_create.enabled",
]

CAPABILITY_LABELS = {
    ObservabilityCapability.DISTRIBUTED_TRACING.value: "Distributed Tracing",
    ObservabilityCapability.CENTRALIZED_LOGGING.value: "Centralized Logging",
    ObservabilityCapability.METRICS.value: "Metrics",
    ObservabilityCapability.HEALTH_CHECKS.value: "Health Checks",
    ObservabilityCapability.BUSINESS_KPIS.value: "Business KPIs",
    ObservabilityCapability.EVENT_MONITORING.value: "Event Monitoring",
    ObservabilityCapability.QUEUE_MONITORING.value: "Queue Monitoring",
    ObservabilityCapability.API_MONITORING.value: "API Monitoring",
    ObservabilityCapability.WORKFLOW_MONITORING.value: "Workflow Monitoring",
    ObservabilityCapability.AI_MONITORING.value: "AI Monitoring",
    ObservabilityCapability.ALERTING.value: "Alerting",
    ObservabilityCapability.INCIDENT_MANAGEMENT.value: "Incident Management",
    ObservabilityCapability.SERVICE_DEPENDENCY_GRAPH.value: "Service Dependency Graph",
    ObservabilityCapability.OPERATIONAL_DASHBOARD.value: "Operational Dashboard",
}

PLATFORM_EDGES = [
    ("enterprise_api_gateway", "identity", "auth_delegate"),
    ("enterprise_api_gateway", "integration", "ingress_delegate"),
    ("enterprise_observability", "analytics", "metrics_delegate"),
    ("enterprise_observability", "notifications", "alert_delegate"),
    ("enterprise_observability", "security_incident", "incident_delegate"),
    ("enterprise_message_orchestration", "enterprise_event_bus", "transport_delegate"),
    ("enterprise_reliability_platform", "enterprise_event_bus", "delivery_delegate"),
    ("analytics", "notifications", "alert_delegate"),
    ("workflow", "analytics", "kpi_delegate"),
    ("ai_governance", "analytics", "ai_metrics_delegate"),
]


def list_capability_catalog() -> list[dict]:
    return [
        {"capability": c.value, "label": CAPABILITY_LABELS.get(c.value, c.name.replace("_", " ").title())}
        for c in ObservabilityCapability
    ]


def list_policy_keys() -> list[str]:
    return list(POLICY_KEYS)


def load_route_registry(*, registry_path: Path | None = None) -> dict:
    path = registry_path or Path(__file__).resolve().parents[4] / "core" / "gateway" / "route_registry.yaml"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def dependency_map(*, registry: dict | None = None) -> dict:
    reg = registry or load_route_registry()
    nodes: list[dict] = [
        {"id": "enterprise_observability", "type": "platform", "label": "Enterprise Observability"},
        {"id": "analytics", "type": "platform", "label": "Analytics"},
        {"id": "notifications", "type": "platform", "label": "Notifications"},
        {"id": "security_incident", "type": "platform", "label": "Security Incident"},
        {"id": "otel_collector", "type": "infrastructure", "label": "OpenTelemetry Collector"},
        {"id": "prometheus", "type": "infrastructure", "label": "Prometheus"},
        {"id": "loki", "type": "infrastructure", "label": "Loki"},
        {"id": "tempo", "type": "infrastructure", "label": "Tempo"},
    ]
    edges: list[dict] = [
        {"from": src, "to": dst, "type": edge_type}
        for src, dst, edge_type in PLATFORM_EDGES
    ]
    for section in ("public_routes", "platform_routes", "business_routes"):
        for route in reg.get(section, []):
            ctx = route.get("context_id")
            if ctx and not any(n["id"] == ctx for n in nodes):
                nodes.append({"id": ctx, "type": "context", "label": ctx.replace("_", " ").title()})
            if ctx:
                edges.append({
                    "from": "enterprise_api_gateway",
                    "to": ctx,
                    "type": "routes_to",
                })
    return {
        "nodes": nodes,
        "edges": edges,
        "multi_tenant": True,
        "unified_telemetry": True,
        "otel_bootstrap": "shared/infrastructure/observability/telemetry.py",
    }


def build_service_dependency_graph(*, registry: dict | None = None) -> dict:
    reg = registry or load_route_registry()
    services: dict[str, dict] = {}
    for section in ("public_routes", "platform_routes", "business_routes"):
        for route in reg.get(section, []):
            ctx = route.get("context_id", "unknown")
            services.setdefault(ctx, {
                "service_id": ctx,
                "label": ctx.replace("_", " ").title(),
                "routes": [],
                "dependencies": [],
            })
            services[ctx]["routes"].append(route.get("prefix", ""))
    for src, dst, edge_type in PLATFORM_EDGES:
        if src in services:
            services[src]["dependencies"].append({"target": dst, "type": edge_type})
        else:
            services.setdefault(src, {
                "service_id": src,
                "label": src.replace("_", " ").title(),
                "routes": [],
                "dependencies": [{"target": dst, "type": edge_type}],
            })
        if dst not in services:
            services.setdefault(dst, {
                "service_id": dst,
                "label": dst.replace("_", " ").title(),
                "routes": [],
                "dependencies": [],
            })
    for route in reg.get("platform_routes", []) + reg.get("business_routes", []):
        ctx = route.get("context_id")
        if ctx:
            services.setdefault("enterprise_api_gateway", {
                "service_id": "enterprise_api_gateway",
                "label": "Enterprise Api Gateway",
                "routes": [],
                "dependencies": [],
            })
            dep = {"target": ctx, "type": "routes_to"}
            if dep not in services["enterprise_api_gateway"]["dependencies"]:
                services["enterprise_api_gateway"]["dependencies"].append(dep)

    infra_ids = {"otel_collector", "prometheus", "loki", "tempo", "outbox_dispatcher", "kafka_connector", "rabbitmq_connector"}
    platform_ids = {
        "enterprise_observability", "enterprise_api_gateway", "analytics", "notifications",
        "security_incident", "enterprise_event_bus", "enterprise_message_orchestration",
        "enterprise_reliability_platform", "identity", "integration", "workflow", "ai_governance",
    }

    def node_type(service_id: str) -> str:
        if service_id in infra_ids:
            return "infrastructure"
        if service_id in platform_ids or service_id.startswith("enterprise_"):
            return "platform"
        if "connector" in service_id:
            return "connector"
        return "context"

    nodes = [
        {
            "id": s["service_id"],
            "label": s["label"],
            "type": node_type(s["service_id"]),
            "route_count": len(s["routes"]),
        }
        for s in services.values()
    ]
    edges: list[dict] = []
    seen_edges: set[tuple[str, str, str]] = set()
    for s in services.values():
        for dep in s["dependencies"]:
            key = (s["service_id"], dep["target"], dep["type"])
            if key in seen_edges:
                continue
            seen_edges.add(key)
            edges.append({"from": s["service_id"], "to": dep["target"], "type": dep["type"]})

    return {
        "services": list(services.values()),
        "nodes": nodes,
        "edges": edges,
        "total_services": len(services),
        "graph_type": "service_dependency",
    }


def evaluate_alert(*, value: float, operator: str, threshold: float) -> bool:
    ops = {
        "gt": value > threshold,
        "gte": value >= threshold,
        "lt": value < threshold,
        "lte": value <= threshold,
        "eq": value == threshold,
    }
    return ops.get(operator, False)


def aggregate_platform_status(*, health_checks: list[dict]) -> str:
    if not health_checks:
        return HealthStatus.HEALTHY.value
    statuses = {h.get("status") for h in health_checks}
    if HealthStatus.UNHEALTHY.value in statuses:
        return HealthStatus.UNHEALTHY.value
    if HealthStatus.DEGRADED.value in statuses:
        return HealthStatus.DEGRADED.value
    return HealthStatus.HEALTHY.value


def build_business_kpis(*, metrics: list[dict]) -> dict:
    kpi_keys = {
        "events.total": "Total Events",
        "users.created": "Users Created",
        "users.logged_in": "User Logins",
        "workflows.completed": "Workflows Completed",
        "documents.uploaded": "Documents Uploaded",
        "encounters.completed": "Encounters Completed",
    }
    by_key = {m["metric_key"]: m for m in metrics if m.get("metric_key") in kpi_keys}
    tiles = []
    for key, label in kpi_keys.items():
        m = by_key.get(key, {"value": 0, "unit": "count"})
        tiles.append({"metric_key": key, "label": label, "value": m.get("value", 0), "unit": m.get("unit", "count")})
    return {"kpis": tiles, "total_kpis": len(tiles)}


def build_event_monitoring(*, metrics: list[dict]) -> dict:
    event_metrics = [m for m in metrics if m.get("metric_key", "").startswith("events.")]
    total = sum(m.get("value", 0) for m in event_metrics)
    return {
        "events_per_minute": round(total / max(len(event_metrics), 1), 2),
        "top_event_types": sorted(event_metrics, key=lambda m: m.get("value", 0), reverse=True)[:5],
        "total_event_metrics": len(event_metrics),
    }


def build_queue_monitoring(*, metrics: list[dict]) -> dict:
    queue_keys = ["queue.outbox.pending", "queue.outbox.lag_seconds", "queue.outbox.failures", "queue.consumer.throughput"]
    readings = {m["metric_key"]: m for m in metrics if m.get("metric_key") in queue_keys}
    return {
        "pending": readings.get("queue.outbox.pending", {}).get("value", 0),
        "lag_seconds": readings.get("queue.outbox.lag_seconds", {}).get("value", 0),
        "failures": readings.get("queue.outbox.failures", {}).get("value", 0),
        "throughput_eps": readings.get("queue.consumer.throughput", {}).get("value", 0),
        "status": "healthy" if readings.get("queue.outbox.lag_seconds", {}).get("value", 0) < 300 else "degraded",
    }


def build_api_monitoring(*, metrics: list[dict], logs: list[dict]) -> dict:
    http_metrics = [m for m in metrics if m.get("metric_key", "").startswith("http.")]
    api_logs = [l for l in logs if l.get("logger", "").startswith("marpich.gateway")]
    durations = [l.get("duration_ms", 0) for l in api_logs if l.get("duration_ms")]
    p95 = sorted(durations)[int(len(durations) * 0.95)] if durations else 0
    error_logs = [l for l in api_logs if (l.get("status") or 0) >= 500]
    return {
        "request_count": len(api_logs),
        "error_count": len(error_logs),
        "error_rate": round(len(error_logs) / max(len(api_logs), 1), 4),
        "p95_latency_ms": p95,
        "http_metrics": http_metrics,
    }


def build_workflow_monitoring(*, metrics: list[dict]) -> dict:
    wf = [m for m in metrics if "workflow" in m.get("metric_key", "")]
    completed = next((m.get("value", 0) for m in wf if m.get("metric_key") == "workflows.completed"), 0)
    return {
        "workflows_completed": completed,
        "workflow_metrics": wf,
        "active_processes": int(completed * 0.15),
    }


def build_ai_monitoring(*, metrics: list[dict]) -> dict:
    ai = [m for m in metrics if m.get("metric_key", "").startswith("ai.")]
    return {
        "ai_requests": sum(m.get("value", 0) for m in ai if "requests" in m.get("metric_key", "")),
        "ai_latency_p95_ms": next((m.get("value", 0) for m in ai if "latency" in m.get("metric_key", "")), 0),
        "ai_error_rate": next((m.get("value", 0) for m in ai if "error" in m.get("metric_key", "")), 0),
        "ai_metrics": ai,
    }


def build_operational_dashboard(
    *,
    profile: dict | None,
    health_checks: list[dict],
    metrics: list[dict],
    logs: list[dict],
    traces: list[dict],
    alerts: list[dict],
    incidents: list[dict],
) -> dict:
    platform_status = aggregate_platform_status(health_checks=health_checks)
    api = build_api_monitoring(metrics=metrics, logs=logs)
    queue = build_queue_monitoring(metrics=metrics)
    open_incidents = [i for i in incidents if i.get("status") != "resolved"]
    active_alerts = [a for a in alerts if a.get("active")]
    return {
        "dashboard_id": "platform.system-health",
        "platform_status": platform_status,
        "summary": {
            "capabilities": len(ObservabilityCapability),
            "health_checks": len(health_checks),
            "metrics_captured": len(metrics),
            "logs_ingested": len(logs),
            "traces_recorded": len(traces),
            "active_alerts": len(active_alerts),
            "open_incidents": len(open_incidents),
            "error_rate": api["error_rate"],
            "p95_latency_ms": api["p95_latency_ms"],
            "queue_lag_seconds": queue["lag_seconds"],
        },
        "rows": [
            {
                "id": "overview",
                "title": "Platform Overview",
                "widgets": [
                    {"id": "platform_status", "type": "status_tile", "value": platform_status},
                    {"id": "error_rate", "type": "gauge", "value": api["error_rate"]},
                    {"id": "p95_latency", "type": "timeseries", "value": api["p95_latency_ms"], "unit": "ms"},
                ],
            },
            {
                "id": "infrastructure",
                "title": "Infrastructure",
                "widgets": [
                    {"id": "health_matrix", "type": "status_matrix", "checks": health_checks},
                    {"id": "queue_lag", "type": "gauge", "value": queue["lag_seconds"], "unit": "seconds"},
                ],
            },
            {
                "id": "business",
                "title": "Business & Alerts",
                "widgets": [
                    {"id": "business_kpis", "type": "kpi_tiles", "data": build_business_kpis(metrics=metrics)},
                    {"id": "active_alerts", "type": "alert_list", "count": len(active_alerts)},
                ],
            },
        ],
        "profile": profile,
        "capabilities": list_capability_catalog(),
    }


def generate_seed_data() -> dict:
    return {
        "traces": [
            {"span_name": "http.server", "service_name": "marpich-backend", "duration_ms": 42.5, "context_name": "enterprise_api_gateway"},
            {"span_name": "db.query", "service_name": "marpich-backend", "duration_ms": 8.2, "context_name": "identity"},
            {"span_name": "workflow.execute", "service_name": "marpich-backend", "duration_ms": 156.0, "context_name": "workflow"},
            {"span_name": "ai.inference", "service_name": "marpich-backend", "duration_ms": 890.0, "context_name": "ai_governance"},
        ],
        "logs": [
            {"level": "INFO", "logger": "marpich.gateway", "message": "gateway request", "duration_ms": 45.2, "status": 200},
            {"level": "WARNING", "logger": "marpich.db", "message": "slow query detected", "duration_ms": 620.0},
            {"level": "ERROR", "logger": "marpich.gateway", "message": "upstream timeout", "duration_ms": 30000.0, "status": 504},
        ],
        "metrics": [
            {"metric_key": "http.server.duration", "metric_type": "histogram", "value": 45.2, "unit": "ms"},
            {"metric_key": "http.server.requests", "metric_type": "counter", "value": 12840, "unit": "count"},
            {"metric_key": "events.total", "metric_type": "counter", "value": 5420, "unit": "count"},
            {"metric_key": "users.logged_in", "metric_type": "counter", "value": 312, "unit": "count"},
            {"metric_key": "workflows.completed", "metric_type": "counter", "value": 89, "unit": "count"},
            {"metric_key": "queue.outbox.pending", "metric_type": "gauge", "value": 12, "unit": "count"},
            {"metric_key": "queue.outbox.lag_seconds", "metric_type": "gauge", "value": 4.5, "unit": "seconds"},
            {"metric_key": "queue.outbox.failures", "metric_type": "counter", "value": 2, "unit": "count"},
            {"metric_key": "queue.consumer.throughput", "metric_type": "gauge", "value": 145.0, "unit": "eps"},
            {"metric_key": "process.cpu.utilization", "metric_type": "gauge", "value": 34.2, "unit": "percent"},
            {"metric_key": "process.memory.usage", "metric_type": "gauge", "value": 1_073_741_824, "unit": "bytes"},
            {"metric_key": "cache.hit_ratio", "metric_type": "gauge", "value": 92.5, "unit": "percent"},
            {"metric_key": "ai.requests.total", "metric_type": "counter", "value": 456, "unit": "count"},
            {"metric_key": "ai.latency.p95", "metric_type": "histogram", "value": 890.0, "unit": "ms"},
            {"metric_key": "ai.error.rate", "metric_type": "gauge", "value": 0.02, "unit": "ratio"},
        ],
        "health_checks": [
            {"check_name": "database", "status": "healthy", "latency_ms": 12.0},
            {"check_name": "redis", "status": "healthy", "latency_ms": 3.0},
            {"check_name": "outbox", "status": "healthy", "latency_ms": 8.0},
            {"check_name": "otel_collector", "status": "degraded", "latency_ms": 250.0},
        ],
        "alerts": [
            {"signal": "infrastructure", "metric_key": "queue.outbox.lag_seconds", "operator": "gt", "threshold": 300, "severity": AlertSeverity.CRITICAL.value},
            {"signal": "api", "metric_key": "http.server.duration", "operator": "gt", "threshold": 1000, "severity": AlertSeverity.WARNING.value},
            {"signal": "ai", "metric_key": "ai.error.rate", "operator": "gt", "threshold": 0.05, "severity": AlertSeverity.WARNING.value},
        ],
    }
