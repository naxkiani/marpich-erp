import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadFederationSession,
  saveSession as saveFederationSession,
} from "./clientAuth";

export type { ApiSession };
export const loginFederationSession = createClientLogin("Federation Admin");
export { loadFederationSession, saveFederationSession };

export type IntelligenceDashboard = {
  analytics: {
    federation_trends: Record<string, unknown>;
    risk_distribution: Record<string, number>;
    trust_distribution: Record<string, number>;
    failed_logins: number;
    ai_insights?: Array<{ type: string; severity: string; message: string; recommendation: string }>;
  };
  models: Array<{ model_id: string; version: string; type: string; status: string }>;
  ai_metrics: Record<string, unknown>;
  performance_targets: Record<string, unknown>;
  quality_gates: string[];
};

export async function fetchIntelligenceDashboard(session: ApiSession): Promise<IntelligenceDashboard> {
  return apiGet("/api/v1/federation/intelligence/dashboard", session);
}

export async function seedFederation(session: ApiSession): Promise<{ seeded: boolean }> {
  return apiPost("/api/v1/federation/seed", session);
}

export async function listProviders(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/federation/providers", session);
}

export async function predictIdentityRisk(
  session: ApiSession,
  features: Record<string, unknown> = {},
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/federation/intelligence/predict", session, {
    model_id: "identity_risk_predictor_v1",
    features,
  });
}

export async function askCopilot(session: ApiSession, question: string): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/federation/intelligence/copilot", session, { question, context: {} });
}

export async function fetchMesh(session: ApiSession): Promise<Record<string, unknown>> {
  return apiGet("/api/v1/federation/fabric/mesh", session);
}

export async function fetchSecurityDashboard(session: ApiSession): Promise<Record<string, unknown>> {
  return apiGet("/api/v1/federation/fabric/security/dashboard", session);
}

export async function fetchComplianceControls(session: ApiSession): Promise<Record<string, unknown>> {
  return apiGet("/api/v1/federation/intelligence/compliance/controls", session);
}
