"use client";

import Link from "next/link";
import { useAuth } from "@marpich/auth-provider";
import { PageLayout } from "@marpich/core";
import {
  AdvancedFilterBar,
  DataTable,
  EmptyState,
  ExportButton,
  PrintButton,
  ProgressBar,
  SkeletonTable,
  StepProgress,
  useAutosave,
  useLocale,
  useToast,
} from "@marpich/shared";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  BANKING_ANALYTICS_SURFACES,
  clearBankingAnalyticsSession,
  compactText,
  fetchBankingAnalyticsCatalog,
  fetchBankingAnalyticsDashboard,
  fetchBankingAnalyticsJobs,
  fetchBankingAnalyticsPolicyKeys,
  fetchBankingAnalyticsSurface,
  fetchBankingExecutiveDashboard,
  fetchBankingRecommendations,
  flattenAnalyticsRows,
  isAuthFailure,
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
  type BankingAnalyticsPayload,
  type BankingAnalyticsPolicyKey,
  type BankingExecutiveDashboard,
  type BankingRecommendations,
} from "@/lib/bankingAnalyticsClient";

type TabId =
  | "overview"
  | "catalog"
  | "recommendations"
  | "jobs"
  | "ai"
  | "policies"
  | (typeof BANKING_ANALYTICS_SURFACES)[number]["id"];

const METRIC_JEWELS = ["forest", "royal", "emerald", "gold", "orange", "purple"] as const;
const DRAFT_KEY = "marpich.banking.analytics.draft";

function StatusChip({ status }: { status: string }) {
  const tone =
    status === "completed" || status === "active" || status === "ok"
      ? "ok"
      : status === "failed" || status === "warning" || status === "attention"
        ? "warn"
        : "muted";
  return <span className={`ba-chip ba-chip--${tone}`}>{status}</span>;
}

function formatMetricDisplay(value: unknown): string {
  if (typeof value === "number") {
    if (Math.abs(value) > 0 && Math.abs(value) < 1) return `${(value * 100).toFixed(1)}%`;
    return compactText(value);
  }
  return compactText(value);
}

function headlineText(value: unknown): string {
  if (!value) return "—";
  if (typeof value === "string") return value;
  if (typeof value === "object") {
    const h = value as Record<string, unknown>;
    if (typeof h.liquidity_ratio === "number") {
      return `Liquidity ${(h.liquidity_ratio * 100).toFixed(1)}% · Loans ${compactText(h.active_loans ?? h.total_loans_outstanding)} · Deposits ${compactText(h.total_deposits)}`;
    }
    return compactText(value);
  }
  return String(value);
}

