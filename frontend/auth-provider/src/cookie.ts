import { SESSION_COOKIE_NAME } from "./config";

/** Cookie holds the access JWT (not the legacy presence flag "1"). */
export function setSessionCookie(accessToken: string): void {
  if (typeof document === "undefined") return;
  const token = accessToken.trim();
  if (!token) return;
  const maxAge = 60 * 60 * 24;
  const secure =
    typeof window !== "undefined" && window.location.protocol === "https:"
      ? "; secure"
      : "";
  // Not HttpOnly — set from SPA; API remains source of truth for AuthZ.
  document.cookie = `${SESSION_COOKIE_NAME}=${encodeURIComponent(token)}; path=/; max-age=${maxAge}; samesite=lax${secure}`;
}

export function clearSessionCookie(): void {
  if (typeof document === "undefined") return;
  document.cookie = `${SESSION_COOKIE_NAME}=; path=/; max-age=0; samesite=lax`;
}
