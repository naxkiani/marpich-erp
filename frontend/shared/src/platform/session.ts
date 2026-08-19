/** Platform session helpers for shell widgets (aligned with @marpich/auth-provider). */

export const PLATFORM_SESSION_KEY = "marpich_auth_session";
export const BFF_API_PREFIX = "/api/backend";

export type PlatformSession = {
  tenantId: string;
  expiresAt?: number;
  userId?: string;
};

export function loadPlatformSession(): PlatformSession | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.sessionStorage.getItem(PLATFORM_SESSION_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as PlatformSession & {
      accessToken?: string;
      refreshToken?: string;
    };
    if (!parsed?.tenantId) return null;
    if (parsed.accessToken || parsed.refreshToken) {
      const cleaned: PlatformSession = {
        tenantId: parsed.tenantId,
        expiresAt: parsed.expiresAt,
        userId: parsed.userId,
      };
      window.sessionStorage.setItem(PLATFORM_SESSION_KEY, JSON.stringify(cleaned));
      return cleaned;
    }
    return { tenantId: parsed.tenantId, expiresAt: parsed.expiresAt, userId: parsed.userId };
  } catch {
    return null;
  }
}

/** Tenant header only — JWT is never exposed to JS; BFF attaches Authorization. */
export function getPlatformAuthHeaders(
  extra?: Record<string, string>,
): Record<string, string> | null {
  const session = loadPlatformSession();
  if (!session) return null;
  return {
    "Content-Type": "application/json",
    "X-Tenant-ID": session.tenantId,
    ...extra,
  };
}

export function platformApiUrl(path: string): string {
  if (typeof window !== "undefined") return `${BFF_API_PREFIX}${path}`;
  return `${API_URL}${path}`;
}

export const API_URL =
  (globalThis as { process?: { env?: Record<string, string | undefined> } }).process?.env
    ?.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
