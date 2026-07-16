"use client";

import { useState } from "react";
import { PasskeyLoginButton } from "./PasskeyLoginButton";
import { useLoginForm } from "./hooks";

export type LoginGateProps = {
  title?: string;
  description?: string;
  defaultTenantId?: string;
  defaultEmail?: string;
  defaultPassword?: string;
  displayName?: string;
  onConnected?: () => void;
  className?: string;
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
}: LoginGateProps) {
  const { submit, isLoading, error, defaultTenantId: tenantDefault, defaultEmail: emailDefault, defaultPassword: passwordDefault } =
    useLoginForm({
      defaultTenantId,
      defaultEmail,
      defaultPassword,
      displayName,
      onSuccess: onConnected,
    });

  const [tenantId, setTenantId] = useState(tenantDefault);
  const [email, setEmail] = useState(emailDefault);
  const [password, setPassword] = useState(passwordDefault);

  async function onConnect() {
    await submit(tenantId, email, password);
  }

  return (
    <section className={className} aria-labelledby="auth-gate-heading">
      <h2 id="auth-gate-heading">{title}</h2>
      {description ? <p className="mp-auth-gate-desc">{description}</p> : null}
      <div className="mp-auth-gate-form">
        <label>
          Tenant ID
          <input className="mp-input" value={tenantId} onChange={(e) => setTenantId(e.target.value)} />
        </label>
        <label>
          Email
          <input className="mp-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label>
          Password
          <input className="mp-input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <button type="button" className="mp-btn mp-btn-primary" onClick={() => void onConnect()} disabled={isLoading}>
          {isLoading ? "Connecting…" : "Connect"}
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
