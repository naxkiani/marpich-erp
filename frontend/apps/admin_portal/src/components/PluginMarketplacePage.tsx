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
  fetchInstalledPlugins,
  fetchMarketplaceDashboard,
  fetchMarketplaceListings,
  installPlugin,
  invokePlugin,
  loadPluginsSession,
  loginPluginsSession,
  savePluginsSession,
  uninstallPlugin,
  verifyPlugin,
  type ApiSession,
  type MarketplaceDashboard,
  type PluginInstallation,
  type PluginListing,
} from "@/lib/pluginsClient";

const DRAFT_KEY = "marpich.plugins.marketplace.draft";

function StatusChip({ status }: { status: string }) {
  const tone =
    status === "published" || status === "verified" || status === "enabled" || status === "true" || status === "ok"
      ? "ok"
      : status === "community" || status === "disabled" || status === "false"
        ? "warn"
        : status === "failed" || status === "unsigned"
          ? "bad"
          : "muted";
  return (
    <span className={`plg-chip plg-chip--${tone}`} data-status={status}>
      {status}
    </span>
  );
}

export function PluginMarketplacePage() {
  const { push } = useToast();
  const { t } = useLocale();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(15);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("plugins-demo");
  const [email, setEmail] = useState("admin@plugins.dev");
  const [password, setPassword] = useState("SecurePass123!");
  const [filterQ, setFilterQ] = useState("");
  const [typeFilter, setTypeFilter] = useState("");
  const [trustFilter, setTrustFilter] = useState("");
  const [selectedPluginId, setSelectedPluginId] = useState("");
  const [draftReady, setDraftReady] = useState(false);
  const [lastInvoke, setLastInvoke] = useState<Record<string, unknown> | null>(null);
  const [lastAction, setLastAction] = useState<string | null>(null);

  const [dashboard, setDashboard] = useState<MarketplaceDashboard | null>(null);
  const [listings, setListings] = useState<PluginListing[]>([]);
  const [installed, setInstalled] = useState<PluginInstallation[]>([]);

  const formDraft = useMemo(
    () => ({ filterQ, typeFilter, trustFilter }),
    [filterQ, trustFilter, typeFilter],
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
        if (typeof parsed.typeFilter === "string") setTypeFilter(parsed.typeFilter);
        if (typeof parsed.trustFilter === "string") setTrustFilter(parsed.trustFilter);
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
      setProgress(30);
      setError(null);
      try {
        const [dash, list, inst] = await Promise.all([
          fetchMarketplaceDashboard(active),
          fetchMarketplaceListings(active),
          fetchInstalledPlugins(active),
        ]);
        setDashboard(dash);
        setListings(list);
        setInstalled(inst);
        setSelectedPluginId((prev) => {
          if (prev && list.some((p) => p.plugin_id === prev)) return prev;
          return list[0]?.plugin_id ?? "";
        });
        setProgress(100);
      } catch (err) {
        setError(err instanceof Error ? err.message : t("plugins.loadFailed"));
        setProgress(100);
      } finally {
        setLoading(false);
      }
    },
    [t],
  );

  useEffect(() => {
    const stored = loadPluginsSession();
    if (stored) {
      setSession(stored);
      void loadData(stored);
      return;
    }
    setLoading(false);
    setProgress(100);
  }, [loadData]);

  const installedIds = useMemo(() => new Set(installed.map((i) => i.plugin_id)), [installed]);

  const stats = useMemo(() => {
    if (!dashboard) return [];
    const types = Object.keys(dashboard.listings_by_type).length;
    return [
      {
        label: t("plugins.stat.listings"),
        value: Object.values(dashboard.listings_by_type).reduce((a, b) => a + b, 0),
        tone: "ok" as const,
      },
      { label: t("plugins.stat.types"), value: types, tone: "ok" as const },
      {
        label: t("plugins.stat.installed"),
        value: dashboard.installed_count,
        tone: "ok" as const,
      },
      {
        label: t("plugins.stat.upgrades"),
        value: dashboard.upgrade_backlog.length,
        tone: dashboard.upgrade_backlog.length ? ("warn" as const) : ("ok" as const),
      },
      {
        label: t("plugins.stat.violations"),
        value: dashboard.sandbox_violations_24h,
        tone: dashboard.sandbox_violations_24h ? ("warn" as const) : ("ok" as const),
      },
    ];
  }, [dashboard, t]);

  const q = filterQ.toLowerCase().trim();

  const listingRows = useMemo(
    () =>
      listings
        .filter((p) => {
          if (typeFilter && p.plugin_type !== typeFilter) return false;
          if (trustFilter && p.trust_level !== trustFilter) return false;
          if (!q) return true;
          const hay =
            `${p.plugin_id} ${p.display_name} ${p.publisher_name} ${p.plugin_type} ${p.trust_level}`.toLowerCase();
          return hay.includes(q);
        })
        .map((p) => ({
          id: p.plugin_id,
          name: p.display_name,
          type: p.plugin_type,
          publisher: p.publisher_name,
          version: p.current_version,
          trust: p.trust_level,
          sandbox: p.sandbox_profile,
          installed: installedIds.has(p.plugin_id) ? t("plugins.yes") : t("plugins.no"),
        })),
    [installedIds, listings, q, t, trustFilter, typeFilter],
  );

  const installedRows = useMemo(
    () =>
      installed
        .filter((i) => {
          if (!q) return true;
          return `${i.plugin_id} ${i.installed_version}`.toLowerCase().includes(q);
        })
        .map((i) => ({
          id: i.plugin_id,
          plugin: i.plugin_id,
          version: i.installed_version,
          enabled: i.enabled ? t("plugins.enabled") : t("plugins.disabled"),
          sandbox: i.sandbox_profile,
        })),
    [installed, q, t],
  );

  const selectedListing = useMemo(
    () => listings.find((p) => p.plugin_id === selectedPluginId) ?? null,
    [listings, selectedPluginId],
  );

  const selectedInstall = useMemo(
    () => installed.find((i) => i.plugin_id === selectedPluginId) ?? null,
    [installed, selectedPluginId],
  );

  const lifecycleStep = useMemo(() => {
    if (!listings.length) return 0;
    if (lastInvoke) return 3;
    if (installed.length > 0) return 2;
    return 1;
  }, [installed.length, lastInvoke, listings.length]);

  const workflowSteps = useMemo(
    () => [
      t("plugins.step.browse"),
      t("plugins.step.install"),
      t("plugins.step.invoke"),
      t("plugins.step.monitor"),
    ],
    [t],
  );

  const exportRows = useMemo(
    () =>
      listingRows.map((r) => ({
        id: r.id,
        name: r.name,
        type: r.type,
        publisher: r.publisher,
        version: r.version,
        trust: r.trust,
        installed: r.installed,
      })),
    [listingRows],
  );

  async function onConnect() {
    try {
      const next = await loginPluginsSession(tenantId, email, password);
      setSession(next);
      savePluginsSession(next);
      push({ message: t("plugins.connected") });
      await loadData(next);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : t("plugins.connectFailed") });
    }
  }

  async function onInstall(plugin: PluginListing) {
    if (!session) return;
    try {
      await installPlugin(session, plugin.plugin_id, plugin.permissions);
      setLastAction(t("plugins.install"));
      await loadData(session);
      push({ message: `${t("plugins.install")} — ${t("plugins.done")}` });
    } catch (err) {
      push({
        message: err instanceof Error ? err.message : `${t("plugins.install")} ${t("plugins.failed")}`,
      });
    }
  }

  async function onUninstall(pluginId: string) {
    if (!session) return;
    try {
      await uninstallPlugin(session, pluginId);
      setLastAction(t("plugins.uninstall"));
      await loadData(session);
      push({ message: `${t("plugins.uninstall")} — ${t("plugins.done")}` });
    } catch (err) {
      push({
        message:
          err instanceof Error ? err.message : `${t("plugins.uninstall")} ${t("plugins.failed")}`,
      });
    }
  }

  async function onInvoke(plugin: PluginListing) {
    if (!session) return;
    const point = plugin.extension_points[0];
    if (!point) {
      push({ message: t("plugins.noExtension") });
      return;
    }
    try {
      const result = await invokePlugin(session, plugin.plugin_id, point, { source: "admin" });
      setLastInvoke(result);
      setLastAction(t("plugins.invoke"));
      push({ message: `${t("plugins.invoke")} — ${t("plugins.done")}` });
    } catch (err) {
      push({
        message: err instanceof Error ? err.message : `${t("plugins.invoke")} ${t("plugins.failed")}`,
      });
    }
  }

  async function onVerify(pluginId: string) {
    if (!session) return;
    try {
      await verifyPlugin(session, pluginId);
      setLastAction(t("plugins.verify"));
      push({ message: `${t("plugins.verify")} — ${t("plugins.done")}` });
    } catch (err) {
      push({
        message: err instanceof Error ? err.message : `${t("plugins.verify")} ${t("plugins.failed")}`,
      });
    }
  }

  return (
    <PageLayout
      title={t("plugins.title")}
      subtitle={t("plugins.subtitle")}
      breadcrumb={[
        { label: t("app.name"), href: "/" },
        { label: t("plugins.breadcrumb"), href: "/enterprise/plugins" },
        { label: t("plugins.title") },
      ]}
      actions={
        session ? (
          <>
            <ExportButton
              label={t("common.export")}
              rows={exportRows}
              filename="plugin-marketplace.csv"
            />
            <PrintButton label={t("common.print")} />
            {selectedListing && !selectedInstall ? (
              <button
                type="button"
                className="mp-btn mp-btn-primary"
                onClick={() => void onInstall(selectedListing)}
              >
                {t("plugins.install")}
              </button>
            ) : null}
            {selectedListing && selectedInstall ? (
              <button
                type="button"
                className="mp-btn mp-btn-primary"
                onClick={() => void onInvoke(selectedListing)}
              >
                {t("plugins.invoke")}
              </button>
            ) : null}
            <button
              type="button"
              className="mp-btn"
              onClick={() => session && void loadData(session)}
              disabled={loading}
            >
              {t("common.refresh")}
            </button>
          </>
        ) : null
      }
    >
      <ProgressBar value={progress} label={loading ? t("plugins.loading") : t("plugins.ready")} />

      {!session ? (
        <section className="plg-connect" aria-labelledby="connect-heading">
          <h2 id="connect-heading">{t("plugins.connectHint")}</h2>
          <p className="plg-muted">{t("plugins.connectHelp")}</p>
          <div className="plg-form">
            <label>
              {t("dashboard.tenant")}
              <input className="mp-input" value={tenantId} onChange={(e) => setTenantId(e.target.value)} />
            </label>
            <label>
              {t("dashboard.email")}
              <input className="mp-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            </label>
            <label>
              {t("dashboard.password")}
              <input
                className="mp-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </label>
            <button type="button" className="mp-btn mp-btn-primary" onClick={() => void onConnect()}>
              {t("plugins.connect")}
            </button>
          </div>
        </section>
      ) : null}

      {error ? (
        <p className="plg-error" role="alert">
          {error}
        </p>
      ) : null}
      {session && loading ? <SkeletonTable rows={4} cols={4} /> : null}

      {session && dashboard && !loading ? (
        <div className="plg-layout">
          <aside className="plg-aside" aria-label={t("plugins.rail")}>
            <section className="plg-panel-card">
              <header className="plg-panel-head">
                <h2>{t("plugins.workflow")}</h2>
              </header>
              <div className="plg-panel-body">
                <StepProgress steps={workflowSteps} current={lifecycleStep} />
                {draftSaving ? (
                  <p className="mp-field-help" aria-live="polite">
                    {t("plugins.draftSaved")}…
                  </p>
                ) : (
                  <p className="mp-field-help">{t("plugins.workflowHint")}</p>
                )}
                {selectedListing ? (
                  <p className="mp-field-help">
                    <StatusChip status={selectedListing.trust_level} /> · {selectedListing.display_name}
                  </p>
                ) : (
                  <p className="mp-field-help">{t("plugins.selectHint")}</p>
                )}
              </div>
            </section>

            <section className="plg-panel-card">
              <header className="plg-panel-head">
                <h2>{t("plugins.rail.status")}</h2>
              </header>
              <div className="plg-panel-body">
                <div className="plg-status-row">
                  <span>{t("dashboard.tenant")}</span>
                  <strong>{session.tenantId}</strong>
                </div>
                {lastAction ? (
                  <p className="mp-field-help">
                    {t("plugins.lastAction")}: {lastAction}
                  </p>
                ) : null}
              </div>
            </section>
          </aside>

          <div className="plg-main">
            <div className="plg-stats">
              {stats.map((stat) => (
                <article
                  key={stat.label}
                  className={`plg-stat${stat.tone === "warn" ? " plg-stat-warn" : ""}`}
                >
                  <span className="plg-stat-value">{stat.value}</span>
                  <span className="plg-stat-label">{stat.label}</span>
                </article>
              ))}
            </div>

            <div className="plg-filters">
              <AdvancedFilterBar
                filters={[{ id: "q", label: t("common.filter"), type: "text" }]}
                onChange={(values) => setFilterQ(values.q ?? "")}
              />
              <label className="mp-filter-item">
                <span>{t("plugins.field.type")}</span>
                <select
                  className="mp-input"
                  value={typeFilter}
                  onChange={(e) => setTypeFilter(e.target.value)}
                >
                  <option value="">{t("plugins.filterAll")}</option>
                  <option value="widget">widget</option>
                  <option value="report">report</option>
                  <option value="module">module</option>
                  <option value="integration">integration</option>
                </select>
              </label>
              <label className="mp-filter-item">
                <span>{t("plugins.field.trust")}</span>
                <select
                  className="mp-input"
                  value={trustFilter}
                  onChange={(e) => setTrustFilter(e.target.value)}
                >
                  <option value="">{t("plugins.filterAll")}</option>
                  <option value="community">community</option>
                  <option value="verified">verified</option>
                  <option value="enterprise">enterprise</option>
                </select>
              </label>
            </div>

            {dashboard.top_publishers.length ? (
              <div className="plg-context">
                {dashboard.top_publishers.map((pub) => (
                  <span key={pub.publisher}>
                    {pub.publisher}: {pub.listings}
                  </span>
                ))}
              </div>
            ) : null}

            <section aria-labelledby="listings-heading">
              <h2 id="listings-heading">
                {t("plugins.listings")} ({listings.length})
              </h2>
              {listingRows.length ? (
                <>
                  <DataTable
                    columns={[
                      { key: "name", header: t("plugins.col.name"), sortable: true },
                      { key: "type", header: t("plugins.col.type"), sortable: true },
                      { key: "publisher", header: t("plugins.col.publisher"), sortable: true },
                      { key: "version", header: t("plugins.col.version"), sortable: true },
                      {
                        key: "trust",
                        header: t("plugins.field.trust"),
                        sortable: true,
                        render: (row) => <StatusChip status={String(row.trust)} />,
                      },
                      { key: "installed", header: t("plugins.col.installed"), sortable: true },
                    ]}
                    rows={listingRows}
                    selectable
                    onSelectionChange={(ids) => {
                      if (ids[0]) setSelectedPluginId(ids[0]);
                    }}
                  />
                  {selectedListing ? (
                    <section
                      className="plg-detail-panel mp-animate-in"
                      aria-label={t("plugins.detail")}
                    >
                      <header>{t("plugins.detail")}</header>
                      <dl className="plg-detail-dl">
                        <div>
                          <dt>{t("plugins.col.id")}</dt>
                          <dd>{selectedListing.plugin_id}</dd>
                        </div>
                        <div>
                          <dt>{t("plugins.col.name")}</dt>
                          <dd>{selectedListing.display_name}</dd>
                        </div>
                        <div>
                          <dt>{t("plugins.field.trust")}</dt>
                          <dd>
                            <StatusChip status={selectedListing.trust_level} />
                          </dd>
                        </div>
                        <div>
                          <dt>{t("plugins.col.sandbox")}</dt>
                          <dd>{selectedListing.sandbox_profile}</dd>
                        </div>
                        <div>
                          <dt>{t("plugins.col.permissions")}</dt>
                          <dd>{selectedListing.permissions.join(", ") || "—"}</dd>
                        </div>
                        <div>
                          <dt>{t("plugins.col.extensions")}</dt>
                          <dd>{selectedListing.extension_points.join(", ") || "—"}</dd>
                        </div>
                      </dl>
                      <p className="plg-muted">{selectedListing.description}</p>
                      <div className="plg-actions-row">
                        {!selectedInstall ? (
                          <button
                            type="button"
                            className="mp-btn mp-btn-primary"
                            onClick={() => void onInstall(selectedListing)}
                          >
                            {t("plugins.install")}
                          </button>
                        ) : (
                          <>
                            <button
                              type="button"
                              className="mp-btn mp-btn-primary"
                              onClick={() => void onInvoke(selectedListing)}
                            >
                              {t("plugins.invoke")}
                            </button>
                            <button
                              type="button"
                              className="mp-btn"
                              onClick={() => void onUninstall(selectedListing.plugin_id)}
                            >
                              {t("plugins.uninstall")}
                            </button>
                          </>
                        )}
                        <button
                          type="button"
                          className="mp-btn"
                          onClick={() => void onVerify(selectedListing.plugin_id)}
                        >
                          {t("plugins.verify")}
                        </button>
                      </div>
                    </section>
                  ) : null}
                </>
              ) : (
                <EmptyState
                  title={t("plugins.noListings")}
                  description={t("plugins.noListingsHint")}
                  action={
                    <button
                      type="button"
                      className="mp-btn mp-btn-primary"
                      onClick={() => session && void loadData(session)}
                    >
                      {t("common.refresh")}
                    </button>
                  }
                />
              )}
            </section>

            <div className="plg-grid">
              <section aria-labelledby="installed-heading">
                <h2 id="installed-heading">
                  {t("plugins.installed")} ({installed.length})
                </h2>
                {installedRows.length ? (
                  <DataTable
                    columns={[
                      { key: "plugin", header: t("plugins.col.id"), sortable: true },
                      { key: "version", header: t("plugins.col.version"), sortable: true },
                      {
                        key: "enabled",
                        header: t("plugins.field.enabled"),
                        sortable: true,
                        render: (row) => <StatusChip status={String(row.enabled)} />,
                      },
                      { key: "sandbox", header: t("plugins.col.sandbox"), sortable: true },
                    ]}
                    rows={installedRows}
                  />
                ) : (
                  <EmptyState
                    title={t("plugins.noInstalled")}
                    description={t("plugins.noInstalledHint")}
                  />
                )}
              </section>

              <section aria-labelledby="invoke-heading">
                <h2 id="invoke-heading">{t("plugins.lastInvoke")}</h2>
                {lastInvoke ? (
                  <pre className="plg-pre" aria-live="polite">
                    {JSON.stringify(lastInvoke, null, 2)}
                  </pre>
                ) : (
                  <EmptyState
                    title={t("plugins.noInvoke")}
                    description={t("plugins.noInvokeHint")}
                  />
                )}
              </section>
            </div>

            {dashboard.upgrade_backlog.length ? (
              <section aria-labelledby="upgrades-heading">
                <h2 id="upgrades-heading">{t("plugins.upgrades")}</h2>
                <DataTable
                  columns={[
                    { key: "plugin", header: t("plugins.col.id"), sortable: true },
                    { key: "current", header: t("plugins.col.current"), sortable: true },
                    { key: "latest", header: t("plugins.col.latest"), sortable: true },
                  ]}
                  rows={dashboard.upgrade_backlog.map((u) => ({
                    id: u.plugin_id,
                    plugin: u.plugin_id,
                    current: u.current_version,
                    latest: u.latest_version,
                  }))}
                />
              </section>
            ) : null}
          </div>
        </div>
      ) : null}

      <style jsx>{`
        .plg-connect {
          margin: 1rem 0 1.5rem;
          padding: 1rem;
          border: 1px solid var(--mp-border, #e2e8f0);
          border-radius: 8px;
        }
        .plg-form {
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
        .plg-muted {
          color: var(--mp-text-muted, #64748b);
          margin: 0.5rem 0;
        }
        .plg-error {
          color: var(--mp-orange);
          margin: 0.75rem 0;
        }
        .plg-layout {
          display: grid;
          grid-template-columns: minmax(220px, 280px) 1fr;
          gap: 1.25rem;
          align-items: start;
        }
        .plg-aside {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
          position: sticky;
          top: 1rem;
        }
        .plg-panel-card {
          border: 1px solid var(--mp-border, #e2e8f0);
          border-radius: 8px;
          background: var(--mp-surface, #fff);
          overflow: hidden;
        }
        .plg-panel-head {
          padding: 0.65rem 0.85rem;
          border-bottom: 1px solid var(--mp-border, #e2e8f0);
          background: var(--mp-surface-2, #f8fafc);
        }
        .plg-panel-head h2 {
          margin: 0;
          font-size: 0.95rem;
        }
        .plg-panel-body {
          padding: 0.85rem;
        }
        .plg-status-row {
          display: flex;
          justify-content: space-between;
          gap: 0.5rem;
          font-size: 0.85rem;
        }
        .plg-main {
          min-width: 0;
        }
        .plg-stats {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
          gap: 0.75rem;
          margin: 0 0 1rem;
        }
        .plg-stat {
          padding: 1rem;
          border-radius: 8px;
          background: var(--mp-surface-2, #f8fafc);
          border: 1px solid var(--mp-border, #e2e8f0);
        }
        .plg-stat-warn {
          border-color: #f59e0b;
        }
        .plg-stat-value {
          display: block;
          font-size: 1.2rem;
          font-weight: 700;
        }
        .plg-stat-label {
          font-size: 0.75rem;
          color: var(--mp-text-muted, #64748b);
        }
        .plg-filters {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
          align-items: end;
          margin-bottom: 1rem;
        }
        .plg-context {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
          margin-bottom: 1rem;
          font-size: 0.85rem;
          color: var(--mp-text-muted, #64748b);
        }
        .plg-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 1.25rem;
          margin: 1.5rem 0;
        }
        .plg-chip {
          display: inline-block;
          padding: 0.1rem 0.45rem;
          border-radius: 4px;
          font-size: 0.75rem;
          font-weight: 600;
        }
        .plg-chip--ok {
          background: #dcfce7;
          color: #166534;
        }
        .plg-chip--warn {
          background: #fef3c7;
          color: #92400e;
        }
        .plg-chip--bad {
          background: #fee2e2;
          color: #991b1b;
        }
        .plg-chip--muted {
          background: #f1f5f9;
          color: #475569;
        }
        .plg-detail-panel {
          margin-top: 0.75rem;
          padding: 0.85rem 1rem;
          border: 1px solid var(--mp-border, #e2e8f0);
          border-radius: 8px;
          background: var(--mp-surface-2, #f8fafc);
        }
        .plg-detail-panel header {
          font-weight: 600;
          margin-bottom: 0.5rem;
        }
        .plg-detail-dl {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
          gap: 0.5rem 1rem;
          margin: 0 0 0.75rem;
        }
        .plg-detail-dl dt {
          font-size: 0.7rem;
          color: var(--mp-text-muted, #64748b);
          margin: 0;
        }
        .plg-detail-dl dd {
          margin: 0.15rem 0 0;
          font-size: 0.9rem;
          word-break: break-word;
        }
        .plg-actions-row {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .plg-pre {
          margin: 0;
          padding: 0.85rem;
          border: 1px solid var(--mp-border, #e2e8f0);
          border-radius: 8px;
          background: var(--mp-surface-2, #f8fafc);
          overflow: auto;
          font-size: 0.8rem;
          max-height: 280px;
        }
        h2 {
          margin: 0 0 0.75rem;
          font-size: 1.1rem;
        }
        @media (max-width: 960px) {
          .plg-layout {
            grid-template-columns: 1fr;
          }
          .plg-aside {
            position: static;
          }
          .plg-grid {
            grid-template-columns: 1fr;
          }
        }
        @media (prefers-reduced-motion: reduce) {
          .mp-animate-in {
            animation: none !important;
          }
        }
      `}</style>
    </PageLayout>
  );
}
