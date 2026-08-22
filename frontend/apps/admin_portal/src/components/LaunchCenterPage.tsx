"use client";

import { LoginGate, useAuth, type AuthSession } from "@marpich/auth-provider";
import { PageLayout } from "@marpich/core";
import {
  DataTable,
  DeskAlert,
  EmptyState,
  KpiStrip,
  ProgressBar,
  SkeletonTable,
  StepProgress,
  mapDeskStatsToKpiItems,
  useLocale,
  useToast,
} from "@marpich/shared";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  createLaunchCenterPlan,
  demoLabel,
  fetchLaunchCenterStatus,
  productionExecutionLocked,
  releaseSelectable,
  requestLaunchCenterProvision,
  type LaunchCenterPlan,
  type LaunchCenterWorkspace,
} from "@/lib/launchCenterClient";

type SectionId =
  | "dashboard"
  | "providers"
  | "environments"
  | "wizard"
  | "plan"
  | "releases"
  | "jobs"
  | "runtime"
  | "database"
  | "secrets"
  | "dns"
  | "backup"
  | "restore"
  | "rollback"
  | "observability"
  | "drift"
  | "security"
  | "audit"
  | "plans";

const SECTIONS: Array<{ id: SectionId; key: string }> = [
  { id: "dashboard", key: "launchCenter.section.dashboard" },
  { id: "providers", key: "launchCenter.section.providers" },
  { id: "environments", key: "launchCenter.section.environments" },
  { id: "wizard", key: "launchCenter.section.wizard" },
  { id: "plan", key: "launchCenter.section.plan" },
  { id: "releases", key: "launchCenter.section.releases" },
  { id: "jobs", key: "launchCenter.section.jobs" },
  { id: "runtime", key: "launchCenter.section.runtime" },
  { id: "database", key: "launchCenter.section.database" },
  { id: "secrets", key: "launchCenter.section.secrets" },
  { id: "dns", key: "launchCenter.section.dns" },
  { id: "backup", key: "launchCenter.section.backup" },
  { id: "restore", key: "launchCenter.section.restore" },
  { id: "rollback", key: "launchCenter.section.rollback" },
  { id: "observability", key: "launchCenter.section.observability" },
  { id: "drift", key: "launchCenter.section.drift" },
  { id: "security", key: "launchCenter.section.security" },
  { id: "audit", key: "launchCenter.section.audit" },
  { id: "plans", key: "launchCenter.section.plans" },
];

const WIZARD_KEYS = [
  "provider",
  "region",
  "environment",
  "profile",
  "release",
  "resources",
  "database",
  "networking",
  "secrets",
  "cost",
  "security",
  "plan",
  "authorization",
  "provision",
  "deploy",
  "verify",
];

