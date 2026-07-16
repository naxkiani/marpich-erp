"use client";

import { LoginGate, useAuth, type AuthSession } from "@marpich/auth-provider";
import { PageLayout } from "@marpich/core";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast } from "@marpich/shared";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  createSchJob,
  fetchSchCatalog,
  fetchSchDashboard,
  fetchSchDependencies,
  fetchSchHistory,
  fetchSchJobs,
  fetchSchMonitoring,
  pauseSchJob,
  resumeSchJob,
  seedSch,
  triggerSchJob,
  type SchCatalog,
  type SchDashboard,
  type SchMonitoring,
} from "@/lib/enterpriseSchedulerClient";

const CAPABILITY_LABELS: Record<string, string> = {
  cron_jobs: "Cron Jobs",
  calendar_jobs: "Calendar Jobs",
  recurring_jobs: "Recurring Jobs",
  event_triggered_jobs: "Event Triggered Jobs",
  workflow_triggered_jobs: "Workflow Triggered Jobs",
  retry: "Retry",
  priority: "Priority",
  dependency: "Dependency",
  distributed_scheduling: "Distributed Scheduling",
  job_history: "Job History",
  monitoring: "Monitoring",
  scheduler_dashboard: "Scheduler Dashboard",
};

const JOB_TYPE_LABELS: Record<string, string> = {
  cron: "Cron",
  calendar: "Calendar",
  recurring: "Recurring",
  event: "Event",
  workflow: "Workflow",
};

