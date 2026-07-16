"""Enterprise Observability repository ports."""
from __future__ import annotations

from abc import ABC, abstractmethod

from contexts.enterprise_observability.domain.aggregates.enterprise_observability_platform import (
    HealthCheckResult,
    LogEntry,
    MetricSnapshot,
    MonitoringAlert,
    ObservabilityIncident,
    ObservabilityProfile,
    TraceSpan,
)


class IObservabilityProfileRepository(ABC):
    @abstractmethod
    async def save(self, profile: ObservabilityProfile) -> None: ...

    @abstractmethod
    async def find_by_tenant(self, tenant_id: str) -> ObservabilityProfile | None: ...

    @abstractmethod
    def next_profile_ref(self, tenant_id: str) -> str: ...


class ITraceSpanRepository(ABC):
    @abstractmethod
    async def save(self, span: TraceSpan) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[TraceSpan]: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, trace_ref: str) -> list[TraceSpan]: ...

    @abstractmethod
    def next_trace_ref(self, tenant_id: str) -> str: ...


class ILogEntryRepository(ABC):
    @abstractmethod
    async def save(self, entry: LogEntry) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[LogEntry]: ...

    @abstractmethod
    def next_log_ref(self, tenant_id: str) -> str: ...


class IMetricSnapshotRepository(ABC):
    @abstractmethod
    async def save(self, snapshot: MetricSnapshot) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[MetricSnapshot]: ...

    @abstractmethod
    def next_metric_ref(self, tenant_id: str) -> str: ...


class IHealthCheckResultRepository(ABC):
    @abstractmethod
    async def save(self, result: HealthCheckResult) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[HealthCheckResult]: ...

    @abstractmethod
    def next_check_ref(self, tenant_id: str) -> str: ...


class IMonitoringAlertRepository(ABC):
    @abstractmethod
    async def save(self, alert: MonitoringAlert) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[MonitoringAlert]: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, alert_ref: str) -> MonitoringAlert | None: ...

    @abstractmethod
    def next_alert_ref(self, tenant_id: str) -> str: ...


class IObservabilityIncidentRepository(ABC):
    @abstractmethod
    async def save(self, incident: ObservabilityIncident) -> None: ...

    @abstractmethod
    async def list_by_tenant(self, tenant_id: str) -> list[ObservabilityIncident]: ...

    @abstractmethod
    async def find_by_ref(self, tenant_id: str, incident_ref: str) -> ObservabilityIncident | None: ...

    @abstractmethod
    def next_incident_ref(self, tenant_id: str) -> str: ...
