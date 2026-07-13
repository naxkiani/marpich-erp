import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadEwpSession,
  saveSession as saveEwpSession,
} from "./clientAuth";

export type { ApiSession };

export const loginEwpSession = createClientLogin("Webhook Platform Admin");
export { loadEwpSession, saveEwpSession };
export type EwpCapability = {
  capability: string;
  label: string;
};

export type EwpCatalog = {
  capabilities: EwpCapability[];
  policy_keys: string[];
  auth_methods: string[];
  directions: string[];
  signed_payloads: boolean;
};

export type EwpDashboard = {
  summary: {
    capabilities: number;
    incoming_endpoints: number;
    outgoing_subscriptions: number;
    filter_rules: number;
    deliveries_total: number;
    deliveries_delivered: number;
    deliveries_failed: number;
    success_rate_pct: number;
    replay_jobs: number;
    incoming_receipts: number;
    incoming_signature_valid: number;
    active_secrets: number;
    signature_required: boolean;
    retry_enabled: boolean;
  };
  profile: Record<string, unknown> | null;
  deliveries_by_status: Record<string, number>;
  deliveries_by_direction: Record<string, number>;
  recent_deliveries: Array<Record<string, unknown>>;
  active_replays: Array<Record<string, unknown>>;
  endpoint_health: Array<Record<string, unknown>>;
  subscription_health: Array<Record<string, unknown>>;
};



export function fetchEwpCatalog(session: ApiSession): Promise<EwpCatalog> {
  return apiGet("/api/v1/enterprise-webhook-platform/catalog", session);
}

export function fetchEwpDashboard(session: ApiSession): Promise<EwpDashboard> {
  return apiGet("/api/v1/enterprise-webhook-platform/dashboard", session);
}

export function fetchIncomingEndpoints(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-webhook-platform/incoming-endpoints", session);
}

export function fetchOutgoingSubscriptions(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-webhook-platform/outgoing-subscriptions", session);
}

export function fetchEwpDeliveries(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-webhook-platform/deliveries", session);
}

export function fetchEwpSecrets(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-webhook-platform/secrets", session);
}

export function seedEwp(session: ApiSession): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-webhook-platform/seed", session);
}

export function dispatchOutgoingWebhook(
  session: ApiSession,
  subscriptionRef: string,
  eventName: string,
  payload: Record<string, unknown>,
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-webhook-platform/outgoing/dispatch", session, {
    subscription_ref: subscriptionRef,
    event_name: eventName,
    payload,
  });
}

export function receiveIncomingWebhook(
  session: ApiSession,
  endpointRef: string,
  eventName: string,
  payload: Record<string, unknown>,
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-webhook-platform/incoming/receive", session, {
    endpoint_ref: endpointRef,
    event_name: eventName,
    payload,
  });
}

export function rotateEwpSecret(session: ApiSession, secretRef: string): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-webhook-platform/secrets/rotate", session, { secret_ref: secretRef });
}

export function replayEwpDeliveries(session: ApiSession, limit = 10): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-webhook-platform/replay", session, { limit });
}
