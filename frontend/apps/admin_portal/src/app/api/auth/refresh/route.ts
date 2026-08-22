import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import {
  ACCESS_COOKIE,
  ACCESS_MAX_AGE,
  REFRESH_COOKIE,
  REFRESH_MAX_AGE,
  backendApiUrl,
  cookieBase,
  sameOrigin,
} from "@/lib/bffAuth";

export async function POST(request: Request) {
  if (!sameOrigin(request)) {
    return NextResponse.json({ ok: false }, { status: 403 });
  }
  const jar = await cookies();
  const refreshToken = jar.get(REFRESH_COOKIE)?.value ?? "";
  const tenantId = request.headers.get("x-tenant-id")?.trim() ?? "";
  if (!refreshToken || !tenantId) {
    return NextResponse.json({ ok: false }, { status: 401 });
  }
  const api = backendApiUrl();
  const res = await fetch(`${api}/api/v1/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-Tenant-ID": tenantId },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });
  if (!res.ok) {
    const out = NextResponse.json({ ok: false }, { status: 401 });
    out.cookies.set({ name: ACCESS_COOKIE, value: "", ...cookieBase(0) });
    out.cookies.set({ name: REFRESH_COOKIE, value: "", ...cookieBase(0) });
    return out;
  }
  const json = (await res.json()) as {
    data?: { access_token?: string; refresh_token?: string; expires_in?: number };
  };
  const accessToken = json.data?.access_token?.trim() ?? "";
  const nextRefresh = json.data?.refresh_token?.trim() || refreshToken;
  if (!accessToken) {
    return NextResponse.json({ ok: false }, { status: 502 });
  }
  const expiresAt = json.data?.expires_in ? Date.now() + json.data.expires_in * 1000 : undefined;
  const out = NextResponse.json({ tenantId, expiresAt });
  out.cookies.set({ name: ACCESS_COOKIE, value: accessToken, ...cookieBase(ACCESS_MAX_AGE) });
  out.cookies.set({ name: REFRESH_COOKIE, value: nextRefresh, ...cookieBase(REFRESH_MAX_AGE) });
  return out;
}
