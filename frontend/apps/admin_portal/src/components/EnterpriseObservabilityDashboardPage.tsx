"use client";

import { PageLayout } from "@marpich/core";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast } from "@marpich/shared";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  createEobIncident,
  fetchEobAiMonitoring,
  fetchEobAlerts,
  fetchEobApiMonitoring,
  fetchEobBusinessKpis,
  fetchEobCatalog,
  fetchEobEventMonitoring,
  fetchEobHealthChecks,
  fetchEobIncidents,
  fetchEobLogs,
  fetchEobMetrics,
  fetchEobOperationalDashboard,
  fetchEobQueueMonitoring,
  fetchEobServiceDependencyGraph,
  fetchEobTraces,
  fetchEobWorkflowMonitoring,
  loadEobSession,
  loginEobSession,
  resolveEobIncident,
  saveEobSession,
  seedEob,
  type ApiSession,
  type EobCatalog,
  type EobHealthChecks,
  type EobOperationalDashboard,
  type EobServiceGraph,
} from "@/lib/enterpriseObservabilityClient";
import { ServiceDependencyGraphCanvas } from "@/components/ServiceDependencyGraphCanvas";

const CAPABILITY_LABELS: Record<string, string> = {
  distributed_tracing: "Distributed Tracing",
  centralized_logging: "Centralized Logging",
  metrics: "Metrics",
  health_checks: "Health Checks",
  business_kpis: "Business KPIs",
  event_monitoring: "Event Monitoring",
  queue_monitoring: "Queue Monitoring",
  api_monitoring: "API Monitoring",
  workflow_monitoring: "Workflow Monitoring",
  ai_monitoring: "AI Monitoring",
  alerting: "Alerting",
  incident_management: "Incident Management",
  service_dependency_graph: "Service Dependency Graph",
  operational_dashboard: "Operational Dashboard",
};

function statusTone(status: string): "ok" | "warn" | "bad" {
  if (status === "healthy" || status === "ok") return "ok";
  if (status === "degraded") return "warn";
  return "bad";
}

