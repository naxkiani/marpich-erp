import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadEebSession,
  saveSession as saveEebSession,
} from "./clientAuth";

export type { ApiSession };

export const loginEebSession = createClientLogin("Event Bus Admin");
export { loadEebSession, saveEebSession };
export type EebCapability = {
  capability: string;
  label: string;
};

export type EebCatalog = {
  capabilities: EebCapability[];
  event_categories: string[];
  policy_keys: string[];
  immutable_events: boolean;
  append_only: boolean;
  transports: string[];
};

export type EebDashboard = {
  summary: {
    capabilities: number;
    event_categories: number;
    catalog_events: number;
    immutable_events: number;
    registered_schemas: number;
    transport_bindings: number;
    active_transports: number;
    publications_recorded: number;
    immutable_events_enforced: boolean;
    append_only: boolean;
  };
  profile: Record<string, unknown> | null;
  catalog_summary: {
    total_events: number;
    immutable_events: number;
    by_category: Record<string, number>;
    entries: Array<Record<string, unknown>>;
  };
  schema_registry_summary: {
    total_schemas: number;
    registered_schemas: number;
    entries: Array<Record<string, unknown>>;
  };
  transports: Array<Record<string, unknown>>;
  event_bus_mode: string;
};

export type EebEventCatalog = {
  total_events: number;
  immutable_events: number;
  by_category: Record<string, number>;
  entries: Array<Record<string, unknown>>;
};

export type EebSchemaRegistry = {
  total_schemas: number;
  registered_schemas: number;
  entries: Array<Record<string, unknown>>;
};


export async function fetchEebCatalog(session: ApiSession): Promise<EebCatalog> {
  return apiGet("/api/v1/enterprise-event-bus/catalog", session);
}

export async function fetchEebDashboard(session: ApiSession): Promise<EebDashboard> {
  return apiGet("/api/v1/enterprise-event-bus/dashboard", session);
}

export async function fetchEventCatalog(session: ApiSession): Promise<EebEventCatalog> {
  return apiGet("/api/v1/enterprise-event-bus/event-catalog", session);
}

export async function fetchSchemaRegistry(session: ApiSession): Promise<EebSchemaRegistry> {
  return apiGet("/api/v1/enterprise-event-bus/schema-registry", session);
}

export async function fetchTransports(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-event-bus/transports", session);
}

export async function fetchPublications(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-event-bus/publications", session);
}

export async function fetchDiscover(session: ApiSession): Promise<{ discovered: number; entries: Array<Record<string, unknown>> }> {
  return apiGet("/api/v1/enterprise-event-bus/discover", session);
}

export async function seedEeb(session: ApiSession): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-event-bus/seed", session);
}

export async function publishEebEvent(
  session: ApiSession,
  body: {
    event_name: string;
    event_version?: number;
    source_context: string;
    payload: Record<string, unknown>;
    transport_type?: string;
  },
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-event-bus/publish", session, {
    event_version: 1,
    transport_type: "in_process",
    ...body,
  });
}

export async function validateEebEnvelope(
  session: ApiSession,
  envelope: Record<string, unknown>,
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-event-bus/validate", session, { envelope });
}

export async function registerEebSchema(
  session: ApiSession,
  body: { event_name: string; event_version?: number; schema_path: string; compatibility?: string },
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-event-bus/schema-registry", session, {
    event_version: 1,
    compatibility: "backward",
    ...body,
  });
}
