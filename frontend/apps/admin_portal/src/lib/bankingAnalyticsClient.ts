import {
  type ApiSession,
  apiGet,
  apiPost,
  clearSession,
  createClientLogin,
  loadSession as loadBankingAnalyticsSession,
  saveSession as saveBankingAnalyticsSession,
} from "./clientAuth";

export type { ApiSession };

/** True for HTTP auth failures or error messages that mention them. */
export function isAuthFailure(messageOrStatus: string | number): boolean {
  if (typeof messageOrStatus === "number") {
    return messageOrStatus === 401 || messageOrStatus === 403;
  }
  const m = messageOrStatus.toLowerCase();
  return (
    /\b401\b/.test(m) ||
    /\b403\b/.test(m) ||
    m.includes("unauthorized") ||
    m.includes("forbidden") ||
    m.includes("session expired")
  );
}

export const loginBankingAnalyticsSession = createClientLogin("Banking Analytics Admin");
export { loadBankingAnalyticsSession, saveBankingAnalyticsSession };

export function clearBankingAnalyticsSession(): void {
  clearSession();
}

/** Display helper for metrics / unknown API payloads. */
export function compactText(value: unknown): string {
  if (Array.isArray(value)) return value.map((item) => compactText(item)).join(", ");
  if (value && typeof value === "object") {
    try {
      return JSON.stringify(value);
    } catch {
      return String(value);
    }
  }
  if (value === null || value === undefined || value === "") return "—";
  if (typeof value === "number") {
    return Number.isInteger(value)
      ? value.toLocaleString()
      : value.toLocaleString(undefined, { maximumFractionDigits: 4 });
  }
  return String(value);
}

export type BankingAnalyticsPayload = Record<string, unknown>;

export type BankingAnalyticsPolicyKey = {
  key: string;
  description?: string;
  [key: string]: unknown;
};

export type BankingAnalyticsSurface = {
  id: string;
  path: string;
  labelKey: string;
  jewel: "forest" | "royal" | "emerald" | "gold" | "orange" | "purple";
};

/** Capability tabs that load dedicated analytics GET surfaces (not overview/AI/jobs). */
export const BANKING_ANALYTICS_SURFACES: readonly BankingAnalyticsSurface[] = [
  { id: "liquidity_kpis", path: "liquidity-kpis", labelKey: "banking.surface.liquidity_kpis", jewel: "forest" },
  { id: "deposit_trends", path: "deposit-trends", labelKey: "banking.surface.deposit_trends", jewel: "royal" },
  { id: "loan_portfolio", path: "loan-portfolio", labelKey: "banking.surface.loan_portfolio", jewel: "emerald" },
  {
    id: "customer_segmentation",
    path: "customer-segmentation",
    labelKey: "banking.surface.customer_segmentation",
    jewel: "gold",
  },
  {
    id: "branch_performance",
    path: "branch-performance",
    labelKey: "banking.surface.branch_performance",
    jewel: "orange",
  },
  { id: "revenue_analysis", path: "revenue-analysis", labelKey: "banking.surface.revenue_analysis", jewel: "purple" },
  { id: "risk_indicators", path: "risk-indicators", labelKey: "banking.surface.risk_indicators", jewel: "forest" },
  {
    id: "portfolio_quality",
    path: "portfolio-quality",
    labelKey: "banking.surface.portfolio_quality",
    jewel: "royal",
  },
  {
    id: "delinquency_analysis",
    path: "delinquency-analysis",
    labelKey: "banking.surface.delinquency_analysis",
    jewel: "emerald",
  },
  { id: "forecasting", path: "forecasting", labelKey: "banking.surface.forecasting", jewel: "gold" },
  { id: "fraud_detection", path: "fraud-detection", labelKey: "banking.surface.fraud_detection", jewel: "orange" },
  {
    id: "customer_insights",
    path: "customer-insights",
    labelKey: "banking.surface.customer_insights",
    jewel: "purple",
  },
] as const;

export type BankingAnalyticsRow = { id: string; metric: string; value: string };

/** Flatten nested analytics payloads into DataTable rows. */
export function flattenAnalyticsRows(
  payload: BankingAnalyticsPayload | undefined | null,
  group = "surface",
): BankingAnalyticsRow[] {
  if (!payload || typeof payload !== "object") return [];
  const rows: BankingAnalyticsRow[] = [];

  const walk = (obj: Record<string, unknown>, prefix = "") => {
    for (const [key, value] of Object.entries(obj)) {
      const metric = (prefix ? `${prefix}.` : "") + key.replaceAll("_", " ");
      if (value && typeof value === "object" && !Array.isArray(value)) {
        walk(value as Record<string, unknown>, metric);
        continue;
      }
      rows.push({
        id: `${group}-${rows.length}-${key}`,
        metric,
        value: compactText(value),
      });
    }
  };

  walk(payload);
  return rows;
}

export type BankingAnalyticsCapability = {
  capability: string;
  label: string;
  description?: string;
  explainable?: boolean;
  policy_key?: string;
  supported?: boolean;
};

export type BankingAnalyticsDashboard = {
  liquidity_kpis: Record<string, unknown>;
  executive_headline: string;
  explainable: boolean;
  recommendation_count?: number;
  summary?: Record<string, unknown>;
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
  insights: Array<Record<string, unknown> | string>;
  explanation?: string;
  top_recommendations?: Array<Record<string, unknown>>;
  [key: string]: unknown;
};

export async function fetchBankingAnalyticsCatalog(
  session: ApiSession,
): Promise<BankingAnalyticsCapability[]> {
  return apiGet("/api/v1/banking/analytics/catalog", session);
}

export async function fetchBankingAnalyticsPolicyKeys(
  session: ApiSession,
): Promise<BankingAnalyticsPolicyKey[]> {
  return apiGet("/api/v1/banking/analytics/policy-keys", session);
}

export async function fetchBankingAnalyticsSurface(
  session: ApiSession,
  path: string,
): Promise<BankingAnalyticsPayload> {
  const url = path.startsWith("/api/")
    ? path
    : `/api/v1/banking/analytics/${path.replace(/^\//, "")}`;
  return apiGet(url, session);
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
