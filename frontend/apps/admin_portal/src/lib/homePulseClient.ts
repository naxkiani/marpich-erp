/** Home dashboard pulse — parallel, fail-soft sync with platform services. */

import {
  type ApiSession,
  apiGet,
} from "./clientAuth";
import { fetchAuditStats, queryAuditEntries, type AuditEntry, type AuditStats } from "./auditClient";
import { listInbox, type InboxMessage } from "./notificationsClient";

export type AnalyticsHomePulse = {
  metrics_count: number;
  dashboards_count: number;
  alerts_count: number;
  tenant_id?: string;
  signal_class?: string;
  production_kpis?: string;
  data_quality?: {
    status?: string;
    reason?: string;
    freshness?: string;
    confidence?: string;
  };
};

export function homePulseHasDataQualityWarning(
  pulse: { analytics: AnalyticsHomePulse | null } | null,
): boolean {
  if (!pulse?.analytics) return false;
  return pulse.analytics.data_quality?.status === "DATA_QUALITY_WARNING";
}

export type WorkflowTaskSummary = {
  id: string;
  title?: string;
  status?: string;
  definition_id?: string;
};

export type HomePulseSource =
  | "analytics"
  | "notifications"
  | "workflow"
  | "audit_stats"
  | "audit_recent";

export type HomePulseResult = {
  loadedAt: string;
  analytics: AnalyticsHomePulse | null;
  unreadNotifications: number;
  recentNotifications: InboxMessage[];
  openTasks: number;
  recentTasks: WorkflowTaskSummary[];
  auditStats: AuditStats | null;
  recentAudit: AuditEntry[];
  errors: Partial<Record<HomePulseSource, string>>;
};

function asList<T>(value: unknown): T[] {
  if (Array.isArray(value)) return value as T[];
  return [];
}

async function settle<T>(
  source: HomePulseSource,
  promise: Promise<T>,
  errors: HomePulseResult["errors"],
): Promise<T | null> {
  try {
    return await promise;
  } catch (err) {
    errors[source] = err instanceof Error ? err.message : String(err);
    return null;
  }
}

/**
 * Load home pulse in parallel. Each source fails independently so AuthZ gaps
 * (e.g. missing analytics.dashboards.read) do not blank the whole dashboard.
 */
export async function fetchHomePulse(session: ApiSession): Promise<HomePulseResult> {
  const errors: HomePulseResult["errors"] = {};

  const [analytics, inbox, tasks, auditStats, auditPage] = await Promise.all([
    settle(
      "analytics",
      apiGet<AnalyticsHomePulse>("/api/v1/analytics/home-pulse", session),
      errors,
    ),
    settle("notifications", listInbox(session, true), errors),
    settle(
      "workflow",
      apiGet<WorkflowTaskSummary[] | { items?: WorkflowTaskSummary[] }>(
        "/api/v1/workflow/tasks",
        session,
      ),
      errors,
    ),
    settle("audit_stats", fetchAuditStats(session), errors),
    settle(
      "audit_recent",
      queryAuditEntries(session, { limit: 5, offset: 0 }),
      errors,
    ),
  ]);

  const taskList = asList<WorkflowTaskSummary>(
    Array.isArray(tasks) ? tasks : tasks?.items,
  );
  const inboxList = asList<InboxMessage>(inbox);

  return {
    loadedAt: new Date().toISOString(),
    analytics: analytics,
    unreadNotifications: inboxList.length,
    recentNotifications: inboxList.slice(0, 5),
    openTasks: taskList.length,
    recentTasks: taskList.slice(0, 5),
    auditStats,
    recentAudit: auditPage?.items?.slice(0, 5) ?? [],
    errors,
  };
}

export function homePulseHasPartialErrors(pulse: HomePulseResult | null): boolean {
  if (!pulse) return false;
  return Object.keys(pulse.errors).length > 0;
}
