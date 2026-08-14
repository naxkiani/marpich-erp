import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadEmoSession,
  saveSession as saveEmoSession,
} from "./clientAuth";

export type { ApiSession };

export const loginEmoSession = createClientLogin("Message Orchestration Admin");
export { loadEmoSession, saveEmoSession };
export type EmoCapability = {
  capability: string;
  label: string;
};

export type EmoCatalog = {
  capabilities: EmoCapability[];
  policy_keys: string[];
  queue_types: string[];
  exactly_once: boolean;
  ordering: boolean;
};

export type EmoDashboard = {
  summary: {
    capabilities: number;
    routing_rules: number;
    transformation_rules: number;
    queue_bindings: number;
    messages_total: number;
    messages_delivered: number;
    messages_failed: number;
    success_rate_pct: number;
    replay_jobs: number;
    delivery_receipts: number;
    exactly_once_enforced: boolean;
    ordering_enforced: boolean;
  };
  profile: Record<string, unknown> | null;
  messages_by_status: Record<string, number>;
  queues_by_type: Record<string, number>;
  recent_messages: Array<Record<string, unknown>>;
  active_replays: Array<Record<string, unknown>>;
  queue_health: Array<{ queue_type: string; queue_name: string; status: string }>;
};

export type EmoWorkerStatus = {
  enabled: boolean;
  running: boolean;
  poll_interval_ms: number;
  batch_size: number;
  pending_total: number;
  pending_by_queue: Record<string, number>;
  last_batch: Record<string, number> | null;
};


export async function fetchEmoCatalog(session: ApiSession): Promise<EmoCatalog> {
  return apiGet("/api/v1/enterprise-message-orchestration/catalog", session);
}

export async function fetchEmoDashboard(session: ApiSession): Promise<EmoDashboard> {
  return apiGet("/api/v1/enterprise-message-orchestration/dashboard", session);
}

export async function fetchEmoWorkerStatus(session: ApiSession): Promise<EmoWorkerStatus> {
  return apiGet("/api/v1/enterprise-message-orchestration/worker/status", session);
}

export async function fetchEmoMessages(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-message-orchestration/messages", session);
}

export async function fetchEmoQueues(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-message-orchestration/queues", session);
}

export async function seedEmo(session: ApiSession): Promise<{ seeded: boolean }> {
  return apiPost("/api/v1/enterprise-message-orchestration/seed", session);
}

export async function dispatchEmoMessage(
  session: ApiSession,
  body: {
    topic: string;
    payload: Record<string, unknown>;
    idempotency_key?: string;
    failed?: boolean;
    retry_count?: number;
    priority?: number;
    delay_seconds?: number;
    scheduled?: boolean;
  },
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-message-orchestration/dispatch", session, body);
}

export async function workerDispatchOnce(session: ApiSession): Promise<Record<string, number>> {
  return apiPost("/api/v1/enterprise-message-orchestration/worker/dispatch-once", session);
}

export async function archiveEmoMessage(
  session: ApiSession,
  messageRef: string,
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-message-orchestration/archive", session, { message_ref: messageRef });
}

export async function replayEmoMessages(
  session: ApiSession,
  sourceArchive: string,
  limit = 10,
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-message-orchestration/replay", session, {
    source_archive: sourceArchive,
    limit,
  });
}
