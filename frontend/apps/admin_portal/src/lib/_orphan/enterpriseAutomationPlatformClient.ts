import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadAutomationSession,
  saveSession as saveAutomationSession,
} from "./clientAuth";

export type { ApiSession };

export const loginAutomationSession = createClientLogin("Automation Admin");
export { loadAutomationSession, saveAutomationSession };
export type AutomationCatalog = {
  capabilities: Array<{ capability: string; label: string }>;
  policy_keys: string[];
  no_code_blocks: Array<Record<string, unknown>>;
  no_code: boolean;
  visual_designer: boolean;
};

export type AutomationDashboard = {
  summary: {
    capabilities: number;
    automation_definitions: number;
    no_code_definitions: number;
    automation_instances: number;
    instances_completed: number;
    instances_failed: number;
    awaiting_approval: number;
    success_rate_pct: number;
    step_executions: number;
    pending_approvals: number;
    scheduled_jobs: number;
    active_schedules: number;
    no_code_enabled: boolean;
    ai_enabled: boolean;
  };
  profile: Record<string, unknown> | null;
  instances_by_status: Record<string, number>;
  steps_by_type: Record<string, number>;
  recent_instances: Array<Record<string, unknown>>;
  recent_executions: Array<Record<string, unknown>>;
  pending_approvals: Array<Record<string, unknown>>;
  active_schedules: Array<Record<string, unknown>>;
};

export type DesignerNode = {
  id: string;
  label: string;
  type: string;
  block_type: string;
  x: number;
  y: number;
  color?: string;
  config?: Record<string, unknown>;
  no_code?: boolean;
};

export type AutomationDesignerGraph = {
  definition_ref: string;
  name: string;
  no_code: boolean;
  nodes: DesignerNode[];
  edges: Array<{ from: string; to: string; type: string }>;
  no_code_blocks: Array<Record<string, unknown>>;
  block_palette: Array<{ block_type: string; label: string; color: string }>;
};



export const fetchAutomationCatalog = (s: ApiSession) =>
  apiGet<AutomationCatalog>("/api/v1/enterprise-automation-platform/catalog", s);
export const fetchAutomationDashboard = (s: ApiSession) =>
  apiGet<AutomationDashboard>("/api/v1/enterprise-automation-platform/dashboard", s);
export const fetchAutomationDefinitions = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-automation-platform/definitions", s);
export const fetchAutomationDesigner = (s: ApiSession, definitionRef: string) =>
  apiGet<AutomationDesignerGraph>(`/api/v1/enterprise-automation-platform/definitions/${definitionRef}/designer`, s);
export const fetchAutomationInstances = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-automation-platform/instances", s);
export const fetchAutomationExecutions = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-automation-platform/executions", s);
export const fetchAutomationApprovals = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-automation-platform/approvals", s);
export const fetchAutomationSchedules = (s: ApiSession) =>
  apiGet<Array<Record<string, unknown>>>("/api/v1/enterprise-automation-platform/schedules", s);
export const seedAutomation = (s: ApiSession) =>
  apiPost<Record<string, unknown>>("/api/v1/enterprise-automation-platform/seed", s);
export const startAutomation = (s: ApiSession, definitionRef: string, triggerContext?: Record<string, unknown>) =>
  apiPost<Record<string, unknown>>("/api/v1/enterprise-automation-platform/automations/start", s, {
    definition_ref: definitionRef,
    trigger_context: triggerContext ?? {},
  });
export const advanceAutomation = (s: ApiSession, instanceRef: string) =>
  apiPost<Record<string, unknown>>(`/api/v1/enterprise-automation-platform/automations/${instanceRef}/advance`, s);
export const decideApproval = (s: ApiSession, approvalRef: string, approved: boolean, note = "") =>
  apiPost<Record<string, unknown>>(`/api/v1/enterprise-automation-platform/approvals/${approvalRef}/decide`, s, {
    approved,
    note,
  });
