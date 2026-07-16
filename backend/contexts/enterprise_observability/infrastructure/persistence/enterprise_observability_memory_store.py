"""In-memory Enterprise Observability persistence."""
from __future__ import annotations

from contexts.enterprise_observability.domain.aggregates.enterprise_observability_platform import (
    HealthCheckResult,
    LogEntry,
    MetricSnapshot,
    MonitoringAlert,
    ObservabilityIncident,
    ObservabilityProfile,
    TraceSpan,
)
from contexts.enterprise_observability.domain.ports.enterprise_observability_repositories import (
    IHealthCheckResultRepository,
    ILogEntryRepository,
    IMetricSnapshotRepository,
    IMonitoringAlertRepository,
    IObservabilityIncidentRepository,
    IObservabilityProfileRepository,
    ITraceSpanRepository,
)


class _RefCounter:
    _counters: dict[str, int] = {}

    @classmethod
    def reset(cls) -> None:
        cls._counters = {}

    @classmethod
    def next(cls, tenant_id: str, prefix: str) -> str:
        key = f"{tenant_id}:{prefix}"
        n = cls._counters.get(key, 0) + 1
        cls._counters[key] = n
        return f"{prefix}-{tenant_id[:4].upper()}-{n:05d}"


class InMemoryObservabilityProfileRepository(IObservabilityProfileRepository):
    _store: dict[str, ObservabilityProfile] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, profile: ObservabilityProfile) -> None:
        self._store[str(profile.id)] = profile

    async def find_by_tenant(self, tenant_id: str) -> ObservabilityProfile | None:
        for profile in self._store.values():
            if profile.tenant_id == tenant_id:
                return profile
        return None

    def next_profile_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-OBS-PRF")


class InMemoryTraceSpanRepository(ITraceSpanRepository):
    _store: dict[str, TraceSpan] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, span: TraceSpan) -> None:
        self._store[str(span.id)] = span

    async def list_by_tenant(self, tenant_id: str) -> list[TraceSpan]:
        return [s for s in self._store.values() if s.tenant_id == tenant_id]

    async def find_by_ref(self, tenant_id: str, trace_ref: str) -> list[TraceSpan]:
        return [s for s in self._store.values() if s.tenant_id == tenant_id and s.trace_ref == trace_ref]

    def next_trace_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-OBS-TRC")


class InMemoryLogEntryRepository(ILogEntryRepository):
    _store: dict[str, LogEntry] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, entry: LogEntry) -> None:
        self._store[str(entry.id)] = entry

    async def list_by_tenant(self, tenant_id: str) -> list[LogEntry]:
        return [e for e in self._store.values() if e.tenant_id == tenant_id]

    def next_log_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-OBS-LOG")


class InMemoryMetricSnapshotRepository(IMetricSnapshotRepository):
    _store: dict[str, MetricSnapshot] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, snapshot: MetricSnapshot) -> None:
        self._store[str(snapshot.id)] = snapshot

    async def list_by_tenant(self, tenant_id: str) -> list[MetricSnapshot]:
        return [m for m in self._store.values() if m.tenant_id == tenant_id]

    def next_metric_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-OBS-MET")


class InMemoryHealthCheckResultRepository(IHealthCheckResultRepository):
    _store: dict[str, HealthCheckResult] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, result: HealthCheckResult) -> None:
        self._store[str(result.id)] = result

    async def list_by_tenant(self, tenant_id: str) -> list[HealthCheckResult]:
        return [h for h in self._store.values() if h.tenant_id == tenant_id]

    def next_check_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-OBS-HLT")


class InMemoryMonitoringAlertRepository(IMonitoringAlertRepository):
    _store: dict[str, MonitoringAlert] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, alert: MonitoringAlert) -> None:
        self._store[str(alert.id)] = alert

    async def list_by_tenant(self, tenant_id: str) -> list[MonitoringAlert]:
        return [a for a in self._store.values() if a.tenant_id == tenant_id]

    async def find_by_ref(self, tenant_id: str, alert_ref: str) -> MonitoringAlert | None:
        for alert in self._store.values():
            if alert.tenant_id == tenant_id and alert.alert_ref == alert_ref:
                return alert
        return None

    def next_alert_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-OBS-ALT")


class InMemoryObservabilityIncidentRepository(IObservabilityIncidentRepository):
    _store: dict[str, ObservabilityIncident] = {}

    @classmethod
    def reset(cls) -> None:
        cls._store = {}

    async def save(self, incident: ObservabilityIncident) -> None:
        self._store[str(incident.id)] = incident

    async def list_by_tenant(self, tenant_id: str) -> list[ObservabilityIncident]:
        return [i for i in self._store.values() if i.tenant_id == tenant_id]

    async def find_by_ref(self, tenant_id: str, incident_ref: str) -> ObservabilityIncident | None:
        for incident in self._store.values():
            if incident.tenant_id == tenant_id and incident.incident_ref == incident_ref:
                return incident
        return None

    def next_incident_ref(self, tenant_id: str) -> str:
        return _RefCounter.next(tenant_id, "ERP-OBS-INC")
