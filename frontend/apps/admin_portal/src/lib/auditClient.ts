import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadAuditSession,
  saveSession as saveAuditSession,
} from "./clientAuth";

export type { ApiSession };
export const loginAuditSession = createClientLogin("Audit Admin");
export { loadAuditSession, saveAuditSession };

export type AuditEntry = {
  id: string;
  tenant_id: string;
  event_name: string;
  source_context: string;
  correlation_id: string;
  action: string;
  resource_type: string;
  resource_id?: string | null;
  actor_id?: string | null;
  severity: string;
  payload?: Record<string, unknown>;
  occurred_at: string;
  recorded_at: string;
};

export type AuditEntriesPage = {
  items: AuditEntry[];
  total: number;
  limit: number;
  offset: number;
};

export type AuditStats = {
  total_entries: number;
  security_events: number;
  last_24h: number;
  top_events: Array<{ event_name: string; count: number }>;
};

export type AuditExport = {
  id: string;
  tenant_id: string;
  status: string;
  format: string;
  filters: Record<string, unknown>;
  entry_count: number;
  error?: string | null;
  requested_by?: string | null;
  created_at: string;
  completed_at?: string | null;
  data?: AuditEntry[];
};

export type RecordAuditPayload = {
  action: string;
  resource_type: string;
  resource_id?: string | null;
  severity?: "info" | "security" | "compliance";
  payload?: Record<string, unknown>;
};

export type CreateExportPayload = {
  format?: "json" | "csv";
  event_name?: string | null;
  severity?: string | null;
  actor_id?: string | null;
  date_from?: string | null;
  date_to?: string | null;
};

export async function queryAuditEntries(
  session: ApiSession,
  params: {
    event_name?: string;
    severity?: string;
    actor_id?: string;
    date_from?: string;
    date_to?: string;
    limit?: number;
    offset?: number;
  } = {},
): Promise<AuditEntriesPage> {
  const qs = new URLSearchParams();
  if (params.event_name) qs.set("event_name", params.event_name);
  if (params.severity) qs.set("severity", params.severity);
  if (params.actor_id) qs.set("actor_id", params.actor_id);
  if (params.date_from) qs.set("date_from", params.date_from);
  if (params.date_to) qs.set("date_to", params.date_to);
  if (params.limit != null) qs.set("limit", String(params.limit));
  if (params.offset != null) qs.set("offset", String(params.offset));
  const q = qs.toString();
  return apiGet(`/api/v1/audit/entries${q ? `?${q}` : ""}`, session);
}

export async function getAuditEntry(session: ApiSession, entryId: string): Promise<AuditEntry> {
  return apiGet(`/api/v1/audit/entries/${encodeURIComponent(entryId)}`, session);
}

export async function recordAuditEntry(
  session: ApiSession,
  payload: RecordAuditPayload,
): Promise<AuditEntry> {
  return apiPost("/api/v1/audit/entries", session, payload);
}

export async function fetchAuditStats(session: ApiSession): Promise<AuditStats> {
  return apiGet("/api/v1/audit/stats", session);
}

export async function createAuditExport(
  session: ApiSession,
  payload: CreateExportPayload,
): Promise<AuditExport> {
  return apiPost("/api/v1/audit/exports", session, payload);
}

export async function getAuditExport(session: ApiSession, exportId: string): Promise<AuditExport> {
  return apiGet(`/api/v1/audit/exports/${encodeURIComponent(exportId)}`, session);
}
