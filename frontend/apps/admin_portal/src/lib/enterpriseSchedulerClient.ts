const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export type ApiSession = { tenantId: string; accessToken: string };

export type SchCatalog = {
  capabilities: Array<{ capability: string; label: string }>;
  policy_keys: string[];
  job_types: string[];
  delegation: Record<string, string | boolean>;
};

export type SchDashboard = {
  summary: {
    capabilities: number;
    jobs_total: number;
    executions_total: number;
    succeeded: number;
    failed: number;
    running: number;
    success_rate_pct: number;
    dependencies: number;
    distributed_shards: number;
    paused_jobs: number;
    jobs_by_type: Record<string, number>;
    jobs_by_shard: Record<string, number>;
  };
  profile: Record<string, unknown> | null;
  recent_executions: Array<Record<string, unknown>>;
  jobs_by_status: Record<string, number>;
  executions_by_status: Record<string, number>;
  capabilities: Array<{ capability: string; label: string }>;
};

export type SchMonitoring = {
  jobs_total: number;
  executions_total: number;
  succeeded: number;
  failed: number;
  running: number;
  success_rate_pct: number;
  jobs_by_type: Record<string, number>;
  jobs_by_shard: Record<string, number>;
  paused_jobs: number;
};

const SESSION_KEY = "marpich_sch_session";

export function loadSchSession(): ApiSession | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.sessionStorage.getItem(SESSION_KEY);
    return raw ? (JSON.parse(raw) as ApiSession) : null;
  } catch {
    return null;
  }
}

export function saveSchSession(session: ApiSession): void {
  window.sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

function headers(session: ApiSession): HeadersInit {
  return {
    "Content-Type": "application/json",
    "X-Tenant-ID": session.tenantId,
    Authorization: `Bearer ${session.accessToken}`,
  };
}

async function apiGet<T>(path: string, session: ApiSession): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, { headers: headers(session) });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? body.message ?? `HTTP ${res.status}`);
  }
  return (await res.json()).data as T;
}

async function apiPost<T>(path: string, session: ApiSession, body: unknown = {}): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? `HTTP ${res.status}`);
  }
  return (await res.json()).data as T;
}

export async function loginSchSession(tenantId: string, email: string, password: string): Promise<ApiSession> {
  const tenantHeaders = { "Content-Type": "application/json", "X-Tenant-ID": tenantId };
  await fetch(`${API_URL}/api/v1/auth/register`, {
    method: "POST",
    headers: tenantHeaders,
    body: JSON.stringify({ email, password, display_name: "Scheduler Admin" }),
  }).catch(() => undefined);
  const login = await fetch(`${API_URL}/api/v1/auth/login`, {
    method: "POST",
    headers: tenantHeaders,
    body: JSON.stringify({ email, password }),
  });
  if (!login.ok) throw new Error("Login failed — check tenant, email, and password");
  const json = await login.json();
  const session: ApiSession = { tenantId, accessToken: json.data.access_token };
  saveSchSession(session);
  return session;
}

export async function fetchSchCatalog(session: ApiSession): Promise<SchCatalog> {
  return apiGet("/api/v1/enterprise-scheduler/catalog", session);
}

export async function fetchSchDashboard(session: ApiSession): Promise<SchDashboard> {
  return apiGet("/api/v1/enterprise-scheduler/dashboard", session);
}

export async function fetchSchJobs(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-scheduler/jobs", session);
}

export async function fetchSchHistory(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-scheduler/history", session);
}

export async function fetchSchDependencies(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-scheduler/dependencies", session);
}

export async function fetchSchMonitoring(session: ApiSession): Promise<SchMonitoring> {
  return apiGet("/api/v1/enterprise-scheduler/monitoring", session);
}

export async function seedSch(session: ApiSession): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-scheduler/seed", session);
}

export async function triggerSchJob(session: ApiSession, jobRef: string): Promise<Record<string, unknown>> {
  return apiPost(`/api/v1/enterprise-scheduler/jobs/${jobRef}/trigger`, session);
}

export async function pauseSchJob(session: ApiSession, jobRef: string): Promise<Record<string, unknown>> {
  return apiPost(`/api/v1/enterprise-scheduler/jobs/${jobRef}/pause`, session);
}

export async function resumeSchJob(session: ApiSession, jobRef: string): Promise<Record<string, unknown>> {
  return apiPost(`/api/v1/enterprise-scheduler/jobs/${jobRef}/resume`, session);
}

export async function createSchJob(
  session: ApiSession,
  body: { name: string; job_type: string; cron_expression?: string; priority?: number },
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-scheduler/jobs", session, body);
}
