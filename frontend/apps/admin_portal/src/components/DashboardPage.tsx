"use client";

import Link from "next/link";
import { useAuth } from "@marpich/auth-provider";
import { PageLayout } from "@marpich/core";
import {
  AdvancedFilterBar,
  DataTable,
  EmptyState,
  ExportButton,
  KpiStrip,
  ProgressBar,
  PrintButton,
  SkeletonTable,
  StepProgress,
  useAutosave,
  useLocale,
  useTenantModules,
  useToast,
} from "@marpich/shared";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  PLATFORM_LAUNCH_LINKS,
  activatePlatformModule,
  fetchIndustryPacks,
  fetchPlatformTenants,
  jewelForPack,
  packInitials,
  provisionPlatformTenant,
  suspendPlatformTenant,
  type IndustryPack,
  type ModuleJewel,
  type PlatformTenant,
} from "@/lib/platformClient";
import {
  fetchHomePulse,
  homePulseHasPartialErrors,
  type HomePulseResult,
} from "@/lib/homePulseClient";

const DRAFT_KEY = "marpich.dashboard.platform.draft";

type TabId = "overview" | "tenants" | "packs" | "launch";

const METRIC_JEWELS: ModuleJewel[] = ["forest", "royal", "emerald", "gold", "orange"];

const LAUNCH_JEWELS: Record<string, ModuleJewel> = {
  hospital: "emerald",
  clinic: "royal",
  pharmacy: "forest",
  laboratory: "purple",
  university: "royal",
  banking: "gold",
  documents: "silver",
  observability: "orange",
  scheduler: "purple",
  integration: "forest",
};

function StatusChip({ status, label }: { status: string; label?: string }) {
  const tone =
    status === "active" || status === "Active"
      ? "ok"
      : status === "suspended" || status === "Suspended" || status === "guest"
        ? "warn"
        : "muted";
  return <span className={`mp-dash-chip mp-dash-chip--${tone}`}>{label ?? status}</span>;
}

