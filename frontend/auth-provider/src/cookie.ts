import { SESSION_COOKIE_NAME, SESSION_COOKIE_VALUE } from "./config";

export function setSessionCookie(): void {
  if (typeof document === "undefined") return;
  const maxAge = 60 * 60 * 24;
  document.cookie = `${SESSION_COOKIE_NAME}=${SESSION_COOKIE_VALUE}; path=/; max-age=${maxAge}; samesite=lax`;
}

export function clearSessionCookie(): void {
  if (typeof document === "undefined") return;
  document.cookie = `${SESSION_COOKIE_NAME}=; path=/; max-age=0; samesite=lax`;
}
