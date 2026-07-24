"use client";

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
  createAuditExport,
  fetchAuditStats,
  getAuditEntry,
  getAuditExport,
  loadAuditSession,
  loginAuditSession,
  queryAuditEntries,
  recordAuditEntry,
  saveAuditSession,
  type ApiSession,
  type AuditEntry,
  type AuditExport,
  type AuditStats,
} from "@/lib/auditClient";

const DRAFT_KEY = "marpich.audit.desk.draft";

type TabId = "entries" | "record" | "exports" | "stats";

function SeverityChip({ severity }: { severity: string }) {
  const tone =
    severity === "security"
      ? "bad"
      : severity === "compliance"
        ? "warn"
        : severity === "info" || severity === "completed"
          ? "ok"
          : "muted";
  return (
    <span className={`aud-chip aud-chip--${tone}`} data-status={severity}>
      {severity}
    </span>
  );
}

export function AuditDeskPage() {
  const { push } = useToast();
  const { t } = useLocale();
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("audit-demo");
  const [email, setEmail] = useState("audit@demo.dev");
  const [password, setPassword] = useState("SecurePass123!");
  const [tab, setTab] = useState<TabId>("entries");
  const [filterQ, setFilterQ] = useState("");
  const [severityFilter, setSeverityFilter] = useState("");
  const [eventFilter, setEventFilter] = useState("");
  const [draftReady, setDraftReady] = useState(false);
  const [lastAction, setLastAction] = useState<string | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const [entries, setEntries] = useState<AuditEntry[]>([]);
  const [total, setTotal] = useState(0);
  const [stats, setStats] = useState<AuditStats | null>(null);
  const [detail, setDetail] = useState<AuditEntry | null>(null);
  const [lastExport, setLastExport] = useState<AuditExport | null>(null);

  const [recordAction, setRecordAction] = useState("manual.review");
  const [recordResourceType, setRecordResourceType] = useState("document");
  const [recordResourceId, setRecordResourceId] = useState("");
  const [recordSeverity, setRecordSeverity] = useState<"info" | "security" | "compliance">(
    "info",
  );
  const [exportFormat, setExportFormat] = useState<"json" | "csv">("json");

  const formDraft = useMemo(
    () => ({
      filterQ,
      severityFilter,
      eventFilter,
      tab,
      recordAction,
      recordResourceType,
      recordResourceId,
      recordSeverity,
      exportFormat,
    }),
    [
      eventFilter,
      exportFormat,
      filterQ,
      recordAction,
      recordResourceId,
      recordResourceType,
      recordSeverity,
      severityFilter,
      tab,
    ],
  );

  const persistDraft = useCallback(
    async (values: typeof formDraft) => {
      if (!draftReady) return;
      try {
        localStorage.setItem(DRAFT_KEY, JSON.stringify(values));
      } catch {
        /* ignore */
      }
    },
    [draftReady],
  );

  const { saving: draftSaving } = useAutosave(formDraft, persistDraft, 900);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(DRAFT_KEY);
      if (raw) {
        const parsed = JSON.parse(raw) as Partial<typeof formDraft>;
        if (typeof parsed.filterQ === "string") setFilterQ(parsed.filterQ);
        if (typeof parsed.severityFilter === "string") setSeverityFilter(parsed.severityFilter);
        if (typeof parsed.eventFilter === "string") setEventFilter(parsed.eventFilter);
        if (
          parsed.tab === "entries" ||
          parsed.tab === "record" ||
          parsed.tab === "exports" ||
          parsed.tab === "stats"
        ) {
          setTab(parsed.tab);
        }
        if (typeof parsed.recordAction === "string" && parsed.recordAction.trim()) {
          setRecordAction(parsed.recordAction);
        }
        if (typeof parsed.recordResourceType === "string" && parsed.recordResourceType.trim()) {
          setRecordResourceType(parsed.recordResourceType);
        }
        if (typeof parsed.recordResourceId === "string") setRecordResourceId(parsed.recordResourceId);
        if (
          parsed.recordSeverity === "info" ||
          parsed.recordSeverity === "security" ||
          parsed.recordSeverity === "compliance"
        ) {
          setRecordSeverity(parsed.recordSeverity);
        }
        if (parsed.exportFormat === "json" || parsed.exportFormat === "csv") {
          setExportFormat(parsed.exportFormat);
        }
      }
    } catch {
      /* ignore */
    } finally {
      setDraftReady(true);
    }
  }, []);

  const loadData = useCallback(
    async (active: ApiSession) => {
      setLoading(true);
      setProgress(40);
      setError(null);
      try {
        const [page, statsData] = await Promise.all([
          queryAuditEntries(active, {
            event_name: eventFilter.trim() || undefined,
            severity: severityFilter || undefined,
            limit: 100,
            offset: 0,
          }),
          fetchAuditStats(active),
        ]);
        setEntries(page.items);
        setTotal(page.total);
        setStats(statsData);
        setSelectedId((prev) => {
          if (prev && page.items.some((e) => e.id === prev)) return prev;
          return page.items[0]?.id ?? null;
        });
        setProgress(100);
      } catch (err) {
        setError(err instanceof Error ? err.message : t("audit.loadFailed"));
        setProgress(100);
      } finally {
        setLoading(false);
      }
    },
    [eventFilter, severityFilter, t],
  );

  useEffect(() => {
    const existing = loadAuditSession();
    if (!existing) {
      setLoading(false);
      setProgress(100);
      return;
    }
    setSession(existing);
    setTenantId(existing.tenantId);
    void loadData(existing);
    // eslint-disable-next-line react-hooks/exhaustive-deps -- mount once
  }, []);

  useEffect(() => {
    if (!session || !selectedId) {
      setDetail(null);
      return;
    }
    const fromList = entries.find((e) => e.id === selectedId);
    if (fromList) setDetail(fromList);
    void getAuditEntry(session, selectedId)
      .then(setDetail)
      .catch(() => undefined);
  }, [entries, selectedId, session]);

  const lifecycleStep = useMemo(() => {
    if (!session) return 0;
    if (entries.length === 0) return 1;
    if (detail) return 2;
    if (lastExport || lastAction === "export") return 3;
    return 1;
  }, [detail, entries.length, lastAction, lastExport, session]);

  const workflowSteps = useMemo(
    () => [
      { id: "connect", label: t("audit.step.connect") },
      { id: "query", label: t("audit.step.query") },
      { id: "inspect", label: t("audit.step.inspect") },
      { id: "export", label: t("audit.step.export") },
    ],
    [t],
  );

  const q = filterQ.toLowerCase().trim();

  const entryRows = useMemo(
    () =>
      entries
        .filter((e) => {
          if (!q) return true;
          const hay =
            `${e.event_name} ${e.action} ${e.resource_type} ${e.severity} ${e.actor_id ?? ""}`.toLowerCase();
          return hay.includes(q);
        })
        .map((e) => ({
          id: e.id,
          event: e.event_name,
          action: e.action,
          resource: e.resource_type,
          severity: e.severity,
          actor: e.actor_id ?? "—",
          occurred: e.occurred_at.slice(0, 19).replace("T", " "),
        })),
    [entries, q],
  );

  const topEventRows = useMemo(
    () =>
      (stats?.top_events ?? []).map((row, index) => ({
        id: `${row.event_name}-${index}`,
        event: row.event_name,
        count: row.count,
      })),
    [stats],
  );

  const exportRows = useMemo(() => {
    if (tab === "stats") return topEventRows;
    return entryRows;
  }, [entryRows, tab, topEventRows]);

  async function onConnect() {
    setBusy(true);
    setError(null);
    try {
      const next = await loginAuditSession(tenantId, email, password);
      saveAuditSession(next);
      setSession(next);
      setLastAction("connect");
      push({ message: t("audit.connected") });
      await loadData(next);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("audit.connectFailed"));
    } finally {
      setBusy(false);
    }
  }

  async function onRefresh() {
    if (!session) return;
    await loadData(session);
    setLastAction("refresh");
  }

  async function onRecord() {
    if (!session) return;
    if (!recordAction.trim() || !recordResourceType.trim()) {
      push({ message: t("audit.recordRequired") });
      return;
    }
    setBusy(true);
    try {
      await recordAuditEntry(session, {
        action: recordAction.trim(),
        resource_type: recordResourceType.trim(),
        resource_id: recordResourceId.trim() || null,
        severity: recordSeverity,
      });
      setLastAction("record");
      push({ message: t("audit.recorded") });
      setTab("entries");
      await loadData(session);
    } catch (err) {
      push({
        message: err instanceof Error ? err.message : t("audit.recordFailed"),
      });
    } finally {
      setBusy(false);
    }
  }

  async function onCreateExport() {
    if (!session) return;
    setBusy(true);
    try {
      const created = await createAuditExport(session, {
        format: exportFormat,
        event_name: eventFilter.trim() || null,
        severity: severityFilter || null,
      });
      const fetched = await getAuditExport(session, created.id);
      setLastExport(fetched);
      setLastAction("export");
      setTab("exports");
      push({ message: t("audit.exportReady") });
    } catch (err) {
      push({
        message: err instanceof Error ? err.message : t("audit.exportFailed"),
      });
    } finally {
      setBusy(false);
    }
  }

  const railStats = [
    { label: t("audit.stat.total"), value: stats?.total_entries ?? total },
    { label: t("audit.stat.security"), value: stats?.security_events ?? 0 },
    { label: t("audit.stat.last24h"), value: stats?.last_24h ?? 0 },
    { label: t("audit.stat.shown"), value: entries.length },
  ];

  return (
    <PageLayout
      title={t("audit.title")}
      subtitle={t("audit.subtitle")}
      breadcrumb={[
        { label: t("app.name"), href: "/" },
        { label: t("audit.breadcrumb") },
        { label: t("audit.title") },
      ]}
      actions={
        <>
          <ExportButton rows={exportRows} filename="audit-desk.csv" />
          <PrintButton />
          {session ? (
            <button type="button" className="mp-btn" onClick={() => void onRefresh()} disabled={loading}>
              {t("audit.refresh")}
            </button>
          ) : null}
        </>
      }
    >
      <ProgressBar value={progress} label={loading ? t("audit.loading") : t("audit.ready")} />

      {!session ? (
        <section className="aud-connect" aria-label={t("audit.connect")}>
          <p className="mp-field-help">{t("audit.connectHint")}</p>
          <div className="aud-connect-form">
            <label>
              {t("audit.field.tenant")}
              <input
                className="mp-input"
                value={tenantId}
                onChange={(e) => setTenantId(e.target.value)}
                autoComplete="organization"
              />
            </label>
            <label>
              {t("audit.field.email")}
              <input
                className="mp-input"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="username"
              />
            </label>
            <label>
              {t("audit.field.password")}
              <input
                className="mp-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
              />
            </label>
            <button
              type="button"
              className="mp-btn mp-btn-primary"
              disabled={busy}
              onClick={() => void onConnect()}
            >
              {busy ? t("audit.connecting") : t("audit.connect")}
            </button>
          </div>
          {error ? (
            <p className="mp-field-help" role="alert">
              {error}
            </p>
          ) : null}
        </section>
      ) : (
        <div className="aud-layout">
          <aside className="aud-aside" aria-label={t("audit.rail")}>
            <section className="aud-panel-card">
              <header className="aud-panel-head">
                <h2>{t("audit.workflow")}</h2>
              </header>
              <div className="aud-panel-body">
                <StepProgress steps={workflowSteps} current={lifecycleStep} />
                {draftSaving ? (
                  <p className="mp-field-help" aria-live="polite">
                    {t("audit.draftSaved")}…
                  </p>
                ) : (
                  <p className="mp-field-help">{t("audit.workflowHint")}</p>
                )}
                {lastAction ? (
                  <p className="mp-field-help">
                    {t("audit.lastAction")}: {lastAction}
                  </p>
                ) : null}
              </div>
            </section>

            <section className="aud-panel-card">
              <header className="aud-panel-head">
                <h2>{t("audit.stats")}</h2>
              </header>
              <div className="aud-panel-body aud-stats">
                {railStats.map((s) => (
                  <div key={s.label} className="aud-stat">
                    <span className="aud-stat-value">{s.value}</span>
                    <span className="aud-stat-label">{s.label}</span>
                  </div>
                ))}
              </div>
            </section>
          </aside>

          <div className="aud-main">
            {error ? (
              <p className="mp-field-help" role="alert">
                {error}
              </p>
            ) : null}

            <div className="aud-tabs" role="tablist" aria-label={t("audit.tabs")}>
              {(
                [
                  ["entries", t("audit.tab.entries")],
                  ["record", t("audit.tab.record")],
                  ["exports", t("audit.tab.exports")],
                  ["stats", t("audit.tab.stats")],
                ] as const
              ).map(([id, label]) => (
                <button
                  key={id}
                  type="button"
                  role="tab"
                  aria-selected={tab === id}
                  className={`mp-btn${tab === id ? " mp-btn-primary" : ""}`}
                  onClick={() => setTab(id)}
                >
                  {label}
                </button>
              ))}
            </div>

            <div className="aud-filters">
              <AdvancedFilterBar
                filters={[{ id: "q", label: t("audit.filterPlaceholder"), type: "text" }]}
                onChange={(values) => setFilterQ(values.q ?? "")}
              />
              <label className="mp-filter-item">
                <span>{t("audit.field.severity")}</span>
                <select
                  className="mp-input"
                  value={severityFilter}
                  onChange={(e) => {
                    setSeverityFilter(e.target.value);
                    if (session) {
                      const next = e.target.value;
                      void queryAuditEntries(session, {
                        event_name: eventFilter.trim() || undefined,
                        severity: next || undefined,
                        limit: 100,
                      })
                        .then((page) => {
                          setEntries(page.items);
                          setTotal(page.total);
                        })
                        .catch((err: unknown) =>
                          setError(err instanceof Error ? err.message : t("audit.loadFailed")),
                        );
                    }
                  }}
                  aria-label={t("audit.field.severity")}
                >
                  <option value="">{t("audit.filter.all")}</option>
                  <option value="info">info</option>
                  <option value="security">security</option>
                  <option value="compliance">compliance</option>
                </select>
              </label>
              <label className="mp-filter-item">
                <span>{t("audit.field.eventName")}</span>
                <input
                  className="mp-input"
                  value={eventFilter}
                  onChange={(e) => setEventFilter(e.target.value)}
                  onBlur={() => {
                    if (session) void loadData(session);
                  }}
                />
              </label>
            </div>

            {tab === "entries" ? (
              loading ? (
                <SkeletonTable rows={6} cols={6} />
              ) : entryRows.length === 0 ? (
                <EmptyState
                  title={t("audit.empty.entries")}
                  description={t("audit.empty.entriesHint")}
                />
              ) : (
                <div className="aud-split">
                  <DataTable
                    columns={[
                      { key: "event", header: t("audit.col.event"), sortable: true },
                      { key: "action", header: t("audit.col.action"), sortable: true },
                      { key: "resource", header: t("audit.col.resource"), sortable: true },
                      {
                        key: "severity",
                        header: t("audit.col.severity"),
                        sortable: true,
                        render: (row) => <SeverityChip severity={String(row.severity)} />,
                      },
                      { key: "actor", header: t("audit.col.actor"), sortable: true },
                      { key: "occurred", header: t("audit.col.occurred"), sortable: true },
                    ]}
                    rows={entryRows}
                    selectable
                    onSelectionChange={(ids) => {
                      if (ids[0]) setSelectedId(ids[0]);
                    }}
                  />
                  {detail ? (
                    <article className="aud-detail" aria-label={t("audit.detail")}>
                      <header>
                        <h3>{detail.event_name}</h3>
                        <SeverityChip severity={detail.severity} />
                      </header>
                      <dl className="aud-detail-dl">
                        <div>
                          <dt>{t("audit.col.action")}</dt>
                          <dd>{detail.action}</dd>
                        </div>
                        <div>
                          <dt>{t("audit.col.resource")}</dt>
                          <dd>
                            {detail.resource_type}
                            {detail.resource_id ? ` / ${detail.resource_id}` : ""}
                          </dd>
                        </div>
                        <div>
                          <dt>{t("audit.col.actor")}</dt>
                          <dd>{detail.actor_id ?? "—"}</dd>
                        </div>
                        <div>
                          <dt>{t("audit.col.context")}</dt>
                          <dd>{detail.source_context}</dd>
                        </div>
                        <div>
                          <dt>{t("audit.col.correlation")}</dt>
                          <dd>{detail.correlation_id}</dd>
                        </div>
                      </dl>
                      <pre className="aud-payload">
                        {JSON.stringify(detail.payload ?? {}, null, 2)}
                      </pre>
                    </article>
                  ) : null}
                </div>
              )
            ) : null}

            {tab === "record" ? (
              <section className="aud-compose" aria-label={t("audit.tab.record")}>
                <p className="mp-field-help">{t("audit.recordHint")}</p>
                <label>
                  {t("audit.field.action")}
                  <input
                    className="mp-input"
                    value={recordAction}
                    onChange={(e) => setRecordAction(e.target.value)}
                  />
                </label>
                <label>
                  {t("audit.field.resourceType")}
                  <input
                    className="mp-input"
                    value={recordResourceType}
                    onChange={(e) => setRecordResourceType(e.target.value)}
                  />
                </label>
                <label>
                  {t("audit.field.resourceId")}
                  <input
                    className="mp-input"
                    value={recordResourceId}
                    onChange={(e) => setRecordResourceId(e.target.value)}
                  />
                </label>
                <label>
                  {t("audit.field.severity")}
                  <select
                    className="mp-input"
                    value={recordSeverity}
                    onChange={(e) =>
                      setRecordSeverity(e.target.value as "info" | "security" | "compliance")
                    }
                  >
                    <option value="info">info</option>
                    <option value="security">security</option>
                    <option value="compliance">compliance</option>
                  </select>
                </label>
                <button
                  type="button"
                  className="mp-btn mp-btn-primary"
                  disabled={busy}
                  onClick={() => void onRecord()}
                >
                  {busy ? t("audit.recording") : t("audit.record")}
                </button>
              </section>
            ) : null}

            {tab === "exports" ? (
              <section className="aud-compose" aria-label={t("audit.tab.exports")}>
                <p className="mp-field-help">{t("audit.exportHint")}</p>
                <label>
                  {t("audit.field.format")}
                  <select
                    className="mp-input"
                    value={exportFormat}
                    onChange={(e) => setExportFormat(e.target.value as "json" | "csv")}
                  >
                    <option value="json">json</option>
                    <option value="csv">csv</option>
                  </select>
                </label>
                <button
                  type="button"
                  className="mp-btn mp-btn-primary"
                  disabled={busy}
                  onClick={() => void onCreateExport()}
                >
                  {busy ? t("audit.exporting") : t("audit.createExport")}
                </button>
                {lastExport ? (
                  <article className="aud-detail" aria-label={t("audit.exportDetail")}>
                    <header>
                      <h3>
                        {t("audit.exportDetail")} · {lastExport.id.slice(0, 8)}
                      </h3>
                      <SeverityChip severity={lastExport.status} />
                    </header>
                    <p className="mp-field-help">
                      {lastExport.format} · {lastExport.entry_count} {t("audit.entries")}
                    </p>
                    {lastExport.data && lastExport.data.length > 0 ? (
                      <pre className="aud-payload">
                        {JSON.stringify(lastExport.data.slice(0, 5), null, 2)}
                      </pre>
                    ) : null}
                  </article>
                ) : (
                  <EmptyState title={t("audit.empty.exports")} description={t("audit.empty.exportsHint")} />
                )}
              </section>
            ) : null}

            {tab === "stats" ? (
              loading ? (
                <SkeletonTable rows={5} cols={2} />
              ) : topEventRows.length === 0 ? (
                <EmptyState title={t("audit.empty.stats")} />
              ) : (
                <DataTable
                  columns={[
                    { key: "event", header: t("audit.col.event"), sortable: true },
                    { key: "count", header: t("audit.col.count"), sortable: true },
                  ]}
                  rows={topEventRows}
                />
              )
            ) : null}
          </div>
        </div>
      )}

      <style jsx>{`
        .aud-connect {
          max-width: 28rem;
          margin-top: 1rem;
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .aud-connect-form {
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
        }
        .aud-layout {
          display: grid;
          grid-template-columns: minmax(220px, 280px) minmax(0, 1fr);
          gap: 1.25rem;
          margin-top: 1rem;
          align-items: start;
        }
        .aud-aside {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .aud-panel-card {
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: 0.5rem;
          background: var(--mp-surface, #fff);
        }
        .aud-panel-head {
          padding: 0.75rem 1rem;
          border-bottom: 1px solid var(--mp-border, #d8dee6);
        }
        .aud-panel-head h2 {
          margin: 0;
          font-size: 0.95rem;
        }
        .aud-panel-body {
          padding: 0.85rem 1rem;
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
        }
        .aud-stats {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 0.75rem;
        }
        .aud-stat {
          display: flex;
          flex-direction: column;
          gap: 0.15rem;
        }
        .aud-stat-value {
          font-size: 1.25rem;
          font-weight: 600;
        }
        .aud-stat-label {
          font-size: 0.8rem;
          color: var(--mp-muted, #667085);
        }
        .aud-main {
          min-width: 0;
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .aud-tabs {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .aud-filters {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
          align-items: end;
        }
        .aud-split {
          display: grid;
          grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr);
          gap: 1rem;
          align-items: start;
        }
        .aud-detail {
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: 0.5rem;
          padding: 1rem;
          background: var(--mp-surface, #fff);
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
        }
        .aud-detail header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 0.5rem;
        }
        .aud-detail h3 {
          margin: 0;
          font-size: 0.95rem;
          word-break: break-word;
        }
        .aud-detail-dl {
          margin: 0;
          display: flex;
          flex-direction: column;
          gap: 0.4rem;
        }
        .aud-detail-dl div {
          display: grid;
          grid-template-columns: 7rem 1fr;
          gap: 0.5rem;
        }
        .aud-detail-dl dt {
          color: var(--mp-muted, #667085);
          font-size: 0.8rem;
        }
        .aud-detail-dl dd {
          margin: 0;
          font-size: 0.85rem;
          word-break: break-word;
        }
        .aud-payload {
          margin: 0;
          padding: 0.75rem;
          border-radius: 0.35rem;
          background: color-mix(in srgb, var(--mp-border, #d8dee6) 35%, transparent);
          font-size: 0.75rem;
          overflow: auto;
          max-height: 16rem;
        }
        .aud-compose {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
          max-width: 36rem;
        }
        :global(.aud-chip) {
          display: inline-block;
          padding: 0.15rem 0.45rem;
          border-radius: 0.25rem;
          font-size: 0.75rem;
          text-transform: lowercase;
        }
        :global(.aud-chip--ok) {
          background: color-mix(in srgb, #12b76a 18%, transparent);
          color: #027a48;
        }
        :global(.aud-chip--warn) {
          background: color-mix(in srgb, #f79009 18%, transparent);
          color: #b54708;
        }
        :global(.aud-chip--bad) {
          background: color-mix(in srgb, #f04438 18%, transparent);
          color: #b42318;
        }
        :global(.aud-chip--muted) {
          background: color-mix(in srgb, #98a2b3 18%, transparent);
          color: #475467;
        }
        @media (max-width: 960px) {
          .aud-layout,
          .aud-split {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </PageLayout>
  );
}