export function EnterpriseSchedulerDashboardPage() {
  const { push } = useToast();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(15);
  const [error, setError] = useState<string | null>(null);

  const [catalog, setCatalog] = useState<SchCatalog | null>(null);
  const [dashboard, setDashboard] = useState<SchDashboard | null>(null);
  const [monitoring, setMonitoring] = useState<SchMonitoring | null>(null);
  const [jobs, setJobs] = useState<Array<Record<string, unknown>>>([]);
  const [history, setHistory] = useState<Array<Record<string, unknown>>>([]);
  const [dependencies, setDependencies] = useState<Array<Record<string, unknown>>>([]);
  const [lastAction, setLastAction] = useState<string | null>(null);

  const loadData = useCallback(async (active: AuthSession) => {
    setLoading(true);
    setProgress(30);
    setError(null);
    try {
      const [cat, dash, mon, jobList, hist, deps] = await Promise.all([
        fetchSchCatalog(active),
        fetchSchDashboard(active),
        fetchSchMonitoring(active),
        fetchSchJobs(active),
        fetchSchHistory(active),
        fetchSchDependencies(active),
      ]);
      setCatalog(cat);
      setDashboard(dash);
      setMonitoring(mon);
      setJobs(jobList);
      setHistory(hist);
      setDependencies(deps);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load scheduler dashboard");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (authLoading) return;
    if (session) {
      void loadData(session);
      return;
    }
    setLoading(false);
    setProgress(100);
  }, [authLoading, loadData, session]);

  const stats = useMemo(() => {
    if (!dashboard) return [];
    const s = dashboard.summary;
    return [
      { label: "Jobs", value: s.jobs_total, tone: "ok" as const },
      { label: "Executions", value: s.executions_total, tone: "ok" as const },
      { label: "Success rate", value: `${s.success_rate_pct}%`, tone: s.success_rate_pct < 90 ? "warn" : "ok" },
      { label: "Running", value: s.running, tone: s.running ? "warn" : "ok" },
      { label: "Failed", value: s.failed, tone: s.failed ? "warn" : "ok" },
      { label: "Paused", value: s.paused_jobs, tone: s.paused_jobs ? "warn" : "ok" },
      { label: "Dependencies", value: s.dependencies, tone: "ok" as const },
      { label: "Shards", value: s.distributed_shards, tone: "ok" as const },
    ];
  }, [dashboard]);

  const capabilityRows = useMemo(() => {
    if (!catalog) return [];
    return catalog.capabilities.map((c) => ({
      capability: CAPABILITY_LABELS[c.capability] ?? c.label,
      key: c.capability,
    }));
  }, [catalog]);

  const jobRows = useMemo(
    () =>
      jobs.map((j) => ({
        ref: String(j.job_ref ?? "—"),
        name: String(j.name ?? "—"),
        type: JOB_TYPE_LABELS[String(j.job_type)] ?? String(j.job_type),
        status: String(j.status ?? "—"),
        priority: String(j.priority ?? "—"),
        shard: String(j.worker_shard ?? "—"),
      })),
    [jobs],
  );

  const historyRows = useMemo(
    () =>
      history.slice(0, 20).map((h) => ({
        ref: String(h.execution_ref ?? "—"),
        job: String(h.job_ref ?? "—"),
        status: String(h.status ?? "—"),
        attempt: String(h.attempt ?? "—"),
        duration: `${h.duration_ms ?? 0}ms`,
      })),
    [history],
  );

  const depRows = useMemo(
    () =>
      dependencies.map((d) => ({
        job: String(d.job_ref ?? "—"),
        depends_on: String(d.depends_on_job_ref ?? "—"),
        required: String(d.required_status ?? "—"),
      })),
    [dependencies],
  );

  async function runAction(label: string, fn: (s: AuthSession) => Promise<unknown>) {
    if (!session) return;
    try {
      await fn(session);
      setLastAction(label);
      await loadData(session);
      push({ message: `${label} completed` });
    } catch (err) {
      push({ message: err instanceof Error ? err.message : `${label} failed` });
    }
  }

  const firstJobRef = jobs[0]?.job_ref ? String(jobs[0].job_ref) : null;

  return (
    <PageLayout
      title="Enterprise Scheduler"
      breadcrumb={[
        { label: "Marpich", href: "/" },
        { label: "Enterprise", href: "/modules" },
        { label: "Scheduler" },
      ]}
      actions={
        isAuthenticated && session ? (
          <>
            <button type="button" className="mp-btn" onClick={() => void runAction("Seed", seedSch)}>
              Seed
            </button>
            <button
              type="button"
              className="mp-btn"
              onClick={() =>
                void runAction("Create cron job", (s) =>
                  createSchJob(s, { name: "Ad-hoc Cron", job_type: "cron", cron_expression: "0 */6 * * *", priority: 6 }),
                )
              }
            >
              New cron job
            </button>
            {firstJobRef ? (
              <button
                type="button"
                className="mp-btn mp-btn-primary"
                onClick={() => void runAction("Trigger", (s) => triggerSchJob(s, firstJobRef))}
              >
                Trigger latest
              </button>
            ) : null}
            <button type="button" className="mp-btn" onClick={() => session && void loadData(session)} disabled={loading}>
              Refresh
            </button>
          </>
        ) : null
      }
    >
      <p className="sch-subtitle">
        Cron, calendar, recurring, event and workflow triggered jobs with retry, priority, dependency chains, distributed scheduling, history, and monitoring.
      </p>

      <ProgressBar value={progress} label={loading ? "Loading scheduler dashboard…" : "Dashboard ready"} />

      {!isAuthenticated ? (
        <LoginGate
          title="Connect to API"
          defaultTenantId="sch-demo"
          defaultEmail="admin@sch.dev"
        />
      ) : null}

      {error ? <p className="sch-error" role="alert">{error}</p> : null}
      {isAuthenticated && loading ? <SkeletonTable rows={4} cols={4} /> : null}

      {isAuthenticated && dashboard && !loading ? (
        <>
          <p className="sch-muted">
            Tenant <strong>{session?.tenantId}</strong>
            {lastAction ? ` · Last action: ${lastAction}` : ""}
            {monitoring ? ` · ${monitoring.success_rate_pct}% success` : ""}
          </p>

          <div className="sch-stats">
            {stats.map((stat) => (
              <article key={stat.label} className={`sch-stat${stat.tone === "warn" ? " sch-stat-warn" : ""}`}>
                <span className="sch-stat-value">{stat.value}</span>
                <span className="sch-stat-label">{stat.label}</span>
              </article>
            ))}
          </div>

          {monitoring ? (
            <div className="sch-context">
              {Object.entries(monitoring.jobs_by_type).map(([type, count]) => (
                <span key={type}>{JOB_TYPE_LABELS[type] ?? type}: {count}</span>
              ))}
            </div>
          ) : null}

          <div className="sch-grid">
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

            <section aria-labelledby="deps-heading">
              <h2 id="deps-heading">Job dependencies ({dependencies.length})</h2>
              {depRows.length ? (
                <DataTable
                  columns={[
                    { key: "job", header: "Job", sortable: true },
                    { key: "depends_on", header: "Depends on", sortable: true },
                    { key: "required", header: "Required", sortable: true },
                  ]}
                  rows={depRows}
                />
              ) : (
                <EmptyState title="No dependencies" description="Run Seed to link dependent jobs." />
              )}
            </section>
          </div>

          <section aria-labelledby="jobs-heading">
            <h2 id="jobs-heading">Scheduled jobs ({jobs.length})</h2>
            {jobRows.length ? (
              <>
                <DataTable
                  columns={[
                    { key: "ref", header: "Ref", sortable: true },
                    { key: "name", header: "Name", sortable: true },
                    { key: "type", header: "Type", sortable: true },
                    { key: "status", header: "Status", sortable: true },
                    { key: "priority", header: "Priority", sortable: true },
                    { key: "shard", header: "Shard", sortable: true },
                  ]}
                  rows={jobRows}
                />
                <div className="sch-actions-row">
                  {jobs.slice(0, 3).map((j) => {
                    const ref = String(j.job_ref);
                    const isPaused = j.status === "paused";
                    return (
                      <button
                        key={ref}
                        type="button"
                        className="mp-btn"
                        onClick={() =>
                          void runAction(isPaused ? "Resume" : "Pause", (s) =>
                            isPaused ? resumeSchJob(s, ref) : pauseSchJob(s, ref),
                          )
                        }
                      >
                        {isPaused ? "Resume" : "Pause"} {String(j.name).slice(0, 12)}
                      </button>
                    );
                  })}
                </div>
              </>
            ) : (
              <EmptyState
                title="No jobs"
                description="Seed defaults or create a cron job."
                action={
                  <button type="button" className="mp-btn mp-btn-primary" onClick={() => void runAction("Seed", seedSch)}>
                    Seed defaults
                  </button>
                }
              />
            )}
          </section>

          <section aria-labelledby="history-heading">
            <h2 id="history-heading">Job history ({history.length})</h2>
            {historyRows.length ? (
              <DataTable
                columns={[
                  { key: "ref", header: "Execution", sortable: true },
                  { key: "job", header: "Job", sortable: true },
                  { key: "status", header: "Status", sortable: true },
                  { key: "attempt", header: "Attempt", sortable: true },
                  { key: "duration", header: "Duration", sortable: true },
                ]}
                rows={historyRows}
              />
            ) : (
              <EmptyState title="No history" description="Trigger a job to record execution history." />
            )}
          </section>
        </>
      ) : null}

      <style jsx>{`
        .sch-subtitle { color: var(--mp-text-muted, #64748b); margin: 0 0 1rem; }
        .sch-connect { margin: 1rem 0 1.5rem; padding: 1rem; border: 1px solid var(--mp-border, #e2e8f0); border-radius: 8px; }
        .sch-form { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem; align-items: end; margin-top: 0.75rem; }
        label { display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.85rem; }
        .sch-muted { color: var(--mp-text-muted, #64748b); margin: 0.5rem 0; }
        .sch-error { color: #b91c1c; margin: 0.75rem 0; }
        .sch-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 0.75rem; margin: 1rem 0; }
        .sch-stat { padding: 1rem; border-radius: 8px; background: var(--mp-surface-2, #f8fafc); border: 1px solid var(--mp-border, #e2e8f0); }
        .sch-stat-warn { border-color: #f59e0b; background: #fffbeb; }
        .sch-stat-value { display: block; font-size: 1.2rem; font-weight: 700; }
        .sch-stat-label { font-size: 0.75rem; color: var(--mp-text-muted, #64748b); }
        .sch-context { display: flex; flex-wrap: wrap; gap: 1rem; font-size: 0.85rem; color: var(--mp-text-muted, #64748b); margin-bottom: 1rem; }
        .sch-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 1.25rem; margin-bottom: 1.5rem; }
        .sch-actions-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; }
        h2 { margin: 0 0 0.75rem; font-size: 1.1rem; }
        @media (max-width: 960px) { .sch-grid { grid-template-columns: 1fr; } }
      `}</style>
    </PageLayout>
  );
}
