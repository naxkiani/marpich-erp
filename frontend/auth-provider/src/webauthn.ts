import { API_URL } from "./config";
import { saveSession, tenantHeaders } from "./session";
import type { AuthSession, LoginCredentials } from "./types";

type TokenPayload = {
  access_token: string;
  refresh_token?: string;
  expires_in?: number;
};

function sessionFromTokens(tenantId: string, tokens: TokenPayload): AuthSession {
  const expiresAt = tokens.expires_in ? Date.now() + tokens.expires_in * 1000 : undefined;
  return {
    tenantId,
    accessToken: tokens.access_token,
    refreshToken: tokens.refresh_token,
    expiresAt,
  };
}

export async function beginPasskeyLogin(tenantId: string, email: string): Promise<{
  challenge_id: string;
  options: PublicKeyCredentialRequestOptionsJSON;
}> {
  const res = await fetch(`${API_URL}/api/v1/authentication/webauthn/login/options`, {
    method: "POST",
    headers: tenantHeaders(tenantId),
    body: JSON.stringify({ email }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? "Failed to begin passkey login");
  }
  return (await res.json()).data;
}

export async function completePasskeyLogin(
  tenantId: string,
  challengeId: string,
  credential: AuthenticationCredentialJSON,
): Promise<AuthSession> {
  const res = await fetch(`${API_URL}/api/v1/authentication/webauthn/login/verify`, {
    method: "POST",
    headers: tenantHeaders(tenantId),
    body: JSON.stringify({ challenge_id: challengeId, credential }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? "Passkey verification failed");
  }
  const json = await res.json();
  const session = sessionFromTokens(tenantId, json.data as TokenPayload);
  saveSession(session);
  return session;
}

export type PublicKeyCredentialRequestOptionsJSON = {
  challenge: string;
  timeout?: number;
  rpId?: string;
  allowCredentials?: Array<{ id: string; type: string; transports?: string[] }>;
  userVerification?: UserVerificationRequirement;
};

export type AuthenticationCredentialJSON = {
  id: string;
  rawId: string;
  type: string;
  response: {
    authenticatorData: string;
    clientDataJSON: string;
    signature: string;
    userHandle?: string;
  };
};

function base64URLToBuffer(base64URL: string): ArrayBuffer {
  const base64 = base64URL.replace(/-/g, "+").replace(/_/g, "/");
  const pad = base64.length % 4 === 0 ? "" : "=".repeat(4 - (base64.length % 4));
  const binary = atob(base64 + pad);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
  return bytes.buffer;
}

function bufferToBase64URL(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer);
  let binary = "";
  for (let i = 0; i < bytes.length; i += 1) binary += String.fromCharCode(bytes[i]);
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

function toRequestOptions(options: PublicKeyCredentialRequestOptionsJSON): PublicKeyCredentialRequestOptions {
  return {
    ...options,
    challenge: base64URLToBuffer(options.challenge),
    allowCredentials: options.allowCredentials?.map((cred) => ({
      type: cred.type as PublicKeyCredentialType,
      id: base64URLToBuffer(cred.id),
      transports: cred.transports as AuthenticatorTransport[] | undefined,
    })),
  };
}

function credentialToJSON(credential: PublicKeyCredential): AuthenticationCredentialJSON {
  const response = credential.response as AuthenticatorAssertionResponse;
  return {
    id: credential.id,
    rawId: bufferToBase64URL(credential.rawId),
    type: credential.type,
    response: {
      authenticatorData: bufferToBase64URL(response.authenticatorData),
      clientDataJSON: bufferToBase64URL(response.clientDataJSON),
      signature: bufferToBase64URL(response.signature),
      userHandle: response.userHandle ? bufferToBase64URL(response.userHandle) : undefined,
    },
  };
}

export async function loginWithPasskey(credentials: LoginCredentials): Promise<AuthSession> {
  const { tenantId, email } = credentials;
  if (!email) throw new Error("Email is required for passkey login");
  if (typeof window === "undefined" || !window.PublicKeyCredential) {
    throw new Error("WebAuthn is not supported in this browser");
  }
  const { challenge_id, options } = await beginPasskeyLogin(tenantId, email);
  const assertion = (await navigator.credentials.get({
    publicKey: toRequestOptions(options),
  })) as PublicKeyCredential | null;
  if (!assertion) throw new Error("Passkey authentication was cancelled");
  return completePasskeyLogin(tenantId, challenge_id, credentialToJSON(assertion));
}

export function isWebAuthnSupported(): boolean {
  return typeof window !== "undefined" && Boolean(window.PublicKeyCredential);
}
