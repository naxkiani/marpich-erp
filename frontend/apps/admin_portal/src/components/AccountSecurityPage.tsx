"use client";

import { PageLayout } from "@marpich/core";
import {
  EmptyState,
  ExportButton,
  PrintButton,
  ProgressBar,
  StepProgress,
  useAutosave,
  useLocale,
  useToast,
} from "@marpich/shared";
import { useAuth } from "@marpich/auth-provider";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useMemo, useState } from "react";

const DRAFT_KEY = "marpich.account.security.draft";

type ModuleCard = {
  id: string;
  href: string;
  titleKey: string;
  hintKey: string;
  status: string;
};

function Chip({ status }: { status: string }) {
  const tone =
    status === "active" || status === "ready" || status === "on"
      ? "ok"
      : status === "recommended" || status === "pending"
        ? "warn"
        : "muted";
  return (
    <span className={`acs-chip acs-chip--${tone}`} data-status={status}>
      {status}
    </span>
  );
}

export function AccountSecurityPage() {
  const router = useRouter();
  const { push } = useToast();
  const { t } = useLocale();
  const { isAuthenticated, isLoading, user, session, logout } = useAuth();
  const [progress, setProgress] = useState(20);
  const [draftReady, setDraftReady] = useState(false);
  const [privacyOn, setPrivacyOn] = useState(true);
  const [securityEmails, setSecurityEmails] = useState(true);
  const [selectedModule, setSelectedModule] = useState("mfa");
  const [lastAction, setLastAction] = useState<string | null>(null);

  const formDraft = useMemo(
    () => ({ privacyOn, securityEmails, selectedModule }),
    [privacyOn, securityEmails, selectedModule],
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
        if (typeof parsed.privacyOn === "boolean") setPrivacyOn(parsed.privacyOn);
        if (typeof parsed.securityEmails === "boolean") {
          setSecurityEmails(parsed.securityEmails);
        }
        if (typeof parsed.selectedModule === "string" && parsed.selectedModule.trim()) {
          setSelectedModule(parsed.selectedModule);
        }
      }
    } catch {
      /* ignore */
    } finally {
      setDraftReady(true);
      setProgress(100);
    }
  }, []);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace("/login?returnTo=/account/security");
    }
  }, [isAuthenticated, isLoading, router]);

  const modules: ModuleCard[] = useMemo(
    () => [
      {
        id: "mfa",
        href: "/account/mfa",
        titleKey: "accountSecurity.mod.mfa",
        hintKey: "accountSecurity.mod.mfaHint",
        status: "recommended",
      },
      {
        id: "passkeys",
        href: "/account/passkeys",
        titleKey: "accountSecurity.mod.passkeys",
        hintKey: "accountSecurity.mod.passkeysHint",
        status: "recommended",
      },
      {
        id: "recovery",
        href: "/account/change-password",
        titleKey: "accountSecurity.mod.recovery",
        hintKey: "accountSecurity.mod.recoveryHint",
        status: "ready",
      },
      {
        id: "devices",
        href: "/account/security#devices",
        titleKey: "accountSecurity.mod.devices",
        hintKey: "accountSecurity.mod.devicesHint",
        status: "pending",
      },
    ],
    [],
  );

  const selected = modules.find((m) => m.id === selectedModule) ?? modules[0];

  const lifecycleStep = useMemo(() => {
    if (!isAuthenticated) return 0;
    if (!privacyOn && !securityEmails) return 1;
    if (privacyOn || securityEmails) return 2;
    return 3;
  }, [isAuthenticated, privacyOn, securityEmails]);

  const workflowSteps = useMemo(
    () => [
      t("accountSecurity.step.signIn"),
      t("accountSecurity.step.protect"),
      t("accountSecurity.step.privacy"),
      t("accountSecurity.step.review"),
    ],
    [t],
  );

  const exportRows = useMemo(
    () => [
      {
        email: user?.email ?? "",
        tenant: session?.tenantId ?? "",
        privacy_minimized: privacyOn ? "yes" : "no",
        security_emails: securityEmails ? "yes" : "no",
      },
    ],
    [privacyOn, securityEmails, session?.tenantId, user?.email],
  );

  async function onRefreshSession() {
    setLastAction(t("accountSecurity.refreshSession"));
    push({ message: t("accountSecurity.sessionHint") });
  }

  async function onLogoutAll() {
    setLastAction(t("accountSecurity.logout"));
    await logout();
    router.push("/login");
  }

  if (isLoading) {
    return (
      <PageLayout title={t("accountSecurity.title")}>
        <ProgressBar value={40} label={t("accountSecurity.loading")} />
      </PageLayout>
    );
  }

  if (!isAuthenticated) return null;

  return (
    <PageLayout
      title={t("accountSecurity.title")}
      subtitle={t("accountSecurity.subtitle")}
      breadcrumb={[
        { label: t("app.name"), href: "/" },
        { label: t("accountSecurity.breadcrumb"), href: "/account/security" },
        { label: t("accountSecurity.title") },
      ]}
      actions={
        <>
          <ExportButton
            label={t("common.export")}
            rows={exportRows}
            filename="account-security-preferences.csv"
          />
          <PrintButton label={t("common.print")} />
          <button type="button" className="mp-btn" onClick={() => void onRefreshSession()}>
            {t("accountSecurity.refreshSession")}
          </button>
          <button type="button" className="mp-btn" onClick={() => void onLogoutAll()}>
            {t("accountSecurity.logout")}
          </button>
        </>
      }
    >
      <ProgressBar value={progress} label={t("accountSecurity.ready")} />

      <div className="acs-layout">
        <aside className="acs-aside" aria-label={t("accountSecurity.rail")}>
          <section className="acs-panel-card">
            <header className="acs-panel-head">
              <h2>{t("accountSecurity.workflow")}</h2>
            </header>
            <div className="acs-panel-body">
              <StepProgress steps={workflowSteps} current={lifecycleStep} />
              {draftSaving ? (
                <p className="mp-field-help" aria-live="polite">
                  {t("accountSecurity.draftSaved")}…
                </p>
              ) : (
                <p className="mp-field-help">{t("accountSecurity.workflowHint")}</p>
              )}
              {selected ? (
                <p className="mp-field-help">
                  <Chip status={selected.status} /> · {t(selected.titleKey)}
                </p>
              ) : null}
            </div>
          </section>

          <section className="acs-panel-card">
            <header className="acs-panel-head">
              <h2>{t("accountSecurity.rail.status")}</h2>
            </header>
            <div className="acs-panel-body">
              <div className="acs-status-row">
                <span>{t("dashboard.tenant")}</span>
                <strong>{session?.tenantId ?? "—"}</strong>
              </div>
              <div className="acs-status-row">
                <span>{t("dashboard.email")}</span>
                <strong>{user?.email ?? "—"}</strong>
              </div>
              {lastAction ? (
                <p className="mp-field-help">
                  {t("accountSecurity.lastAction")}: {lastAction}
                </p>
              ) : null}
            </div>
          </section>
        </aside>

        <div className="acs-main">
          <section aria-labelledby="profile-heading">
            <h2 id="profile-heading">{t("accountSecurity.profile")}</h2>
            <p className="acs-muted">
              {user?.email ?? t("accountSecurity.signedIn")} · {t("dashboard.tenant")}{" "}
              {session?.tenantId}
            </p>
          </section>

          <section aria-labelledby="modules-heading">
            <h2 id="modules-heading">{t("accountSecurity.modules")}</h2>
            <div className="acs-module-grid">
              {modules.map((mod) => (
                <button
                  key={mod.id}
                  type="button"
                  className={`acs-module${selectedModule === mod.id ? " acs-module-active" : ""}`}
                  onClick={() => setSelectedModule(mod.id)}
                >
                  <span className="acs-module-title">{t(mod.titleKey)}</span>
                  <Chip status={mod.status} />
                  <span className="acs-module-hint">{t(mod.hintKey)}</span>
                </button>
              ))}
            </div>

            {selected ? (
              <section
                className="acs-detail-panel mp-animate-in"
                aria-label={t("accountSecurity.detail")}
              >
                <header>{t(selected.titleKey)}</header>
                <p className="acs-muted">{t(selected.hintKey)}</p>
                <div className="acs-actions-row">
                  <Link className="mp-btn mp-btn-primary" href={selected.href}>
                    {t("accountSecurity.open")}
                  </Link>
                </div>
              </section>
            ) : null}
          </section>

          <section id="devices" aria-labelledby="sessions-heading">
            <h2 id="sessions-heading">{t("accountSecurity.sessions")}</h2>
            <div className="acs-session-card">
              <div className="acs-status-row">
                <span>{t("accountSecurity.currentSession")}</span>
                <Chip status="active" />
              </div>
              <p className="acs-muted">
                {t("dashboard.tenant")}: {session?.tenantId ?? "—"}
              </p>
              <EmptyState
                title={t("accountSecurity.noDevices")}
                description={t("accountSecurity.noDevicesHint")}
              />
            </div>
          </section>

          <section aria-labelledby="privacy-heading">
            <h2 id="privacy-heading">{t("accountSecurity.privacy")}</h2>
            <div className="acs-privacy">
              <label className="acs-check">
                <input
                  type="checkbox"
                  checked={privacyOn}
                  onChange={(e) => setPrivacyOn(e.target.checked)}
                />
                {t("accountSecurity.privacyMinimize")}
              </label>
              <label className="acs-check">
                <input
                  type="checkbox"
                  checked={securityEmails}
                  onChange={(e) => setSecurityEmails(e.target.checked)}
                />
                {t("accountSecurity.privacyEmails")}
              </label>
            </div>
          </section>

          <section aria-labelledby="linked-heading">
            <h2 id="linked-heading">{t("accountSecurity.linked")}</h2>
            <EmptyState
              title={t("accountSecurity.noLinked")}
              description={t("accountSecurity.noLinkedHint")}
              action={
                <Link className="mp-btn" href="/enterprise/federation">
                  {t("accountSecurity.openFederation")}
                </Link>
              }
            />
          </section>
        </div>
      </div>

      <style jsx>{`
        .acs-layout {
          display: grid;
          grid-template-columns: minmax(220px, 280px) 1fr;
          gap: 1.25rem;
          align-items: start;
        }
        .acs-aside {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
          position: sticky;
          top: 1rem;
        }
        .acs-panel-card {
          border: 1px solid var(--mp-border, #e2e8f0);
          border-radius: 8px;
          background: var(--mp-surface, #fff);
          overflow: hidden;
        }
        .acs-panel-head {
          padding: 0.65rem 0.85rem;
          border-bottom: 1px solid var(--mp-border, #e2e8f0);
          background: var(--mp-surface-2, #f8fafc);
        }
        .acs-panel-head h2 {
          margin: 0;
          font-size: 0.95rem;
        }
        .acs-panel-body {
          padding: 0.85rem;
        }
        .acs-status-row {
          display: flex;
          justify-content: space-between;
          gap: 0.5rem;
          font-size: 0.85rem;
          margin-bottom: 0.35rem;
        }
        .acs-main {
          min-width: 0;
        }
        .acs-muted {
          color: var(--mp-text-muted, #64748b);
          margin: 0.35rem 0 1rem;
        }
        .acs-module-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
          gap: 0.75rem;
          margin-bottom: 0.75rem;
        }
        .acs-module {
          text-align: start;
          padding: 0.85rem;
          border: 1px solid var(--mp-border, #e2e8f0);
          border-radius: 8px;
          background: var(--mp-surface, #fff);
          cursor: pointer;
          display: flex;
          flex-direction: column;
          gap: 0.35rem;
        }
        .acs-module-active {
          border-color: #0ea5e9;
          box-shadow: 0 0 0 1px #0ea5e9;
        }
        .acs-module-title {
          font-weight: 600;
          font-size: 0.95rem;
        }
        .acs-module-hint {
          font-size: 0.8rem;
          color: var(--mp-text-muted, #64748b);
        }
        .acs-chip {
          display: inline-block;
          width: fit-content;
          padding: 0.1rem 0.45rem;
          border-radius: 4px;
          font-size: 0.75rem;
          font-weight: 600;
        }
        .acs-chip--ok {
          background: #dcfce7;
          color: #166534;
        }
        .acs-chip--warn {
          background: #fef3c7;
          color: #92400e;
        }
        .acs-chip--muted {
          background: #f1f5f9;
          color: #475569;
        }
        .acs-detail-panel,
        .acs-session-card {
          margin-top: 0.5rem;
          padding: 0.85rem 1rem;
          border: 1px solid var(--mp-border, #e2e8f0);
          border-radius: 8px;
          background: var(--mp-surface-2, #f8fafc);
        }
        .acs-detail-panel header {
          font-weight: 600;
          margin-bottom: 0.35rem;
        }
        .acs-actions-row {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          margin-top: 0.75rem;
        }
        .acs-privacy {
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
        }
        .acs-check {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.95rem;
        }
        h2 {
          margin: 0 0 0.75rem;
          font-size: 1.1rem;
        }
        section {
          margin-bottom: 1.5rem;
        }
        @media (max-width: 960px) {
          .acs-layout {
            grid-template-columns: 1fr;
          }
          .acs-aside {
            position: static;
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
