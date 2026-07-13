import { clearSessionCookie, setSessionCookie } from "./cookie";
import { SESSION_STORAGE_KEY } from "./config";
import type { AuthSession } from "./types";

export function loadSession(): AuthSession | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.sessionStorage.getItem(SESSION_STORAGE_KEY);
    return raw ? (JSON.parse(raw) as AuthSession) : null;
  } catch {
    return null;
  }
}

export function saveSession(session: AuthSession): void {
  if (typeof window === "undefined") return;
  window.sessionStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(session));
  setSessionCookie();
}

export function clearSession(): void {
  if (typeof window === "undefined") return;
  window.sessionStorage.removeItem(SESSION_STORAGE_KEY);
  clearSessionCookie();
}

export function isSessionExpired(session: AuthSession): boolean {
  if (!session.expiresAt) return false;
  return Date.now() >= session.expiresAt - 30_000;
}

export function authHeaders(session: AuthSession): HeadersInit {
  return {
    "Content-Type": "application/json",
    "X-Tenant-ID": session.tenantId,
    Authorization: `Bearer ${session.accessToken}`,
  };
}

export function tenantHeaders(tenantId: string): HeadersInit {
  return {
    "Content-Type": "application/json",
    "X-Tenant-ID": tenantId,
  };
}
