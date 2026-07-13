import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadEcfSession,
  saveSession as saveEcfSession,
} from "./clientAuth";

export type { ApiSession };

export const loginEcfSession = createClientLogin("Connector Framework Admin");
export { loadEcfSession, saveEcfSession };
export type EcfCapability = { capability: string; label: string };

export type EcfCatalog = {
  capabilities: EcfCapability[];
  policy_keys: string[];
  connector_types: string[];
  sdk_types: string[];
  plugin_extensible: boolean;
  connector_sdk: string;
};

export type EcfDashboard = {
  summary: {
    capabilities: number;
    connector_instances: number;
    active_instances: number;
    plugin_bindings: number;
    sdk_registered_types: number;
    executions_total: number;
    executions_succeeded: number;
    success_rate_pct: number;
    health_checks: number;
    healthy_connectors: number;
    health_check_enabled: boolean;
    plugin_connectors_enabled: boolean;
  };
  profile: Record<string, unknown> | null;
  instances_by_status: Record<string, number>;
  instances_by_type: Record<string, number>;
  executions_by_status: Record<string, number>;
  recent_executions: Array<Record<string, unknown>>;
  instance_health: Array<Record<string, unknown>>;
  plugin_bindings: Array<Record<string, unknown>>;
};



export const fetchEcfCatalog = (s: ApiSession) => apiGet<EcfCatalog>("/api/v1/enterprise-connector-framework/catalog", s);
export const fetchEcfDashboard = (s: ApiSession) => apiGet<EcfDashboard>("/api/v1/enterprise-connector-framework/dashboard", s);
export const fetchEcfConnectors = (s: ApiSession) => apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-connector-framework/connectors", s);
export const fetchEcfConnectorCatalog = (s: ApiSession) => apiGet<{ total: number; entries: Array<Record<string, unknown>> }>("/api/v1/enterprise-connector-framework/connector-catalog", s);
export const fetchEcfSdk = (s: ApiSession) => apiGet<Record<string, unknown>>("/api/v1/enterprise-connector-framework/sdk", s);
export const fetchEcfExecutions = (s: ApiSession) => apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-connector-framework/executions", s);
export const seedEcf = (s: ApiSession) => apiPost<Record<string, unknown>>("/api/v1/enterprise-connector-framework/seed", s);
export const testEcfConnector = (s: ApiSession, instanceRef: string) =>
  apiPost<Record<string, unknown>>(`/api/v1/enterprise-connector-framework/connectors/${instanceRef}/test`, s);
export const executeEcfOperation = (s: ApiSession, instanceRef: string, operation: string, payload: Record<string, unknown>) =>
  apiPost<Record<string, unknown>>(`/api/v1/enterprise-connector-framework/connectors/${instanceRef}/execute`, s, { operation, payload });
