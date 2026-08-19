import { SESSION_COOKIE_NAME } from "@marpich/auth-provider";

export const ACCESS_COOKIE = SESSION_COOKIE_NAME;
export const REFRESH_COOKIE = "marpich_refresh";
export const ACCESS_MAX_AGE = 60 * 60 * 24;
export const REFRESH_MAX_AGE = 60 * 60 * 24 * 7;

export function backendApiUrl(): string {
  return (
    process.env.API_URL?.trim() ||
    process.env.NEXT_PUBLIC_API_URL?.trim() ||
    "http://127.0.0.1:8000"
  );
}

export function cookieBase(maxAge: number) {
  return {
    httpOnly: true as const,
    sameSite: "lax" as const,
    path: "/",
    maxAge,
    secure: process.env.NODE_ENV === "production",
  };
}

export function sameOrigin(request: Request): boolean {
  const origin = request.headers.get("origin");
  const host = request.headers.get("host");
  if (!origin || !host) return true;
  try {
    return new URL(origin).host === host;
  } catch {
    return false;
  }
}
