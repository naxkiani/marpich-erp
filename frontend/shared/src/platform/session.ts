/** Platform session helpers for shell widgets (aligned with @marpich/auth-provider). */

export const PLATFORM_SESSION_KEY = "marpich_auth_session";

export type PlatformSession = {
  tenantId: string;
  accessToken: string;
  refreshToken?: string;
  expiresAt?: number;
  userId?: string;
};

export function loadPlatformSession(): PlatformSession | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.sessionStorage.getItem(PLATFORM_SESSION_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as PlatformSession;
    if (!parsed?.accessToken || !parsed?.tenantId) return null;
    return parsed;
  } catch {
    return null;
  }
}

export function getPlatformAuthHeaders(
  extra?: Record<string, string>,
): Record<string, string> | null {
  const session = loadPlatformSession();
  if (!session) return null;
  return {
    "Content-Type": "application/json",
    "X-Tenant-ID": session.tenantId,
    Authorization: `Bearer ${session.accessToken}`,
    ...extra,
  };
}

export const API_URL =
  (globalThis as { process?: { env?: Record<string, string | undefined> } }).process?.env
    ?.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