export function DashboardPage() {
  const { t } = useLocale();
  const { setEnabledModules, refresh: refreshTenantModules } = useTenantModules();
  const { push } = useToast();
  const { session: authSession, isAuthenticated, isLoading: authLoading, login } = useAuth();

  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [tab, setTab] = useState<TabId>("overview");

  const [packs, setPacks] = useState<IndustryPack[]>([]);
  const [tenants, setTenants] = useState<PlatformTenant[]>([]);
  const [filterQ, setFilterQ] = useState("");
  const [filterStatus, setFilterStatus] = useState("");

  const [tenantName, setTenantName] = useState("Acme Hospital");
  const [tenantSlug, setTenantSlug] = useState("acme-hospital");
  const [tenantPack, setTenantPack] = useState("hospital");
  const [tenantTier, setTenantTier] = useState("professional");
  const [selectedTenantSlug, setSelectedTenantSlug] = useState("");
  const [moduleToActivate, setModuleToActivate] = useState("");

  const [localEmail, setLocalEmail] = useState("platform@demo.dev");
  const [localPassword, setLocalPassword] = useState("SecurePass123!");
  const [localTenant, setLocalTenant] = useState("platform-demo");
  const [draftReady, setDraftReady] = useState(false);
  const [lastAction, setLastAction] = useState<string | null>(null);
  const [pulse, setPulse] = useState<HomePulseResult | null>(null);
  const [pulseLoading, setPulseLoading] = useState(false);

  const session = authSession;

  const formDraft = useMemo(
    () => ({
      tab,
      filterQ,
      filterStatus,
      tenantName,
      tenantSlug,
      tenantPack,
      tenantTier,
      localEmail,
      localTenant,
    }),
    [
      filterQ,
      filterStatus,
      localEmail,
      localTenant,
      tab,
      tenantName,
      tenantPack,
      tenantSlug,
      tenantTier,
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
        if (
          parsed.tab === "overview" ||
          parsed.tab === "tenants" ||
          parsed.tab === "packs" ||
          parsed.tab === "launch"
        ) {
          setTab(parsed.tab);
        }
        if (typeof parsed.filterQ === "string") setFilterQ(parsed.filterQ);
        if (typeof parsed.filterStatus === "string") setFilterStatus(parsed.filterStatus);
        if (typeof parsed.tenantName === "string" && parsed.tenantName.trim()) {
          setTenantName(parsed.tenantName);
        }
        if (typeof parsed.tenantSlug === "string" && parsed.tenantSlug.trim()) {
          setTenantSlug(parsed.tenantSlug);
        }
        if (typeof parsed.tenantPack === "string" && parsed.tenantPack.trim()) {
          setTenantPack(parsed.tenantPack);
        }
        if (typeof parsed.tenantTier === "string" && parsed.tenantTier.trim()) {
          setTenantTier(parsed.tenantTier);
        }
        if (typeof parsed.localEmail === "string" && parsed.localEmail.trim()) {
          setLocalEmail(parsed.localEmail);
        }
        if (typeof parsed.localTenant === "string" && parsed.localTenant.trim()) {
          setLocalTenant(parsed.localTenant);
        }
      }
    } catch {
      /* ignore */
    } finally {
      setDraftReady(true);
    }
  }, []);

  const loadCatalog = useCallback(async () => {
    setProgress(35);
    const catalog = await fetchIndustryPacks();
    setPacks(catalog);
    setTenantPack((prev) => prev || catalog[0]?.pack_id || "hospital");
    setLastAction("catalog");
    setProgress(60);
    return catalog;
  }, []);

  const loadTenants = useCallback(async () => {
    if (!session) {
      setTenants([]);
      return;
    }
    setProgress(75);
    try {
      const list = await fetchPlatformTenants(session, { limit: 100, offset: 0 });
      setTenants(Array.isArray(list) ? list : []);
      setSelectedTenantSlug((prev) => {
        if (prev && list.some((x) => x.slug === prev)) return prev;
        return list[0]?.slug ?? "";
      });
    } catch (err) {
      setTenants([]);
      throw err;
    }
  }, [session]);

  const loadPulse = useCallback(async () => {
    if (!session) {
      setPulse(null);
      return;
    }
    setPulseLoading(true);
    try {
      const next = await fetchHomePulse(session);
      setPulse(next);
      setLastAction("pulse");
    } catch {
      setPulse(null);
    } finally {
      setPulseLoading(false);
    }
  }, [session]);

  const refreshAll = useCallback(async () => {
    setLoading(true);
    setError(null);
    setProgress(20);
    try {
      await loadCatalog();
      if (session) {
        // Parallel platform + pulse — faster home load
        const results = await Promise.allSettled([loadTenants(), loadPulse()]);
        const tenantFail = results[0];
        if (tenantFail.status === "rejected") {
          const err = tenantFail.reason;
          setError(
            err instanceof Error ? err.message : t("dashboard.tenantsLoadFailed"),
          );
        }
      } else {
        setPulse(null);
      }
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("dashboard.loadFailed"));
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [loadCatalog, loadPulse, loadTenants, session, t]);

  useEffect(() => {
    if (authLoading) return;
    void refreshAll();
  }, [authLoading, refreshAll]);

  const selectedTenant = useMemo(
    () => tenants.find((x) => x.slug === selectedTenantSlug) ?? null,
    [tenants, selectedTenantSlug],
  );

  const selectedPack = useMemo(
    () => packs.find((p) => p.pack_id === tenantPack) ?? null,
    [packs, tenantPack],
  );

  const activatableModules = useMemo(() => {
    if (!selectedTenant) return [];
    const pack = packs.find((p) => p.pack_id === selectedTenant.industry_pack);
    const enabled = new Set(selectedTenant.enabled_modules ?? []);
    const candidates = [
      ...(pack?.optional_modules ?? []),
      ...(pack?.required_modules ?? []),
    ];
    return [...new Set(candidates)].filter((m) => !enabled.has(m));
  }, [selectedTenant, packs]);

  useEffect(() => {
    if (!moduleToActivate && activatableModules[0]) {
      setModuleToActivate(activatableModules[0]);
    }
  }, [activatableModules, moduleToActivate]);

  const stats = useMemo(() => {
    const active = tenants.filter((x) => x.status === "active").length;
    const suspended = tenants.filter((x) => x.status === "suspended").length;
    const modules = tenants.reduce((n, x) => n + (x.enabled_modules?.length ?? 0), 0);
    const locked = !isAuthenticated;
    return [
      { label: t("dashboard.stat.packs"), value: packs.length, locked: false },
      {
        label: t("dashboard.stat.tenants"),
        value: locked ? "—" : tenants.length,
        locked,
      },
      {
        label: t("dashboard.stat.active"),
        value: locked ? "—" : active,
        locked,
      },
      {
        label: t("dashboard.stat.suspended"),
        value: locked ? "—" : suspended,
        locked,
      },
      {
        label: t("dashboard.stat.modules"),
        value: locked ? "—" : modules,
        locked,
      },
    ];
  }, [isAuthenticated, packs.length, tenants, t]);

  const pulseKpis = useMemo(() => {
    const unread = pulse?.unreadNotifications ?? 0;
    const tasks = pulse?.openTasks ?? 0;
    const audit24 = pulse?.auditStats?.last_24h ?? 0;
    const dashboards = pulse?.analytics?.dashboards_count ?? 0;
    return [
      {
        id: "notifications",
        label: t("dashboard.pulse.unread"),
        value: unread,
        href: "/enterprise/notifications",
        tone: unread > 0 ? ("warn" as const) : ("ok" as const),
      },
      {
        id: "workflow",
        label: t("dashboard.pulse.tasks"),
        value: tasks,
        href: "/enterprise/workflows",
        tone: tasks > 0 ? ("warn" as const) : ("default" as const),
      },
      {
        id: "audit",
        label: t("dashboard.pulse.audit24h"),
        value: audit24,
        href: "/enterprise/audit",
        tone: "default" as const,
      },
      {
        id: "analytics",
        label: t("dashboard.pulse.dashboards"),
        value: dashboards,
        href: "/banking/analytics",
        tone: "default" as const,
      },
    ];
  }, [pulse, t]);

  const filteredTenants = useMemo(() => {
    const q = filterQ.toLowerCase().trim();
    return tenants.filter((x) => {
      if (filterStatus && x.status !== filterStatus) return false;
      if (!q) return true;
      return (
        x.name.toLowerCase().includes(q) ||
        x.slug.toLowerCase().includes(q) ||
        x.industry_pack.toLowerCase().includes(q)
      );
    });
  }, [tenants, filterQ, filterStatus]);

  const filteredPacks = useMemo(() => {
    const q = filterQ.toLowerCase().trim();
    if (!q) return packs;
    return packs.filter(
      (p) =>
        p.pack_id.includes(q) ||
        p.display_name.toLowerCase().includes(q) ||
        p.description.toLowerCase().includes(q),
    );
  }, [packs, filterQ]);

  const exportRows = useMemo(
    () =>
      filteredTenants.map((x) => ({
        slug: x.slug,
        name: x.name,
        pack: x.industry_pack,
        tier: x.tier,
        status: x.status,
        modules: (x.enabled_modules ?? []).join("|"),
      })),
    [filteredTenants],
  );

  const tabs: { id: TabId; label: string }[] = [
    { id: "overview", label: t("dashboard.tab.overview") },
    { id: "tenants", label: t("dashboard.tab.tenants") },
    { id: "packs", label: t("dashboard.tab.packs") },
    { id: "launch", label: t("dashboard.tab.launch") },
  ];

  const lifecycleStep = useMemo(() => {
    if (tenants.length > 0 && isAuthenticated) return 3;
    if (isAuthenticated && packs.length > 0) return 2;
    if (packs.length > 0) return 1;
    return 0;
  }, [isAuthenticated, packs.length, tenants.length]);

  const workflowSteps = useMemo(
    () => [
      t("dashboard.step.signIn"),
      t("dashboard.step.catalog"),
      t("dashboard.step.provision"),
      t("dashboard.step.operate"),
    ],
    [t],
  );

  async function onLocalSignIn() {
    setBusy(true);
    setError(null);
    try {
      await login({
        tenantId: localTenant,
        email: localEmail,
        password: localPassword,
        displayName: "Platform Admin",
        registerIfMissing: true,
      });
      setLastAction("signIn");
      push({ message: t("dashboard.signedIn") });
    } catch (err) {
      setError(err instanceof Error ? err.message : t("dashboard.signInFailed"));
    } finally {
      setBusy(false);
    }
  }

  async function onProvision() {
    setBusy(true);
    setError(null);
    try {
      const created = await provisionPlatformTenant(session, {
        name: tenantName,
        slug: tenantSlug,
        industry_pack: tenantPack,
        tier: tenantTier,
        optional_modules: selectedPack?.optional_modules?.slice(0, 1) ?? [],
      });
      push({ message: `${t("dashboard.tenantProvisioned")}: ${created.slug}` });
      setSelectedTenantSlug(created.slug);
      setTab("tenants");
      setLastAction("provision");
      if (session) await loadTenants();
      else setTenants((prev) => [created, ...prev.filter((x) => x.slug !== created.slug)]);
    } catch (err) {
      const msg = err instanceof Error ? err.message : t("dashboard.provisionFailed");
      setError(msg);
      push({ message: msg });
    } finally {
      setBusy(false);
    }
  }

  async function onActivateModule() {
    if (!session || !selectedTenantSlug || !moduleToActivate) return;
    setBusy(true);
    try {
      const updated = await activatePlatformModule(session, selectedTenantSlug, moduleToActivate);
      push({ message: `${t("dashboard.moduleActivated")}: ${moduleToActivate}` });
      setTenants((prev) => prev.map((x) => (x.slug === updated.slug ? updated : x)));
      setEnabledModules(updated.slug, updated.enabled_modules ?? [], {
        name: updated.name,
        industryPack: updated.industry_pack,
      });
      await refreshTenantModules();
      setModuleToActivate("");
      setLastAction("activate");
    } catch (err) {
      push({
        message: err instanceof Error ? err.message : t("dashboard.activateFailed"),
      });
    } finally {
      setBusy(false);
    }
  }

  async function onSuspend() {
    if (!session || !selectedTenantSlug) return;
    setBusy(true);
    try {
      const updated = await suspendPlatformTenant(session, selectedTenantSlug);
      push({
        message: `${t("dashboard.tenantSuspended")}: ${updated.slug}`,
        onUndo: undefined,
      });
      setTenants((prev) => prev.map((x) => (x.slug === updated.slug ? updated : x)));
    } catch (err) {
      push({
        message: err instanceof Error ? err.message : t("dashboard.suspendFailed"),
      });
    } finally {
      setBusy(false);
    }
  }

  return (
    <PageLayout
      title={t("demo.title")}
      subtitle={t("dashboard.subtitle")}
      breadcrumb={[
        { label: t("app.name"), href: "/" },
        { label: t("demo.title") },
      ]}
      actions={
        <>
          <ExportButton label={t("common.export")} rows={exportRows} filename="platform-tenants.csv" />
          <PrintButton label={t("common.print")} />
          <button
            type="button"
            className="mp-btn"
            disabled={loading || busy || authLoading}
            onClick={() => void refreshAll()}
          >
            {t("common.refresh")}
          </button>
          {!isAuthenticated ? (
            <Link href="/login?returnTo=/" className="mp-btn">
              {t("dashboard.openLogin")}
            </Link>
          ) : null}
        </>
      }
    >
      <ProgressBar
        value={progress}
        label={loading || authLoading ? t("dashboard.loading") : t("dashboard.ready")}
      />

      {error ? (
        <p className="mp-dash-alert" role="alert">
          {error}
        </p>
      ) : null}

      {!isAuthenticated && !authLoading ? (
        <section
          id="dash-session"
          className="mp-dash-session"
          aria-label={t("dashboard.session")}
        >
          <div className="mp-dash-session-banner">
            <h2>{t("dashboard.sessionHint")}</h2>
            <p>{t("dashboard.sessionHelp")}</p>
          </div>
          <div className="mp-dash-session-body">
            <div className="mp-form mp-dash-form-grid">
              <div className="mp-field">
                <label htmlFor="dash-tenant">{t("dashboard.tenant")}</label>
                <input
                  id="dash-tenant"
                  className="mp-input"
                  value={localTenant}
                  onChange={(e) => setLocalTenant(e.target.value)}
                />
              </div>
              <div className="mp-field">
                <label htmlFor="dash-email">{t("dashboard.email")}</label>
                <input
                  id="dash-email"
                  className="mp-input"
                  type="email"
                  value={localEmail}
                  onChange={(e) => setLocalEmail(e.target.value)}
                />
              </div>
              <div className="mp-field">
                <label htmlFor="dash-password">{t("dashboard.password")}</label>
                <input
                  id="dash-password"
                  className="mp-input"
                  type="password"
                  value={localPassword}
                  onChange={(e) => setLocalPassword(e.target.value)}
                />
              </div>
            </div>
            <div className="mp-dash-actions">
              <button
                type="button"
                className="mp-btn mp-btn-primary"
                disabled={busy}
                onClick={() => void onLocalSignIn()}
              >
                {t("dashboard.signIn")}
              </button>
              <Link href="/login?returnTo=/" className="mp-btn">
                {t("dashboard.openLogin")}
              </Link>
            </div>
          </div>
        </section>
      ) : null}

      {loading || authLoading ? (
        <SkeletonTable rows={5} cols={4} />
      ) : (
        <div className="mp-dash-layout">
          <aside className="mp-dash-aside" aria-label={t("dashboard.rail")}>
            <section className="mp-dash-panel-card">
              <header className="mp-dash-panel-head mp-dash-jewel-bar--royal">
                <h2>{t("dashboard.workflow")}</h2>
              </header>
              <div className="mp-dash-panel-body">
                <StepProgress steps={workflowSteps} current={lifecycleStep} />
                {draftSaving ? (
                  <p className="mp-field-help" aria-live="polite">
                    {t("dashboard.draftSaved")}…
                  </p>
                ) : (
                  <p className="mp-field-help">{t("dashboard.workflowHint")}</p>
                )}
                {lastAction ? (
                  <p className="mp-field-help">
                    {t("dashboard.lastAction")}: {lastAction}
                  </p>
                ) : null}
              </div>
            </section>

            <section className="mp-dash-panel-card mp-dash-status-card">
              <header className="mp-dash-panel-head mp-dash-jewel-bar--forest">
                <h2>{t("dashboard.rail.status")}</h2>
              </header>
              <div className="mp-dash-panel-body">
                <div className="mp-dash-status-row">
                  <span className="mp-dash-status-label">{t("dashboard.session")}</span>
                  <StatusChip
                    status={isAuthenticated ? "active" : "guest"}
                    label={
                      isAuthenticated
                        ? t("dashboard.rail.signedIn")
                        : t("dashboard.rail.guest")
                    }
                  />
                </div>
                <div className="mp-dash-status-row">
                  <span className="mp-dash-status-label">{t("dashboard.stat.packs")}</span>
                  <strong>{packs.length}</strong>
                </div>
                <div className="mp-dash-status-row">
                  <span className="mp-dash-status-label">{t("dashboard.stat.tenants")}</span>
                  <strong>{isAuthenticated ? tenants.length : "—"}</strong>
                </div>
                {isAuthenticated && session ? (
                  <p className="mp-field-help mp-dash-status-hint">
                    {session.tenantId}
                  </p>
                ) : (
                  <p className="mp-field-help">{t("dashboard.authRequiredOps")}</p>
                )}
                <div className="mp-dash-actions">
                  {!isAuthenticated ? (
                    <a href="#dash-session" className="mp-btn mp-btn-primary">
                      {t("dashboard.signIn")}
                    </a>
                  ) : (
                    <Link href="/modules" className="mp-btn mp-btn-primary">
                      {t("modules.title")}
                    </Link>
                  )}
                  <button
                    type="button"
                    className="mp-btn"
                    disabled={loading || busy}
                    onClick={() => void refreshAll()}
                  >
                    {t("common.refresh")}
                  </button>
                </div>
              </div>
            </section>

            <section className="mp-dash-panel-card">
              <header className="mp-dash-panel-head mp-dash-jewel-bar--emerald">
                <h2>{t("dashboard.rail.shortcuts")}</h2>
              </header>
              <div className="mp-dash-panel-body mp-dash-panel-body--tight">
                <ul className="mp-dash-rail-launch">
                  {PLATFORM_LAUNCH_LINKS.slice(0, 6).map((link) => {
                    const jewel = LAUNCH_JEWELS[link.id] ?? "silver";
                    return (
                      <li key={link.id}>
                        <Link href={link.href} className="mp-dash-rail-link">
                          <span
                            className={`mp-dash-icon mp-dash-icon--sm mp-dash-jewel--${jewel}`}
                            aria-hidden
                          >
                            {packInitials(t(link.labelKey))}
                          </span>
                          <span>{t(link.labelKey)}</span>
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              </div>
            </section>

            {selectedPack ? (
              <section className="mp-dash-panel-card">
                <header className="mp-dash-panel-head mp-dash-jewel-bar--gold">
                  <h2>{t("dashboard.rail.packFocus")}</h2>
                </header>
                <div className="mp-dash-panel-body">
                  <div className="mp-dash-pack-focus">
                    <span
                      className={`mp-dash-icon mp-dash-jewel--${jewelForPack(selectedPack.pack_id, 0)}`}
                      aria-hidden
                    >
                      {packInitials(selectedPack.display_name)}
                    </span>
                    <div className="mp-dash-pack-text">
                      <strong>{selectedPack.display_name}</strong>
                      <span>{selectedPack.pack_id}</span>
                    </div>
                  </div>
                  <p className="mp-dash-pack-desc">
                    {selectedPack.description || t("dashboard.rail.packFocusHint")}
                  </p>
                  <div className="mp-dash-chip-row">
                    <span className="mp-dash-chip mp-dash-chip--ok">
                      {selectedPack.required_modules.length} {t("dashboard.requiredModules")}
                    </span>
                    <span className="mp-dash-chip">
                      {selectedPack.optional_modules.length} {t("dashboard.optionalModules")}
                    </span>
                  </div>
                  {(selectedPack.compliance_frameworks ?? []).length > 0 ? (
                    <p className="mp-field-help">
                      {t("dashboard.compliance")}:{" "}
                      {(selectedPack.compliance_frameworks ?? []).slice(0, 3).join(", ")}
                    </p>
                  ) : null}
                  <button
                    type="button"
                    className="mp-btn"
                    onClick={() => setTab("packs")}
                  >
                    {t("dashboard.tab.packs")}
                  </button>
                </div>
              </section>
            ) : null}

            {isAuthenticated ? (
              <>
            <section className="mp-dash-panel-card">
              <header className="mp-dash-panel-head mp-dash-jewel-bar--forest">
                <h2>{t("dashboard.provision")}</h2>
              </header>
              <div className="mp-dash-panel-body">
                <div className="mp-form mp-dash-form-stack">
                  <div className="mp-field">
                    <label htmlFor="prov-name">{t("dashboard.field.name")}</label>
                    <input
                      id="prov-name"
                      className="mp-input"
                      value={tenantName}
                      onChange={(e) => setTenantName(e.target.value)}
                    />
                  </div>
                  <div className="mp-field">
                    <label htmlFor="prov-slug">{t("dashboard.field.slug")}</label>
                    <input
                      id="prov-slug"
                      className="mp-input"
                      value={tenantSlug}
                      onChange={(e) => setTenantSlug(e.target.value)}
                      pattern="^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$"
                    />
                  </div>
                  <div className="mp-field">
                    <label htmlFor="prov-pack">{t("dashboard.field.pack")}</label>
                    <select
                      id="prov-pack"
                      className="mp-select"
                      value={tenantPack}
                      onChange={(e) => setTenantPack(e.target.value)}
                    >
                      {packs.map((p) => (
                        <option key={p.pack_id} value={p.pack_id}>
                          {p.display_name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="mp-field">
                    <label htmlFor="prov-tier">{t("dashboard.field.tier")}</label>
                    <select
                      id="prov-tier"
                      className="mp-select"
                      value={tenantTier}
                      onChange={(e) => setTenantTier(e.target.value)}
                    >
                      <option value="starter">starter</option>
                      <option value="professional">professional</option>
                      <option value="enterprise">enterprise</option>
                    </select>
                  </div>
                </div>
                <button
                  type="button"
                  className="mp-btn mp-btn-primary"
                  disabled={busy || !tenantName || !tenantSlug || !tenantPack}
                  onClick={() => void onProvision()}
                >
                  {t("dashboard.provision")}
                </button>
              </div>
            </section>

            <section className="mp-dash-panel-card">
              <header className="mp-dash-panel-head mp-dash-jewel-bar--royal">
                <h2>{t("dashboard.moduleOps")}</h2>
              </header>
              <div className="mp-dash-panel-body">
                <div className="mp-form mp-dash-form-stack">
                  <div className="mp-field">
                    <label htmlFor="mod-tenant">{t("dashboard.field.tenant")}</label>
                    <select
                      id="mod-tenant"
                      className="mp-select"
                      value={selectedTenantSlug}
                      onChange={(e) => setSelectedTenantSlug(e.target.value)}
                      disabled={!tenants.length}
                    >
                      <option value="">—</option>
                      {tenants.map((x) => (
                        <option key={x.slug} value={x.slug}>
                          {x.name} ({x.slug})
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="mp-field">
                    <label htmlFor="mod-id">{t("dashboard.field.module")}</label>
                    <select
                      id="mod-id"
                      className="mp-select"
                      value={moduleToActivate}
                      onChange={(e) => setModuleToActivate(e.target.value)}
                      disabled={!activatableModules.length}
                    >
                      <option value="">—</option>
                      {activatableModules.map((m) => (
                        <option key={m} value={m}>
                          {m}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
                <div className="mp-dash-actions">
                  <button
                    type="button"
                    className="mp-btn"
                    disabled={busy || !isAuthenticated || !moduleToActivate}
                    onClick={() => void onActivateModule()}
                  >
                    {t("dashboard.activateModule")}
                  </button>
                  <button
                    type="button"
                    className="mp-btn mp-btn-danger"
                    disabled={
                      busy ||
                      !isAuthenticated ||
                      !selectedTenant ||
                      selectedTenant.status === "suspended"
                    }
                    onClick={() => void onSuspend()}
                  >
                    {t("dashboard.suspend")}
                  </button>
                </div>
              </div>
            </section>
              </>
            ) : null}
          </aside>

          <div className="mp-dash-main">
            <section className="mp-dash-metrics" aria-label={t("dashboard.metrics")} aria-live="polite">
              {stats.map((s, i) => {
                const jewel = METRIC_JEWELS[i % METRIC_JEWELS.length]!;
                return (
                  <div
                    key={s.label}
                    className={`mp-dash-metric mp-dash-metric--${jewel}${s.locked ? " mp-dash-metric--locked" : ""}`}
                    title={s.locked ? t("dashboard.authRequiredOps") : undefined}
                  >
                    <span className="mp-dash-metric-label">{s.label}</span>
                    <strong aria-label={s.locked ? t("dashboard.authRequiredOps") : undefined}>
                      {s.value}
                    </strong>
                  </div>
                );
              })}
            </section>

            {isAuthenticated ? (
              <section
                className="mp-dash-panel-card mp-dash-pulse"
                aria-labelledby="dash-pulse-title"
                aria-busy={pulseLoading || undefined}
              >
                <header className="mp-dash-panel-head mp-dash-jewel-bar--royal">
                  <h2 id="dash-pulse-title">{t("dashboard.pulse.title")}</h2>
                </header>
                <div className="mp-dash-panel-body">
                  <p className="mp-field-help">{t("dashboard.pulse.hint")}</p>
                  <KpiStrip
                    label={t("dashboard.pulse.title")}
                    loading={pulseLoading && !pulse}
                    items={pulseKpis}
                  />
                  {homePulseHasPartialErrors(pulse) ? (
                    <p className="mp-field-help" role="status">
                      {t("dashboard.pulse.partial")}
                    </p>
                  ) : null}
                  {pulse && pulse.recentAudit.length > 0 ? (
                    <div className="mp-dash-pulse-feed" aria-label={t("dashboard.pulse.recentAudit")}>
                      <h3 className="mp-dash-pulse-feed-title">{t("dashboard.pulse.recentAudit")}</h3>
                      <ul className="mp-dash-pulse-list">
                        {pulse.recentAudit.map((entry) => (
                          <li key={entry.id}>
                            <Link href="/enterprise/audit">{entry.event_name || entry.action}</Link>
                            <span className="mp-field-help">
                              {entry.source_context} · {entry.severity}
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : null}
                  {pulse && pulse.recentTasks.length > 0 ? (
                    <div className="mp-dash-pulse-feed" aria-label={t("dashboard.pulse.recentTasks")}>
                      <h3 className="mp-dash-pulse-feed-title">{t("dashboard.pulse.recentTasks")}</h3>
                      <ul className="mp-dash-pulse-list">
                        {pulse.recentTasks.map((task) => (
                          <li key={task.id}>
                            <Link href="/enterprise/workflows">
                              {task.title || task.id}
                            </Link>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : null}
                  {!pulseLoading && !pulse ? (
                    <EmptyState
                      title={t("dashboard.pulse.empty")}
                      description={t("dashboard.pulse.emptyHint")}
                    />
                  ) : null}
                </div>
              </section>
            ) : null}

            <AdvancedFilterBar
              filters={[
                { id: "q", label: t("common.filter"), type: "text" },
                { id: "status", label: t("dashboard.field.status"), type: "text" },
              ]}
              onChange={(values) => {
                setFilterQ(values.q ?? "");
                setFilterStatus((values.status ?? "").toLowerCase().trim());
              }}
            />

            <div className="mp-dash-tabs" role="tablist" aria-label={t("demo.title")}>
              {tabs.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  role="tab"
                  id={`dash-tab-${item.id}`}
                  aria-selected={tab === item.id}
                  aria-controls={`dash-panel-${item.id}`}
                  className={`mp-dash-tab ${tab === item.id ? "mp-dash-tab--on" : ""}`}
                  onClick={() => setTab(item.id)}
                >
                  {item.label}
                </button>
              ))}
            </div>

            <div
              role="tabpanel"
              id={`dash-panel-${tab}`}
              aria-labelledby={`dash-tab-${tab}`}
              className="mp-dash-panel mp-animate-in"
            >
              {tab === "overview" ? (
                <div className="mp-dash-overview">
                  <section aria-labelledby="dash-overview-tenants">
                    <h2 id="dash-overview-tenants">{t("dashboard.recentTenants")}</h2>
                    {filteredTenants.length === 0 ? (
                      <EmptyState
                        title={t("dashboard.noTenants")}
                        description={t("dashboard.noTenantsHint")}
                        action={
                          <button
                            type="button"
                            className="mp-btn mp-btn-primary"
                            onClick={() => void onProvision()}
                          >
                            {t("dashboard.provision")}
                          </button>
                        }
                      />
                    ) : (
                      <DataTable
                        columns={[
                          { key: "name", header: t("dashboard.field.name"), sortable: true },
                          { key: "slug", header: t("dashboard.field.slug"), sortable: true },
                          { key: "pack", header: t("dashboard.field.pack"), sortable: true },
                          {
                            key: "status",
                            header: t("dashboard.field.status"),
                            sortable: true,
                            render: (row) => <StatusChip status={String(row.status)} />,
                          },
                          { key: "modules", header: t("dashboard.stat.modules"), sortable: true },
                        ]}
                        rows={filteredTenants.slice(0, 8).map((x) => ({
                          id: x.slug,
                          name: x.name,
                          slug: x.slug,
                          pack: x.industry_pack,
                          status: x.status,
                          modules: String(x.enabled_modules?.length ?? 0),
                        }))}
                        selectable
                        onSelectionChange={(ids) => {
                          if (ids[0]) setSelectedTenantSlug(ids[0]);
                        }}
                      />
                    )}
                  </section>
                  <section aria-labelledby="dash-overview-packs">
                    <h2 id="dash-overview-packs">{t("dashboard.featuredPacks")}</h2>
                    <ul className="mp-dash-pack-list">
                      {packs.slice(0, 8).map((p, index) => {
                        const jewel = jewelForPack(p.pack_id, index);
                        return (
                          <li key={p.pack_id}>
                            <button
                              type="button"
                              className="mp-dash-pack-item"
                              onClick={() => {
                                setTenantPack(p.pack_id);
                                setTab("packs");
                              }}
                            >
                              <span
                                className={`mp-dash-icon mp-dash-jewel--${jewel}`}
                                aria-hidden
                              >
                                {packInitials(p.display_name)}
                              </span>
                              <span className="mp-dash-pack-text">
                                <strong>{p.display_name}</strong>
                                <span>{p.pack_id}</span>
                                <span className="mp-field-help">
                                  {p.required_modules.length}+{p.optional_modules.length} modules
                                </span>
                              </span>
                            </button>
                          </li>
                        );
                      })}
                    </ul>
                  </section>
                </div>
              ) : null}

              {tab === "tenants" ? (
                filteredTenants.length === 0 ? (
                  <EmptyState
                    title={t("dashboard.noTenants")}
                    description={
                      isAuthenticated
                        ? t("dashboard.noTenantsHint")
                        : t("dashboard.authRequiredOps")
                    }
                  />
                ) : (
                  <DataTable
                    columns={[
                      { key: "name", header: t("dashboard.field.name"), sortable: true },
                      { key: "slug", header: t("dashboard.field.slug"), sortable: true },
                      { key: "pack", header: t("dashboard.field.pack"), sortable: true },
                      { key: "tier", header: t("dashboard.field.tier"), sortable: true },
                      {
                        key: "status",
                        header: t("dashboard.field.status"),
                        sortable: true,
                        render: (row) => <StatusChip status={String(row.status)} />,
                      },
                      { key: "modules", header: t("dashboard.stat.modules"), sortable: true },
                      { key: "updated", header: t("dashboard.field.updated"), sortable: true },
                    ]}
                    rows={filteredTenants.map((x) => ({
                      id: x.slug,
                      name: x.name,
                      slug: x.slug,
                      pack: x.industry_pack,
                      tier: x.tier,
                      status: x.status,
                      modules: String(x.enabled_modules?.length ?? 0),
                      updated: x.updated_at?.slice(0, 10) ?? "—",
                    }))}
                    selectable
                    onSelectionChange={(ids) => {
                      if (ids[0]) setSelectedTenantSlug(ids[0]);
                    }}
                  />
                )
              ) : null}

              {tab === "packs" ? (
                filteredPacks.length === 0 ? (
                  <EmptyState title={t("demo.empty")} description={t("common.filter")} />
                ) : (
                  <DataTable
                    columns={[
                      { key: "pack_id", header: "ID", sortable: true },
                      { key: "display_name", header: t("dashboard.field.name"), sortable: true },
                      { key: "required", header: t("dashboard.requiredModules"), sortable: true },
                      { key: "optional", header: t("dashboard.optionalModules"), sortable: true },
                      { key: "locale", header: "Locale", sortable: true },
                      { key: "compliance", header: t("dashboard.compliance") },
                    ]}
                    rows={filteredPacks.map((p) => ({
                      id: p.pack_id,
                      pack_id: p.pack_id,
                      display_name: p.display_name,
                      required: String(p.required_modules.length),
                      optional: String(p.optional_modules.length),
                      locale: p.default_locale,
                      compliance: (p.compliance_frameworks ?? []).join(", ") || "—",
                    }))}
                    selectable
                    onSelectionChange={(ids) => {
                      if (ids[0]) setTenantPack(ids[0]);
                    }}
                  />
                )
              ) : null}

              {tab === "launch" ? (
                <ul className="mp-dash-launch" aria-label={t("dashboard.tab.launch")}>
                  {PLATFORM_LAUNCH_LINKS.map((link) => {
                    const jewel = LAUNCH_JEWELS[link.id] ?? "silver";
                    return (
                      <li key={link.id}>
                        <Link href={link.href} className="mp-dash-launch-item">
                          <span
                            className={`mp-dash-icon mp-dash-jewel--${jewel}`}
                            aria-hidden
                          >
                            {packInitials(t(link.labelKey))}
                          </span>
                          <span className="mp-dash-pack-text">
                            <strong>{t(link.labelKey)}</strong>
                            <span className="mp-field-help">{link.href}</span>
                          </span>
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              ) : null}
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        .mp-dash-layout {
          display: grid;
          grid-template-columns: minmax(300px, 340px) minmax(0, 1fr);
          gap: 1.25rem 1.5rem;
          align-items: start;
        }
        .mp-dash-aside,
        .mp-dash-main {
          display: flex;
          flex-direction: column;
          gap: 0.85rem;
          min-width: 0;
        }
        .mp-dash-aside {
          position: sticky;
          top: 4.5rem;
          align-self: start;
          max-height: calc(100vh - 5.5rem);
          overflow: auto;
          padding-inline-end: 0.15rem;
          scrollbar-gutter: stable;
        }
        /* Vertical lifecycle steps — horizontal wrap was crushing the narrow rail */
        .mp-dash-aside :global(.mp-step-progress) {
          display: flex;
          flex-direction: column;
          flex-wrap: nowrap;
          align-items: stretch;
          gap: 0.4rem;
          margin-block-end: 0.65rem;
        }
        .mp-dash-aside :global(.mp-step-progress li) {
          width: 100%;
          box-sizing: border-box;
          padding: 0.4rem 0.5rem;
          border-radius: var(--mp-radius-sm);
          background: color-mix(in srgb, var(--mp-bg-muted) 65%, transparent);
        }
        .mp-dash-aside :global(.mp-step-active) {
          background: color-mix(in srgb, var(--mp-forest) 10%, transparent);
        }
        .mp-dash-aside :global(.mp-step-index) {
          flex-shrink: 0;
        }
        .mp-dash-session {
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius);
          overflow: hidden;
          background: var(--mp-bg-elevated);
          box-shadow: var(--mp-shadow);
          margin-block-end: 1rem;
        }
        .mp-dash-session-banner {
          background: var(--mp-forest);
          color: var(--mp-fg-on-brand);
          padding: 1rem 1.15rem;
          box-shadow: inset 0 -2px 0 var(--mp-gold-soft);
        }
        .mp-dash-session-banner h2 {
          margin: 0 0 0.35rem;
          font-size: 1rem;
          font-weight: 600;
        }
        .mp-dash-session-banner p {
          margin: 0;
          opacity: 0.88;
          font-size: 0.88rem;
        }
        .mp-dash-session-body {
          padding: 1rem 1.15rem 1.15rem;
        }
        .mp-dash-panel-card {
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius);
          background: var(--mp-bg-elevated);
          box-shadow: none;
          overflow: hidden;
        }
        .mp-dash-aside .mp-dash-panel-card {
          box-shadow: 0 1px 2px rgb(20 24 32 / 4%);
        }
        .mp-dash-panel-head {
          padding: 0.55rem 0.85rem;
          color: var(--mp-fg);
          background: var(--mp-bg-subtle, var(--mp-bg-muted));
          border-block-end: 2px solid var(--mp-gold);
        }
        .mp-dash-panel-head h2 {
          margin: 0;
          font-size: 0.72rem;
          letter-spacing: 0.06em;
          text-transform: uppercase;
          font-weight: 650;
          color: var(--mp-fg);
        }
        /* Calm rail headers — gold accent only (no rainbow blocks). */
        .mp-dash-aside .mp-dash-jewel-bar--forest,
        .mp-dash-aside .mp-dash-jewel-bar--royal,
        .mp-dash-aside .mp-dash-jewel-bar--emerald,
        .mp-dash-aside .mp-dash-jewel-bar--gold {
          background: var(--mp-bg-subtle, var(--mp-bg-muted));
          color: var(--mp-fg);
          box-shadow: none;
        }
        .mp-dash-aside .mp-dash-jewel-bar--gold h2,
        .mp-dash-aside .mp-dash-panel-head h2 {
          color: var(--mp-fg);
        }
        .mp-dash-jewel-bar--forest {
          background: linear-gradient(120deg, var(--mp-forest), #2f5a48);
          box-shadow: inset 0 -2px 0 var(--mp-gold-soft);
          color: #fff;
        }
        .mp-dash-jewel-bar--royal {
          background: linear-gradient(120deg, var(--mp-royal), var(--mp-royal-bright));
          box-shadow: inset 0 -2px 0 var(--mp-gold-soft);
          color: #fff;
        }
        .mp-dash-jewel-bar--emerald {
          background: linear-gradient(120deg, var(--mp-emerald), var(--mp-emerald-bright));
          box-shadow: inset 0 -2px 0 var(--mp-gold-soft);
          color: #fff;
        }
        .mp-dash-jewel-bar--gold {
          background: linear-gradient(120deg, var(--mp-gold), var(--mp-gold-soft));
          color: #1a1a1a;
          box-shadow: inset 0 -2px 0 rgba(0, 0, 0, 0.12);
        }
        .mp-dash-jewel-bar--gold h2 {
          color: #1a1a1a;
        }
        .mp-dash-panel-body {
          padding: 0.85rem;
        }
        .mp-dash-panel-body--tight {
          padding: 0.5rem 0.55rem;
        }
        .mp-dash-form-grid {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 0.65rem 0.75rem;
          margin-block-end: 0.75rem;
        }
        @media (max-width: 720px) {
          .mp-dash-form-grid {
            grid-template-columns: 1fr;
          }
        }
        .mp-dash-form-stack {
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
          margin-block-end: 0.85rem;
        }
        .mp-dash-actions {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .mp-dash-status-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 0.75rem;
          padding: 0.35rem 0;
          border-block-end: 1px solid var(--mp-border);
        }
        .mp-dash-status-row:last-of-type {
          border-block-end: none;
          margin-block-end: 0.35rem;
        }
        .mp-dash-status-label {
          font-size: 0.8rem;
          color: var(--mp-fg-muted);
        }
        .mp-dash-status-row strong {
          font-size: 1.05rem;
          color: var(--mp-forest);
        }
        .mp-dash-status-hint {
          margin: 0.35rem 0 0.65rem;
          word-break: break-all;
        }
        .mp-dash-rail-launch {
          list-style: none;
          margin: 0;
          padding: 0;
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }
        .mp-dash-rail-link {
          display: flex;
          align-items: center;
          gap: 0.65rem;
          padding: 0.45rem 0.5rem;
          border-radius: var(--mp-radius-sm);
          text-decoration: none;
          color: var(--mp-fg);
          font-size: 0.86rem;
          font-weight: 500;
          transition: background var(--mp-transition);
        }
        .mp-dash-rail-link:hover {
          background: color-mix(in srgb, var(--mp-forest) 8%, transparent);
        }
        .mp-dash-icon--sm {
          width: 1.85rem;
          height: 1.85rem;
          font-size: 0.62rem;
          border-radius: 0.4rem;
        }
        .mp-dash-pack-focus {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-block-end: 0.65rem;
        }
        .mp-dash-pack-desc {
          margin: 0 0 0.65rem;
          font-size: 0.84rem;
          color: var(--mp-fg-muted);
          line-height: 1.45;
        }
        .mp-dash-chip-row {
          display: flex;
          flex-wrap: wrap;
          gap: 0.35rem;
          margin-block-end: 0.75rem;
        }
        .mp-dash-metrics {
          display: grid;
          grid-template-columns: repeat(5, minmax(0, 1fr));
          gap: 0.65rem;
        }
        .mp-dash-metric {
          padding: 0.85rem 0.9rem;
          border-radius: var(--mp-radius);
          background: var(--mp-bg-elevated);
          border: 1px solid var(--mp-border);
          border-block-start: 3px solid var(--mp-silver);
          box-shadow: var(--mp-shadow);
        }
        .mp-dash-metric--locked {
          opacity: 0.72;
        }
        .mp-dash-metric--locked strong {
          color: var(--mp-fg-muted);
          font-weight: 600;
        }
        .mp-dash-metric--forest {
          border-block-start-color: var(--mp-forest);
        }
        .mp-dash-metric--royal {
          border-block-start-color: var(--mp-royal);
        }
        .mp-dash-metric--emerald {
          border-block-start-color: var(--mp-emerald);
        }
        .mp-dash-metric--gold {
          border-block-start-color: var(--mp-gold);
        }
        .mp-dash-metric--orange {
          border-block-start-color: var(--mp-orange);
        }
        .mp-dash-metric strong {
          display: block;
          font-size: 1.35rem;
          line-height: 1.2;
          color: var(--mp-fg);
        }
        .mp-dash-metric--forest strong {
          color: var(--mp-forest);
        }
        .mp-dash-metric--royal strong {
          color: var(--mp-royal);
        }
        .mp-dash-metric--emerald strong {
          color: var(--mp-emerald);
        }
        .mp-dash-metric--gold strong {
          color: var(--mp-gold);
        }
        .mp-dash-metric--orange strong {
          color: var(--mp-orange);
        }
        .mp-dash-metric-label {
          display: block;
          color: var(--mp-fg-muted);
          font-size: 0.72rem;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          margin-block-end: 0.25rem;
        }
        .mp-dash-tabs {
          display: flex;
          flex-wrap: wrap;
          gap: 0.4rem;
        }
        .mp-dash-tab {
          border: 1px solid var(--mp-border);
          background: var(--mp-bg-elevated);
          color: var(--mp-fg-muted);
          border-radius: 999px;
          padding: 0.35rem 0.85rem;
          font-size: 0.82rem;
          cursor: pointer;
          transition: background var(--mp-transition), color var(--mp-transition),
            border-color var(--mp-transition);
        }
        .mp-dash-tab--on {
          background: var(--mp-forest);
          border-color: var(--mp-forest);
          color: #fff;
          box-shadow: inset 0 -1px 0 var(--mp-gold-soft);
        }
        .mp-dash-overview {
          display: grid;
          gap: 1.25rem;
        }
        .mp-dash-overview h2 {
          margin: 0 0 0.75rem;
          font-size: 0.85rem;
          letter-spacing: 0.06em;
          text-transform: uppercase;
          color: var(--mp-fg-muted);
          font-weight: 600;
          padding-block-end: 0.35rem;
          border-block-end: 1px solid var(--mp-border);
        }
        .mp-dash-pack-list,
        .mp-dash-launch {
          list-style: none;
          margin: 0;
          padding: 0;
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr));
          gap: 0.65rem;
        }
        .mp-dash-pack-item,
        .mp-dash-launch-item {
          display: flex;
          flex-direction: row;
          align-items: center;
          gap: 0.75rem;
          width: 100%;
          padding: 0.75rem 0.85rem;
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius);
          background: var(--mp-bg-elevated);
          box-shadow: var(--mp-shadow);
          text-align: start;
          text-decoration: none;
          color: inherit;
          cursor: pointer;
          transition:
            border-color var(--mp-transition),
            transform var(--mp-transition);
        }
        .mp-dash-pack-item:hover,
        .mp-dash-launch-item:hover {
          border-color: var(--mp-gold);
          transform: translateY(-1px);
        }
        .mp-dash-icon {
          display: grid;
          place-items: center;
          width: 2.5rem;
          height: 2.5rem;
          border-radius: 0.5rem;
          font-size: 0.78rem;
          font-weight: 700;
          letter-spacing: 0.04em;
          color: #fff;
          flex-shrink: 0;
        }
        .mp-dash-jewel--royal {
          background: linear-gradient(145deg, var(--mp-royal-bright), var(--mp-royal));
        }
        .mp-dash-jewel--emerald {
          background: linear-gradient(145deg, var(--mp-emerald-bright), var(--mp-emerald));
        }
        .mp-dash-jewel--forest {
          background: linear-gradient(145deg, #2f5a48, var(--mp-forest));
        }
        .mp-dash-jewel--gold {
          background: linear-gradient(145deg, var(--mp-gold-soft), var(--mp-gold));
          color: #1a1a1a;
        }
        .mp-dash-jewel--orange {
          background: linear-gradient(145deg, #e06a3a, var(--mp-orange));
        }
        .mp-dash-jewel--purple {
          background: linear-gradient(145deg, var(--mp-purple-soft), var(--mp-purple));
        }
        .mp-dash-jewel--silver {
          background: linear-gradient(145deg, #cfd3da, var(--mp-silver));
          color: #1a1a1a;
        }
        .mp-dash-pack-text {
          display: flex;
          flex-direction: column;
          gap: 0.12rem;
          min-width: 0;
        }
        .mp-dash-pack-text strong {
          font-size: 0.9rem;
          font-weight: 600;
        }
        .mp-dash-pack-text > span:not(.mp-field-help) {
          font-size: 0.72rem;
          color: var(--mp-fg-muted);
        }
        :global(.mp-dash-chip) {
          display: inline-block;
          padding: 0.12rem 0.5rem;
          border-radius: 999px;
          font-size: 0.72rem;
          font-weight: 600;
          letter-spacing: 0.02em;
          background: var(--mp-bg-muted);
          color: var(--mp-fg-muted);
        }
        :global(.mp-dash-chip--ok) {
          background: var(--mp-success-bg);
          color: var(--mp-emerald);
        }
        :global(.mp-dash-chip--warn) {
          background: var(--mp-warning-bg);
          color: var(--mp-gold);
        }
        :global(.mp-dash-chip--muted) {
          background: color-mix(in srgb, var(--mp-silver) 28%, transparent);
          color: var(--mp-fg-muted);
        }
        .mp-dash-alert {
          color: var(--mp-orange);
          margin: 0.5rem 0;
        }
        .mp-dash-pulse {
          margin-block-end: 0.25rem;
        }
        .mp-dash-pulse-feed {
          margin-block-start: 0.85rem;
        }
        .mp-dash-pulse-feed-title {
          margin: 0 0 0.4rem;
          font-size: 0.78rem;
          letter-spacing: 0.05em;
          text-transform: uppercase;
          color: var(--mp-fg-muted);
          font-weight: 650;
        }
        .mp-dash-pulse-list {
          list-style: none;
          margin: 0;
          padding: 0;
          display: flex;
          flex-direction: column;
          gap: 0.45rem;
        }
        .mp-dash-pulse-list li {
          display: flex;
          flex-direction: column;
          gap: 0.15rem;
          padding: 0.45rem 0.55rem;
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius-sm);
          background: var(--mp-bg-subtle, var(--mp-bg-muted));
        }
        .mp-dash-pulse-list a {
          color: var(--mp-forest);
          text-decoration: none;
          font-weight: 600;
          font-size: 0.88rem;
        }
        .mp-dash-pulse-list a:hover,
        .mp-dash-pulse-list a:focus-visible {
          text-decoration: underline;
          outline: none;
        }
        @media (max-width: 960px) {
          .mp-dash-layout {
            grid-template-columns: 1fr;
          }
          .mp-dash-aside {
            position: static;
            max-height: none;
            order: 2;
          }
          .mp-dash-main {
            order: 1;
          }
          .mp-dash-metrics {
            grid-template-columns: repeat(2, minmax(0, 1fr));
          }
        }
        @media (prefers-reduced-motion: reduce) {
          .mp-dash-pack-item,
          .mp-dash-launch-item {
            transition: none;
          }
        }
      `}</style>
    </PageLayout>
  );
}
