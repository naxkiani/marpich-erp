import { NextResponse } from "next/server";
import { backendApiUrl, sameOrigin } from "@/lib/bffAuth";
import { ACCESS_COOKIE, ACCESS_MAX_AGE, REFRESH_COOKIE, REFRESH_MAX_AGE, cookieBase } from "@/lib/bffAuth";

type LoginBody = {
  tenantId?: unknown;
  email?: unknown;
  password?: unknown;
  displayName?: unknown;
  registerIfMissing?: unknown;
};

export async function POST(request: Request) {
  if (!sameOrigin(request)) {
    return NextResponse.json({ ok: false }, { status: 403 });
  }
  const body = ((await request.json().catch(() => null)) as LoginBody | null) ?? {};
  const tenantId = typeof body.tenantId === "string" ? body.tenantId.trim() : "";
  const email = typeof body.email === "string" ? body.email.trim() : "";
  const password = typeof body.password === "string" ? body.password : "";
  const displayName = typeof body.displayName === "string" ? body.displayName : "Marpich Admin";
  const registerIfMissing = body.registerIfMissing !== false;
  if (!tenantId || !email || !password) {
    return NextResponse.json({ ok: false, detail: "tenantId, email, and password required" }, { status: 400 });
  }

  const api = backendApiUrl();
  const headers = { "Content-Type": "application/json", "X-Tenant-ID": tenantId };
  if (registerIfMissing) {
    await fetch(`${api}/api/v1/auth/register`, {
      method: "POST",
      headers,
      body: JSON.stringify({ email, password, display_name: displayName }),
    }).catch(() => undefined);
  }
  const login = await fetch(`${api}/api/v1/auth/login`, {
    method: "POST",
    headers,
    body: JSON.stringify({ email, password }),
  });
  if (!login.ok) {
    return NextResponse.json({ ok: false, detail: "Login failed" }, { status: 401 });
  }
  const json = (await login.json()) as {
    data?: { access_token?: string; refresh_token?: string; expires_in?: number };
  };
  const accessToken = json.data?.access_token?.trim() ?? "";
  const refreshToken = json.data?.refresh_token?.trim() ?? "";
  if (!accessToken) {
    return NextResponse.json({ ok: false, detail: "No access token" }, { status: 502 });
  }
  const expiresAt = json.data?.expires_in ? Date.now() + json.data.expires_in * 1000 : undefined;
  const res = NextResponse.json({ tenantId, expiresAt });
  res.cookies.set({ name: ACCESS_COOKIE, value: accessToken, ...cookieBase(ACCESS_MAX_AGE) });
  if (refreshToken) {
    res.cookies.set({ name: REFRESH_COOKIE, value: refreshToken, ...cookieBase(REFRESH_MAX_AGE) });
  }
  return res;
}
