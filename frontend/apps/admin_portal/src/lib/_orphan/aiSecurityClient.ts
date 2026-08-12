import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadAISecuritySession,
  saveSession as saveAISecuritySession,
} from "./clientAuth";

export type { ApiSession };

export const loginAISecuritySession = createClientLogin("AI Security Admin");
export { loadAISecuritySession, saveAISecuritySession };
export type AISecurityEvidence = {
  security_events: Array<Record<string, unknown>>;
  policy_references: Array<Record<string, unknown>>;
  audit_evidence: Array<Record<string, unknown>>;
};

export type AISecurityRecommendation = {
  recommendation_ref: string;
  capability: string;
  title: string;
  recommendation: string;
  explanation: string;
  evidence: AISecurityEvidence;
  data_sources: string[];
  confidence: number;
  explainable: boolean;
  autonomous_execution: boolean;
  has_traceable_evidence: boolean;
  created_at: string;
};

export type AISecurityDashboard = {
  summary: {
    capabilities: number;
    recommendations: number;
    analyses: number;
    executive_reports: number;
    attack_events: number;
    open_incidents: number;
    fraud_alerts: number;
    all_recommendations_evidence_backed: boolean;
    evidence_required: boolean;
  };
  by_capability: Record<string, number>;
  security_context: {
    failed_logins_24h: number;
    anomaly_score: number;
    high_risk_items: number;
  };
  recent_recommendations: AISecurityRecommendation[];
  delegation: Record<string, boolean>;
  generated_at: string;
};

export type AISecurityCatalog = {
  capabilities: Array<{ capability: string; label: string; explainable?: boolean }>;
  policy_keys: string[];
  explainable: boolean;
  autonomous_execution: boolean;
  evidence_required: boolean;
};


export async function fetchAISecurityCatalog(session: ApiSession): Promise<AISecurityCatalog> {
  return apiGet("/api/v1/ai-security/catalog", session);
}

export async function fetchAISecurityDashboard(session: ApiSession): Promise<AISecurityDashboard> {
  return apiGet("/api/v1/ai-security/dashboard", session);
}

export async function fetchAISecurityRecommendations(
  session: ApiSession,
): Promise<AISecurityRecommendation[]> {
  return apiGet("/api/v1/ai-security/recommendations", session);
}

export async function seedAISecurity(session: ApiSession): Promise<{ seeded: boolean }> {
  return apiPost("/api/v1/ai-security/seed", session);
}

export async function analyzeThreats(
  session: ApiSession,
): Promise<{ recommendations: AISecurityRecommendation[]; count: number }> {
  return apiPost("/api/v1/ai-security/analyze/threats", session);
}

export async function analyzeFraud(session: ApiSession): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/ai-security/analyze/fraud", session);
}

export async function analyzeRisk(session: ApiSession): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/ai-security/analyze/risk", session);
}

export async function analyzeAnomalies(session: ApiSession): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/ai-security/analyze/anomalies", session);
}

export async function assessIdentityRisk(session: ApiSession): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/ai-security/analyze/identity-risk", session);
}

export async function generateExecutiveReport(session: ApiSession): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/ai-security/executive-report", session);
}

export async function fetchIncidentSummary(session: ApiSession): Promise<Record<string, unknown>> {
  return apiGet("/api/v1/ai-security/incidents/summary", session);
}
