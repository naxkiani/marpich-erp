"""Enterprise Observability application service."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime

from contexts.enterprise_observability.domain.aggregates.enterprise_observability_platform import (
    AlertSeverity,
    HealthCheckResult,
    LogEntry,
    MetricSnapshot,
    MonitoringAlert,
    ObservabilityIncident,
    ObservabilityProfile,
    TraceSpan,
)
from contexts.enterprise_observability.domain.events.enterprise_observability_integration_events import (
    AlertTriggeredIntegration,
    IncidentCreatedIntegration,
    IncidentResolvedIntegration,
    OperationalDashboardGeneratedIntegration,
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
from contexts.enterprise_observability.domain.services import enterprise_observability_engine as engine
from shared.application.ports.policy import IPolicyEvaluator
from shared.application.result import Result
from shared.domain.value_objects.tenant_id import TenantId
from shared.infrastructure.messaging.event_bus import publish_integration_event


class EnterpriseObservabilityApplicationService:
    def __init__(
        self,
        profiles: IObservabilityProfileRepository,
        traces: ITraceSpanRepository,
        logs: ILogEntryRepository,
        metrics: IMetricSnapshotRepository,
        health_checks: IHealthCheckResultRepository,
        alerts: IMonitoringAlertRepository,
        incidents: IObservabilityIncidentRepository,
        policy_evaluator: IPolicyEvaluator,
    ) -> None:
        self._profiles = profiles
        self._traces = traces
        self._logs = logs
        self._metrics = metrics
        self._health_checks = health_checks
        self._alerts = alerts
        self._incidents = incidents
        self._policy = policy_evaluator

    async def _policy_params(self, tenant_id: str) -> dict:
        profile = await self._profiles.find_by_tenant(tenant_id)
        params = {
            "tracing_enabled": profile.tracing_enabled if profile else True,
            "tracing_sampling_rate": profile.tracing_sampling_rate if profile else 0.1,
            "logging_retention_days": profile.logging_retention_days if profile else 90,
            "metrics_enabled": profile.metrics_enabled if profile else True,
            "health_checks_enabled": profile.health_checks_enabled if profile else True,
            "alerting_enabled": profile.alerting_enabled if profile else True,
            "incident_auto_create": profile.incident_auto_create if profile else True,
        }
        pmap = {
            "enterprise_observability.tracing.enabled": ("tracing_enabled", "enabled"),
            "enterprise_observability.tracing.sampling_rate": ("tracing_sampling_rate", "rate"),
            "enterprise_observability.logging.retention_days": ("logging_retention_days", "days"),
            "enterprise_observability.metrics.enabled": ("metrics_enabled", "enabled"),
            "enterprise_observability.health_checks.enabled": ("health_checks_enabled", "enabled"),
            "enterprise_observability.alerting.enabled": ("alerting_enabled", "enabled"),
            "enterprise_observability.incident.auto_create.enabled": ("incident_auto_create", "enabled"),
        }
        for key, (target, field) in pmap.items():
            decision = await self._policy.evaluate(tenant_id=tenant_id, domain="platform", policy_key=key, facts={})
            if decision.parameters and field in decision.parameters:
                params[target] = decision.parameters[field]
        return params

    async def _ensure_profile(self, tenant_id: str) -> ObservabilityProfile:
        profile = await self._profiles.find_by_tenant(tenant_id)
        if profile:
            return profile
        profile = ObservabilityProfile.create(
            tenant_id=tenant_id,
            profile_ref=self._profiles.next_profile_ref(tenant_id),
        )
        await self._profiles.save(profile)
        return profile

    async def handle_tenant_provisioned(self, event: dict) -> None:
        tenant_id = event.get("tenant_id") or event.get("payload", {}).get("tenant_id")
        if not tenant_id:
            return
        await self.seed(tenant_id)

    async def list_catalog(self) -> Result[dict]:
        return Result.ok({
            "capabilities": engine.list_capability_catalog(),
            "policy_keys": engine.list_policy_keys(),
            "otel_bootstrap": "shared/infrastructure/observability/telemetry.py",
            "delegation": {
                "business_metrics": "analytics",
                "alert_delivery": "notifications",
                "security_incidents": "security_incident",
                "local_metrics_duplication": False,
            },
        })

    async def get_dependency_map(self) -> Result[dict]:
        return Result.ok(engine.dependency_map())

    async def get_threat_map(self, tenant_id: str) -> Result[dict]:
        """Read-only security/ops threat projection — no parallel analytics store."""
        incidents = [i.to_dict() for i in await self._incidents.list_by_tenant(tenant_id)]
        alerts = [a.to_dict() for a in await self._alerts.list_by_tenant(tenant_id)]
        nodes = []
        for alert in alerts[:50]:
            nodes.append({
                "id": alert.get("alert_ref") or alert.get("id"),
                "kind": "alert",
                "severity": alert.get("severity") or alert.get("level") or "warning",
                "label": alert.get("title") or alert.get("name") or "alert",
                "region": (alert.get("metadata") or {}).get("region", "global"),
            })
        for incident in incidents[:50]:
            nodes.append({
                "id": incident.get("incident_ref") or incident.get("id"),
                "kind": "incident",
                "severity": incident.get("severity") or "critical",
                "label": incident.get("title") or "incident",
                "region": (incident.get("metadata") or {}).get("region", "global"),
            })
        return Result.ok({
            "tenant_id": tenant_id,
            "generated_at": datetime.now(UTC).isoformat(),
            "node_count": len(nodes),
            "nodes": nodes,
            "source": "enterprise_observability",
            "note": "Threat map projects alerts/incidents; not a local security DB.",
        })

    async def get_service_dependency_graph(self) -> Result[dict]:
        return Result.ok(engine.build_service_dependency_graph())

    async def seed(self, tenant_id: str) -> Result[dict]:
        await self._ensure_profile(tenant_id)
        correlation_id = str(uuid.uuid4())
        seed_data = engine.generate_seed_data()
        trace_count = 0
        log_count = 0
        metric_count = 0
        health_count = 0
        alert_count = 0

        trace_ref = self._traces.next_trace_ref(tenant_id)
        for tdata in seed_data["traces"]:
            span = TraceSpan.record(
                tenant_id=tenant_id,
                trace_ref=trace_ref,
                span_name=tdata["span_name"],
                service_name=tdata["service_name"],
                correlation_id=correlation_id,
                duration_ms=tdata["duration_ms"],
                context_name=tdata.get("context_name", ""),
            )
            await self._traces.save(span)
            trace_count += 1

        for ldata in seed_data["logs"]:
            entry = LogEntry.ingest(
                tenant_id=tenant_id,
                log_ref=self._logs.next_log_ref(tenant_id),
                level=ldata["level"],
                logger=ldata["logger"],
                message=ldata["message"],
                correlation_id=correlation_id,
                duration_ms=ldata.get("duration_ms"),
                status=ldata.get("status"),
            )
            await self._logs.save(entry)
            log_count += 1

        for mdata in seed_data["metrics"]:
            snapshot = MetricSnapshot.capture(
                tenant_id=tenant_id,
                metric_ref=self._metrics.next_metric_ref(tenant_id),
                metric_key=mdata["metric_key"],
                metric_type=mdata["metric_type"],
                value=mdata["value"],
                unit=mdata.get("unit", ""),
            )
            await self._metrics.save(snapshot)
            metric_count += 1

        for hdata in seed_data["health_checks"]:
            result = HealthCheckResult.probe(
                tenant_id=tenant_id,
                check_ref=self._health_checks.next_check_ref(tenant_id),
                check_name=hdata["check_name"],
                status=hdata["status"],
                latency_ms=hdata["latency_ms"],
            )
            await self._health_checks.save(result)
            health_count += 1

        for adata in seed_data["alerts"]:
            alert = MonitoringAlert.define(
                tenant_id=tenant_id,
                alert_ref=self._alerts.next_alert_ref(tenant_id),
                signal=adata["signal"],
                metric_key=adata["metric_key"],
                operator=adata["operator"],
                threshold=adata["threshold"],
                severity=adata["severity"],
            )
            await self._alerts.save(alert)
            alert_count += 1

        return Result.ok({
            "seeded": True,
            "traces": trace_count,
            "logs": log_count,
            "metrics": metric_count,
            "health_checks": health_count,
            "alerts": alert_count,
        })

    async def get_dashboard(self, tenant_id: str) -> Result[dict]:
        return await self.get_operational_dashboard(tenant_id)

    async def get_operational_dashboard(self, tenant_id: str) -> Result[dict]:
        profile = await self._profiles.find_by_tenant(tenant_id)
        health = [h.to_dict() for h in await self._health_checks.list_by_tenant(tenant_id)]
        metrics = [m.to_dict() for m in await self._metrics.list_by_tenant(tenant_id)]
        logs = [l.to_dict() for l in await self._logs.list_by_tenant(tenant_id)]
        traces = [t.to_dict() for t in await self._traces.list_by_tenant(tenant_id)]
        alerts = [a.to_dict() for a in await self._alerts.list_by_tenant(tenant_id)]
        incidents = [i.to_dict() for i in await self._incidents.list_by_tenant(tenant_id)]
        dashboard = engine.build_operational_dashboard(
            profile=profile.to_dict() if profile else None,
            health_checks=health,
            metrics=metrics,
            logs=logs,
            traces=traces,
            alerts=alerts,
            incidents=incidents,
        )
        await publish_integration_event(
            OperationalDashboardGeneratedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                platform_status=dashboard["platform_status"],
                active_alerts=dashboard["summary"]["active_alerts"],
                open_incidents=dashboard["summary"]["open_incidents"],
            )
        )
        return Result.ok(dashboard)

    async def list_traces(self, tenant_id: str) -> Result[list[dict]]:
        spans = await self._traces.list_by_tenant(tenant_id)
        return Result.ok([s.to_dict() for s in spans])

    async def get_trace(self, tenant_id: str, trace_ref: str) -> Result[list[dict]]:
        spans = await self._traces.find_by_ref(tenant_id, trace_ref)
        if not spans:
            return Result.fail("trace_not_found")
        return Result.ok([s.to_dict() for s in spans])

    async def record_trace(
        self,
        tenant_id: str,
        *,
        span_name: str,
        service_name: str,
        duration_ms: float,
        correlation_id: str,
        status: str = "ok",
        context_name: str = "",
        parent_ref: str = "",
        attributes: dict | None = None,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not params["tracing_enabled"]:
            return Result.fail("tracing_disabled")
        trace_ref = self._traces.next_trace_ref(tenant_id)
        span = TraceSpan.record(
            tenant_id=tenant_id,
            trace_ref=trace_ref,
            span_name=span_name,
            service_name=service_name,
            correlation_id=correlation_id,
            duration_ms=duration_ms,
            status=status,
            context_name=context_name,
            parent_ref=parent_ref,
            attributes=attributes,
        )
        await self._traces.save(span)
        return Result.ok(span.to_dict())

    async def list_logs(self, tenant_id: str) -> Result[list[dict]]:
        entries = await self._logs.list_by_tenant(tenant_id)
        return Result.ok([e.to_dict() for e in entries])

    async def ingest_log(
        self,
        tenant_id: str,
        *,
        level: str,
        logger: str,
        message: str,
        correlation_id: str,
        context_name: str = "",
        duration_ms: float | None = None,
        status: int | None = None,
        metadata: dict | None = None,
    ) -> Result[dict]:
        entry = LogEntry.ingest(
            tenant_id=tenant_id,
            log_ref=self._logs.next_log_ref(tenant_id),
            level=level,
            logger=logger,
            message=message,
            correlation_id=correlation_id,
            context_name=context_name,
            duration_ms=duration_ms,
            status=status,
            metadata=metadata,
        )
        await self._logs.save(entry)
        return Result.ok(entry.to_dict())

    async def list_metrics(self, tenant_id: str) -> Result[list[dict]]:
        snapshots = await self._metrics.list_by_tenant(tenant_id)
        return Result.ok([m.to_dict() for m in snapshots])

    async def list_health_checks(self, tenant_id: str) -> Result[dict]:
        checks = [h.to_dict() for h in await self._health_checks.list_by_tenant(tenant_id)]
        return Result.ok({
            "status": engine.aggregate_platform_status(health_checks=checks),
            "checks": checks,
        })

    async def get_business_kpis(self, tenant_id: str) -> Result[dict]:
        metrics = [m.to_dict() for m in await self._metrics.list_by_tenant(tenant_id)]
        return Result.ok(engine.build_business_kpis(metrics=metrics))

    async def get_event_monitoring(self, tenant_id: str) -> Result[dict]:
        metrics = [m.to_dict() for m in await self._metrics.list_by_tenant(tenant_id)]
        return Result.ok(engine.build_event_monitoring(metrics=metrics))

    async def get_queue_monitoring(self, tenant_id: str) -> Result[dict]:
        metrics = [m.to_dict() for m in await self._metrics.list_by_tenant(tenant_id)]
        return Result.ok(engine.build_queue_monitoring(metrics=metrics))

    async def get_api_monitoring(self, tenant_id: str) -> Result[dict]:
        metrics = [m.to_dict() for m in await self._metrics.list_by_tenant(tenant_id)]
        logs = [l.to_dict() for l in await self._logs.list_by_tenant(tenant_id)]
        return Result.ok(engine.build_api_monitoring(metrics=metrics, logs=logs))

    async def get_workflow_monitoring(self, tenant_id: str) -> Result[dict]:
        metrics = [m.to_dict() for m in await self._metrics.list_by_tenant(tenant_id)]
        return Result.ok(engine.build_workflow_monitoring(metrics=metrics))

    async def get_ai_monitoring(self, tenant_id: str) -> Result[dict]:
        metrics = [m.to_dict() for m in await self._metrics.list_by_tenant(tenant_id)]
        return Result.ok(engine.build_ai_monitoring(metrics=metrics))

    async def list_alerts(self, tenant_id: str) -> Result[list[dict]]:
        alerts = await self._alerts.list_by_tenant(tenant_id)
        return Result.ok([a.to_dict() for a in alerts])

    async def create_alert(
        self,
        tenant_id: str,
        *,
        signal: str,
        metric_key: str,
        operator: str,
        threshold: float,
        severity: str,
    ) -> Result[dict]:
        params = await self._policy_params(tenant_id)
        if not params["alerting_enabled"]:
            return Result.fail("alerting_disabled")
        alert = MonitoringAlert.define(
            tenant_id=tenant_id,
            alert_ref=self._alerts.next_alert_ref(tenant_id),
            signal=signal,
            metric_key=metric_key,
            operator=operator,
            threshold=threshold,
            severity=severity,
        )
        await self._alerts.save(alert)
        await self._evaluate_alerts(tenant_id)
        return Result.ok(alert.to_dict())

    async def _evaluate_alerts(self, tenant_id: str) -> None:
        alerts = await self._alerts.list_by_tenant(tenant_id)
        metrics = {m.metric_key: m.value for m in await self._metrics.list_by_tenant(tenant_id)}
        params = await self._policy_params(tenant_id)
        for alert in alerts:
            if not alert.active:
                continue
            value = metrics.get(alert.metric_key, 0)
            if engine.evaluate_alert(value=value, operator=alert.operator, threshold=alert.threshold):
                alert.triggered_count += 1
                alert.last_triggered_at = datetime.now(UTC)
                await self._alerts.save(alert)
                await publish_integration_event(
                    AlertTriggeredIntegration(
                        tenant_id=TenantId(tenant_id),
                        correlation_id=str(uuid.uuid4()),
                        alert_ref=alert.alert_ref,
                        signal=alert.signal,
                        metric_key=alert.metric_key,
                        severity=alert.severity,
                    )
                )
                if params["incident_auto_create"] and alert.severity == AlertSeverity.CRITICAL.value:
                    await self.create_incident(
                        tenant_id,
                        title=f"Alert triggered: {alert.metric_key}",
                        severity=alert.severity,
                        source_signal=alert.signal,
                        summary=f"{alert.metric_key} {alert.operator} {alert.threshold}",
                    )

    async def list_incidents(self, tenant_id: str) -> Result[list[dict]]:
        incidents = await self._incidents.list_by_tenant(tenant_id)
        return Result.ok([i.to_dict() for i in incidents])

    async def create_incident(
        self,
        tenant_id: str,
        *,
        title: str,
        severity: str,
        source_signal: str,
        summary: str = "",
        correlation_id: str = "",
    ) -> Result[dict]:
        incident = ObservabilityIncident.open(
            tenant_id=tenant_id,
            incident_ref=self._incidents.next_incident_ref(tenant_id),
            title=title,
            severity=severity,
            source_signal=source_signal,
            correlation_id=correlation_id,
            summary=summary,
        )
        await self._incidents.save(incident)
        await publish_integration_event(
            IncidentCreatedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=correlation_id or str(uuid.uuid4()),
                incident_ref=incident.incident_ref,
                title=title,
                severity=severity,
                source_signal=source_signal,
            )
        )
        return Result.ok(incident.to_dict())

    async def resolve_incident(
        self,
        tenant_id: str,
        incident_ref: str,
        *,
        resolution_summary: str = "",
    ) -> Result[dict]:
        incident = await self._incidents.find_by_ref(tenant_id, incident_ref)
        if not incident:
            return Result.fail("incident_not_found")
        incident.resolve()
        await self._incidents.save(incident)
        await publish_integration_event(
            IncidentResolvedIntegration(
                tenant_id=TenantId(tenant_id),
                correlation_id=str(uuid.uuid4()),
                incident_ref=incident_ref,
                resolution_summary=resolution_summary,
            )
        )
        return Result.ok(incident.to_dict())