export function BankingAnalyticsDashboardPage() {
  const { t } = useLocale();
  const { push } = useToast();
  const {
    session: authSession,
    isAuthenticated,
    isLoading: authLoading,
    login,
    logout,
  } = useAuth();

  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [needsReconnect, setNeedsReconnect] = useState(false);
  const [tab, setTab] = useState<TabId>("overview");
  const [filterQ, setFilterQ] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [selectedJobId, setSelectedJobId] = useState("");
  const [draftReady, setDraftReady] = useState(false);

  const [localSession, setLocalSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("bank-demo");
  const [email, setEmail] = useState("analytics@bank.dev");
  const [password, setPassword] = useState("SecurePass123!");
  const [aiQuery, setAiQuery] = useState("Which portfolio segment needs attention first?");

  const [catalog, setCatalog] = useState<BankingAnalyticsCapability[]>([]);
  const [policyKeys, setPolicyKeys] = useState<BankingAnalyticsPolicyKey[]>([]);
  const [dashboard, setDashboard] = useState<BankingAnalyticsDashboard | null>(null);
  const [executive, setExecutive] = useState<BankingExecutiveDashboard | null>(null);
  const [recommendations, setRecommendations] = useState<BankingRecommendations | null>(null);
  const [jobs, setJobs] = useState<BankingAnalyticsJob[]>([]);
  const [assistant, setAssistant] = useState<BankingAiAssistantResponse | null>(null);
  const [surfaceCache, setSurfaceCache] = useState<Record<string, BankingAnalyticsPayload>>({});
  const [lastAction, setLastAction] = useState<string | null>(null);

  const session = needsReconnect ? null : localSession ?? (isAuthenticated ? authSession : null);

  const draft = useMemo(() => ({ aiQuery, filterQ, statusFilter }), [aiQuery, filterQ, statusFilter]);

  const persistDraft = useCallback(
    async (values: typeof draft) => {
      if (!draftReady) return;
      try {
        localStorage.setItem(DRAFT_KEY, JSON.stringify(values));
      } catch {
        /* ignore quota */
      }
    },
    [draftReady],
  );

  const { saving: draftSaving } = useAutosave(draft, persistDraft, 900);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(DRAFT_KEY);
      if (raw) {
        const parsed = JSON.parse(raw) as Partial<typeof draft>;
        if (typeof parsed.aiQuery === "string" && parsed.aiQuery.trim()) {
          setAiQuery(parsed.aiQuery);
        }
        if (typeof parsed.filterQ === "string") setFilterQ(parsed.filterQ);
        if (typeof parsed.statusFilter === "string") setStatusFilter(parsed.statusFilter);
      }
    } catch {
      /* ignore */
    } finally {
      setDraftReady(true);
    }
  }, []);

  const resetAuthState = useCallback(async () => {
    setNeedsReconnect(true);
    clearBankingAnalyticsSession();
    setLocalSession(null);
    setCatalog([]);
    setPolicyKeys([]);
    setDashboard(null);
    setExecutive(null);
    setRecommendations(null);
    setJobs([]);
    setAssistant(null);
    setSurfaceCache({});
    setSelectedJobId("");
    try {
      await logout();
    } catch {
      /* session may already be invalid */
    }
  }, [logout]);

  const loadCore = useCallback(
    async (active: ApiSession) => {
      setLoading(true);
      setProgress(35);
      setError(null);
      try {
        const [cat, policies, dash, exec, recs, jobList] = await Promise.all([
          fetchBankingAnalyticsCatalog(active),
          fetchBankingAnalyticsPolicyKeys(active),
          fetchBankingAnalyticsDashboard(active),
          fetchBankingExecutiveDashboard(active),
          fetchBankingRecommendations(active),
          fetchBankingAnalyticsJobs(active),
        ]);
        setCatalog(Array.isArray(cat) ? cat : []);
        setPolicyKeys(Array.isArray(policies) ? policies : []);
        setDashboard(dash);
        setExecutive(exec);
        setRecommendations(recs);
        setJobs(Array.isArray(jobList) ? jobList : []);
        setNeedsReconnect(false);
        setProgress(70);

        const surfaces = await Promise.all(
          BANKING_ANALYTICS_SURFACES.map(async (s) => {
            try {
              const data = await fetchBankingAnalyticsSurface(active, s.path);
              return [s.id, data] as const;
            } catch (surfaceErr) {
              const msg = surfaceErr instanceof Error ? surfaceErr.message : "";
              if (isAuthFailure(msg)) throw surfaceErr;
              return [s.id, {}] as const;
            }
          }),
        );
        setSurfaceCache(Object.fromEntries(surfaces));
        setProgress(100);
      } catch (err) {
        const message = err instanceof Error ? err.message : t("banking.loadFailed");
        setError(message);
        setProgress(100);
        if (isAuthFailure(message)) {
          await resetAuthState();
          setError(t("banking.sessionExpired"));
        }
      } finally {
        setLoading(false);
      }
    },
    [resetAuthState, t],
  );

  useEffect(() => {
    if (authLoading) return;
    if (needsReconnect) {
      setLoading(false);
      setProgress(100);
      return;
    }
    const stored = loadBankingAnalyticsSession();
    if (stored) {
      setLocalSession(stored);
      void loadCore(stored);
      return;
    }
    if (authSession && isAuthenticated) {
      void loadCore(authSession);
      return;
    }
    setLoading(false);
    setProgress(100);
  }, [authLoading, authSession, isAuthenticated, loadCore, needsReconnect]);

  const stats = useMemo(() => {
    const summary = dashboard?.summary ?? {};
    return [
      { label: t("banking.stat.capabilities"), value: catalog.length },
      { label: t("banking.stat.customers"), value: compactText(summary.customer_count ?? "—") },
      { label: t("banking.stat.loans"), value: compactText(summary.loan_count ?? "—") },
      { label: t("banking.stat.deposits"), value: compactText(summary.deposit_count ?? "—") },
      {
        label: t("banking.stat.recommendations"),
        value: recommendations?.recommendation_count ?? recommendations?.recommendations?.length ?? 0,
      },
      { label: t("banking.stat.jobs"), value: jobs.length },
    ];
  }, [catalog.length, dashboard, jobs.length, recommendations, t]);

  const tabs: { id: TabId; label: string }[] = useMemo(
    () => [
      { id: "overview", label: t("banking.tab.overview") },
      ...BANKING_ANALYTICS_SURFACES.map((s) => ({ id: s.id as TabId, label: t(s.labelKey) })),
      { id: "recommendations", label: t("banking.tab.recommendations") },
      { id: "ai", label: t("banking.tab.ai") },
      { id: "jobs", label: t("banking.tab.jobs") },
      { id: "catalog", label: t("banking.tab.catalog") },
      { id: "policies", label: t("banking.tab.policies") },
    ],
    [t],
  );

  const q = filterQ.toLowerCase().trim();

  const capabilityRows = useMemo(
    () =>
      catalog
        .filter((item) => {
          if (!q) return true;
          return [item.capability, item.label, item.policy_key]
            .filter(Boolean)
            .join(" ")
            .toLowerCase()
            .includes(q);
        })
        .map((item, index) => ({
          id: `${item.capability}-${index}`,
          capability: item.label || item.capability,
          key: item.capability,
          supported: item.supported === false ? t("banking.no") : t("banking.yes"),
          explainable: item.explainable === false ? t("banking.no") : t("banking.yes"),
        })),
    [catalog, q, t],
  );

  const recommendationRows = useMemo(
    () =>
      (recommendations?.recommendations ?? [])
        .filter((item) => {
          if (!q) return true;
          return compactText(item).toLowerCase().includes(q);
        })
        .map((item, index) => ({
          id: `rec-${index}`,
          recommendation: compactText(item.action ?? item.title ?? item.recommendation ?? item.detail),
          priority: compactText(item.priority ?? "normal"),
          category: compactText(item.category ?? "—"),
          confidence: compactText(item.confidence ?? "—"),
          explanation: compactText(item.explanation ?? item.detail ?? "—"),
        })),
    [recommendations, q],
  );

  const jobRows = useMemo(
    () =>
      jobs
        .filter((job) => {
          if (statusFilter && job.status !== statusFilter) return false;
          if (!q) return true;
          return `${job.capability} ${job.status}`.toLowerCase().includes(q);
        })
        .map((job, index) => ({
          id: job.id ?? job.job_id ?? `job-${index}`,
          capability: job.capability,
          status: job.status,
          confidence: compactText(job.confidence ?? "—"),
          created: compactText(job.created_at?.slice(0, 19) ?? "—"),
          completed: compactText(job.completed_at?.slice(0, 19) ?? "—"),
        })),
    [jobs, q, statusFilter],
  );

  const selectedJob = useMemo(
    () =>
      jobs.find((job, index) => (job.id ?? job.job_id ?? `job-${index}`) === selectedJobId) ?? null,
    [jobs, selectedJobId],
  );

  const recommendationCount =
    recommendations?.recommendation_count ?? recommendations?.recommendations?.length ?? 0;

  const lifecycleStep = useMemo(() => {
    if (!catalog.length) return 0;
    if (!jobs.length) return 1;
    if (!recommendationCount) return 2;
    return 3;
  }, [catalog.length, jobs.length, recommendationCount]);

  const workflowSteps = useMemo(
    () => [
      t("banking.step.catalog"),
      t("banking.step.analyze"),
      t("banking.step.recommend"),
      t("banking.step.ai"),
    ],
    [t],
  );

  useEffect(() => {
    if (!jobs.length) {
      if (selectedJobId) setSelectedJobId("");
      return;
    }
    const stillThere = jobs.some(
      (job, index) => (job.id ?? job.job_id ?? `job-${index}`) === selectedJobId,
    );
    if (!stillThere) {
      const first = jobs[0]!;
      setSelectedJobId(first.id ?? first.job_id ?? "job-0");
    }
  }, [jobs, selectedJobId]);

  const policyRows = useMemo(
    () =>
      policyKeys
        .filter((p) => !q || `${p.key} ${p.description ?? ""}`.toLowerCase().includes(q))
        .map((p, index) => ({
          id: `policy-${index}`,
          key: p.key,
          description: compactText(p.description ?? "—"),
        })),
    [policyKeys, q],
  );

  const assistantRows = useMemo(
    () =>
      (assistant?.insights ?? []).map((item, index) => {
        if (typeof item === "string") {
          return {
            id: `insight-${index}`,
            insight: item,
            severity: "info",
            action: t("banking.review"),
          };
        }
        return {
          id: `insight-${index}`,
          insight: compactText(item.insight ?? item.title ?? item.message),
          severity: compactText(item.severity ?? "info"),
          action: compactText(item.action ?? item.recommendation ?? t("banking.review")),
        };
      }),
    [assistant, t],
  );

  const activeSurface = BANKING_ANALYTICS_SURFACES.find((s) => s.id === tab);
  const surfaceRows = useMemo(() => {
    if (!activeSurface) return [];
    const rows = flattenAnalyticsRows(surfaceCache[activeSurface.id], activeSurface.id);
    if (!q) return rows;
    return rows.filter(
      (r) => r.metric.toLowerCase().includes(q) || r.value.toLowerCase().includes(q),
    );
  }, [activeSurface, surfaceCache, q]);

  const exportRows = useMemo(() => {
    if (tab === "jobs") return jobRows;
    if (tab === "recommendations") return recommendationRows;
    if (tab === "catalog") return capabilityRows;
    if (tab === "policies") return policyRows;
    if (activeSurface) return surfaceRows;
    return stats.map((s) => ({ metric: s.label, value: String(s.value) }));
  }, [
    tab,
    jobRows,
    recommendationRows,
    capabilityRows,
    policyRows,
    activeSurface,
    surfaceRows,
    stats,
  ]);

  const executiveHeadline =
    executive?.headline && typeof executive.headline === "object"
      ? (executive.headline as Record<string, unknown>)
      : dashboard?.executive_headline && typeof dashboard.executive_headline === "object"
        ? (dashboard.executive_headline as Record<string, unknown>)
        : null;

  const executiveKpiRows = useMemo(() => {
    if (!executiveHeadline) return [];
    return Object.entries(executiveHeadline).map(([key, value]) => ({
      id: `exec-${key}`,
      metric: key.replaceAll("_", " "),
      value: formatMetricDisplay(value),
    }));
  }, [executiveHeadline]);

  async function onConnect() {
    setBusy(true);
    setError(null);
    try {
      const next = await loginBankingAnalyticsSession(tenantId, email, password);
      setLocalSession(next);
      saveBankingAnalyticsSession(next);
      setNeedsReconnect(false);
      try {
        await login({
          tenantId,
          email,
          password,
          displayName: "Banking Analytics Admin",
          registerIfMissing: true,
        });
      } catch {
        /* local banking session is enough for this page */
      }
      push({ message: t("banking.connected") });
      await loadCore(next);
    } catch (err) {
      const message = err instanceof Error ? err.message : t("banking.connectFailed");
      setError(message);
      push({ message });
    } finally {
      setBusy(false);
    }
  }

  async function runAction(label: string, fn: (active: ApiSession) => Promise<unknown>) {
    if (!session) return;
    setBusy(true);
    try {
      await fn(session);
      setLastAction(label);
      await loadCore(session);
      push({ message: `${label} — ${t("banking.done")}` });
    } catch (err) {
      const message = err instanceof Error ? err.message : `${label} ${t("banking.failed")}`;
      if (isAuthFailure(message)) {
        await resetAuthState();
        setError(t("banking.sessionExpired"));
      }
      push({ message });
    } finally {
      setBusy(false);
    }
  }

  return (
    <PageLayout
      title={t("banking.title")}
      subtitle={t("banking.subtitle")}
      breadcrumb={[
        { label: t("app.name"), href: "/" },
        { label: t("banking.breadcrumb"), href: "/banking/analytics" },
        { label: t("banking.analytics") },
      ]}
      actions={
        <>
          <ExportButton label={t("common.export")} rows={exportRows} filename="banking-analytics.csv" />
          <PrintButton label={t("common.print")} />
          {session ? (
            <>
              <button
                type="button"
                className="mp-btn"
                disabled={busy || loading}
                onClick={() =>
                  void runAction(t("banking.cap.forecast"), (active) =>
                    runBankingAnalysis(active, "forecasting"),
                  )
                }
              >
                {t("banking.runForecast")}
              </button>
              <button
                type="button"
                className="mp-btn mp-btn-primary"
                disabled={busy || loading}
                onClick={() =>
                  void runAction(t("banking.tab.ai"), async (active) => {
                    const result = await runBankingAiAssistant(active, aiQuery);
                    setAssistant(result);
                    setTab("ai");
                    return result;
                  })
                }
              >
                {t("banking.askAi")}
              </button>
              <button
                type="button"
                className="mp-btn"
                disabled={loading || busy}
                onClick={() => void loadCore(session)}
              >
                {t("common.refresh")}
              </button>
            </>
          ) : (
            <Link href="/login?returnTo=/banking/analytics" className="mp-btn mp-btn-primary">
              {t("dashboard.signIn")}
            </Link>
          )}
        </>
      }
    >
      <ProgressBar
        value={progress}
        label={loading || authLoading ? t("banking.loading") : t("banking.ready")}
      />

      {error ? (
        <p className="ba-alert" role="alert">
          {error}
        </p>
      ) : null}

      {!session && !authLoading ? (
        <section className="ba-session" aria-label={t("dashboard.session")}>
          <div className="ba-session-banner">
            <h2>{t("banking.connectHint")}</h2>
            <p>{t("banking.connectHelp")}</p>
          </div>
          <div className="ba-session-body">
            <div className="mp-form ba-form-grid">
              <div className="mp-field">
                <label htmlFor="ba-tenant">{t("dashboard.tenant")}</label>
                <input
                  id="ba-tenant"
                  className="mp-input"
                  value={tenantId}
                  onChange={(e) => setTenantId(e.target.value)}
                />
              </div>
              <div className="mp-field">
                <label htmlFor="ba-email">{t("dashboard.email")}</label>
                <input
                  id="ba-email"
                  className="mp-input"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div className="mp-field">
                <label htmlFor="ba-password">{t("dashboard.password")}</label>
                <input
                  id="ba-password"
                  className="mp-input"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>
            <div className="ba-actions">
              <button
                type="button"
                className="mp-btn mp-btn-primary"
                disabled={busy}
                onClick={() => void onConnect()}
              >
                {t("banking.connect")}
              </button>
              <Link href="/login?returnTo=/banking/analytics" className="mp-btn">
                {t("dashboard.openLogin")}
              </Link>
            </div>
          </div>
        </section>
      ) : null}

      {session && (loading || authLoading) ? <SkeletonTable rows={6} cols={4} /> : null}

      {session && !loading ? (
        <div className="ba-layout">
          <aside className="ba-aside" aria-label={t("banking.rail")}>
            <section className="ba-panel-card">
              <header className="ba-panel-head ba-jewel-bar--emerald">
                <h2>{t("banking.workflow")}</h2>
              </header>
              <div className="ba-panel-body">
                <StepProgress steps={workflowSteps} current={lifecycleStep} />
                {draftSaving ? (
                  <p className="mp-field-help" aria-live="polite">
                    {t("banking.draftSaved")}…
                  </p>
                ) : (
                  <p className="mp-field-help">{t("banking.workflowHint")}</p>
                )}
                {selectedJob ? (
                  <p className="mp-field-help">
                    <StatusChip status={selectedJob.status} /> · {selectedJob.capability}
                  </p>
                ) : (
                  <p className="mp-field-help">{t("banking.selectJobHint")}</p>
                )}
              </div>
            </section>

            <section className="ba-panel-card">
              <header className="ba-panel-head ba-jewel-bar--forest">
                <h2>{t("banking.rail.status")}</h2>
              </header>
              <div className="ba-panel-body">
                <div className="ba-status-row">
                  <span>{t("dashboard.tenant")}</span>
                  <strong>{session.tenantId}</strong>
                </div>
                <div className="ba-status-row">
                  <span>{t("banking.explainable")}</span>
                  <strong>
                    {dashboard?.explainable ? t("banking.yes") : t("banking.no")}
                  </strong>
                </div>
                {lastAction ? (
                  <p className="mp-field-help">
                    {t("banking.lastAction")}: {lastAction}
                  </p>
                ) : null}
                <p className="ba-headline">{headlineText(executive?.headline ?? dashboard?.executive_headline)}</p>
              </div>
            </section>

            <section className="ba-panel-card">
              <header className="ba-panel-head ba-jewel-bar--royal">
                <h2>{t("banking.rail.run")}</h2>
              </header>
              <div className="ba-panel-body ba-panel-body--tight">
                <ul className="ba-run-list">
                  {BANKING_ANALYTICS_SURFACES.map((s) => (
                    <li key={s.id}>
                      <button
                        type="button"
                        className="ba-run-link"
                        disabled={busy}
                        onClick={() =>
                          void runAction(t(s.labelKey), async (active) => {
                            await runBankingAnalysis(active, s.id);
                            setTab(s.id);
                          })
                        }
                      >
                        <span className={`ba-dot ba-jewel--${s.jewel}`} aria-hidden />
                        <span>{t(s.labelKey)}</span>
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            </section>

            <section className="ba-panel-card">
              <header className="ba-panel-head ba-jewel-bar--gold">
                <h2>{t("banking.tab.ai")}</h2>
              </header>
              <div className="ba-panel-body">
                <label className="mp-field" htmlFor="ba-ai-query">
                  <span>{t("banking.aiQuestion")}</span>
                  <textarea
                    id="ba-ai-query"
                    className="mp-input ba-textarea"
                    rows={4}
                    value={aiQuery}
                    onChange={(e) => setAiQuery(e.target.value)}
                  />
                </label>
                <button
                  type="button"
                  className="mp-btn mp-btn-primary"
                  disabled={busy || !aiQuery.trim()}
                  onClick={() =>
                    void runAction(t("banking.tab.ai"), async (active) => {
                      const result = await runBankingAiAssistant(active, aiQuery);
                      setAssistant(result);
                      setTab("ai");
                      return result;
                    })
                  }
                >
                  {t("banking.askAi")}
                </button>
                <p className="mp-field-help">{t("banking.aiHint")}</p>
              </div>
            </section>
          </aside>

          <div className="ba-main">
            <section className="ba-metrics" aria-label={t("banking.metrics")}>
              {stats.map((s, i) => {
                const jewel = METRIC_JEWELS[i % METRIC_JEWELS.length]!;
                return (
                  <div key={s.label} className={`ba-metric ba-metric--${jewel}`}>
                    <span className="ba-metric-label">{s.label}</span>
                    <strong>{s.value}</strong>
                  </div>
                );
              })}
            </section>

            <div className="ba-filters">
              <AdvancedFilterBar
                filters={[{ id: "q", label: t("common.filter"), type: "text" }]}
                onChange={(values) => setFilterQ(values.q ?? "")}
              />
              <label className="mp-filter-item ba-status-filter">
                <span>{t("banking.col.status")}</span>
                <select
                  className="mp-input"
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  aria-label={t("banking.col.status")}
                >
                  <option value="">{t("banking.filterAll")}</option>
                  <option value="completed">completed</option>
                  <option value="running">running</option>
                  <option value="queued">queued</option>
                  <option value="failed">failed</option>
                </select>
              </label>
            </div>

            <div className="ba-tabs" role="tablist" aria-label={t("banking.title")}>
              {tabs.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  role="tab"
                  aria-selected={tab === item.id}
                  className={`ba-tab ${tab === item.id ? "ba-tab--on" : ""}`}
                  onClick={() => setTab(item.id)}
                >
                  {item.label}
                </button>
              ))}
            </div>

            <div className="ba-panel mp-animate-in" role="tabpanel">
              {tab === "overview" ? (
                <div className="ba-overview">
                  <section className="ba-card">
                    <h2>{t("banking.cap.executive")}</h2>
                    <p className="ba-headline">
                      {headlineText(executive?.headline ?? dashboard?.executive_headline)}
                    </p>
                    <p className="mp-field-help">
                      {t("banking.audience")}: {executive?.audience ?? "executive"} ·{" "}
                      {t("banking.explainable")}:{" "}
                      {executive?.explainable || dashboard?.explainable
                        ? t("banking.yes")
                        : t("banking.no")}
                    </p>
                    {executiveKpiRows.length === 0 ? (
                      <EmptyState
                        title={t("banking.noExecutive")}
                        description={t("banking.noExecutiveHint")}
                      />
                    ) : (
                      <DataTable
                        columns={[
                          { key: "metric", header: t("banking.col.metric"), sortable: true },
                          { key: "value", header: t("banking.col.value"), sortable: true },
                        ]}
                        rows={executiveKpiRows}
                      />
                    )}
                  </section>
                  <section className="ba-card">
                    <h2>{t("banking.tab.recommendations")}</h2>
                    {recommendationRows.length === 0 ? (
                      <EmptyState
                        title={t("banking.noRecommendations")}
                        description={t("banking.noRecommendationsHint")}
                      />
                    ) : (
                      <DataTable
                        columns={[
                          { key: "recommendation", header: t("banking.col.recommendation"), sortable: true },
                          { key: "priority", header: t("banking.col.priority"), sortable: true },
                          { key: "category", header: t("banking.col.category"), sortable: true },
                        ]}
                        rows={recommendationRows.slice(0, 8)}
                      />
                    )}
                  </section>
                  <section className="ba-card">
                    <h2>{t("banking.surfaceGrid")}</h2>
                    <ul className="ba-surface-grid">
                      {BANKING_ANALYTICS_SURFACES.map((s) => (
                        <li key={s.id}>
                          <button
                            type="button"
                            className="ba-surface-tile"
                            onClick={() => setTab(s.id)}
                          >
                            <span className={`ba-icon ba-jewel--${s.jewel}`} aria-hidden>
                              {t(s.labelKey).slice(0, 2).toUpperCase()}
                            </span>
                            <span>
                              <strong>{t(s.labelKey)}</strong>
                              <span className="mp-field-help">
                                {flattenAnalyticsRows(surfaceCache[s.id]).length} {t("banking.metrics")}
                              </span>
                            </span>
                          </button>
                        </li>
                      ))}
                    </ul>
                  </section>
                </div>
              ) : null}

              {activeSurface ? (
                <section>
                  <div className="ba-surface-head">
                    <h2>{t(activeSurface.labelKey)}</h2>
                    <button
                      type="button"
                      className="mp-btn mp-btn-primary"
                      disabled={busy}
                      onClick={() =>
                        void runAction(t(activeSurface.labelKey), (active) =>
                          runBankingAnalysis(active, activeSurface.id),
                        )
                      }
                    >
                      {t("banking.runAnalysis")}
                    </button>
                  </div>
                  {surfaceRows.length === 0 ? (
                    <EmptyState
                      title={t("demo.empty")}
                      description={t("banking.emptySurfaceHint")}
                    />
                  ) : (
                    <DataTable
                      columns={[
                        { key: "metric", header: t("banking.col.metric"), sortable: true },
                        { key: "value", header: t("banking.col.value"), sortable: true },
                      ]}
                      rows={surfaceRows}
                    />
                  )}
                </section>
              ) : null}

              {tab === "recommendations" ? (
                recommendationRows.length === 0 ? (
                  <EmptyState
                    title={t("banking.noRecommendations")}
                    description={t("banking.noRecommendationsHint")}
                  />
                ) : (
                  <DataTable
                    columns={[
                      { key: "recommendation", header: t("banking.col.recommendation"), sortable: true },
                      { key: "priority", header: t("banking.col.priority"), sortable: true },
                      { key: "category", header: t("banking.col.category"), sortable: true },
                      { key: "confidence", header: t("banking.col.confidence"), sortable: true },
                      { key: "explanation", header: t("banking.col.explanation"), sortable: true },
                    ]}
                    rows={recommendationRows}
                  />
                )
              ) : null}

              {tab === "ai" ? (
                <section className="ba-ai">
                  <p className="mp-field-help">{assistant?.explanation ?? t("banking.aiHint")}</p>
                  {assistantRows.length === 0 ? (
                    <EmptyState title={t("banking.noInsights")} description={t("banking.aiHint")} />
                  ) : (
                    <DataTable
                      columns={[
                        { key: "insight", header: t("banking.col.insight"), sortable: true },
                        { key: "severity", header: t("banking.col.severity"), sortable: true },
                        { key: "action", header: t("banking.col.action"), sortable: true },
                      ]}
                      rows={assistantRows}
                    />
                  )}
                  {(assistant?.top_recommendations?.length ?? 0) > 0 ? (
                    <>
                      <h3>{t("banking.tab.recommendations")}</h3>
                      <DataTable
                        columns={[
                          {
                            key: "recommendation",
                            header: t("banking.col.recommendation"),
                            sortable: true,
                          },
                          { key: "priority", header: t("banking.col.priority"), sortable: true },
                        ]}
                        rows={(assistant?.top_recommendations ?? []).map((item, index) => ({
                          id: `ai-rec-${index}`,
                          recommendation: compactText(item.action ?? item.detail),
                          priority: compactText(item.priority ?? "normal"),
                        }))}
                      />
                    </>
                  ) : null}
                </section>
              ) : null}

              {tab === "jobs" ? (
                jobRows.length === 0 ? (
                  <EmptyState title={t("banking.noJobs")} description={t("banking.noJobsHint")} />
                ) : (
                  <>
                    <DataTable
                      columns={[
                        { key: "capability", header: t("banking.col.capability"), sortable: true },
                        {
                          key: "status",
                          header: t("banking.col.status"),
                          sortable: true,
                          render: (row) => <StatusChip status={String(row.status)} />,
                        },
                        { key: "confidence", header: t("banking.col.confidence"), sortable: true },
                        { key: "created", header: t("banking.col.created"), sortable: true },
                        { key: "completed", header: t("banking.col.completed"), sortable: true },
                      ]}
                      rows={jobRows}
                      selectable
                      onSelectionChange={(ids) => {
                        if (ids[0]) setSelectedJobId(ids[0]);
                      }}
                    />
                    {selectedJob ? (
                      <section
                        className="ba-detail-panel mp-animate-in"
                        aria-label={t("banking.jobDetail")}
                      >
                        <header>{t("banking.jobDetail")}</header>
                        <dl className="ba-detail-dl">
                          <div>
                            <dt>{t("banking.col.capability")}</dt>
                            <dd>{selectedJob.capability}</dd>
                          </div>
                          <div>
                            <dt>{t("banking.col.status")}</dt>
                            <dd>
                              <StatusChip status={selectedJob.status} />
                            </dd>
                          </div>
                          <div>
                            <dt>{t("banking.col.confidence")}</dt>
                            <dd>{compactText(selectedJob.confidence ?? "—")}</dd>
                          </div>
                          <div>
                            <dt>{t("banking.col.created")}</dt>
                            <dd>{compactText(selectedJob.created_at?.slice(0, 19) ?? "—")}</dd>
                          </div>
                          <div>
                            <dt>{t("banking.col.completed")}</dt>
                            <dd>{compactText(selectedJob.completed_at?.slice(0, 19) ?? "—")}</dd>
                          </div>
                        </dl>
                        {selectedJob.result ? (
                          <pre className="ba-result-pre">{compactText(selectedJob.result)}</pre>
                        ) : null}
                        <div className="ba-actions">
                          <button
                            type="button"
                            className="mp-btn"
                            onClick={() => setTab("recommendations")}
                          >
                            {t("banking.tab.recommendations")}
                          </button>
                          <button
                            type="button"
                            className="mp-btn mp-btn-primary"
                            disabled={busy}
                            onClick={() =>
                              void runAction(selectedJob.capability, (active) =>
                                runBankingAnalysis(active, selectedJob.capability),
                              )
                            }
                          >
                            {t("banking.runAnalysis")}
                          </button>
                        </div>
                      </section>
                    ) : null}
                  </>
                )
              ) : null}

              {tab === "catalog" ? (
                <DataTable
                  columns={[
                    { key: "capability", header: t("banking.col.capability"), sortable: true },
                    { key: "key", header: t("banking.col.key"), sortable: true },
                    { key: "supported", header: t("banking.col.supported"), sortable: true },
                    { key: "explainable", header: t("banking.explainable"), sortable: true },
                  ]}
                  rows={capabilityRows}
                />
              ) : null}

              {tab === "policies" ? (
                <DataTable
                  columns={[
                    { key: "key", header: t("banking.col.policy"), sortable: true },
                    { key: "description", header: t("banking.col.description"), sortable: true },
                  ]}
                  rows={policyRows}
                />
              ) : null}
            </div>
          </div>
        </div>
      ) : null}

      <style jsx>{`
        .ba-layout {
          display: grid;
          grid-template-columns: minmax(280px, 340px) 1fr;
          gap: 1.25rem;
          align-items: start;
          direction: ltr;
        }
        .ba-aside,
        .ba-main {
          display: flex;
          flex-direction: column;
          gap: 1rem;
          min-width: 0;
          direction: inherit;
        }
        :global([dir="rtl"]) .ba-aside,
        :global([dir="rtl"]) .ba-main {
          direction: rtl;
        }
        .ba-aside {
          position: sticky;
          top: 4.5rem;
          max-height: calc(100vh - 5.5rem);
          overflow: auto;
        }
        .ba-alert {
          color: var(--mp-orange);
          margin: 0.5rem 0;
        }
        .ba-session {
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius);
          overflow: hidden;
          background: var(--mp-bg-elevated);
          box-shadow: var(--mp-shadow);
          margin-block-end: 1rem;
        }
        .ba-session-banner {
          background: var(--mp-forest);
          color: var(--mp-fg-on-brand);
          padding: 1rem 1.15rem;
          box-shadow: inset 0 -2px 0 var(--mp-gold-soft);
        }
        .ba-session-banner h2 {
          margin: 0 0 0.35rem;
          font-size: 1rem;
        }
        .ba-session-banner p {
          margin: 0;
          opacity: 0.9;
          font-size: 0.88rem;
        }
        .ba-session-body {
          padding: 1rem;
        }
        .ba-form-grid {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 0.75rem;
          margin-block-end: 0.85rem;
        }
        .ba-actions {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .ba-panel-card {
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius);
          background: var(--mp-bg-elevated);
          box-shadow: var(--mp-shadow);
          overflow: hidden;
        }
        .ba-panel-head {
          padding: 0.7rem 1rem;
          color: #fff;
        }
        .ba-panel-head h2 {
          margin: 0;
          font-size: 0.82rem;
          letter-spacing: 0.05em;
          text-transform: uppercase;
        }
        .ba-jewel-bar--forest {
          background: linear-gradient(120deg, var(--mp-forest), #2f5a48);
          box-shadow: inset 0 -2px 0 var(--mp-gold-soft);
        }
        .ba-jewel-bar--emerald {
          background: linear-gradient(120deg, var(--mp-emerald), #047857);
          box-shadow: inset 0 -2px 0 var(--mp-gold-soft);
        }
        .ba-jewel-bar--royal {
          background: linear-gradient(120deg, var(--mp-royal), var(--mp-royal-bright));
          box-shadow: inset 0 -2px 0 var(--mp-gold-soft);
        }
        .ba-jewel-bar--gold {
          background: linear-gradient(120deg, var(--mp-gold), var(--mp-gold-soft));
          color: #1a1a1a;
        }
        .ba-jewel-bar--gold h2 {
          color: #1a1a1a;
        }
        .ba-filters {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
          align-items: end;
        }
        .ba-status-filter {
          display: grid;
          gap: 0.25rem;
          min-inline-size: 10rem;
        }
        .ba-detail-panel {
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius);
          padding: 0.75rem 1rem;
          display: grid;
          gap: 0.65rem;
          margin-block-start: 0.85rem;
          background: var(--mp-bg-elevated);
        }
        .ba-detail-panel header {
          font-weight: 600;
        }
        .ba-detail-dl {
          display: grid;
          gap: 0.45rem;
          margin: 0;
          grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr));
        }
        .ba-detail-dl dt {
          font-size: 0.8em;
          color: var(--mp-fg-muted);
        }
        .ba-detail-dl dd {
          margin: 0;
          font-weight: 500;
        }
        .ba-result-pre {
          margin: 0;
          padding: 0.65rem 0.75rem;
          border-radius: var(--mp-radius-sm, 0.35rem);
          background: color-mix(in srgb, var(--mp-royal) 6%, transparent);
          font-size: 0.78rem;
          overflow: auto;
          max-block-size: 10rem;
          white-space: pre-wrap;
          word-break: break-word;
        }
        .ba-panel-body {
          padding: 1rem;
        }
        .ba-panel-body--tight {
          padding: 0.55rem;
        }
        .ba-status-row {
          display: flex;
          justify-content: space-between;
          gap: 0.75rem;
          padding: 0.35rem 0;
          border-block-end: 1px solid var(--mp-border);
          font-size: 0.85rem;
        }
        .ba-headline {
          margin: 0.75rem 0 0;
          font-size: 0.9rem;
          font-weight: 600;
          line-height: 1.4;
        }
        .ba-run-list {
          list-style: none;
          margin: 0;
          padding: 0;
          display: flex;
          flex-direction: column;
          gap: 0.2rem;
        }
        .ba-run-link {
          width: 100%;
          display: flex;
          align-items: center;
          gap: 0.55rem;
          padding: 0.4rem 0.5rem;
          border: 0;
          border-radius: var(--mp-radius-sm);
          background: transparent;
          cursor: pointer;
          text-align: start;
          color: inherit;
          font-size: 0.84rem;
        }
        .ba-run-link:hover {
          background: color-mix(in srgb, var(--mp-royal) 8%, transparent);
        }
        .ba-dot {
          width: 0.65rem;
          height: 0.65rem;
          border-radius: 999px;
          flex-shrink: 0;
        }
        .ba-textarea {
          min-height: 5.5rem;
          resize: vertical;
          margin-block: 0.35rem 0.65rem;
        }
        .ba-metrics {
          display: grid;
          grid-template-columns: repeat(6, minmax(0, 1fr));
          gap: 0.65rem;
        }
        .ba-metric {
          padding: 0.8rem 0.85rem;
          border-radius: var(--mp-radius);
          background: var(--mp-bg-elevated);
          border: 1px solid var(--mp-border);
          border-block-start: 3px solid var(--mp-silver);
          box-shadow: var(--mp-shadow);
        }
        .ba-metric--forest {
          border-block-start-color: var(--mp-forest);
        }
        .ba-metric--royal {
          border-block-start-color: var(--mp-royal);
        }
        .ba-metric--emerald {
          border-block-start-color: var(--mp-emerald);
        }
        .ba-metric--gold {
          border-block-start-color: var(--mp-gold);
        }
        .ba-metric--orange {
          border-block-start-color: var(--mp-orange);
        }
        .ba-metric--purple {
          border-block-start-color: var(--mp-purple);
        }
        .ba-metric strong {
          display: block;
          font-size: 1.2rem;
        }
        .ba-metric-label {
          display: block;
          font-size: 0.7rem;
          text-transform: uppercase;
          letter-spacing: 0.04em;
          color: var(--mp-fg-muted);
          margin-block-end: 0.2rem;
        }
        .ba-tabs {
          display: flex;
          flex-wrap: wrap;
          gap: 0.35rem;
        }
        .ba-tab {
          border: 1px solid var(--mp-border);
          background: var(--mp-bg-elevated);
          color: var(--mp-fg-muted);
          border-radius: 999px;
          padding: 0.3rem 0.75rem;
          font-size: 0.78rem;
          cursor: pointer;
        }
        .ba-tab--on {
          background: var(--mp-forest);
          border-color: var(--mp-forest);
          color: #fff;
          box-shadow: inset 0 -1px 0 var(--mp-gold-soft);
        }
        .ba-panel {
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius);
          background: var(--mp-bg-elevated);
          box-shadow: var(--mp-shadow);
          padding: 1rem;
        }
        .ba-overview {
          display: grid;
          gap: 1rem;
        }
        .ba-card h2,
        .ba-surface-head h2,
        .ba-ai h3 {
          margin: 0 0 0.75rem;
          font-size: 0.85rem;
          letter-spacing: 0.05em;
          text-transform: uppercase;
          color: var(--mp-fg-muted);
        }
        .ba-surface-head {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 0.75rem;
          margin-block-end: 0.85rem;
        }
        .ba-surface-grid {
          list-style: none;
          margin: 0;
          padding: 0;
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(12.5rem, 1fr));
          gap: 0.65rem;
        }
        .ba-surface-tile {
          width: 100%;
          aspect-ratio: 8 / 5;
          display: flex;
          align-items: center;
          gap: 0.65rem;
          padding: 0.65rem 0.75rem;
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius);
          background: var(--mp-bg-subtle);
          cursor: pointer;
          text-align: start;
          color: inherit;
        }
        .ba-surface-tile:hover {
          border-color: var(--mp-gold);
        }
        .ba-surface-tile strong {
          display: block;
          font-size: 0.84rem;
        }
        .ba-icon {
          width: 2.4rem;
          height: 2.4rem;
          border-radius: 0.45rem;
          display: grid;
          place-items: center;
          color: #fff;
          font-size: 0.7rem;
          font-weight: 700;
          flex-shrink: 0;
        }
        .ba-jewel--forest {
          background: linear-gradient(145deg, #2f5a48, var(--mp-forest));
        }
        .ba-jewel--royal {
          background: linear-gradient(145deg, var(--mp-royal-bright), var(--mp-royal));
        }
        .ba-jewel--emerald {
          background: linear-gradient(145deg, var(--mp-emerald-bright), var(--mp-emerald));
        }
        .ba-jewel--gold {
          background: linear-gradient(145deg, var(--mp-gold-soft), var(--mp-gold));
          color: #1a1a1a;
        }
        .ba-jewel--orange {
          background: linear-gradient(145deg, #e06a3a, var(--mp-orange));
        }
        .ba-jewel--purple {
          background: linear-gradient(145deg, var(--mp-purple-soft), var(--mp-purple));
        }
        .ba-jewel--silver {
          background: linear-gradient(145deg, #cfd3da, var(--mp-silver));
          color: #1a1a1a;
        }
        :global(.ba-chip) {
          display: inline-block;
          padding: 0.1rem 0.45rem;
          border-radius: 999px;
          font-size: 0.72rem;
          font-weight: 600;
          background: var(--mp-bg-muted);
          color: var(--mp-fg-muted);
        }
        :global(.ba-chip--ok) {
          background: var(--mp-success-bg);
          color: var(--mp-emerald);
        }
        :global(.ba-chip--warn) {
          background: var(--mp-warning-bg);
          color: var(--mp-gold);
        }
        :global(.ba-chip--muted) {
          background: color-mix(in srgb, var(--mp-silver) 28%, transparent);
        }
        @media (max-width: 1100px) {
          .ba-metrics {
            grid-template-columns: repeat(3, minmax(0, 1fr));
          }
        }
        @media (max-width: 960px) {
          .ba-layout {
            grid-template-columns: 1fr;
          }
          .ba-aside {
            position: static;
            max-height: none;
          }
          .ba-form-grid {
            grid-template-columns: 1fr;
          }
          .ba-metrics {
            grid-template-columns: repeat(2, minmax(0, 1fr));
          }
        }
      `}</style>
    </PageLayout>
  );
}
