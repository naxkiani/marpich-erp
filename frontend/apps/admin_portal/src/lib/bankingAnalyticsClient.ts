import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadBankingAnalyticsSession,
  saveSession as saveBankingAnalyticsSession,
} from "./clientAuth";

export type { ApiSession };

export const loginBankingAnalyticsSession = createClientLogin("Banking Analytics Admin");
export { loadBankingAnalyticsSession, saveBankingAnalyticsSession };

export type BankingAnalyticsCapability = {
  capability: string;
  label: string;
  description?: string;
  explainable?: boolean;
  policy_key?: string;
};

export type BankingAnalyticsDashboard = {
  liquidity_kpis: Record<string, unknown>;
  executive_headline: string;
  explainable: boolean;
  recommendation_count?: number;
  [key: string]: unknown;
};

export type BankingExecutiveDashboard = {
  audience: string;
  headline: string;
  explainable: boolean;
  highlights?: string[];
  kpis?: Array<Record<string, unknown>>;
  [key: string]: unknown;
};

export type BankingLiquidityKpis = {
  kpis: Array<Record<string, unknown>>;
  [key: string]: unknown;
};

export type BankingLoanPortfolio = {
  total_loans: number;
  [key: string]: unknown;
};

export type BankingRecommendations = {
  explainable: boolean;
  recommendation_count?: number;
  recommendations: Array<Record<string, unknown>>;
  [key: string]: unknown;
};

export type BankingAnalyticsJob = {
  id?: string;
  job_id?: string;
  capability: string;
  status: string;
  created_at?: string;
  completed_at?: string | null;
  result?: Record<string, unknown> | null;
  [key: string]: unknown;
};

export type BankingAiAssistantResponse = {
  assistant: string;
  explainable: boolean;
  autonomous_execution: boolean;
  insights: Array<Record<string, unknown>>;
  [key: string]: unknown;
};

export async function fetchBankingAnalyticsCatalog(
  session: ApiSession,
): Promise<BankingAnalyticsCapability[]> {
  return apiGet("/api/v1/banking/analytics/catalog", session);
}

export async function fetchBankingAnalyticsDashboard(
  session: ApiSession,
): Promise<BankingAnalyticsDashboard> {
  return apiGet("/api/v1/banking/analytics/dashboard", session);
}

export async function fetchBankingExecutiveDashboard(
  session: ApiSession,
): Promise<BankingExecutiveDashboard> {
  return apiGet("/api/v1/banking/analytics/executive-dashboard", session);
}

export async function fetchBankingLiquidityKpis(
  session: ApiSession,
): Promise<BankingLiquidityKpis> {
  return apiGet("/api/v1/banking/analytics/liquidity-kpis", session);
}

export async function fetchBankingLoanPortfolio(
  session: ApiSession,
): Promise<BankingLoanPortfolio> {
  return apiGet("/api/v1/banking/analytics/loan-portfolio", session);
}

export async function fetchBankingRecommendations(
  session: ApiSession,
): Promise<BankingRecommendations> {
  return apiGet("/api/v1/banking/analytics/recommendations", session);
}

export async function fetchBankingAnalyticsJobs(
  session: ApiSession,
): Promise<BankingAnalyticsJob[]> {
  return apiGet("/api/v1/banking/analytics/jobs", session);
}

export async function runBankingAiAssistant(
  session: ApiSession,
  query: string,
): Promise<BankingAiAssistantResponse> {
  return apiPost("/api/v1/banking/analytics/ai-assistant", session, { query });
}

export async function runBankingAnalysis(
  session: ApiSession,
  capability: string,
  inputData: Record<string, unknown> = {},
): Promise<BankingAnalyticsJob> {
  return apiPost(`/api/v1/banking/analytics/analyze/${capability}`, session, {
    input_data: inputData,
  });
}
