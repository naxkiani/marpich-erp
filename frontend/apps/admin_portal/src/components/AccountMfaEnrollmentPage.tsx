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
import {
  fetchIdentityMe,
  setupMfa,
  verifyMfaSetup,
  type IdentityMe,
  type MfaSetupResult,
} from "@/lib/identityMfaClient";

const DRAFT_KEY = "marpich.account.mfa.draft";

function Chip({ status }: { status: string }) {
  const tone =
    status === "enabled" || status === "ok" || status === "active"
      ? "ok"
      : status === "pending" || status === "setup"
        ? "warn"
        : status === "error" || status === "disabled"
          ? "bad"
          : "muted";
  return (
    <span className={`mfa-chip mfa-chip--${tone}`} data-status={status}>
      {status}
    </span>
  );
}

export function AccountMfaEnrollmentPage() {
  const router = useRouter();
  const { push } = useToast();
  const { t } = useLocale();
  const { isAuthenticated, isLoading, user, session, reloadUser } = useAuth();

  const [progress, setProgress] = useState(15);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [me, setMe] = useState<IdentityMe | null>(null);
  const [setup, setSetup] = useState<MfaSetupResult | null>(null);
  const [code, setCode] = useState("");
  const [backupCodes, setBackupCodes] = useState<string[]>([]);
  const [lastAction, setLastAction] = useState<string | null>(null);
  const [draftReady, setDraftReady] = useState(false);
  const [showSecret, setShowSecret] = useState(false);

  const formDraft = useMemo(() => ({ code: code.slice(0, 8) }), [code]);

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
        if (typeof parsed.code === "string" && /^\d{0,8}$/.test(parsed.code)) {
          setCode(parsed.code);
        }
      }
    } catch {
      /* ignore */
    } finally {
      setDraftReady(true);
    }
  }, []);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace("/login?returnTo=/account/mfa");
    }
  }, [isAuthenticated, isLoading, router]);

  const loadMe = useCallback(async () => {
    if (!session) return;
    setLoading(true);
    setError(null);
    setProgress(40);
    try {
      const profile = await fetchIdentityMe(session);
      setMe(profile);
      setProgress(100);
      setLastAction("me");
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err));
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    if (isAuthenticated && session) {
      void loadMe();
    }
  }, [isAuthenticated, loadMe, session]);

  const mfaEnabled = Boolean(me?.mfa_enabled ?? user?.mfa_enabled);

  const lifecycleStep = useMemo(() => {
    if (backupCodes.length > 0 || mfaEnabled) return 3;
    if (setup) return 2;
    if (me) return 1;
    return 0;
  }, [backupCodes.length, me, mfaEnabled, setup]);

  const workflowSteps = useMemo(
    () => [
      { id: "status", label: t("accountMfa.step.status") },
      { id: "enroll", label: t("accountMfa.step.enroll") },
      { id: "verify", label: t("accountMfa.step.verify") },
      { id: "backup", label: t("accountMfa.step.backup") },
    ],
    [t],
  );

  const exportRows = useMemo(() => {
    const rows: Array<Record<string, string>> = [
      {
        field: "email",
        value: me?.email ?? user?.email ?? "",
      },
      {
        field: "mfa_enabled",
        value: String(mfaEnabled),
      },
      {
        field: "has_setup_secret",
        value: String(Boolean(setup?.secret)),
      },
    ];
    backupCodes.forEach((c, i) => {
      rows.push({ field: `backup_${i + 1}`, value: c });
    });
    return rows;
  }, [backupCodes, me?.email, mfaEnabled, setup?.secret, user?.email]);

  async function onBeginSetup() {
    if (!session) return;
    setBusy(true);
    setError(null);
    setProgress(55);
    try {
      const result = await setupMfa(session);
      setSetup(result);
      setBackupCodes([]);
      setLastAction("setup");
      push({ message: t("accountMfa.setupStarted") });
      setProgress(100);
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      setError(msg);
      push({ message: `${t("accountMfa.setupFailed")}: ${msg}` });
      setProgress(100);
    } finally {
      setBusy(false);
    }
  }

  async function onVerify() {
    if (!session || code.trim().length < 6) return;
    setBusy(true);
    setError(null);
    setProgress(70);
    try {
      const result = await verifyMfaSetup(session, code.trim());
      setBackupCodes(result.backup_codes ?? []);
      setMe((prev) => (prev ? { ...prev, mfa_enabled: true } : prev));
      setSetup(null);
      setCode("");
      try {
        localStorage.removeItem(DRAFT_KEY);
      } catch {
        /* ignore */
      }
      setLastAction("verify");
      push({ message: t("accountMfa.verifyOk") });
      await reloadUser();
      setProgress(100);
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      setError(msg);
      push({ message: `${t("accountMfa.verifyFailed")}: ${msg}` });
      setProgress(100);
    } finally {
      setBusy(false);
    }
  }

  async function onCopy(text: string, label: string) {
    try {
      await navigator.clipboard.writeText(text);
      setLastAction(`copy:${label}`);
      push({ message: t("accountMfa.copied") });
    } catch {
      push({ message: t("accountMfa.copyFailed") });
    }
  }

  if (isLoading || !isAuthenticated) return null;

  return (
    <PageLayout
      title={t("accountSecurity.mod.mfa")}
      subtitle={t("accountMfa.subtitle")}
      breadcrumb={[
        { label: t("app.name"), href: "/" },
        { label: t("accountSecurity.breadcrumb"), href: "/account/security" },
        { label: t("accountSecurity.mod.mfa") },
      ]}
      actions={
        <>
          <ExportButton
            label={t("common.export")}
            rows={exportRows}
            filename="account-mfa-enrollment.csv"
          />
          <PrintButton label={t("common.print")} />
          <Link className="mp-btn" href="/account/security">
            {t("accountSecurity.back")}
          </Link>
          <button
            type="button"
            className="mp-btn"
            disabled={busy || loading}
            onClick={() => void loadMe()}
          >
            {t("accountMfa.refresh")}
          </button>
        </>
      }
    >
      <ProgressBar
        value={progress}
        label={loading ? t("accountMfa.loading") : t("accountMfa.ready")}
      />

      <div className="mfa-layout">
        <aside className="mfa-aside" aria-label={t("accountMfa.rail")}>
          <section className="mfa-panel-card">
            <header className="mfa-panel-head">
              <h2>{t("accountMfa.workflow")}</h2>
            </header>
            <div className="mfa-panel-body">
              <StepProgress steps={workflowSteps} current={lifecycleStep} />
              {draftSaving ? (
                <p className="mp-field-help" aria-live="polite">
                  {t("accountMfa.draftSaved")}…
                </p>
              ) : (
                <p className="mp-field-help">{t("accountMfa.workflowHint")}</p>
              )}
            </div>
          </section>

          <section className="mfa-panel-card">
            <header className="mfa-panel-head">
              <h2>{t("accountMfa.rail.status")}</h2>
            </header>
            <div className="mfa-panel-body">
              <div className="mfa-status-row">
                <span>{t("dashboard.email")}</span>
                <strong>{me?.email ?? user?.email ?? "—"}</strong>
              </div>
              <div className="mfa-status-row">
                <span>{t("accountMfa.status")}</span>
                <Chip status={mfaEnabled ? "enabled" : setup ? "setup" : "disabled"} />
              </div>
              {lastAction ? (
                <p className="mp-field-help">
                  {t("accountSecurity.lastAction")}: {lastAction}
                </p>
              ) : null}
            </div>
          </section>
        </aside>

        <div className="mfa-main">
          {error ? (
            <p className="mp-error" role="alert">
              {error}
            </p>
          ) : null}

          {mfaEnabled && backupCodes.length === 0 ? (
            <EmptyState
              title={t("accountMfa.alreadyEnabled")}
              description={t("accountMfa.alreadyEnabledHint")}
              action={
                <Link className="mp-btn mp-btn-primary" href="/account/security">
                  {t("accountSecurity.back")}
                </Link>
              }
            />
          ) : null}

          {!mfaEnabled || backupCodes.length > 0 ? (
            <>
              <section aria-labelledby="mfa-enroll-heading">
                <h2 id="mfa-enroll-heading">{t("accountMfa.enrollTitle")}</h2>
                <p className="mfa-muted">{t("accountMfa.enrollHint")}</p>
                {!setup && !mfaEnabled ? (
                  <button
                    type="button"
                    className="mp-btn mp-btn-primary"
                    disabled={busy || loading || !session}
                    onClick={() => void onBeginSetup()}
                  >
                    {t("accountMfa.beginSetup")}
                  </button>
                ) : null}
              </section>

              {setup ? (
                <section
                  className="mfa-detail-panel mp-animate-in"
                  aria-labelledby="mfa-secret-heading"
                >
                  <h2 id="mfa-secret-heading">{t("accountMfa.secretTitle")}</h2>
                  <p className="mfa-muted">{t("accountMfa.secretHint")}</p>
                  <div className="mfa-secret-box">
                    <code aria-label={t("accountMfa.secretLabel")}>
                      {showSecret ? setup.secret : "••••••••••••••••"}
                    </code>
                    <div className="mfa-actions-row">
                      <button
                        type="button"
                        className="mp-btn"
                        onClick={() => setShowSecret((v) => !v)}
                      >
                        {showSecret ? t("accountMfa.hideSecret") : t("accountMfa.showSecret")}
                      </button>
                      <button
                        type="button"
                        className="mp-btn"
                        onClick={() => void onCopy(setup.secret, "secret")}
                      >
                        {t("accountMfa.copySecret")}
                      </button>
                      <button
                        type="button"
                        className="mp-btn"
                        onClick={() => void onCopy(setup.provisioning_uri, "uri")}
                      >
                        {t("accountMfa.copyUri")}
                      </button>
                    </div>
                  </div>
                  <p className="mp-field-help mfa-uri">{t("accountMfa.uriLabel")}</p>
                  <code className="mfa-uri-value">{setup.provisioning_uri}</code>

                  <label className="mfa-code-field" htmlFor="mfa-totp-code">
                    {t("accountMfa.codeLabel")}
                    <input
                      id="mfa-totp-code"
                      inputMode="numeric"
                      autoComplete="one-time-code"
                      maxLength={8}
                      value={code}
                      onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 8))}
                      placeholder="000000"
                    />
                  </label>
                  <button
                    type="button"
                    className="mp-btn mp-btn-primary"
                    disabled={busy || code.trim().length < 6}
                    onClick={() => void onVerify()}
                  >
                    {t("accountMfa.verify")}
                  </button>
                </section>
              ) : null}

              {backupCodes.length > 0 ? (
                <section
                  className="mfa-detail-panel mp-animate-in"
                  aria-labelledby="mfa-backup-heading"
                >
                  <h2 id="mfa-backup-heading">{t("accountMfa.backupTitle")}</h2>
                  <p className="mfa-muted">{t("accountMfa.backupHint")}</p>
                  <ul className="mfa-backup-list">
                    {backupCodes.map((c) => (
                      <li key={c}>
                        <code>{c}</code>
                      </li>
                    ))}
                  </ul>
                  <button
                    type="button"
                    className="mp-btn"
                    onClick={() => void onCopy(backupCodes.join("\n"), "backup")}
                  >
                    {t("accountMfa.copyBackup")}
                  </button>
                </section>
              ) : null}
            </>
          ) : null}
        </div>
      </div>

      <style jsx>{`
        .mfa-layout {
          display: grid;
          grid-template-columns: minmax(220px, 280px) 1fr;
          gap: 1.25rem;
          margin-top: 1rem;
        }
        .mfa-aside {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .mfa-main {
          display: flex;
          flex-direction: column;
          gap: 1.25rem;
        }
        .mfa-panel-card {
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: 0.5rem;
          background: var(--mp-surface, #fff);
        }
        .mfa-panel-head {
          padding: 0.75rem 1rem;
          border-bottom: 1px solid var(--mp-border, #d8dee6);
        }
        .mfa-panel-head h2 {
          margin: 0;
          font-size: 0.95rem;
        }
        .mfa-panel-body {
          padding: 0.85rem 1rem;
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
        }
        .mfa-status-row {
          display: flex;
          justify-content: space-between;
          gap: 0.5rem;
          font-size: 0.85rem;
        }
        .mfa-muted {
          color: var(--mp-muted, #667085);
          margin: 0 0 0.75rem;
        }
        .mfa-detail-panel {
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: 0.5rem;
          padding: 1rem 1.1rem;
          background: var(--mp-surface, #fff);
        }
        .mfa-detail-panel h2 {
          margin: 0 0 0.35rem;
          font-size: 1.05rem;
        }
        .mfa-secret-box {
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
          margin: 0.75rem 0;
        }
        .mfa-secret-box code {
          font-size: 1.05rem;
          letter-spacing: 0.08em;
          padding: 0.65rem 0.75rem;
          background: var(--mp-bg-muted, #f4f6f8);
          border-radius: 0.35rem;
        }
        .mfa-actions-row {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .mfa-uri {
          margin-bottom: 0.25rem;
        }
        .mfa-uri-value {
          display: block;
          word-break: break-all;
          font-size: 0.75rem;
          margin-bottom: 1rem;
          opacity: 0.85;
        }
        .mfa-code-field {
          display: flex;
          flex-direction: column;
          gap: 0.35rem;
          margin-bottom: 0.85rem;
          font-size: 0.9rem;
        }
        .mfa-code-field input {
          max-width: 12rem;
          padding: 0.55rem 0.65rem;
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: 0.35rem;
          font-size: 1.1rem;
          letter-spacing: 0.2em;
        }
        .mfa-backup-list {
          list-style: none;
          margin: 0 0 0.85rem;
          padding: 0;
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(7rem, 1fr));
          gap: 0.45rem;
        }
        .mfa-backup-list code {
          display: block;
          padding: 0.4rem 0.5rem;
          background: var(--mp-bg-muted, #f4f6f8);
          border-radius: 0.3rem;
          text-align: center;
        }
        .mfa-chip {
          display: inline-flex;
          align-items: center;
          padding: 0.1rem 0.45rem;
          border-radius: 999px;
          font-size: 0.75rem;
          text-transform: lowercase;
        }
        .mfa-chip--ok {
          background: #e8f7ee;
          color: #067647;
        }
        .mfa-chip--warn {
          background: #fff4e5;
          color: #b54708;
        }
        .mfa-chip--bad {
          background: #fee4e2;
          color: #b42318;
        }
        .mfa-chip--muted {
          background: #f2f4f7;
          color: #475467;
        }
        @media (max-width: 900px) {
          .mfa-layout {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </PageLayout>
  );
}
