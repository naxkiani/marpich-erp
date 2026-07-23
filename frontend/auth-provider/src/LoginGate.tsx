"use client";

import { useEffect, useState } from "react";
import { PasskeyLoginButton } from "./PasskeyLoginButton";
import { useLoginForm } from "./hooks";

export type LoginGateLabels = {
  tenant?: string;
  email?: string;
  password?: string;
  connect?: string;
  connecting?: string;
};

export type LoginGateProps = {
  title?: string;
  description?: string;
  defaultTenantId?: string;
  defaultEmail?: string;
  defaultPassword?: string;
  displayName?: string;
  onConnected?: () => void;
  className?: string;
  labels?: LoginGateLabels;
  /** Controlled values — when set with onChange*, parent owns draft persistence. */
  tenantId?: string;
  email?: string;
  password?: string;
  onTenantIdChange?: (value: string) => void;
  onEmailChange?: (value: string) => void;
  onPasswordChange?: (value: string) => void;
};

export function LoginGate({
  title = "Connect to API",
  description,
  defaultTenantId,
  defaultEmail,
  defaultPassword,
  displayName,
  onConnected,
  className = "mp-auth-gate",
  labels,
  tenantId: controlledTenant,
  email: controlledEmail,
  password: controlledPassword,
  onTenantIdChange,
  onEmailChange,
  onPasswordChange,
}: LoginGateProps) {
  const {
    submit,
    isLoading,
    error,
    defaultTenantId: tenantDefault,
    defaultEmail: emailDefault,
    defaultPassword: passwordDefault,
  } = useLoginForm({
    defaultTenantId,
    defaultEmail,
    defaultPassword,
    displayName,
    onSuccess: onConnected,
  });

  const [localTenantId, setLocalTenantId] = useState(tenantDefault);
  const [localEmail, setLocalEmail] = useState(emailDefault);
  const [localPassword, setLocalPassword] = useState(passwordDefault);

  const tenantId = controlledTenant ?? localTenantId;
  const email = controlledEmail ?? localEmail;
  const password = controlledPassword ?? localPassword;

  useEffect(() => {
    if (controlledTenant === undefined) setLocalTenantId(tenantDefault);
  }, [controlledTenant, tenantDefault]);

  useEffect(() => {
    if (controlledEmail === undefined) setLocalEmail(emailDefault);
  }, [controlledEmail, emailDefault]);

  async function onConnect() {
    await submit(tenantId, email, password);
  }

  return (
    <section className={className} aria-labelledby="auth-gate-heading">
      <h2 id="auth-gate-heading">{title}</h2>
      {description ? <p className="mp-auth-gate-desc">{description}</p> : null}
      <div className="mp-auth-gate-form">
        <label>
          {labels?.tenant ?? "Tenant ID"}
          <input
            className="mp-input"
            value={tenantId}
            onChange={(e) => {
              const v = e.target.value;
              onTenantIdChange?.(v);
              if (controlledTenant === undefined) setLocalTenantId(v);
            }}
            autoComplete="organization"
          />
        </label>
        <label>
          {labels?.email ?? "Email"}
          <input
            className="mp-input"
            type="email"
            value={email}
            onChange={(e) => {
              const v = e.target.value;
              onEmailChange?.(v);
              if (controlledEmail === undefined) setLocalEmail(v);
            }}
            autoComplete="username"
          />
        </label>
        <label>
          {labels?.password ?? "Password"}
          <input
            className="mp-input"
            type="password"
            value={password}
            onChange={(e) => {
              const v = e.target.value;
              onPasswordChange?.(v);
              if (controlledPassword === undefined) setLocalPassword(v);
            }}
            autoComplete="current-password"
          />
        </label>
        <button
          type="button"
          className="mp-btn mp-btn-primary"
          onClick={() => void onConnect()}
          disabled={isLoading}
        >
          {isLoading ? (labels?.connecting ?? "Connecting…") : (labels?.connect ?? "Connect")}
        </button>
        <PasskeyLoginButton tenantId={tenantId} email={email} onSuccess={onConnected} />
      </div>
      {error ? (
        <p className="mp-auth-gate-error" role="alert">
          {error}
        </p>
      ) : null}
    </section>
  );
}
