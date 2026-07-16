import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadApiSession,
  saveSession as saveApiSession,
} from "./clientAuth";

export type { ApiSession };

export const loginFxSecuritySession = createClientLogin("FX Security Admin");
export { loadApiSession, saveApiSession };
export type FxSecurityFreeze = {
  freeze_ref: string;
  scope: string;
  scope_value?: string | null;
  reason: string;
  is_active: boolean;
  created_at?: string;
};

export type FxSecurityAuditEntry = {
  audit_ref: string;
  action: string;
  subject_ref: string;
  subject_type: string;
  detail: string;
  operation_type?: string;
  amount?: number;
  currency?: string;
  created_at: string;
};

export type FxSecurityDashboard = {
  active_policies: number;
  active_limits: number;
  access_rules: number;
  active_freezes: number;
  pending_operations: number;
  audit_entries: number;
  financial_actions_audited: number;
};

export async function fetchFxSecurityDashboard(
  session: ApiSession,
): Promise<FxSecurityDashboard> {
  return apiGet("/api/v1/currency-exchange/security/dashboard", session);
}

export async function fetchFxSecurityFreezes(
  session: ApiSession,
): Promise<FxSecurityFreeze[]> {
  return apiGet("/api/v1/currency-exchange/security/freezes", session);
}

export async function fetchFxSecurityAuditTrail(
  session: ApiSession,
): Promise<FxSecurityAuditEntry[]> {
  return apiGet("/api/v1/currency-exchange/security/audit-trail", session);
}

