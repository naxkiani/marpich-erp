const SESSION_COOKIE_PATH = "/api/auth/session";

/** HttpOnly cookies are set by the same-origin BFF — never via document.cookie or sessionStorage. */
export async function setSessionCookie(accessToken: string, refreshToken?: string): Promise<void> {
  if (typeof window === "undefined") return;
  const token = accessToken.trim();
  if (!token) return;
  const res = await fetch(SESSION_COOKIE_PATH, {
    method: "POST",
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ accessToken: token, refreshToken: refreshToken?.trim() || undefined }),
  });
  if (!res.ok) {
    throw new Error("Failed to establish HttpOnly session cookie");
  }
}

export async function clearSessionCookie(): Promise<void> {
  if (typeof window === "undefined") return;
  await fetch(SESSION_COOKIE_PATH, {
    method: "DELETE",
    credentials: "same-origin",
  }).catch(() => undefined);
}
