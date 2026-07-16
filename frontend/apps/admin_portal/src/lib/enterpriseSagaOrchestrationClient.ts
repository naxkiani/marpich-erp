import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadSagaSession,
  saveSession as saveSagaSession,
} from "./clientAuth";

export type { ApiSession };

export const loginSagaSession = createClientLogin("Saga Orchestration Admin");
export { loadSagaSession, saveSagaSession };
export type SagaCapability = { capability: string; label: string };

export type SagaCatalog = {
  capabilities: SagaCapability[];
  policy_keys: string[];
};

export type SagaDashboard = {
  summary: {
    capabilities: number;
    saga_definitions: number;
    saga_instances: number;
    instances_completed: number;
    instances_failed: number;
    success_rate_pct: number;
    step_executions: number;
    compensations: number;
    compensation_enabled: boolean;
    rollback_enabled: boolean;
  };
  profile: Record<string, unknown> | null;
  instances_by_status: Record<string, number>;
  steps_by_status: Record<string, number>;
  recent_instances: Array<Record<string, unknown>>;
  recent_compensations: Array<Record<string, unknown>>;
  active_sagas: Array<Record<string, unknown>>;
};

export type DesignerNode = {
  id: string;
  label: string;
  type: string;
  x: number;
  y: number;
  action?: string;
  parent_step?: string;
  index?: number;
};

export type DesignerEdge = { from: string; to: string; type: string };

export type SagaDesignerGraph = {
  definition_ref: string;
  name: string;
  nodes: DesignerNode[];
  edges: DesignerEdge[];
  compensation_edges: DesignerEdge[];
  state_machine: {
    states: string[];
    transitions: Record<string, string[]>;
  };
};



export const fetchSagaCatalog = (s: ApiSession) =>
  apiGet<SagaCatalog>("/api/v1/enterprise-saga-orchestration/catalog", s);
export const fetchSagaDashboard = (s: ApiSession) =>
  apiGet<SagaDashboard>("/api/v1/enterprise-saga-orchestration/dashboard", s);
export const fetchSagaDefinitions = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-saga-orchestration/definitions", s);
export const fetchSagaDesigner = (s: ApiSession, definitionRef: string) =>
  apiGet<SagaDesignerGraph>(`/api/v1/enterprise-saga-orchestration/definitions/${definitionRef}/designer`, s);
export const fetchSagaInstances = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-saga-orchestration/instances", s);
export const fetchSagaExecutions = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-saga-orchestration/executions", s);
export const fetchSagaCompensations = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-saga-orchestration/compensations", s);
export const seedSaga = (s: ApiSession) =>
  apiPost<Record<string, unknown>>("/api/v1/enterprise-saga-orchestration/seed", s);
export const startSaga = (s: ApiSession, definitionRef: string, inputContext?: Record<string, unknown>) =>
  apiPost<Record<string, unknown>>("/api/v1/enterprise-saga-orchestration/sagas/start", s, {
    definition_ref: definitionRef,
    input_context: inputContext ?? {},
  });
export const advanceSaga = (s: ApiSession, sagaRef: string) =>
  apiPost<Record<string, unknown>>(`/api/v1/enterprise-saga-orchestration/sagas/${sagaRef}/advance`, s);
export const compensateSaga = (s: ApiSession, sagaRef: string) =>
  apiPost<Record<string, unknown>>(`/api/v1/enterprise-saga-orchestration/sagas/${sagaRef}/compensate`, s);
export const rollbackSaga = (s: ApiSession, sagaRef: string) =>
  apiPost<Record<string, unknown>>(`/api/v1/enterprise-saga-orchestration/sagas/${sagaRef}/rollback`, s);
