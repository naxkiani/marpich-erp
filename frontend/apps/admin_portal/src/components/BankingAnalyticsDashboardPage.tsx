"use client";

import { PageLayout } from "@marpich/core";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast } from "@marpich/shared";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  fetchBankingAnalyticsCatalog,
  fetchBankingAnalyticsDashboard,
  fetchBankingAnalyticsJobs,
  fetchBankingExecutiveDashboard,
  fetchBankingLiquidityKpis,
  fetchBankingLoanPortfolio,
  fetchBankingRecommendations,
  loadBankingAnalyticsSession,
  loginBankingAnalyticsSession,
  runBankingAiAssistant,
  runBankingAnalysis,
  saveBankingAnalyticsSession,
  type ApiSession,
  type BankingAiAssistantResponse,
  type BankingAnalyticsCapability,
  type BankingAnalyticsDashboard,
  type BankingAnalyticsJob,
  type BankingExecutiveDashboard,
  type BankingLiquidityKpis,
  type BankingLoanPortfolio,
  type BankingRecommendations,
} from "@/lib/bankingAnalyticsClient";

function asMetricRows(record: Record<string, unknown>, fallbackGroup: string) {
  return Object.entries(record)
    .filter(([, value]) => typeof value !== "object")
    .map(([key, value], index) => ({
      id: `${fallbackGroup}-${index}`,
      metric: key.replaceAll("_", " "),
      value:
        typeof value === "number"
          ? Number.isInteger(value)
            ? value.toLocaleString()
            : value.toFixed(2)
          : String(value),
    }));
}

function compactText(value: unknown) {
  if (Array.isArray(value)) return value.join(", ");
  if (value && typeof value === "object") return JSON.stringify(value);
  return String(value ?? "—");
}

