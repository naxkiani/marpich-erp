import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadEobSession,
  saveSession as saveEobSession,
} from "./clientAuth";

export type { ApiSession };

export const loginEobSession = createClientLogin("Observability Admin");
export { loadEobSession, saveEobSession };
export type EobCapability = {
  capability: string;
  label: string;
};

export type EobCatalog = {
  capabilities: EobCapability[];
  policy_keys: string[];
  otel_bootstrap: string;
  delegation: Record<string, string | boolean>;
};

export type EobOperationalDashboard = {
  dashboard_id: string;
  platform_status: string;
  summary: {
    capabilities: number;
    health_checks: number;
    metrics_captured: number;
    logs_ingested: number;
    traces_recorded: number;
    active_alerts: number;
    open_incidents: number;
    error_rate: number;
    p95_latency_ms: number;
    queue_lag_seconds: number;
  };
  rows: Array<{ id: string; title: string; widgets: Array<Record<string, unknown>> }>;
  profile: Record<string, unknown> | null;
  capabilities: EobCapability[];
};

export type EobServiceGraph = {
  services: Array<{
    service_id: string;
    label: string;
    routes: string[];
    dependencies: Array<{ target: string; type: string }>;
  }>;
  nodes: Array<{
    id: string;
    label: string;
    type: string;
    route_count: number;
  }>;
  edges: Array<{
    from: string;
    to: string;
    type: string;
  }>;
  total_services: number;
  graph_type: string;
};

export type EobHealthChecks = {
  status: string;
  checks: Array<Record<string, unknown>>;
};


export async function fetchEobCatalog(session: ApiSession): Promise<EobCatalog> {
  return apiGet("/api/v1/enterprise-observability/catalog", session);
}

export async function fetchEobOperationalDashboard(session: ApiSession): Promise<EobOperationalDashboard> {
  return apiGet("/api/v1/enterprise-observability/operational-dashboard", session);
}

export async function fetchEobServiceDependencyGraph(session: ApiSession): Promise<EobServiceGraph> {
  return apiGet("/api/v1/enterprise-observability/service-dependency-graph", session);
}

export async function fetchEobTraces(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-observability/traces", session);
}

export async function fetchEobLogs(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-observability/logs", session);
}

export async function fetchEobMetrics(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-observability/metrics", session);
}

export async function fetchEobHealthChecks(session: ApiSession): Promise<EobHealthChecks> {
  return apiGet("/api/v1/enterprise-observability/health-checks", session);
}

export async function fetchEobBusinessKpis(session: ApiSession): Promise<Record<string, unknown>> {
  return apiGet("/api/v1/enterprise-observability/business-kpis", session);
}

export async function fetchEobEventMonitoring(session: ApiSession): Promise<Record<string, unknown>> {
  return apiGet("/api/v1/enterprise-observability/events", session);
}

export async function fetchEobQueueMonitoring(session: ApiSession): Promise<Record<string, unknown>> {
  return apiGet("/api/v1/enterprise-observability/queues", session);
}

export async function fetchEobApiMonitoring(session: ApiSession): Promise<Record<string, unknown>> {
  return apiGet("/api/v1/enterprise-observability/api-monitoring", session);
}

export async function fetchEobWorkflowMonitoring(session: ApiSession): Promise<Record<string, unknown>> {
  return apiGet("/api/v1/enterprise-observability/workflows", session);
}

export async function fetchEobAiMonitoring(session: ApiSession): Promise<Record<string, unknown>> {
  return apiGet("/api/v1/enterprise-observability/ai-monitoring", session);
}

export async function fetchEobAlerts(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-observability/alerts", session);
}

export async function fetchEobIncidents(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-observability/incidents", session);
}

export async function seedEob(session: ApiSession): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-observability/seed", session);
}

export async function createEobIncident(
  session: ApiSession,
  body: { title: string; severity: string; source_signal: string; summary?: string },
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-observability/incidents", session, body);
}

export async function resolveEobIncident(
  session: ApiSession,
  incidentRef: string,
  resolutionSummary = "",
): Promise<Record<string, unknown>> {
  return apiPost(
    `/api/v1/enterprise-observability/incidents/${incidentRef}/resolve`,
    session,
    { resolution_summary: resolutionSummary },
  );
}
