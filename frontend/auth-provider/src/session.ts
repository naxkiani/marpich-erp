import { SESSION_STORAGE_KEY } from "./config";
import { clearSessionCookie, setSessionCookie } from "./cookie";
import type { AuthSession } from "./types";

export function toPublicSession(session: AuthSession): AuthSession {
  return {
    tenantId: session.tenantId,
    expiresAt: session.expiresAt,
    userId: session.userId,
  };
}

function persistPublic(session: AuthSession): void {
  window.sessionStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(toPublicSession(session)));
}

export function loadSession(): AuthSession | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.sessionStorage.getItem(SESSION_STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as AuthSession;
    if (!parsed?.tenantId) return null;
    if (parsed.accessToken || parsed.refreshToken) {
      persistPublic(parsed);
    }
    return toPublicSession(parsed);
  } catch {
    return null;
  }
}

export async function saveSession(session: AuthSession): Promise<void> {
  if (typeof window === "undefined") return;
  if (session.accessToken) {
    await setSessionCookie(session.accessToken, session.refreshToken);
  }
  persistPublic(session);
}

export async function clearSession(): Promise<void> {
  if (typeof window === "undefined") return;
  window.sessionStorage.removeItem(SESSION_STORAGE_KEY);
  await clearSessionCookie();
}

export function isSessionExpired(session: AuthSession): boolean {
  if (!session.expiresAt) return false;
  return Date.now() >= session.expiresAt - 30_000;
}

export function isAuthFailure(status: number): boolean {
  return status === 401 || status === 403;
}

/** Browser calls use the BFF; Authorization is attached server-side from the HttpOnly cookie. */
export function authHeaders(session: AuthSession): HeadersInit {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    "X-Tenant-ID": session.tenantId,
  };
  if (typeof window === "undefined" && session.accessToken) {
    headers.Authorization = `Bearer ${session.accessToken}`;
  }
  return headers;
}

export function tenantHeaders(tenantId: string): HeadersInit {
  return {
    "Content-Type": "application/json",
    "X-Tenant-ID": tenantId,
  };
}
