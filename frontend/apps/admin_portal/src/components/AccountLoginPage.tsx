"use client";

import { LoginGate, useAuth } from "@marpich/auth-provider";
import { PageLayout } from "@marpich/core";
import {
  ProgressBar,
  StepProgress,
  useAutosave,
  useLocale,
} from "@marpich/shared";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useCallback, useEffect, useMemo, useState } from "react";

const DRAFT_KEY = "marpich.account.login.draft";

export function AccountLoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { t } = useLocale();
  const { isAuthenticated, isLoading } = useAuth();

  const returnTo = searchParams.get("returnTo") ?? "/";
  const safeReturnTo = returnTo.startsWith("/") ? returnTo : "/";

  const [progress, setProgress] = useState(20);
  const [draftReady, setDraftReady] = useState(false);
  const [tenantId, setTenantId] = useState("platform-demo");
  const [email, setEmail] = useState("platform@demo.dev");
  const [password, setPassword] = useState("SecurePass123!");
  const [lastAction, setLastAction] = useState<string | null>(null);

  const formDraft = useMemo(() => ({ tenantId, email }), [email, tenantId]);

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
        if (typeof parsed.tenantId === "string" && parsed.tenantId.trim()) {
          setTenantId(parsed.tenantId.trim());
        }
        if (typeof parsed.email === "string" && parsed.email.trim()) {
          setEmail(parsed.email.trim());
        }
      }
    } catch {
      /* ignore */
    } finally {
      setDraftReady(true);
      setProgress(60);
    }
  }, []);

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      setProgress(100);
      setLastAction("redirect");
      router.replace(safeReturnTo);
    } else if (!isLoading) {
      setProgress(100);
    }
  }, [isAuthenticated, isLoading, router, safeReturnTo]);

  const lifecycleStep = useMemo(() => {
    if (isAuthenticated) return 3;
    if (password.length > 0 && email.includes("@") && tenantId.trim()) return 2;
    if (email.includes("@") || tenantId.trim()) return 1;
    return 0;
  }, [email, isAuthenticated, password.length, tenantId]);

  const workflowSteps = useMemo(
    () => [
      { id: "identity", label: t("login.step.identity") },
      { id: "credentials", label: t("login.step.credentials") },
      { id: "authenticate", label: t("login.step.authenticate") },
      { id: "enter", label: t("login.step.enter") },
    ],
    [t],
  );

  return (
    <PageLayout
      title={t("login.title")}
      subtitle={t("login.subtitle")}
      breadcrumb={[
        { label: t("app.name"), href: "/" },
        { label: t("login.title") },
      ]}
      actions={
        <>
          <Link className="mp-btn" href="/account/security">
            {t("nav.mySecurity")}
          </Link>
          <Link className="mp-btn" href="/account/passkeys">
            {t("accountSecurity.mod.passkeys")}
          </Link>
        </>
      }
    >
      <ProgressBar
        value={progress}
        label={isLoading ? t("login.loading") : t("login.ready")}
      />

      <div className="login-layout">
        <aside className="login-aside" aria-label={t("login.rail")}>
          <section className="login-panel-card">
            <header className="login-panel-head">
              <h2>{t("login.workflow")}</h2>
            </header>
            <div className="login-panel-body">
              <StepProgress steps={workflowSteps} current={lifecycleStep} />
              {draftSaving ? (
                <p className="mp-field-help" aria-live="polite">
                  {t("login.draftSaved")}…
                </p>
              ) : (
                <p className="mp-field-help">{t("login.workflowHint")}</p>
              )}
              {lastAction ? (
                <p className="mp-field-help">
                  {t("login.lastAction")}: {lastAction}
                </p>
              ) : null}
            </div>
          </section>

          <section className="login-panel-card">
            <header className="login-panel-head">
              <h2>{t("login.rail.help")}</h2>
            </header>
            <div className="login-panel-body">
              <p className="mp-field-help">{t("login.helpHint")}</p>
              <Link className="mp-btn" href="/account/mfa">
                {t("accountSecurity.mod.mfa")}
              </Link>
            </div>
          </section>
        </aside>

        <div className="login-main">
          <p className="login-desc">{t("login.pageDesc")}</p>
          <LoginGate
            title={t("login.gateTitle")}
            description={t("login.gateDesc")}
            defaultTenantId={tenantId}
            defaultEmail={email}
            defaultPassword={password}
            displayName="Platform Admin"
            tenantId={tenantId}
            email={email}
            password={password}
            onTenantIdChange={setTenantId}
            onEmailChange={setEmail}
            onPasswordChange={setPassword}
            labels={{
              tenant: t("login.field.tenant"),
              email: t("login.field.email"),
              password: t("login.field.password"),
              connect: t("login.connect"),
              connecting: t("login.connecting"),
            }}
            onConnected={() => {
              setLastAction("connected");
              setProgress(100);
              router.replace(safeReturnTo);
            }}
          />
        </div>
      </div>

      <style jsx>{`
        .login-layout {
          display: grid;
          grid-template-columns: minmax(220px, 280px) minmax(0, 28rem);
          gap: 1.25rem;
          margin-top: 1rem;
          align-items: start;
        }
        .login-aside {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .login-panel-card {
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: 0.5rem;
          background: var(--mp-surface, #fff);
        }
        .login-panel-head {
          padding: 0.75rem 1rem;
          border-bottom: 1px solid var(--mp-border, #d8dee6);
        }
        .login-panel-head h2 {
          margin: 0;
          font-size: 0.95rem;
        }
        .login-panel-body {
          padding: 0.85rem 1rem;
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
        }
        .login-desc {
          color: var(--mp-muted, #667085);
          margin: 0 0 1rem;
          line-height: 1.45;
        }
        .login-main {
          min-width: 0;
        }
        @media (max-width: 900px) {
          .login-layout {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </PageLayout>
  );
}
