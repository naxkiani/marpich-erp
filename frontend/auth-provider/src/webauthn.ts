import { API_URL } from "./config";
import { apiDelete, apiGet, apiPost } from "./api-client";
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

export type PasskeyCredential = {
  credential_ref: string;
  tenant_id: string;
  user_id: string;
  credential_id: string;
  nickname: string;
  transports: string[];
  sign_count: number;
  aaguid?: string | null;
  created_at: string;
  last_used_at?: string | null;
};

export type PublicKeyCredentialRequestOptionsJSON = {
  challenge: string;
  timeout?: number;
  rpId?: string;
  allowCredentials?: Array<{ id: string; type: string; transports?: string[] }>;
  userVerification?: UserVerificationRequirement;
};

export type PublicKeyCredentialCreationOptionsJSON = {
  challenge: string;
  rp: { name: string; id?: string };
  user: { id: string; name: string; displayName: string };
  pubKeyCredParams: Array<{ type: string; alg: number }>;
  timeout?: number;
  excludeCredentials?: Array<{ id: string; type: string; transports?: string[] }>;
  authenticatorSelection?: {
    authenticatorAttachment?: AuthenticatorAttachment;
    residentKey?: ResidentKeyRequirement;
    requireResidentKey?: boolean;
    userVerification?: UserVerificationRequirement;
  };
  attestation?: AttestationConveyancePreference;
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

export type RegistrationCredentialJSON = {
  id: string;
  rawId: string;
  type: string;
  response: {
    clientDataJSON: string;
    attestationObject: string;
    transports?: string[];
  };
};

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

export async function listPasskeys(session: AuthSession): Promise<PasskeyCredential[]> {
  return apiGet("/api/v1/authentication/webauthn/credentials", session);
}

export async function beginPasskeyRegistration(session: AuthSession): Promise<{
  challenge_id: string;
  options: PublicKeyCredentialCreationOptionsJSON;
}> {
  return apiPost("/api/v1/authentication/webauthn/register/options", session, {});
}

export async function completePasskeyRegistration(
  session: AuthSession,
  challengeId: string,
  credential: RegistrationCredentialJSON,
  nickname = "Passkey",
): Promise<PasskeyCredential> {
  return apiPost("/api/v1/authentication/webauthn/register/verify", session, {
    challenge_id: challengeId,
    credential,
    nickname,
  });
}

export async function revokePasskey(
  session: AuthSession,
  credentialRef: string,
): Promise<{ revoked: boolean; credential_ref: string }> {
  return apiDelete(
    `/api/v1/authentication/webauthn/credentials/${encodeURIComponent(credentialRef)}`,
    session,
  );
}

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

function toCreationOptions(
  options: PublicKeyCredentialCreationOptionsJSON,
): PublicKeyCredentialCreationOptions {
  return {
    ...options,
    challenge: base64URLToBuffer(options.challenge),
    user: {
      ...options.user,
      id: base64URLToBuffer(options.user.id),
    },
    pubKeyCredParams: options.pubKeyCredParams.map((p) => ({
      type: p.type as PublicKeyCredentialType,
      alg: p.alg,
    })),
    excludeCredentials: options.excludeCredentials?.map((cred) => ({
      type: cred.type as PublicKeyCredentialType,
      id: base64URLToBuffer(cred.id),
      transports: cred.transports as AuthenticatorTransport[] | undefined,
    })),
  };
}

function assertionToJSON(credential: PublicKeyCredential): AuthenticationCredentialJSON {
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

function attestationToJSON(credential: PublicKeyCredential): RegistrationCredentialJSON {
  const response = credential.response as AuthenticatorAttestationResponse;
  const transports =
    typeof response.getTransports === "function" ? response.getTransports() : undefined;
  return {
    id: credential.id,
    rawId: bufferToBase64URL(credential.rawId),
    type: credential.type,
    response: {
      clientDataJSON: bufferToBase64URL(response.clientDataJSON),
      attestationObject: bufferToBase64URL(response.attestationObject),
      transports,
    },
  };
}

export async function loginWithPasskey(credentials: LoginCredentials): Promise<AuthSession> {
  const { tenantId, email } = credentials;
  if (!email) throw new Error("Email is required for passkey login");
  if (!isWebAuthnSupported()) {
    throw new Error("WebAuthn is not supported in this browser");
  }
  const { challenge_id, options } = await beginPasskeyLogin(tenantId, email);
  const assertion = (await navigator.credentials.get({
    publicKey: toRequestOptions(options),
  })) as PublicKeyCredential | null;
  if (!assertion) throw new Error("Passkey authentication was cancelled");
  return completePasskeyLogin(tenantId, challenge_id, assertionToJSON(assertion));
}

export async function registerPasskey(
  session: AuthSession,
  nickname = "Passkey",
): Promise<PasskeyCredential> {
  if (!isWebAuthnSupported()) {
    throw new Error("WebAuthn is not supported in this browser");
  }
  const { challenge_id, options } = await beginPasskeyRegistration(session);
  const attestation = (await navigator.credentials.create({
    publicKey: toCreationOptions(options),
  })) as PublicKeyCredential | null;
  if (!attestation) throw new Error("Passkey registration was cancelled");
  return completePasskeyRegistration(session, challenge_id, attestationToJSON(attestation), nickname);
}

export function isWebAuthnSupported(): boolean {
  return typeof window !== "undefined" && Boolean(window.PublicKeyCredential);
}
