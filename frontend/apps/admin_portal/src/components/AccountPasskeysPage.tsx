"use client";

import { PageLayout } from "@marpich/core";
import {
  DataTable,
  EmptyState,
  ExportButton,
  PrintButton,
  ProgressBar,
  StepProgress,
  useAutosave,
  useLocale,
  useToast,
} from "@marpich/shared";
import {
  isWebAuthnSupported,
  listPasskeys,
  registerPasskey,
  revokePasskey,
  useAuth,
  type PasskeyCredential,
} from "@marpich/auth-provider";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useMemo, useState } from "react";

const DRAFT_KEY = "marpich.account.passkeys.draft";

function Chip({ status }: { status: string }) {
  const tone =
    status === "active" || status === "ok" || status === "supported"
      ? "ok"
      : status === "pending" || status === "unsupported"
        ? "warn"
        : status === "error" || status === "revoked"
          ? "bad"
          : "muted";
  return (
    <span className={`pk-chip pk-chip--${tone}`} data-status={status}>
      {status}
    </span>
  );
}

export function AccountPasskeysPage() {
  const router = useRouter();
  const { push } = useToast();
  const { t } = useLocale();
  const { isAuthenticated, isLoading, user, session } = useAuth();

  const [progress, setProgress] = useState(15);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [credentials, setCredentials] = useState<PasskeyCredential[]>([]);
  const [selectedRef, setSelectedRef] = useState("");
  const [nickname, setNickname] = useState("Passkey");
  const [lastAction, setLastAction] = useState<string | null>(null);
  const [draftReady, setDraftReady] = useState(false);
  const [webauthnOk, setWebauthnOk] = useState(false);

  const formDraft = useMemo(() => ({ nickname }), [nickname]);

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
        if (typeof parsed.nickname === "string" && parsed.nickname.trim()) {
          setNickname(parsed.nickname.trim().slice(0, 64));
        }
      }
    } catch {
      /* ignore */
    } finally {
      setDraftReady(true);
      setWebauthnOk(isWebAuthnSupported());
    }
  }, []);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace("/login?returnTo=/account/passkeys");
    }
  }, [isAuthenticated, isLoading, router]);

  const loadCredentials = useCallback(async () => {
    if (!session) return;
    setLoading(true);
    setError(null);
    setProgress(40);
    try {
      const rows = await listPasskeys(session);
      setCredentials(rows);
      setSelectedRef((prev) => {
        if (prev && rows.some((r) => r.credential_ref === prev)) return prev;
        return rows[0]?.credential_ref ?? "";
      });
      setLastAction("list");
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
      void loadCredentials();
    }
  }, [isAuthenticated, loadCredentials, session]);

  const selected = useMemo(
    () => credentials.find((c) => c.credential_ref === selectedRef) ?? null,
    [credentials, selectedRef],
  );

  const lifecycleStep = useMemo(() => {
    if (credentials.length > 0 && lastAction === "register") return 3;
    if (credentials.length > 0) return 2;
    if (webauthnOk) return 1;
    return 0;
  }, [credentials.length, lastAction, webauthnOk]);

  const workflowSteps = useMemo(
    () => [
      { id: "support", label: t("accountPasskeys.step.support") },
      { id: "register", label: t("accountPasskeys.step.register") },
      { id: "manage", label: t("accountPasskeys.step.manage") },
      { id: "ready", label: t("accountPasskeys.step.ready") },
    ],
    [t],
  );

  const exportRows = useMemo(
    () =>
      credentials.map((c) => ({
        credential_ref: c.credential_ref,
        nickname: c.nickname,
        sign_count: String(c.sign_count),
        created_at: c.created_at,
        last_used_at: c.last_used_at ?? "",
      })),
    [credentials],
  );

  const tableRows = useMemo(
    () =>
      credentials.map((c) => ({
        id: c.credential_ref,
        nickname: c.nickname,
        credential_ref: c.credential_ref,
        sign_count: String(c.sign_count),
        created_at: c.created_at,
      })),
    [credentials],
  );

  async function onRegister() {
    if (!session) return;
    setBusy(true);
    setError(null);
    setProgress(55);
    try {
      const created = await registerPasskey(session, nickname.trim() || "Passkey");
      setCredentials((prev) => [created, ...prev]);
      setSelectedRef(created.credential_ref);
      setLastAction("register");
      push({ message: t("accountPasskeys.registerOk") });
      setProgress(100);
      await loadCredentials();
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      setError(msg);
      push({ message: `${t("accountPasskeys.registerFailed")}: ${msg}` });
      setProgress(100);
    } finally {
      setBusy(false);
    }
  }

  async function onRevoke(ref: string) {
    if (!session) return;
    setBusy(true);
    setError(null);
    setProgress(70);
    try {
      await revokePasskey(session, ref);
      setCredentials((prev) => prev.filter((c) => c.credential_ref !== ref));
      if (selectedRef === ref) setSelectedRef("");
      setLastAction("revoke");
      push({ message: t("accountPasskeys.revokeOk") });
      setProgress(100);
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      setError(msg);
      push({ message: `${t("accountPasskeys.revokeFailed")}: ${msg}` });
      setProgress(100);
    } finally {
      setBusy(false);
    }
  }

  if (isLoading || !isAuthenticated) return null;

  return (
    <PageLayout
      title={t("accountSecurity.mod.passkeys")}
      subtitle={t("accountPasskeys.subtitle")}
      breadcrumb={[
        { label: t("app.name"), href: "/" },
        { label: t("accountSecurity.breadcrumb"), href: "/account/security" },
        { label: t("accountSecurity.mod.passkeys") },
      ]}
      actions={
        <>
          <ExportButton
            label={t("common.export")}
            rows={exportRows}
            filename="account-passkeys.csv"
          />
          <PrintButton label={t("common.print")} />
          <Link className="mp-btn" href="/account/security">
            {t("accountSecurity.back")}
          </Link>
          <button
            type="button"
            className="mp-btn"
            disabled={busy || loading}
            onClick={() => void loadCredentials()}
          >
            {t("accountPasskeys.refresh")}
          </button>
        </>
      }
    >
      <ProgressBar
        value={progress}
        label={loading ? t("accountPasskeys.loading") : t("accountPasskeys.ready")}
      />

      <div className="pk-layout">
        <aside className="pk-aside" aria-label={t("accountPasskeys.rail")}>
          <section className="pk-panel-card">
            <header className="pk-panel-head">
              <h2>{t("accountPasskeys.workflow")}</h2>
            </header>
            <div className="pk-panel-body">
              <StepProgress steps={workflowSteps} current={lifecycleStep} />
              {draftSaving ? (
                <p className="mp-field-help" aria-live="polite">
                  {t("accountPasskeys.draftSaved")}…
                </p>
              ) : (
                <p className="mp-field-help">{t("accountPasskeys.workflowHint")}</p>
              )}
            </div>
          </section>

          <section className="pk-panel-card">
            <header className="pk-panel-head">
              <h2>{t("accountPasskeys.rail.status")}</h2>
            </header>
            <div className="pk-panel-body">
              <div className="pk-status-row">
                <span>{t("dashboard.email")}</span>
                <strong>{user?.email ?? "—"}</strong>
              </div>
              <div className="pk-status-row">
                <span>{t("accountPasskeys.webauthn")}</span>
                <Chip status={webauthnOk ? "supported" : "unsupported"} />
              </div>
              <div className="pk-status-row">
                <span>{t("accountPasskeys.count")}</span>
                <strong>{credentials.length}</strong>
              </div>
              {lastAction ? (
                <p className="mp-field-help">
                  {t("accountSecurity.lastAction")}: {lastAction}
                </p>
              ) : null}
            </div>
          </section>
        </aside>

        <div className="pk-main">
          {error ? (
            <p className="mp-error" role="alert">
              {error}
            </p>
          ) : null}

          {!webauthnOk ? (
            <EmptyState
              title={t("accountPasskeys.unsupported")}
              description={t("accountPasskeys.unsupportedHint")}
            />
          ) : (
            <section aria-labelledby="pk-register-heading">
              <h2 id="pk-register-heading">{t("accountPasskeys.registerTitle")}</h2>
              <p className="pk-muted">{t("accountPasskeys.registerHint")}</p>
              <label className="pk-nick-field" htmlFor="pk-nickname">
                {t("accountPasskeys.nickname")}
                <input
                  id="pk-nickname"
                  value={nickname}
                  maxLength={64}
                  onChange={(e) => setNickname(e.target.value.slice(0, 64))}
                />
              </label>
              <button
                type="button"
                className="mp-btn mp-btn-primary"
                disabled={busy || loading || !session}
                onClick={() => void onRegister()}
              >
                {t("accountPasskeys.register")}
              </button>
            </section>
          )}

          <section aria-labelledby="pk-list-heading">
            <h2 id="pk-list-heading">{t("accountPasskeys.listTitle")}</h2>
            {credentials.length === 0 && !loading ? (
              <EmptyState
                title={t("accountPasskeys.empty")}
                description={t("accountPasskeys.emptyHint")}
              />
            ) : (
              <DataTable
                columns={[
                  { key: "nickname", header: t("accountPasskeys.col.nickname"), sortable: true },
                  { key: "credential_ref", header: t("accountPasskeys.col.ref"), sortable: true },
                  { key: "sign_count", header: t("accountPasskeys.col.signCount"), sortable: true },
                  { key: "created_at", header: t("accountPasskeys.col.created"), sortable: true },
                ]}
                rows={tableRows}
                selectable
                onSelectionChange={(ids) => {
                  if (ids[0]) setSelectedRef(ids[0]);
                }}
              />
            )}

            {selected ? (
              <section
                className="pk-detail-panel mp-animate-in"
                aria-label={t("accountPasskeys.detail")}
              >
                <header>{selected.nickname}</header>
                <p className="pk-muted">
                  {t("accountPasskeys.col.ref")}: {selected.credential_ref}
                </p>
                <p className="pk-muted">
                  {t("accountPasskeys.col.created")}: {selected.created_at}
                </p>
                <p className="pk-muted">
                  {t("accountPasskeys.col.lastUsed")}: {selected.last_used_at ?? "—"}
                </p>
                <button
                  type="button"
                  className="mp-btn"
                  disabled={busy}
                  onClick={() => void onRevoke(selected.credential_ref)}
                >
                  {t("accountPasskeys.revoke")}
                </button>
              </section>
            ) : null}
          </section>
        </div>
      </div>

      <style jsx>{`
        .pk-layout {
          display: grid;
          grid-template-columns: minmax(220px, 280px) 1fr;
          gap: 1.25rem;
          margin-top: 1rem;
        }
        .pk-aside {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .pk-main {
          display: flex;
          flex-direction: column;
          gap: 1.25rem;
        }
        .pk-panel-card {
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: 0.5rem;
          background: var(--mp-surface, #fff);
        }
        .pk-panel-head {
          padding: 0.75rem 1rem;
          border-bottom: 1px solid var(--mp-border, #d8dee6);
        }
        .pk-panel-head h2 {
          margin: 0;
          font-size: 0.95rem;
        }
        .pk-panel-body {
          padding: 0.85rem 1rem;
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
        }
        .pk-status-row {
          display: flex;
          justify-content: space-between;
          gap: 0.5rem;
          font-size: 0.85rem;
        }
        .pk-muted {
          color: var(--mp-muted, #667085);
          margin: 0 0 0.5rem;
        }
        .pk-nick-field {
          display: flex;
          flex-direction: column;
          gap: 0.35rem;
          margin-bottom: 0.85rem;
          max-width: 20rem;
          font-size: 0.9rem;
        }
        .pk-nick-field input {
          padding: 0.55rem 0.65rem;
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: 0.35rem;
        }
        .pk-detail-panel {
          margin-top: 1rem;
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: 0.5rem;
          padding: 1rem 1.1rem;
          background: var(--mp-surface, #fff);
        }
        .pk-detail-panel header {
          font-weight: 600;
          margin-bottom: 0.35rem;
        }
        .pk-chip {
          display: inline-flex;
          align-items: center;
          padding: 0.1rem 0.45rem;
          border-radius: 999px;
          font-size: 0.75rem;
          text-transform: lowercase;
        }
        .pk-chip--ok {
          background: #e8f7ee;
          color: #067647;
        }
        .pk-chip--warn {
          background: #fff4e5;
          color: #b54708;
        }
        .pk-chip--bad {
          background: #fee4e2;
          color: #b42318;
        }
        .pk-chip--muted {
          background: #f2f4f7;
          color: #475467;
        }
        @media (max-width: 900px) {
          .pk-layout {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </PageLayout>
  );
}
