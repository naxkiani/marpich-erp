import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadSchSession,
  saveSession as saveSchSession,
} from "./clientAuth";

export type { ApiSession };

export const loginSchSession = createClientLogin("Scheduler Admin");
export { loadSchSession, saveSchSession };
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
