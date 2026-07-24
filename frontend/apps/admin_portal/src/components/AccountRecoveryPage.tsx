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
  changePassword,
  fetchIdentityMe,
  type IdentityMe,
} from "@/lib/identityMfaClient";

const DRAFT_KEY = "marpich.account.recovery.draft";

function Chip({ status }: { status: string }) {
  const tone =
    status === "ok" || status === "current" || status === "changed"
      ? "ok"
      : status === "required" || status === "pending"
        ? "warn"
        : status === "error"
          ? "bad"
          : "muted";
  return (
    <span className={`rcv-chip rcv-chip--${tone}`} data-status={status}>
      {status}
    </span>
  );
}

export function AccountRecoveryPage() {
  const router = useRouter();
  const { push } = useToast();
  const { t } = useLocale();
  const { isAuthenticated, isLoading, user, session, reloadUser } = useAuth();

  const [progress, setProgress] = useState(15);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [me, setMe] = useState<IdentityMe | null>(null);
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [revokeOthers, setRevokeOthers] = useState(true);
  const [lastChangedAt, setLastChangedAt] = useState<string | null>(null);
  const [lastAction, setLastAction] = useState<string | null>(null);
  const [draftReady, setDraftReady] = useState(false);

  const formDraft = useMemo(() => ({ revokeOthers }), [revokeOthers]);

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
        if (typeof parsed.revokeOthers === "boolean") setRevokeOthers(parsed.revokeOthers);
      }
    } catch {
      /* ignore */
    } finally {
      setDraftReady(true);
    }
  }, []);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace("/login?returnTo=/account/change-password");
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
      setLastChangedAt(profile.password_changed_at ?? null);
      setLastAction("me");
      setProgress(100);
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

  const mustChange = Boolean(me?.password_must_change);

  const lifecycleStep = useMemo(() => {
    if (lastAction === "changed") return 3;
    if (newPassword.length >= 8 && confirmPassword.length >= 8) return 2;
    if (currentPassword.length > 0) return 1;
    return 0;
  }, [confirmPassword.length, currentPassword.length, lastAction, newPassword.length]);

  const workflowSteps = useMemo(
    () => [
      { id: "current", label: t("accountRecovery.step.current") },
      { id: "new", label: t("accountRecovery.step.new") },
      { id: "confirm", label: t("accountRecovery.step.confirm") },
      { id: "done", label: t("accountRecovery.step.done") },
    ],
    [t],
  );

  const exportRows = useMemo(
    () => [
      { field: "email", value: me?.email ?? user?.email ?? "" },
      { field: "password_must_change", value: String(mustChange) },
      { field: "password_changed_at", value: lastChangedAt ?? "" },
      { field: "revoke_other_sessions_pref", value: String(revokeOthers) },
    ],
    [lastChangedAt, me?.email, mustChange, revokeOthers, user?.email],
  );

  const passwordsMatch = newPassword === confirmPassword;
  const canSubmit =
    Boolean(session) &&
    currentPassword.length > 0 &&
    newPassword.length >= 8 &&
    passwordsMatch &&
    currentPassword !== newPassword;

  async function onSubmit() {
    if (!session || !canSubmit) return;
    setBusy(true);
    setError(null);
    setProgress(70);
    try {
      const result = await changePassword(session, {
        current_password: currentPassword,
        new_password: newPassword,
        revoke_other_sessions: revokeOthers,
      });
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
      setLastChangedAt(result.password_changed_at ?? new Date().toISOString());
      setMe((prev) =>
        prev
          ? {
              ...prev,
              password_must_change: result.password_must_change,
              password_changed_at: result.password_changed_at,
            }
          : prev,
      );
      setLastAction("changed");
      push({
        message: result.other_sessions_revoked
          ? t("accountRecovery.changedWithRevoke")
          : t("accountRecovery.changedOk"),
      });
      await reloadUser();
      setProgress(100);
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      setError(msg);
      push({ message: `${t("accountRecovery.changedFailed")}: ${msg}` });
      setProgress(100);
    } finally {
      setBusy(false);
    }
  }

  if (isLoading || !isAuthenticated) return null;

  return (
    <PageLayout
      title={t("accountSecurity.mod.recovery")}
      subtitle={t("accountRecovery.subtitle")}
      breadcrumb={[
        { label: t("app.name"), href: "/" },
        { label: t("accountSecurity.breadcrumb"), href: "/account/security" },
        { label: t("accountSecurity.mod.recovery") },
      ]}
      actions={
        <>
          <ExportButton
            label={t("common.export")}
            rows={exportRows}
            filename="account-recovery-status.csv"
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
            {t("accountRecovery.refresh")}
          </button>
        </>
      }
    >
      <ProgressBar
        value={progress}
        label={loading ? t("accountRecovery.loading") : t("accountRecovery.ready")}
      />

      <div className="rcv-layout">
        <aside className="rcv-aside" aria-label={t("accountRecovery.rail")}>
          <section className="rcv-panel-card">
            <header className="rcv-panel-head">
              <h2>{t("accountRecovery.workflow")}</h2>
            </header>
            <div className="rcv-panel-body">
              <StepProgress steps={workflowSteps} current={lifecycleStep} />
              {draftSaving ? (
                <p className="mp-field-help" aria-live="polite">
                  {t("accountRecovery.draftSaved")}…
                </p>
              ) : (
                <p className="mp-field-help">{t("accountRecovery.workflowHint")}</p>
              )}
            </div>
          </section>

          <section className="rcv-panel-card">
            <header className="rcv-panel-head">
              <h2>{t("accountRecovery.rail.status")}</h2>
            </header>
            <div className="rcv-panel-body">
              <div className="rcv-status-row">
                <span>{t("dashboard.email")}</span>
                <strong>{me?.email ?? user?.email ?? "—"}</strong>
              </div>
              <div className="rcv-status-row">
                <span>{t("accountRecovery.mustChange")}</span>
                <Chip status={mustChange ? "required" : "ok"} />
              </div>
              <div className="rcv-status-row">
                <span>{t("accountRecovery.lastChanged")}</span>
                <strong>{lastChangedAt ?? "—"}</strong>
              </div>
              {lastAction ? (
                <p className="mp-field-help">
                  {t("accountSecurity.lastAction")}: {lastAction}
                </p>
              ) : null}
            </div>
          </section>
        </aside>

        <div className="rcv-main">
          {error ? (
            <p className="mp-error" role="alert">
              {error}
            </p>
          ) : null}

          {mustChange ? (
            <EmptyState
              title={t("accountRecovery.mustChangeTitle")}
              description={t("accountRecovery.mustChangeHint")}
            />
          ) : null}

          <section
            className="rcv-detail-panel"
            aria-labelledby="rcv-form-heading"
          >
            <h2 id="rcv-form-heading">{t("accountRecovery.formTitle")}</h2>
            <p className="rcv-muted">{t("accountRecovery.formHint")}</p>

            <label className="rcv-field" htmlFor="rcv-current">
              {t("accountRecovery.currentPassword")}
              <input
                id="rcv-current"
                type="password"
                autoComplete="current-password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
              />
            </label>

            <label className="rcv-field" htmlFor="rcv-new">
              {t("accountRecovery.newPassword")}
              <input
                id="rcv-new"
                type="password"
                autoComplete="new-password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
            </label>

            <label className="rcv-field" htmlFor="rcv-confirm">
              {t("accountRecovery.confirmPassword")}
              <input
                id="rcv-confirm"
                type="password"
                autoComplete="new-password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </label>

            {!passwordsMatch && confirmPassword.length > 0 ? (
              <p className="mp-error" role="alert">
                {t("accountRecovery.mismatch")}
              </p>
            ) : null}

            <label className="rcv-check">
              <input
                type="checkbox"
                checked={revokeOthers}
                onChange={(e) => setRevokeOthers(e.target.checked)}
              />
              {t("accountRecovery.revokeOthers")}
            </label>
            <p className="mp-field-help">{t("accountRecovery.revokeHint")}</p>

            <div className="rcv-actions">
              <button
                type="button"
                className="mp-btn mp-btn-primary"
                disabled={busy || !canSubmit}
                onClick={() => void onSubmit()}
              >
                {t("accountRecovery.submit")}
              </button>
              <Link className="mp-btn" href="/account/mfa">
                {t("accountRecovery.openMfa")}
              </Link>
              <Link className="mp-btn" href="/account/passkeys">
                {t("accountRecovery.openPasskeys")}
              </Link>
            </div>
          </section>

          <section aria-labelledby="rcv-channels-heading">
            <h2 id="rcv-channels-heading">{t("accountRecovery.channelsTitle")}</h2>
            <EmptyState
              title={t("accountRecovery.channelsEmpty")}
              description={t("accountRecovery.channelsHint")}
            />
          </section>
        </div>
      </div>

      <style jsx>{`
        .rcv-layout {
          display: grid;
          grid-template-columns: minmax(220px, 280px) 1fr;
          gap: 1.25rem;
          margin-top: 1rem;
        }
        .rcv-aside {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .rcv-main {
          display: flex;
          flex-direction: column;
          gap: 1.25rem;
        }
        .rcv-panel-card {
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: 0.5rem;
          background: var(--mp-surface, #fff);
        }
        .rcv-panel-head {
          padding: 0.75rem 1rem;
          border-bottom: 1px solid var(--mp-border, #d8dee6);
        }
        .rcv-panel-head h2 {
          margin: 0;
          font-size: 0.95rem;
        }
        .rcv-panel-body {
          padding: 0.85rem 1rem;
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
        }
        .rcv-status-row {
          display: flex;
          justify-content: space-between;
          gap: 0.5rem;
          font-size: 0.85rem;
        }
        .rcv-muted {
          color: var(--mp-muted, #667085);
          margin: 0 0 0.75rem;
        }
        .rcv-detail-panel {
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: 0.5rem;
          padding: 1rem 1.1rem;
          background: var(--mp-surface, #fff);
        }
        .rcv-detail-panel h2 {
          margin: 0 0 0.35rem;
          font-size: 1.05rem;
        }
        .rcv-field {
          display: flex;
          flex-direction: column;
          gap: 0.35rem;
          margin-bottom: 0.85rem;
          max-width: 22rem;
          font-size: 0.9rem;
        }
        .rcv-field input {
          padding: 0.55rem 0.65rem;
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: 0.35rem;
        }
        .rcv-check {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.9rem;
          margin-top: 0.25rem;
        }
        .rcv-actions {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          margin-top: 1rem;
        }
        .rcv-chip {
          display: inline-flex;
          align-items: center;
          padding: 0.1rem 0.45rem;
          border-radius: 999px;
          font-size: 0.75rem;
          text-transform: lowercase;
        }
        .rcv-chip--ok {
          background: #e8f7ee;
          color: #067647;
        }
        .rcv-chip--warn {
          background: #fff4e5;
          color: #b54708;
        }
        .rcv-chip--bad {
          background: #fee4e2;
          color: #b42318;
        }
        .rcv-chip--muted {
          background: #f2f4f7;
          color: #475467;
        }
        @media (max-width: 900px) {
          .rcv-layout {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </PageLayout>
  );
}