export function EnterpriseObservabilityDashboardPage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(15);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("obs-demo");
  const [email, setEmail] = useState("admin@obs.dev");
  const [password, setPassword] = useState("SecurePass123!");

  const [catalog, setCatalog] = useState<EobCatalog | null>(null);
  const [dashboard, setDashboard] = useState<EobOperationalDashboard | null>(null);
  const [serviceGraph, setServiceGraph] = useState<EobServiceGraph | null>(null);
  const [healthChecks, setHealthChecks] = useState<EobHealthChecks | null>(null);
  const [traces, setTraces] = useState<Array<Record<string, unknown>>>([]);
  const [logs, setLogs] = useState<Array<Record<string, unknown>>>([]);
  const [metrics, setMetrics] = useState<Array<Record<string, unknown>>>([]);
  const [alerts, setAlerts] = useState<Array<Record<string, unknown>>>([]);
  const [incidents, setIncidents] = useState<Array<Record<string, unknown>>>([]);
  const [apiMonitoring, setApiMonitoring] = useState<Record<string, unknown> | null>(null);
  const [queueMonitoring, setQueueMonitoring] = useState<Record<string, unknown> | null>(null);
  const [workflowMonitoring, setWorkflowMonitoring] = useState<Record<string, unknown> | null>(null);
  const [aiMonitoring, setAiMonitoring] = useState<Record<string, unknown> | null>(null);
  const [businessKpis, setBusinessKpis] = useState<Record<string, unknown> | null>(null);
  const [eventMonitoring, setEventMonitoring] = useState<Record<string, unknown> | null>(null);
  const [lastAction, setLastAction] = useState<string | null>(null);

  const loadData = useCallback(async (active: ApiSession) => {
    setLoading(true);
    setProgress(30);
    setError(null);
    try {
      const [
        cat,
        dash,
        graph,
        traceData,
        logData,
        metricData,
        health,
        alertData,
        incidentData,
        apiMon,
        queueMon,
        workflowMon,
        aiMon,
        kpis,
        events,
      ] = await Promise.all([
        fetchEobCatalog(active),
        fetchEobOperationalDashboard(active),
        fetchEobServiceDependencyGraph(active),
        fetchEobTraces(active),
        fetchEobLogs(active),
        fetchEobMetrics(active),
        fetchEobHealthChecks(active),
        fetchEobAlerts(active),
        fetchEobIncidents(active),
        fetchEobApiMonitoring(active),
        fetchEobQueueMonitoring(active),
        fetchEobWorkflowMonitoring(active),
        fetchEobAiMonitoring(active),
        fetchEobBusinessKpis(active),
        fetchEobEventMonitoring(active),
      ]);
      setCatalog(cat);
      setDashboard(dash);
      setServiceGraph(graph);
      setTraces(traceData);
      setLogs(logData);
      setMetrics(metricData);
      setHealthChecks(health);
      setAlerts(alertData);
      setIncidents(incidentData);
      setApiMonitoring(apiMon);
      setQueueMonitoring(queueMon);
      setWorkflowMonitoring(workflowMon);
      setAiMonitoring(aiMon);
      setBusinessKpis(kpis);
      setEventMonitoring(events);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load observability dashboard");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const stored = loadEobSession();
    if (stored) {
      setSession(stored);
      void loadData(stored);
      return;
    }
    setLoading(false);
    setProgress(100);
  }, [loadData]);

  const stats = useMemo(() => {
    if (!dashboard) return [];
    const s = dashboard.summary;
    const tone = statusTone(dashboard.platform_status);
    return [
      { label: "Platform status", value: dashboard.platform_status, tone },
      { label: "Capabilities", value: s.capabilities, tone: "ok" as const },
      { label: "Traces", value: s.traces_recorded, tone: "ok" as const },
      { label: "Logs", value: s.logs_ingested, tone: "ok" as const },
      { label: "Metrics", value: s.metrics_captured, tone: "ok" as const },
      { label: "Error rate", value: `${(s.error_rate * 100).toFixed(2)}%`, tone: s.error_rate > 0.01 ? "warn" : "ok" },
      { label: "p95 latency", value: `${s.p95_latency_ms}ms`, tone: s.p95_latency_ms > 300 ? "warn" : "ok" },
      { label: "Queue lag", value: `${s.queue_lag_seconds}s`, tone: s.queue_lag_seconds > 60 ? "warn" : "ok" },
      { label: "Active alerts", value: s.active_alerts, tone: s.active_alerts ? "warn" : "ok" },
      { label: "Open incidents", value: s.open_incidents, tone: s.open_incidents ? "bad" : "ok" },
    ];
  }, [dashboard]);

  const capabilityRows = useMemo(() => {
    if (!catalog) return [];
    return catalog.capabilities.map((c) => ({
      capability: CAPABILITY_LABELS[c.capability] ?? c.label,
      key: c.capability,
    }));
  }, [catalog]);

  const serviceRows = useMemo(
    () =>
      (serviceGraph?.services ?? []).slice(0, 15).map((s) => ({
        service: s.label,
        routes: String(s.routes.length),
        dependencies: String(s.dependencies.length),
      })),
    [serviceGraph],
  );

  const healthRows = useMemo(
    () =>
      (healthChecks?.checks ?? []).map((c) => ({
        check: String(c.check_name ?? "—"),
        status: String(c.status ?? "—"),
        latency: `${c.latency_ms ?? 0}ms`,
      })),
    [healthChecks],
  );

  const traceRows = useMemo(
    () =>
      traces.slice(0, 10).map((t) => ({
        span: String(t.span_name ?? "—"),
        service: String(t.service_name ?? "—"),
        duration: `${t.duration_ms ?? 0}ms`,
        status: String(t.status ?? "—"),
      })),
    [traces],
  );

  const logRows = useMemo(
    () =>
      logs.slice(0, 10).map((l) => ({
        level: String(l.level ?? "—"),
        logger: String(l.logger ?? "—"),
        message: String(l.message ?? "—").slice(0, 60),
      })),
    [logs],
  );

  const metricRows = useMemo(
    () =>
      metrics.slice(0, 12).map((m) => ({
        key: String(m.metric_key ?? "—"),
        type: String(m.metric_type ?? "—"),
        value: String(m.value ?? "—"),
        unit: String(m.unit ?? ""),
      })),
    [metrics],
  );

  const alertRows = useMemo(
    () =>
      alerts.map((a) => ({
        ref: String(a.alert_ref ?? "—"),
        signal: String(a.signal ?? "—"),
        metric: String(a.metric_key ?? "—"),
        severity: String(a.severity ?? "—"),
        active: a.active ? "Yes" : "No",
      })),
    [alerts],
  );

  const incidentRows = useMemo(
    () =>
      incidents.map((i) => ({
        ref: String(i.incident_ref ?? "—"),
        title: String(i.title ?? "—"),
        severity: String(i.severity ?? "—"),
        status: String(i.status ?? "—"),
      })),
    [incidents],
  );

  const kpiRows = useMemo(() => {
    const kpis = (businessKpis?.kpis as Array<Record<string, unknown>>) ?? [];
    return kpis.map((k) => ({
      label: String(k.label ?? "—"),
      value: String(k.value ?? 0),
      unit: String(k.unit ?? ""),
    }));
  }, [businessKpis]);

  async function onConnect() {
    try {
      const next = await loginEobSession(tenantId, email, password);
      setSession(next);
      saveEobSession(next);
      push({ message: `Connected to tenant ${tenantId}` });
      await loadData(next);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Connection failed" });
    }
  }

  async function runAction(label: string, fn: (s: ApiSession) => Promise<unknown>) {
    if (!session) return;
    try {
      await fn(session);
      setLastAction(label);
      await loadData(session);
      push({ message: `${label} completed`, variant: "success" });
    } catch (err) {
      push({ message: err instanceof Error ? err.message : `${label} failed` });
    }
  }

  const openIncidents = incidents.filter((i) => i.status !== "resolved");

  return (
    <PageLayout
      title="Enterprise Observability"
      breadcrumb={[
        { label: "Marpich", href: "/" },
        { label: "Enterprise", href: "/modules" },
        { label: "Observability" },
      ]}
      actions={
        session ? (
          <>
            <button type="button" className="mp-btn" onClick={() => void runAction("Seed", seedEob)}>
              Seed
            </button>
            <button
              type="button"
              className="mp-btn"
              onClick={() =>
                void runAction("Create incident", (s) =>
                  createEobIncident(s, {
                    title: "Manual observability incident",
                    severity: "warning",
                    source_signal: "dashboard",
                    summary: "Created from admin portal",
                  }),
                )
              }
            >
              New incident
            </button>
            {openIncidents.length ? (
              <button
                type="button"
                className="mp-btn mp-btn-primary"
                onClick={() => {
                  const ref = openIncidents[0]?.incident_ref;
                  if (ref && session) {
                    void runAction("Resolve incident", (s) =>
                      resolveEobIncident(s, String(ref), "Resolved from admin portal"),
                    );
                  }
                }}
              >
                Resolve latest
              </button>
            ) : null}
            <button type="button" className="mp-btn" onClick={() => session && void loadData(session)} disabled={loading}>
              Refresh
            </button>
          </>
        ) : null
      }
    >
      <p className="eob-subtitle">
        Distributed tracing, centralized logging, metrics, health checks, business KPIs, event/queue/API/workflow/AI monitoring, alerting, and incident management.
      </p>

      <ProgressBar value={progress} label={loading ? "Loading observability dashboard…" : "Dashboard ready"} />

      {!session ? (
        <section className="eob-connect" aria-labelledby="connect-heading">
          <h2 id="connect-heading">Connect to API</h2>
          <p className="eob-muted">Sign in to view the operational health dashboard and service dependency graph.</p>
          <div className="eob-form">
            <label>
              Tenant ID
              <input className="mp-input" value={tenantId} onChange={(e) => setTenantId(e.target.value)} />
            </label>
            <label>
              Email
              <input className="mp-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            </label>
            <label>
              Password
              <input className="mp-input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            </label>
            <button type="button" className="mp-btn mp-btn-primary" onClick={() => void onConnect()}>
              Connect
            </button>
          </div>
        </section>
      ) : null}

      {error ? <p className="eob-error" role="alert">{error}</p> : null}
      {session && loading ? <SkeletonTable rows={4} cols={4} /> : null}

      {session && dashboard && !loading ? (
        <>
          <p className="eob-muted">
            Tenant <strong>{session.tenantId}</strong>
            {lastAction ? ` · Last action: ${lastAction}` : ""}
            {dashboard.dashboard_id ? ` · ${dashboard.dashboard_id}` : ""}
            {serviceGraph ? ` · ${serviceGraph.total_services} services` : ""}
          </p>

          <div className="eob-stats">
            {stats.map((stat) => (
              <article
                key={stat.label}
                className={`eob-stat${stat.tone === "warn" ? " eob-stat-warn" : ""}${stat.tone === "bad" ? " eob-stat-bad" : ""}`}
              >
                <span className="eob-stat-value">{stat.value}</span>
                <span className="eob-stat-label">{stat.label}</span>
              </article>
            ))}
          </div>

          <div className="eob-context">
            {apiMonitoring ? (
              <>
                <span>API requests: {String(apiMonitoring.request_count ?? 0)}</span>
                <span>API errors: {String(apiMonitoring.error_count ?? 0)}</span>
              </>
            ) : null}
            {queueMonitoring ? (
              <>
                <span>Queue pending: {String(queueMonitoring.pending ?? 0)}</span>
                <span>Queue status: {String(queueMonitoring.status ?? "—")}</span>
              </>
            ) : null}
            {workflowMonitoring ? (
              <span>Workflows completed: {String(workflowMonitoring.workflows_completed ?? 0)}</span>
            ) : null}
            {aiMonitoring ? (
              <>
                <span>AI requests: {String(aiMonitoring.ai_requests ?? 0)}</span>
                <span>AI error rate: {String(aiMonitoring.ai_error_rate ?? 0)}</span>
              </>
            ) : null}
            {eventMonitoring ? (
              <span>Events/min: {String(eventMonitoring.events_per_minute ?? 0)}</span>
            ) : null}
          </div>

          <div className="eob-grid">
            <section aria-labelledby="capabilities-heading">
              <h2 id="capabilities-heading">Capabilities ({catalog?.capabilities.length ?? 0})</h2>
              <DataTable
                columns={[
                  { key: "capability", header: "Capability", sortable: true },
                  { key: "key", header: "Key", sortable: true },
                ]}
                rows={capabilityRows}
              />
            </section>

            <section aria-labelledby="health-heading">
              <h2 id="health-heading">Health checks ({healthChecks?.status ?? "—"})</h2>
              {healthRows.length ? (
                <DataTable
                  columns={[
                    { key: "check", header: "Check", sortable: true },
                    { key: "status", header: "Status", sortable: true },
                    { key: "latency", header: "Latency", sortable: true },
                  ]}
                  rows={healthRows}
                />
              ) : (
                <EmptyState title="No health checks" description="Run Seed to populate health probes." />
              )}
            </section>
          </div>

          <section aria-labelledby="services-heading">
            <h2 id="services-heading">Service dependency graph ({serviceGraph?.total_services ?? 0} services)</h2>
            {serviceGraph && (serviceGraph.nodes?.length || serviceGraph.services.length) ? (
              <>
                <ServiceDependencyGraphCanvas graph={serviceGraph} />
                {serviceRows.length ? (
                  <details className="eob-graph-table">
                    <summary>Table view</summary>
                    <DataTable
                      columns={[
                        { key: "service", header: "Service", sortable: true },
                        { key: "routes", header: "Routes", sortable: true },
                        { key: "dependencies", header: "Dependencies", sortable: true },
                      ]}
                      rows={serviceRows}
                    />
                  </details>
                ) : null}
              </>
            ) : (
              <EmptyState title="No services" description="Service graph is built from route registry." />
            )}
          </section>

          <div className="eob-grid">
            <section aria-labelledby="kpis-heading">
              <h2 id="kpis-heading">Business KPIs</h2>
              {kpiRows.length ? (
                <DataTable
                  columns={[
                    { key: "label", header: "KPI", sortable: true },
                    { key: "value", header: "Value", sortable: true },
                    { key: "unit", header: "Unit", sortable: true },
                  ]}
                  rows={kpiRows}
                />
              ) : (
                <EmptyState title="No KPIs" description="Run Seed to load business metrics." />
              )}
            </section>

            <section aria-labelledby="metrics-heading">
              <h2 id="metrics-heading">Metrics ({metrics.length})</h2>
              {metricRows.length ? (
                <DataTable
                  columns={[
                    { key: "key", header: "Key", sortable: true },
                    { key: "type", header: "Type", sortable: true },
                    { key: "value", header: "Value", sortable: true },
                    { key: "unit", header: "Unit", sortable: true },
                  ]}
                  rows={metricRows}
                />
              ) : (
                <EmptyState title="No metrics" description="Run Seed to capture metric snapshots." />
              )}
            </section>
          </div>

          <div className="eob-grid">
            <section aria-labelledby="traces-heading">
              <h2 id="traces-heading">Distributed traces ({traces.length})</h2>
              {traceRows.length ? (
                <DataTable
                  columns={[
                    { key: "span", header: "Span", sortable: true },
                    { key: "service", header: "Service", sortable: true },
                    { key: "duration", header: "Duration", sortable: true },
                    { key: "status", header: "Status", sortable: true },
                  ]}
                  rows={traceRows}
                />
              ) : (
                <EmptyState title="No traces" description="Run Seed to record trace spans." />
              )}
            </section>

            <section aria-labelledby="logs-heading">
              <h2 id="logs-heading">Centralized logs ({logs.length})</h2>
              {logRows.length ? (
                <DataTable
                  columns={[
                    { key: "level", header: "Level", sortable: true },
                    { key: "logger", header: "Logger", sortable: true },
                    { key: "message", header: "Message", sortable: true },
                  ]}
                  rows={logRows}
                />
              ) : (
                <EmptyState title="No logs" description="Run Seed to ingest log entries." />
              )}
            </section>
          </div>

          <div className="eob-grid">
            <section aria-labelledby="alerts-heading">
              <h2 id="alerts-heading">Alerts ({alerts.length})</h2>
              {alertRows.length ? (
                <DataTable
                  columns={[
                    { key: "ref", header: "Ref", sortable: true },
                    { key: "signal", header: "Signal", sortable: true },
                    { key: "metric", header: "Metric", sortable: true },
                    { key: "severity", header: "Severity", sortable: true },
                    { key: "active", header: "Active", sortable: true },
                  ]}
                  rows={alertRows}
                />
              ) : (
                <EmptyState title="No alerts" description="Run Seed to create alert rules." />
              )}
            </section>

            <section aria-labelledby="incidents-heading">
              <h2 id="incidents-heading">Incidents ({incidents.length})</h2>
              {incidentRows.length ? (
                <DataTable
                  columns={[
                    { key: "ref", header: "Ref", sortable: true },
                    { key: "title", header: "Title", sortable: true },
                    { key: "severity", header: "Severity", sortable: true },
                    { key: "status", header: "Status", sortable: true },
                  ]}
                  rows={incidentRows}
                />
              ) : (
                <EmptyState
                  title="No incidents"
                  description="Create an incident or let critical alerts auto-create one."
                  action={
                    <button
                      type="button"
                      className="mp-btn mp-btn-primary"
                      onClick={() => void runAction("Seed", seedEob)}
                    >
                      Seed defaults
                    </button>
                  }
                />
              )}
            </section>
          </div>
        </>
      ) : null}

      <style jsx>{`
        .eob-subtitle { color: var(--mp-text-muted, #64748b); margin: 0 0 1rem; }
        .eob-connect { margin: 1rem 0 1.5rem; padding: 1rem; border: 1px solid var(--mp-border, #e2e8f0); border-radius: 8px; }
        .eob-form { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem; align-items: end; margin-top: 0.75rem; }
        label { display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.85rem; }
        .eob-muted { color: var(--mp-text-muted, #64748b); margin: 0.5rem 0; }
        .eob-error { color: #b91c1c; margin: 0.75rem 0; }
        .eob-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 0.75rem; margin: 1rem 0; }
        .eob-stat { padding: 1rem; border-radius: 8px; background: var(--mp-surface-2, #f8fafc); border: 1px solid var(--mp-border, #e2e8f0); }
        .eob-stat-warn { border-color: #f59e0b; background: #fffbeb; }
        .eob-stat-bad { border-color: #ef4444; background: #fef2f2; }
        .eob-stat-value { display: block; font-size: 1.2rem; font-weight: 700; text-transform: capitalize; }
        .eob-stat-label { font-size: 0.75rem; color: var(--mp-text-muted, #64748b); }
        .eob-context { display: flex; flex-wrap: wrap; gap: 1rem; font-size: 0.85rem; color: var(--mp-text-muted, #64748b); margin-bottom: 1rem; }
        .eob-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 1.25rem; margin-bottom: 1.5rem; }
        h2 { margin: 0 0 0.75rem; font-size: 1.1rem; }
        section { margin-bottom: 0.5rem; }
        .eob-graph-table { margin-top: 0.75rem; font-size: 0.85rem; }
        .eob-graph-table summary { cursor: pointer; color: var(--mp-text-muted, #64748b); margin-bottom: 0.5rem; }
        @media (max-width: 960px) { .eob-grid { grid-template-columns: 1fr; } }
      `}</style>
    </PageLayout>
  );
}