export function BankingAnalyticsDashboardPage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(15);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("bank-demo");
  const [email, setEmail] = useState("analytics@bank.dev");
  const [password, setPassword] = useState("SecurePass123!");
  const [aiQuery, setAiQuery] = useState("Which portfolio segment needs attention first?");

  const [catalog, setCatalog] = useState<BankingAnalyticsCapability[]>([]);
  const [dashboard, setDashboard] = useState<BankingAnalyticsDashboard | null>(null);
  const [executive, setExecutive] = useState<BankingExecutiveDashboard | null>(null);
  const [liquidity, setLiquidity] = useState<BankingLiquidityKpis | null>(null);
  const [loanPortfolio, setLoanPortfolio] = useState<BankingLoanPortfolio | null>(null);
  const [recommendations, setRecommendations] = useState<BankingRecommendations | null>(null);
  const [jobs, setJobs] = useState<BankingAnalyticsJob[]>([]);
  const [assistant, setAssistant] = useState<BankingAiAssistantResponse | null>(null);
  const [lastAction, setLastAction] = useState<string | null>(null);

  const loadData = useCallback(async (active: ApiSession) => {
    setLoading(true);
    setProgress(30);
    setError(null);
    try {
      const [cat, dash, exec, liq, loans, recs, jobList] = await Promise.all([
        fetchBankingAnalyticsCatalog(active),
        fetchBankingAnalyticsDashboard(active),
        fetchBankingExecutiveDashboard(active),
        fetchBankingLiquidityKpis(active),
        fetchBankingLoanPortfolio(active),
        fetchBankingRecommendations(active),
        fetchBankingAnalyticsJobs(active),
      ]);
      setCatalog(cat);
      setDashboard(dash);
      setExecutive(exec);
      setLiquidity(liq);
      setLoanPortfolio(loans);
      setRecommendations(recs);
      setJobs(jobList);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load Banking Analytics dashboard");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const stored = loadBankingAnalyticsSession();
    if (stored) {
      setSession(stored);
      void loadData(stored);
      return;
    }
    setLoading(false);
    setProgress(100);
  }, [loadData]);

  const statCards = useMemo(() => {
    if (!dashboard) return [];
    const liquidityKpis =
      dashboard.liquidity_kpis && typeof dashboard.liquidity_kpis === "object"
        ? Object.keys(dashboard.liquidity_kpis).length
        : 0;
    return [
      { label: "Capabilities", value: catalog.length, tone: "ok" as const },
      { label: "Liquidity KPIs", value: liquidityKpis, tone: "ok" as const },
      {
        label: "Recommendations",
        value: recommendations?.recommendations.length ?? recommendations?.recommendation_count ?? 0,
        tone: "ok" as const,
      },
      { label: "Jobs", value: jobs.length, tone: jobs.length ? ("ok" as const) : ("warn" as const) },
      { label: "Explainable", value: dashboard.explainable ? "Yes" : "No", tone: "ok" as const },
      { label: "Portfolio loans", value: loanPortfolio?.total_loans ?? 0, tone: "ok" as const },
    ];
  }, [catalog.length, dashboard, jobs.length, loanPortfolio?.total_loans, recommendations]);

  const capabilityRows = useMemo(
    () =>
      catalog.map((item, index) => ({
        id: `${item.capability}-${index}`,
        capability: item.label || item.capability,
        key: item.capability,
        policy: item.policy_key ?? "—",
        explainable: item.explainable === false ? "No" : "Yes",
      })),
    [catalog],
  );

  const liquidityRows = useMemo(() => {
    if (!liquidity) return [];
    if (Array.isArray(liquidity.kpis)) {
      return liquidity.kpis.map((item, index) => ({
        id: `liquidity-${index}`,
        metric: compactText(item.metric ?? item.label ?? item.kpi ?? `KPI ${index + 1}`),
        value: compactText(item.value ?? item.amount ?? item.score ?? item.status),
      }));
    }
    return asMetricRows(liquidity, "liquidity");
  }, [liquidity]);

  const loanRows = useMemo(() => {
    if (!loanPortfolio) return [];
    return asMetricRows(loanPortfolio, "portfolio");
  }, [loanPortfolio]);

  const recommendationRows = useMemo(
    () =>
      (recommendations?.recommendations ?? []).map((item, index) => ({
        id: `recommendation-${index}`,
        recommendation: compactText(item.title ?? item.recommendation ?? item.message ?? `Recommendation ${index + 1}`),
        priority: compactText(item.priority ?? item.severity ?? "normal"),
        owner: compactText(item.owner ?? item.audience ?? "banking"),
      })),
    [recommendations],
  );

  const jobRows = useMemo(
    () =>
      jobs.map((job, index) => ({
        id: job.id ?? job.job_id ?? `job-${index}`,
        capability: job.capability,
        status: job.status,
        created: compactText(job.created_at ?? "—"),
        completed: compactText(job.completed_at ?? "—"),
      })),
    [jobs],
  );

  const assistantRows = useMemo(
    () =>
      (assistant?.insights ?? []).map((item, index) => ({
        id: `insight-${index}`,
        insight: compactText(item.insight ?? item.title ?? item.message ?? `Insight ${index + 1}`),
        severity: compactText(item.severity ?? "info"),
        action: compactText(item.action ?? item.recommendation ?? "Review"),
      })),
    [assistant],
  );

  const capabilityColumns = useMemo(
    () => [
      { key: "capability", header: "Capability", sortable: true },
      { key: "key", header: "Key", sortable: true },
      { key: "policy", header: "Policy key", sortable: true },
      { key: "explainable", header: "Explainable", sortable: true },
    ],
    [],
  );

  const metricColumns = useMemo(
    () => [
      { key: "metric", header: "Metric", sortable: true },
      { key: "value", header: "Value", sortable: true },
    ],
    [],
  );

  const recommendationColumns = useMemo(
    () => [
      { key: "recommendation", header: "Recommendation", sortable: true },
      { key: "priority", header: "Priority", sortable: true },
      { key: "owner", header: "Owner", sortable: true },
    ],
    [],
  );

  const jobColumns = useMemo(
    () => [
      { key: "capability", header: "Capability", sortable: true },
      { key: "status", header: "Status", sortable: true },
      { key: "created", header: "Created", sortable: true },
      { key: "completed", header: "Completed", sortable: true },
    ],
    [],
  );

  const assistantColumns = useMemo(
    () => [
      { key: "insight", header: "Insight", sortable: true },
      { key: "severity", header: "Severity", sortable: true },
      { key: "action", header: "Suggested action", sortable: true },
    ],
    [],
  );

  async function onConnect() {
    try {
      const next = await loginBankingAnalyticsSession(tenantId, email, password);
      setSession(next);
      saveBankingAnalyticsSession(next);
      push({ message: `Connected to tenant ${tenantId}` });
      await loadData(next);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Connection failed" });
    }
  }

  async function runAction(label: string, fn: (active: ApiSession) => Promise<unknown>) {
    if (!session) return;
    try {
      await fn(session);
      setLastAction(label);
      await loadData(session);
      push({ message: `${label} completed` });
    } catch (err) {
      push({ message: err instanceof Error ? err.message : `${label} failed` });
    }
  }

  return (
    <PageLayout
      title="Banking Analytics"
      breadcrumb={[
        { label: "Marpich", href: "/" },
        { label: "Banking", href: "/banking/analytics" },
        { label: "Analytics" },
      ]}
      actions={
        session ? (
          <>
            <button
              type="button"
              className="mp-btn"
              onClick={() => void runAction("Run forecasting", (active) => runBankingAnalysis(active, "forecasting"))}
            >
              Run forecasting
            </button>
            <button
              type="button"
              className="mp-btn"
              onClick={() => void runAction("Run delinquency analysis", (active) => runBankingAnalysis(active, "delinquency_analysis"))}
            >
              Analyze delinquency
            </button>
            <button
              type="button"
              className="mp-btn mp-btn-primary"
              onClick={() =>
                void runAction("AI assistant", async (active) => {
                  const result = await runBankingAiAssistant(active, aiQuery);
                  setAssistant(result);
                  return result;
                })
              }
            >
              Ask AI
            </button>
            <button
              type="button"
              className="mp-btn"
              onClick={() => session && void loadData(session)}
              disabled={loading}
            >
              Refresh
            </button>
          </>
        ) : null
      }
    >
      <p className="banking-subtitle">
        Executive and operational banking insights over the existing policy-aware Banking Analytics APIs.
      </p>

      <ProgressBar
        value={progress}
        label={loading ? "Loading Banking Analytics…" : "Banking Analytics dashboard ready"}
      />

      {!session ? (
        <section className="banking-connect" aria-labelledby="connect-heading">
          <h2 id="connect-heading">Connect to API</h2>
          <p className="banking-muted">Sign in to view the Banking Analytics dashboard and run assisted analysis.</p>
          <div className="banking-form">
            <label>
              Tenant ID
              <input className="mp-input" value={tenantId} onChange={(e) => setTenantId(e.target.value)} />
            </label>
            <label>
              Email
              <input className="mp-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            </label>
            <label>
              Password
              <input
                className="mp-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </label>
            <button type="button" className="mp-btn mp-btn-primary" onClick={() => void onConnect()}>
              Connect
            </button>
          </div>
        </section>
      ) : null}

      {error ? (
        <p className="banking-error" role="alert">
          {error}
        </p>
      ) : null}

      {session && loading ? <SkeletonTable rows={4} cols={4} /> : null}

      {session && dashboard && !loading ? (
        <>
          <p className="banking-muted">
            Tenant <strong>{session.tenantId}</strong>
            {lastAction ? ` · Last action: ${lastAction}` : ""}
            {executive?.headline ? ` · Headline: ${executive.headline}` : ""}
          </p>

          <div className="banking-stats">
            {statCards.map((stat) => (
              <article
                key={stat.label}
                className={`banking-stat${stat.tone === "warn" ? " banking-stat-warn" : ""}`}
              >
                <span className="banking-stat-value">{stat.value}</span>
                <span className="banking-stat-label">{stat.label}</span>
              </article>
            ))}
          </div>

          <div className="banking-panels">
            <section aria-labelledby="executive-heading">
              <h2 id="executive-heading">Executive snapshot</h2>
              <div className="banking-panel">
                <p className="banking-headline">{executive?.headline ?? dashboard.executive_headline}</p>
                <p className="banking-muted">
                  Audience: <strong>{executive?.audience ?? "executive"}</strong> · Explainable:{" "}
                  <strong>{executive?.explainable ? "Yes" : "No"}</strong>
                </p>
              </div>
            </section>

            <section aria-labelledby="assistant-heading">
              <h2 id="assistant-heading">AI assistant</h2>
              <div className="banking-panel">
                <label className="banking-query">
                  Question
                  <textarea
                    className="mp-input banking-textarea"
                    value={aiQuery}
                    onChange={(e) => setAiQuery(e.target.value)}
                    rows={3}
                  />
                </label>
                <p className="banking-muted">
                  Uses the existing `banking.analytics.write` flow and returns explainable insights only.
                </p>
              </div>
            </section>
          </div>

          <div className="banking-grid">
            <section aria-labelledby="capabilities-heading">
              <h2 id="capabilities-heading">Capabilities ({catalog.length})</h2>
              <DataTable columns={capabilityColumns} rows={capabilityRows} />
            </section>

            <section aria-labelledby="recommendations-heading">
              <h2 id="recommendations-heading">
                Recommendations ({recommendationRows.length || recommendations?.recommendation_count || 0})
              </h2>
              {recommendationRows.length === 0 ? (
                <EmptyState
                  title="No recommendations"
                  description="Run the AI assistant or load a tenant with active banking signals."
                />
              ) : (
                <DataTable columns={recommendationColumns} rows={recommendationRows} />
              )}
            </section>
          </div>

          <div className="banking-grid">
            <section aria-labelledby="liquidity-heading">
              <h2 id="liquidity-heading">Liquidity KPIs</h2>
              {liquidityRows.length === 0 ? (
                <EmptyState title="No liquidity KPIs" description="The current tenant has no KPI rows yet." />
              ) : (
                <DataTable columns={metricColumns} rows={liquidityRows} />
              )}
            </section>

            <section aria-labelledby="portfolio-heading">
              <h2 id="portfolio-heading">Loan portfolio</h2>
              {loanRows.length === 0 ? (
                <EmptyState title="No portfolio metrics" description="No portfolio summary was returned by the API." />
              ) : (
                <DataTable columns={metricColumns} rows={loanRows} />
              )}
            </section>
          </div>

          <section aria-labelledby="jobs-heading">
            <h2 id="jobs-heading">Analysis jobs ({jobs.length})</h2>
            {jobRows.length === 0 ? (
              <EmptyState
                title="No analysis jobs yet"
                description="Run forecasting or delinquency analysis to populate the execution history."
              />
            ) : (
              <DataTable columns={jobColumns} rows={jobRows} />
            )}
          </section>

          <section className="banking-insights" aria-labelledby="insights-heading">
            <h2 id="insights-heading">AI insights</h2>
            {assistantRows.length === 0 ? (
              <EmptyState
                title="No AI insights yet"
                description="Ask the Banking AI assistant a question to generate explainable insights."
              />
            ) : (
              <DataTable columns={assistantColumns} rows={assistantRows} />
            )}
          </section>
        </>
      ) : null}

      <style jsx>{`
        .banking-subtitle {
          color: var(--mp-text-muted, #64748b);
          margin: 0 0 1rem;
        }
        .banking-connect {
          margin: 1rem 0 1.5rem;
          padding: 1rem;
          border: 1px solid var(--mp-border, #e2e8f0);
          border-radius: 8px;
        }
        .banking-form {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
          gap: 0.75rem;
          align-items: end;
          margin-top: 0.75rem;
        }
        label {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
          font-size: 0.85rem;
        }
        .banking-error {
          color: #b91c1c;
          margin: 0.75rem 0;
        }
        .banking-muted {
          color: var(--mp-text-muted, #64748b);
          margin: 0.5rem 0;
        }
        .banking-stats {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
          gap: 0.75rem;
          margin: 1rem 0;
        }
        .banking-stat {
          padding: 1rem;
          border-radius: 8px;
          background: var(--mp-surface-2, #f8fafc);
          border: 1px solid var(--mp-border, #e2e8f0);
        }
        .banking-stat-warn {
          border-color: #f59e0b;
          background: #fffbeb;
        }
        .banking-stat-value {
          display: block;
          font-size: 1.4rem;
          font-weight: 700;
        }
        .banking-stat-label {
          font-size: 0.78rem;
          color: var(--mp-text-muted, #64748b);
        }
        .banking-panels,
        .banking-grid {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 1rem;
          margin-bottom: 1.25rem;
        }
        .banking-panel {
          border: 1px solid var(--mp-border, #e2e8f0);
          border-radius: 8px;
          padding: 1rem;
          background: var(--mp-surface-1, #fff);
        }
        .banking-headline {
          margin: 0 0 0.5rem;
          font-size: 1rem;
          font-weight: 600;
        }
        .banking-query {
          width: 100%;
        }
        .banking-textarea {
          min-height: 90px;
          resize: vertical;
        }
        .banking-insights h2,
        h2 {
          margin: 0 0 0.75rem;
          font-size: 1.1rem;
        }
        @media (max-width: 960px) {
          .banking-panels,
          .banking-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </PageLayout>
  );
}