export function LaunchCenterPage() {
  const { t } = useLocale();
  const { push } = useToast();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(15);
  const [error, setError] = useState<string | null>(null);
  const [section, setSection] = useState<SectionId>("dashboard");
  const [workspace, setWorkspace] = useState<LaunchCenterWorkspace | null>(null);
  const [plan, setPlan] = useState<LaunchCenterPlan | null>(null);
  const [wizardStep, setWizardStep] = useState(0);
  const [provider, setProvider] = useState("AWS");
  const [environment, setEnvironment] = useState("STAGING");
  const [profile, setProfile] = useState("STAGING");
  const [size, setSize] = useState("SMALL");
  const [authorized, setAuthorized] = useState(false);

  const load = useCallback(async (active: AuthSession) => {
    setLoading(true);
    setProgress(35);
    setError(null);
    try {
      const data = await fetchLaunchCenterStatus(active);
      setWorkspace(data);
      setPlan((data.plan as LaunchCenterPlan) ?? null);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("launchCenter.loadFailed"));
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [t]);

  useEffect(() => {
    if (authLoading) return;
    if (session) {
      void load(session);
      return;
    }
    setLoading(false);
    setProgress(100);
  }, [authLoading, load, session]);

  const locked = productionExecutionLocked(workspace);
  const simulated = demoLabel(workspace);

  const kpiItems = useMemo(() => {
    if (!workspace) return [];
    return mapDeskStatsToKpiItems(
      [
        { label: t("launchCenter.kpi.environments"), value: workspace.environments_total, tone: "warn" },
        { label: t("launchCenter.kpi.ready"), value: workspace.environments_ready, tone: "warn" },
        { label: t("launchCenter.kpi.blocked"), value: workspace.environments_blocked, tone: "danger" },
        { label: t("launchCenter.kpi.jobs"), value: workspace.active_jobs, tone: "ok" },
        { label: t("launchCenter.kpi.digest"), value: workspace.DIGEST, tone: "warn" },
      ],
      5,
    );
  }, [t, workspace]);

  const providerRows = useMemo(
    () =>
      Object.entries(workspace?.providers ?? {}).map(([name, row]) => ({
        provider: name,
        status: row.status,
        credentials: row.credentials,
        regions: row.regions,
      })),
    [workspace],
  );

  const releaseRows = useMemo(
    () =>
      (workspace?.releases ?? []).map((row) => ({
        release: row.RELEASE_ID,
        version: String(row.VERSION ?? "—"),
        commit: String(row.COMMIT_SHA ?? "—"),
        image: String(row.IMAGE ?? "—"),
        digest: String(row.IMAGE_DIGEST ?? "NOT_AVAILABLE"),
        security: String(row.SECURITY ?? row.SECURITY_STATUS ?? "—"),
        sbom: String(row.SBOM ?? row.SBOM_ID ?? "—"),
        test: String(row.TEST ?? row.TEST_STATUS ?? "—"),
        promotion: String(row.PROMOTION ?? row.PROMOTION_STATUS ?? "—"),
        selectable: releaseSelectable(row) ? "YES" : "NO",
      })),
    [workspace],
  );

  async function runPlan() {
    if (!session) return;
    try {
      const next = await createLaunchCenterPlan(session, {
        provider,
        environment,
        profile,
      });
      setPlan(next);
      setSection("plan");
      push({ message: `${t("launchCenter.planOnly")} · ${String(next.STATUS ?? "VALIDATION_ONLY")}` });
    } catch (err) {
      push({ message: err instanceof Error ? err.message : t("launchCenter.loadFailed") });
    }
  }

  async function runProvisionBlocked() {
    if (!session) return;
    try {
      const result = await requestLaunchCenterProvision(session, { provider, environment, profile });
      push({
        message: `${t("launchCenter.productionLocked")} · ${String(result.PRODUCTION_DEPLOYMENT ?? "LOCKED")}`,
      });
    } catch (err) {
      push({ message: err instanceof Error ? err.message : t("launchCenter.executeBlocked") });
    }
  }

  const wizardLabel = WIZARD_KEYS[wizardStep] ?? "provider";

  return (
    <PageLayout
      title={t("launchCenter.title")}
      breadcrumb={[
        { label: "Marpich", href: "/" },
        { label: t("launchCenter.breadcrumb"), href: "/modules" },
        { label: t("nav.app.launchCenter") },
      ]}
      actions={
        isAuthenticated && session ? (
          <button type="button" className="mp-btn" onClick={() => void load(session)} disabled={loading}>
            {t("launchCenter.refresh")}
          </button>
        ) : null
      }
    >
      <p className="lc-subtitle">{t("launchCenter.subtitle")}</p>
      <ProgressBar value={progress} label={loading ? t("launchCenter.loading") : t("launchCenter.ready")} />

      {!isAuthenticated ? (
        <LoginGate title={t("launchCenter.signIn")} defaultTenantId="launch-demo" defaultEmail="admin@launch.dev" />
      ) : null}

      {error ? <DeskAlert>{error}</DeskAlert> : null}

      {isAuthenticated && locked ? (
        <DeskAlert>
          {t("launchCenter.productionLocked")} · {t("launchCenter.goLiveRequired")} · {t("launchCenter.g26Blocked")}
        </DeskAlert>
      ) : null}

      {isAuthenticated && workspace?.demo_mode?.enabled ? (
        <p className="lc-muted" role="note">
          <span className="mp-dash-chip mp-dash-chip--warn">{simulated}</span> {t("launchCenter.demoHint")}
        </p>
      ) : null}

      {isAuthenticated ? (
        <div className="lc-tabs" role="tablist" aria-label={t("launchCenter.title")}>
          {SECTIONS.map((item) => (
            <button
              key={item.id}
              type="button"
              role="tab"
              aria-selected={section === item.id}
              className={section === item.id ? "lc-tab lc-tab--on" : "lc-tab"}
              onClick={() => setSection(item.id)}
            >
              {t(item.key)}
            </button>
          ))}
        </div>
      ) : null}

      {isAuthenticated && loading ? <SkeletonTable rows={5} cols={4} /> : null}

      {isAuthenticated && workspace && !loading && section === "dashboard" ? (
        <>
          <KpiStrip label={t("launchCenter.section.dashboard")} items={kpiItems} />
          <section className="lc-grid" aria-labelledby="lc-gov">
            <h2 id="lc-gov">Governance</h2>
            <DataTable
              columns={[
                { key: "gate", header: "Gate" },
                { key: "status", header: t("launchCenter.col.status") },
              ]}
              rows={[
                { gate: "G26", status: String(workspace.G26_STATUS) },
                { gate: "P313", status: String(workspace.P313) },
                { gate: "PRODUCTION_CERTIFICATION", status: String(workspace.PRODUCTION_CERTIFIED) },
                { gate: "GO_LIVE_AUTHORIZATION", status: String(workspace.GO_LIVE_AUTHORIZATION) },
                { gate: "P0", status: String(workspace.P0) },
                { gate: "PRODUCTION_TRAFFIC", status: String(workspace.PRODUCTION_TRAFFIC) },
                { gate: "AUTONOMOUS_KILL_SWITCH", status: workspace.autonomous_operations?.kill_switch ? "ACTIVE" : "STANDBY" },
                { gate: "PRODUCTION_AUTOMATION_LOCK", status: String(workspace.autonomous_operations?.PRODUCTION_AUTOMATION_LOCK ?? "ACTIVE") },
              ]}
            />
            <p className="lc-muted">{t("launchCenter.executeBlocked")}</p>
          </section>
          {workspace.control_plane ? (
            <section className="lc-grid" aria-labelledby="lc-plane">
              <h2 id="lc-plane">Control Plane</h2>
              <DataTable
                columns={[
                  { key: "field", header: "Field" },
                  { key: "status", header: t("launchCenter.col.status") },
                ]}
                rows={[
                  { field: "environment", status: String(workspace.control_plane.environment ?? "—") },
                  { field: "provider", status: String(workspace.control_plane.provider ?? "—") },
                  { field: "region", status: String(workspace.control_plane.region ?? "—") },
                  { field: "profile", status: String(workspace.control_plane.profile ?? "—") },
                  { field: "status", status: String(workspace.control_plane.status ?? "—") },
                  { field: "release", status: String(workspace.control_plane.release ?? "—") },
                  { field: "deployment", status: String(workspace.control_plane.deployment ?? "—") },
                  { field: "database", status: String(workspace.control_plane.database ?? "—") },
                  { field: "network", status: String(workspace.control_plane.network ?? "—") },
                  { field: "DNS", status: String(workspace.control_plane.DNS ?? "—") },
                  { field: "TLS", status: String(workspace.control_plane.TLS ?? "—") },
                  { field: "backup", status: String(workspace.control_plane.backup ?? "—") },
                  { field: "restore", status: String(workspace.control_plane.restore ?? "—") },
                  { field: "observability", status: String(workspace.control_plane.observability ?? "—") },
                  { field: "security", status: String(workspace.control_plane.security ?? "—") },
                  { field: "cost", status: String(workspace.control_plane.cost ?? "COST_NOT_AVAILABLE") },
                  { field: "capacity", status: String(workspace.control_plane.capacity ?? "UNKNOWN") },
                  { field: "drift", status: String(workspace.control_plane.drift ?? "UNKNOWN") },
                ]}
              />
            </section>
          ) : null}
        </>
      ) : null}

      {isAuthenticated && workspace && !loading && section === "providers" ? (
        <DataTable
          columns={[
            { key: "provider", header: t("launchCenter.col.provider"), sortable: true },
            { key: "status", header: t("launchCenter.col.status") },
            { key: "credentials", header: "Authentication" },
            { key: "regions", header: "Regions" },
          ]}
          rows={providerRows}
        />
      ) : null}

      {isAuthenticated && workspace && !loading && section === "environments" ? (
        (workspace.environments ?? []).length === 0 ? (
          <EmptyState title={t("launchCenter.noEnvironments")} description={t("launchCenter.noEnvironmentsHint")} />
        ) : (
          <DataTable
            columns={[
              { key: "id", header: "ENVIRONMENT_ID" },
              { key: "provider", header: t("launchCenter.col.provider") },
              { key: "status", header: t("launchCenter.col.status") },
            ]}
            rows={(workspace.environments ?? []).map((row) => ({
              id: String(row.ENVIRONMENT_ID ?? "—"),
              provider: String(row.PROVIDER ?? "—"),
              status: String(row.STATUS ?? "—"),
            }))}
          />
        )
      ) : null}

      {isAuthenticated && workspace && !loading && section === "wizard" ? (
        <section aria-labelledby="lc-wizard">
          <h2 id="lc-wizard">{t("launchCenter.section.wizard")}</h2>
          <StepProgress steps={WIZARD_KEYS} current={wizardStep} />
          <p className="lc-muted">
            STEP {String(wizardStep + 1).padStart(2, "0")} · {wizardLabel}
          </p>
          {wizardStep === 0 ? (
            <label className="lc-field">
              Provider
              <select value={provider} onChange={(e) => setProvider(e.target.value)}>
                {Object.keys(workspace.providers).map((name) => (
                  <option key={name} value={name}>
                    {name} · {workspace.providers[name]?.status}
                  </option>
                ))}
              </select>
              <span className="mp-field-help">{t("launchCenter.authRequired")}</span>
            </label>
          ) : null}
          {wizardStep === 1 ? (
            <p className="lc-muted" role="status">
              {t("launchCenter.regionUnavailable")}
            </p>
          ) : null}
          {wizardStep === 2 ? (
            <label className="lc-field">
              Environment
              <select value={environment} onChange={(e) => setEnvironment(e.target.value)}>
                {["DEVELOPMENT", "DEMO", "TEST", "STAGING", "PRODUCTION", "DISASTER_RECOVERY"].map((name) => (
                  <option key={name} value={name}>
                    {name}
                  </option>
                ))}
              </select>
            </label>
          ) : null}
          {wizardStep === 3 ? (
            <DataTable
              columns={[
                { key: "profile", header: "Profile" },
                { key: "compute", header: "Compute" },
                { key: "database", header: "Database" },
                { key: "backup", header: "Backup" },
              ]}
              rows={Object.entries(workspace.profiles ?? {}).map(([name, row]) => ({
                profile: name,
                compute: String(row.compute ?? "—"),
                database: String(row.database ?? "—"),
                backup: String(row.backup ?? row.status ?? "—"),
              }))}
            />
          ) : null}
          {wizardStep === 4 ? (
            <EmptyState title={t("launchCenter.noRelease")} description={t("launchCenter.noReleaseHint")} />
          ) : null}
          {wizardStep === 5 ? (
            <label className="lc-field">
              Size
              <select value={size} onChange={(e) => setSize(e.target.value)}>
                {Object.entries(workspace.sizes ?? {}).map(([name, row]) => (
                  <option key={name} value={name}>
                    {name} · CPU {row.cpu} · RAM {row.memory}
                  </option>
                ))}
              </select>
            </label>
          ) : null}
          {wizardStep === 9 ? (
            <p className="lc-muted" role="status">
              {workspace.cost?.TOTAL ?? t("launchCenter.costUnknown")}
            </p>
          ) : null}
          {wizardStep === 12 ? (
            <p className="lc-muted">
              PLAN → REVIEW → APPROVE → EXECUTE. {t("launchCenter.executeBlocked")}
              <button type="button" className="mp-btn" onClick={() => setAuthorized(true)}>
                {t("launchCenter.authorize")}
              </button>
              {authorized ? " · REVIEW RECORDED" : ""}
            </p>
          ) : null}
          {wizardStep >= 13 ? (
            <p className="lc-muted">
              {t("launchCenter.productionLocked")} · {t("launchCenter.dryRun")} = {t("launchCenter.planOnly")}
            </p>
          ) : null}
          <div className="lc-actions">
            <button type="button" className="mp-btn" disabled={wizardStep === 0} onClick={() => setWizardStep((s) => s - 1)}>
              {t("launchCenter.back")}
            </button>
            <button
              type="button"
              className="mp-btn"
              disabled={wizardStep >= WIZARD_KEYS.length - 1}
              onClick={() => setWizardStep((s) => s + 1)}
            >
              {t("launchCenter.next")}
            </button>
            <button type="button" className="mp-btn mp-btn-primary" onClick={() => void runPlan()}>
              {t("launchCenter.dryRun")}
            </button>
            <button type="button" className="mp-btn" disabled aria-disabled="true" title={t("launchCenter.productionLocked")}>
              {t("launchCenter.provision")}
            </button>
          </div>
        </section>
      ) : null}

      {isAuthenticated && workspace && !loading && section === "plan" ? (
        <section aria-labelledby="lc-plan">
          <h2 id="lc-plan">{t("launchCenter.section.plan")}</h2>
          <DataTable
            columns={[
              { key: "resource", header: "Resource" },
              { key: "status", header: t("launchCenter.col.status") },
            ]}
            rows={[
              { resource: "NETWORK", status: String(plan?.network ?? workspace.plan?.network ?? "—") },
              { resource: "DATABASE", status: "METADATA_ONLY" },
              { resource: "COMPUTE", status: String(plan?.STATUS ?? "VALIDATION_ONLY") },
              { resource: "STORAGE", status: "PLAN" },
              { resource: "SECRETS", status: "REFERENCE_ONLY" },
              { resource: "DNS", status: String(plan?.dns ?? "NOT_AVAILABLE") },
              { resource: "TLS", status: String(plan?.tls ?? "CONFIGURED") },
              { resource: "MONITORING", status: String(plan?.observability ?? "CONFIGURED") },
              { resource: "BACKUP", status: "CONFIGURED" },
              { resource: "DEPLOYMENT", status: "DISABLED" },
            ]}
          />
          <p className="lc-muted">{t("launchCenter.planOnly")} · executed={String(plan?.executed ?? false)}</p>
        </section>
      ) : null}

      {isAuthenticated && workspace && !loading && section === "releases" ? (
        releaseRows.length === 0 ? (
          <EmptyState title={t("launchCenter.noRelease")} description={t("launchCenter.noReleaseHint")} />
        ) : (
          <DataTable
            columns={[
              { key: "release", header: t("launchCenter.col.release") },
              { key: "version", header: "VERSION" },
              { key: "commit", header: "COMMIT" },
              { key: "digest", header: t("launchCenter.col.digest") },
              { key: "security", header: "SECURITY" },
              { key: "sbom", header: "SBOM" },
              { key: "test", header: "TEST" },
              { key: "promotion", header: "PROMOTION" },
              { key: "selectable", header: "Selectable" },
            ]}
            rows={releaseRows}
          />
        )
      ) : null}

      {isAuthenticated && workspace && !loading && section === "jobs" ? (
        <EmptyState title="No operational jobs" description={t("launchCenter.executeBlocked")} />
      ) : null}

      {isAuthenticated && workspace && !loading && section === "runtime" ? (
        <DataTable
          columns={[
            { key: "surface", header: "Surface" },
            { key: "status", header: t("launchCenter.col.status") },
          ]}
          rows={[
            { surface: "LIVE", status: String(workspace.health?.LIVE ?? "/live") },
            { surface: "READY", status: String(workspace.health?.READY ?? "/api/v1/ready") },
            { surface: "STATUS", status: String(workspace.health?.status ?? "UNKNOWN") },
          ]}
        />
      ) : null}

      {isAuthenticated && workspace && !loading && section === "database" ? (
        <EmptyState
          title="No managed database"
          description="Metadata only. localhost / 127.0.0.1 / 5433 / 5444 are NON_PRODUCTION."
        />
      ) : null}

      {isAuthenticated && workspace && !loading && section === "secrets" ? (
        <EmptyState title="Secret references only" description="Values stay hidden. Copy and print actions are not provided." />
      ) : null}

      {isAuthenticated && workspace && !loading && section === "dns" ? (
        <EmptyState title="DNS / TLS not verified" description="Self-signed certificates remain NON_PRODUCTION." />
      ) : null}

      {isAuthenticated && workspace && !loading && section === "backup" ? (
        <EmptyState title="No production backup" description="Local or simulated backups are not production evidence." />
      ) : null}

      {isAuthenticated && workspace && !loading && section === "restore" ? (
        <EmptyState title="Restore tests blocked" description="Restore tests must not silently overwrite production data." />
      ) : null}

      {isAuthenticated && workspace && !loading && section === "rollback" ? (
        <section>
          <DataTable
            columns={[
              { key: "field", header: "Field" },
              { key: "value", header: "Value" },
            ]}
            rows={[
              { field: "CURRENT_RELEASE", value: workspace.RELEASE },
              { field: "CURRENT_DIGEST", value: workspace.DIGEST },
              { field: "ROLLBACK_STATUS", value: "LOCKED" },
            ]}
          />
          <button type="button" className="mp-btn" disabled aria-disabled="true">
            ROLLBACK
          </button>
        </section>
      ) : null}

      {isAuthenticated && workspace && !loading && section === "observability" ? (
        <EmptyState
          title={t("launchCenter.section.observability")}
          description="Uses the existing Observability desk. This is not a second monitoring system."
          action={
            <a className="mp-btn" href="/enterprise/observability">
              {t("nav.app.observability")}
            </a>
          }
        />
      ) : null}

      {isAuthenticated && workspace && !loading && section === "drift" ? (
        <DataTable
          columns={[
            { key: "category", header: "Category" },
            { key: "state", header: "State" },
          ]}
          rows={[
            { category: "RELEASE", state: "UNKNOWN" },
            { category: "CONFIGURATION", state: "UNKNOWN" },
            { category: "INFRASTRUCTURE", state: "UNKNOWN" },
            { category: "DATABASE", state: "UNKNOWN" },
            { category: "DNS", state: "UNKNOWN" },
            { category: "TLS", state: "UNKNOWN" },
          ]}
        />
      ) : null}

      {isAuthenticated && workspace && !loading && section === "security" ? (
        <DataTable
          columns={[
            { key: "gate", header: "Gate" },
            { key: "status", header: t("launchCenter.col.status") },
          ]}
          rows={[
            { gate: "IMAGE", status: "DEPLOYMENT BLOCKED" },
            { gate: "SBOM", status: "DECLARED_DEPENDENCIES_ONLY" },
            { gate: "DIGEST", status: workspace.DIGEST },
            { gate: "RBAC", status: "IDENTITY_REUSED" },
          ]}
        />
      ) : null}

      {isAuthenticated && workspace && !loading && section === "audit" ? (
        <EmptyState title="Append-only audit via Audit Platform" description="Operator actions are recorded by the existing audit service. No local audit table." />
      ) : null}

      {isAuthenticated && workspace && !loading && section === "plans" ? (
        <EmptyState title="No saved launch plans" description={`${t("launchCenter.planOnly")} · ${t("launchCenter.dryRun")}`} />
      ) : null}

      {isAuthenticated && locked ? (
        <div className="lc-actions">
          <button type="button" className="mp-btn mp-btn-primary" onClick={() => void runPlan()}>
            {t("launchCenter.dryRun")}
          </button>
          <button
            type="button"
            className="mp-btn"
            disabled
            aria-disabled="true"
            title={t("launchCenter.productionLocked")}
            onClick={() => void runProvisionBlocked()}
          >
            {t("launchCenter.provision")}
          </button>
        </div>
      ) : null}

      <style jsx>{`
        .lc-subtitle {
          margin: 0 0 0.75rem;
          color: var(--mp-fg-muted);
        }
        .lc-muted {
          color: var(--mp-fg-muted);
          font-size: 0.9rem;
        }
        .lc-tabs {
          display: flex;
          flex-wrap: wrap;
          gap: 0.4rem;
          margin: 1rem 0;
        }
        .lc-tab {
          border: 1px solid var(--mp-border);
          background: var(--mp-bg-elevated);
          color: var(--mp-fg-muted);
          border-radius: 999px;
          padding: 0.35rem 0.85rem;
          font-size: 0.82rem;
          cursor: pointer;
        }
        .lc-tab--on {
          background: var(--mp-forest);
          border-color: var(--mp-forest);
          color: #fff;
        }
        .lc-grid h2,
        section h2 {
          margin: 1rem 0 0.75rem;
          font-size: 0.85rem;
          letter-spacing: 0.06em;
          text-transform: uppercase;
        }
        .lc-actions {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          margin-block-start: 1rem;
        }
        .lc-field {
          display: grid;
          gap: 0.35rem;
          max-width: 24rem;
          margin-block: 0.75rem;
        }
      `}</style>
    </PageLayout>
  );
}
