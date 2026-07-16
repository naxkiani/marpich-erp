"""Enterprise Observability Platform aggregates."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from shared.domain.aggregates.aggregate_root import AggregateRoot
from shared.domain.value_objects.unique_id import UniqueId


class ObservabilityCapability(StrEnum):
    DISTRIBUTED_TRACING = "distributed_tracing"
    CENTRALIZED_LOGGING = "centralized_logging"
    METRICS = "metrics"
    HEALTH_CHECKS = "health_checks"
    BUSINESS_KPIS = "business_kpis"
    EVENT_MONITORING = "event_monitoring"
    QUEUE_MONITORING = "queue_monitoring"
    API_MONITORING = "api_monitoring"
    WORKFLOW_MONITORING = "workflow_monitoring"
    AI_MONITORING = "ai_monitoring"
    ALERTING = "alerting"
    INCIDENT_MANAGEMENT = "incident_management"
    SERVICE_DEPENDENCY_GRAPH = "service_dependency_graph"
    OPERATIONAL_DASHBOARD = "operational_dashboard"


class HealthStatus(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class AlertSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class IncidentStatus(StrEnum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    MITIGATING = "mitigating"
    RESOLVED = "resolved"


@dataclass(eq=False, kw_only=True)
class ObservabilityProfile(AggregateRoot):
    tenant_id: str
    profile_ref: str
    tracing_enabled: bool = True
    tracing_sampling_rate: float = 0.1
    logging_retention_days: int = 90
    metrics_enabled: bool = True
    health_checks_enabled: bool = True
    alerting_enabled: bool = True
    incident_auto_create: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def create(cls, *, tenant_id: str, profile_ref: str) -> ObservabilityProfile:
        return cls(id=UniqueId.generate(), tenant_id=tenant_id, profile_ref=profile_ref)

    def to_dict(self) -> dict:
        return {
            "profile_ref": self.profile_ref,
            "tenant_id": self.tenant_id,
            "tracing_enabled": self.tracing_enabled,
            "tracing_sampling_rate": self.tracing_sampling_rate,
            "logging_retention_days": self.logging_retention_days,
            "metrics_enabled": self.metrics_enabled,
            "health_checks_enabled": self.health_checks_enabled,
            "alerting_enabled": self.alerting_enabled,
            "incident_auto_create": self.incident_auto_create,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class TraceSpan(AggregateRoot):
    tenant_id: str
    trace_ref: str
    span_name: str
    service_name: str
    correlation_id: str
    duration_ms: float
    status: str
    context_name: str = ""
    parent_ref: str = ""
    attributes: dict = field(default_factory=dict)
    recorded_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def record(
        cls,
        *,
        tenant_id: str,
        trace_ref: str,
        span_name: str,
        service_name: str,
        correlation_id: str,
        duration_ms: float,
        status: str = "ok",
        context_name: str = "",
        parent_ref: str = "",
        attributes: dict | None = None,
    ) -> TraceSpan:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            trace_ref=trace_ref,
            span_name=span_name,
            service_name=service_name,
            correlation_id=correlation_id,
            duration_ms=duration_ms,
            status=status,
            context_name=context_name,
            parent_ref=parent_ref,
            attributes=attributes or {},
        )

    def to_dict(self) -> dict:
        return {
            "trace_ref": self.trace_ref,
            "span_name": self.span_name,
            "service_name": self.service_name,
            "correlation_id": self.correlation_id,
            "duration_ms": self.duration_ms,
            "status": self.status,
            "context_name": self.context_name,
            "parent_ref": self.parent_ref,
            "attributes": self.attributes,
            "recorded_at": self.recorded_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class LogEntry(AggregateRoot):
    tenant_id: str
    log_ref: str
    level: str
    logger: str
    message: str
    correlation_id: str
    context_name: str = ""
    duration_ms: float | None = None
    status: int | None = None
    metadata: dict = field(default_factory=dict)
    recorded_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def ingest(
        cls,
        *,
        tenant_id: str,
        log_ref: str,
        level: str,
        logger: str,
        message: str,
        correlation_id: str,
        context_name: str = "",
        duration_ms: float | None = None,
        status: int | None = None,
        metadata: dict | None = None,
    ) -> LogEntry:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            log_ref=log_ref,
            level=level,
            logger=logger,
            message=message,
            correlation_id=correlation_id,
            context_name=context_name,
            duration_ms=duration_ms,
            status=status,
            metadata=metadata or {},
        )

    def to_dict(self) -> dict:
        return {
            "log_ref": self.log_ref,
            "level": self.level,
            "logger": self.logger,
            "message": self.message,
            "correlation_id": self.correlation_id,
            "context_name": self.context_name,
            "duration_ms": self.duration_ms,
            "status": self.status,
            "metadata": self.metadata,
            "recorded_at": self.recorded_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class MetricSnapshot(AggregateRoot):
    tenant_id: str
    metric_ref: str
    metric_key: str
    metric_type: str
    value: float
    unit: str = ""
    labels: dict = field(default_factory=dict)
    recorded_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def capture(
        cls,
        *,
        tenant_id: str,
        metric_ref: str,
        metric_key: str,
        metric_type: str,
        value: float,
        unit: str = "",
        labels: dict | None = None,
    ) -> MetricSnapshot:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            metric_ref=metric_ref,
            metric_key=metric_key,
            metric_type=metric_type,
            value=value,
            unit=unit,
            labels=labels or {},
        )

    def to_dict(self) -> dict:
        return {
            "metric_ref": self.metric_ref,
            "metric_key": self.metric_key,
            "metric_type": self.metric_type,
            "value": self.value,
            "unit": self.unit,
            "labels": self.labels,
            "recorded_at": self.recorded_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class HealthCheckResult(AggregateRoot):
    tenant_id: str
    check_ref: str
    check_name: str
    status: str
    latency_ms: float
    details: dict = field(default_factory=dict)
    recorded_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def probe(
        cls,
        *,
        tenant_id: str,
        check_ref: str,
        check_name: str,
        status: str,
        latency_ms: float,
        details: dict | None = None,
    ) -> HealthCheckResult:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            check_ref=check_ref,
            check_name=check_name,
            status=status,
            latency_ms=latency_ms,
            details=details or {},
        )

    def to_dict(self) -> dict:
        return {
            "check_ref": self.check_ref,
            "check_name": self.check_name,
            "status": self.status,
            "latency_ms": self.latency_ms,
            "details": self.details,
            "recorded_at": self.recorded_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class MonitoringAlert(AggregateRoot):
    tenant_id: str
    alert_ref: str
    signal: str
    metric_key: str
    operator: str
    threshold: float
    severity: str
    active: bool = True
    triggered_count: int = 0
    last_triggered_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def define(
        cls,
        *,
        tenant_id: str,
        alert_ref: str,
        signal: str,
        metric_key: str,
        operator: str,
        threshold: float,
        severity: str = AlertSeverity.WARNING.value,
    ) -> MonitoringAlert:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            alert_ref=alert_ref,
            signal=signal,
            metric_key=metric_key,
            operator=operator,
            threshold=threshold,
            severity=severity,
        )

    def to_dict(self) -> dict:
        return {
            "alert_ref": self.alert_ref,
            "signal": self.signal,
            "metric_key": self.metric_key,
            "operator": self.operator,
            "threshold": self.threshold,
            "severity": self.severity,
            "active": self.active,
            "triggered_count": self.triggered_count,
            "last_triggered_at": self.last_triggered_at.isoformat() if self.last_triggered_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(eq=False, kw_only=True)
class ObservabilityIncident(AggregateRoot):
    tenant_id: str
    incident_ref: str
    title: str
    severity: str
    status: str
    source_signal: str
    correlation_id: str = ""
    summary: str = ""
    assigned_to: str = ""
    resolved_at: datetime | None = None
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @classmethod
    def open(
        cls,
        *,
        tenant_id: str,
        incident_ref: str,
        title: str,
        severity: str,
        source_signal: str,
        correlation_id: str = "",
        summary: str = "",
        metadata: dict | None = None,
    ) -> ObservabilityIncident:
        return cls(
            id=UniqueId.generate(),
            tenant_id=tenant_id,
            incident_ref=incident_ref,
            title=title,
            severity=severity,
            status=IncidentStatus.OPEN.value,
            source_signal=source_signal,
            correlation_id=correlation_id,
            summary=summary,
            metadata=metadata or {},
        )

    def resolve(self) -> None:
        self.status = IncidentStatus.RESOLVED.value
        self.resolved_at = datetime.now(UTC)

    def to_dict(self) -> dict:
        return {
            "incident_ref": self.incident_ref,
            "title": self.title,
            "severity": self.severity,
            "status": self.status,
            "source_signal": self.source_signal,
            "correlation_id": self.correlation_id,
            "summary": self.summary,
            "assigned_to": self.assigned_to,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }
