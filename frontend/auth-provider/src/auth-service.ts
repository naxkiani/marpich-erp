import { API_URL } from "./config";
import { apiGet } from "./api-client";
import { clearSession, loadSession, saveSession, tenantHeaders } from "./session";
import type { AuthSession, AuthUser, LoginCredentials } from "./types";

type TokenPayload = {
  access_token: string;
  refresh_token?: string;
  expires_in?: number;
  mfa_required?: boolean;
  mfa_token?: string;
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

export async function registerUser(
  tenantId: string,
  email: string,
  password: string,
  displayName: string,
): Promise<void> {
  await fetch(`${API_URL}/api/v1/auth/register`, {
    method: "POST",
    headers: tenantHeaders(tenantId),
    body: JSON.stringify({ email, password, display_name: displayName }),
  }).catch(() => undefined);
}

export async function loginSession(credentials: LoginCredentials): Promise<AuthSession> {
  const { tenantId, email, password, displayName = "Marpich Admin", registerIfMissing = true } = credentials;

  if (registerIfMissing) {
    await registerUser(tenantId, email, password, displayName);
  }

  const login = await fetch(`${API_URL}/api/v1/auth/login`, {
    method: "POST",
    headers: tenantHeaders(tenantId),
    body: JSON.stringify({ email, password }),
  });
  if (!login.ok) {
    throw new Error("Login failed — check tenant, email, and password");
  }
  const json = await login.json();
  const session = sessionFromTokens(tenantId, json.data as TokenPayload);
  saveSession(session);
  return session;
}

export async function refreshSession(session: AuthSession): Promise<AuthSession> {
  if (!session.refreshToken) return session;

  const res = await fetch(`${API_URL}/api/v1/auth/refresh`, {
    method: "POST",
    headers: tenantHeaders(session.tenantId),
    body: JSON.stringify({ refresh_token: session.refreshToken }),
  });
  if (!res.ok) {
    clearSession();
    throw new Error("Session expired — please sign in again");
  }
  const json = await res.json();
  const next = sessionFromTokens(session.tenantId, json.data as TokenPayload);
  const merged: AuthSession = { ...next, userId: session.userId };
  saveSession(merged);
  return merged;
}

export async function logoutSession(session: AuthSession): Promise<void> {
  if (session.refreshToken) {
    await fetch(`${API_URL}/api/v1/auth/logout`, {
      method: "POST",
      headers: {
        ...tenantHeaders(session.tenantId),
        Authorization: `Bearer ${session.accessToken}`,
      },
      body: JSON.stringify({ refresh_token: session.refreshToken, revoke_all: false }),
    }).catch(() => undefined);
  }
  clearSession();
}

export async function fetchCurrentUser(session: AuthSession): Promise<AuthUser> {
  const data = await apiGet<Record<string, unknown>>("/api/v1/users/me", session);
  const permissions = Array.isArray(data.permissions) ? (data.permissions as string[]) : [];
  const roles = Array.isArray(data.roles) ? (data.roles as string[]) : [];
  return {
    ...data,
    id: String(data.id ?? data.user_id ?? ""),
    email: String(data.email ?? ""),
    display_name: data.display_name ? String(data.display_name) : undefined,
    permissions,
    roles,
  };
}

export function getStoredSession(): AuthSession | null {
  return loadSession();
}
