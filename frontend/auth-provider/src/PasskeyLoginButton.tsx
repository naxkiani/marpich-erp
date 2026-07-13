"use client";

import { useState } from "react";
import { loginWithPasskey, isWebAuthnSupported } from "./webauthn";

export type PasskeyLoginButtonProps = {
  tenantId: string;
  email: string;
  onSuccess?: () => void;
  className?: string;
};

export function PasskeyLoginButton({
  tenantId,
  email,
  onSuccess,
  className = "mp-btn",
}: PasskeyLoginButtonProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isWebAuthnSupported()) return null;

  async function onPasskeyLogin() {
    setLoading(true);
    setError(null);
    try {
      await loginWithPasskey({ tenantId, email, password: "", registerIfMissing: false });
      onSuccess?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Passkey login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mp-passkey-login">
      <button type="button" className={className} onClick={() => void onPasskeyLogin()} disabled={loading || !email}>
        {loading ? "Authenticating…" : "Sign in with passkey"}
      </button>
      {error ? (
        <p className="mp-auth-gate-error" role="alert">
          {error}
        </p>
      ) : null}
    </div>
  );
}
