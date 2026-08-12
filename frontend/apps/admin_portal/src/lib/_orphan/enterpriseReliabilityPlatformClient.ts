import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadReliabilitySession,
  saveSession as saveReliabilitySession,
} from "./clientAuth";

export type { ApiSession };

export const loginReliabilitySession = createClientLogin("Reliability Admin");
export { loadReliabilitySession, saveReliabilitySession };
export type ReliabilityCapability = { capability: string; label: string };

export type ReliabilityCatalog = {
  capabilities: ReliabilityCapability[];
  policy_keys: string[];
  outbox_pattern: boolean;
  inbox_pattern: boolean;
  exactly_once_semantics: boolean;
};

export type ReliabilityDashboard = {
  summary: {
    capabilities: number;
    outbox_messages: number;
    inbox_messages: number;
    idempotency_records: number;
    deduplication_events: number;
    delivery_attempts: number;
    delivery_rate_pct: number;
    dedup_rate_pct: number;
    attempt_success_rate_pct: number;
    processed_inbox: number;
    duplicate_inbox: number;
    failed_outbox: number;
    recovery_jobs: number;
    active_recoveries: number;
    outbox_enabled: boolean;
    inbox_enabled: boolean;
    exactly_once_enabled: boolean;
  };
  profile: Record<string, unknown> | null;
  outbox_by_status: Record<string, number>;
  inbox_by_status: Record<string, number>;
  delivery_by_status: Record<string, number>;
  recent_outbox: Array<Record<string, unknown>>;
  recent_inbox: Array<Record<string, unknown>>;
  recent_deliveries: Array<Record<string, unknown>>;
  recent_deduplications: Array<Record<string, unknown>>;
  recent_recoveries: Array<Record<string, unknown>>;
  failed_outbox: Array<Record<string, unknown>>;
};



export const fetchReliabilityCatalog = (s: ApiSession) =>
  apiGet<ReliabilityCatalog>("/api/v1/enterprise-reliability-platform/catalog", s);
export const fetchReliabilityDashboard = (s: ApiSession) =>
  apiGet<ReliabilityDashboard>("/api/v1/enterprise-reliability-platform/dashboard", s);
export const fetchReliabilityOutbox = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-reliability-platform/outbox", s);
export const fetchReliabilityInbox = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-reliability-platform/inbox", s);
export const fetchReliabilityDeliveries = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-reliability-platform/deliveries", s);
export const fetchReliabilityDeduplications = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-reliability-platform/deduplications", s);
export const fetchReliabilityIdempotency = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-reliability-platform/idempotency", s);
export const fetchReliabilityRecoveries = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-reliability-platform/recovery", s);
export const seedReliability = (s: ApiSession) =>
  apiPost<Record<string, unknown>>("/api/v1/enterprise-reliability-platform/seed", s);
export const publishOutbox = (s: ApiSession, messageRef: string, simulateFailure = false) =>
  apiPost<Record<string, unknown>>(`/api/v1/enterprise-reliability-platform/outbox/${messageRef}/publish`, s, {
    simulate_failure: simulateFailure,
  });
export const processInbox = (s: ApiSession, inboxRef: string) =>
  apiPost<Record<string, unknown>>(`/api/v1/enterprise-reliability-platform/inbox/${inboxRef}/process`, s);
export const replayMessage = (s: ApiSession, messageRef: string, channel = "outbox") =>
  apiPost<Record<string, unknown>>(`/api/v1/enterprise-reliability-platform/replay/${messageRef}`, s, { channel });
export const startRecovery = (s: ApiSession, scope = "failed_outbox") =>
  apiPost<Record<string, unknown>>("/api/v1/enterprise-reliability-platform/recovery/start", s, { scope });
