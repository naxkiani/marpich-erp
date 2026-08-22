import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import {
  ACCESS_COOKIE,
  REFRESH_COOKIE,
  backendApiUrl,
  cookieBase,
  sameOrigin,
} from "@/lib/bffAuth";

export async function POST(request: Request) {
  if (!sameOrigin(request)) {
    return NextResponse.json({ ok: false }, { status: 403 });
  }
  const jar = await cookies();
  const accessToken = jar.get(ACCESS_COOKIE)?.value ?? "";
  const refreshToken = jar.get(REFRESH_COOKIE)?.value ?? "";
  const tenantId = request.headers.get("x-tenant-id")?.trim() ?? "";
  if (refreshToken && tenantId) {
    await fetch(`${backendApiUrl()}/api/v1/auth/logout`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Tenant-ID": tenantId,
        ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      },
      body: JSON.stringify({ refresh_token: refreshToken, revoke_all: false }),
    }).catch(() => undefined);
  }
  const out = NextResponse.json({ ok: true });
  out.cookies.set({ name: ACCESS_COOKIE, value: "", ...cookieBase(0) });
  out.cookies.set({ name: REFRESH_COOKIE, value: "", ...cookieBase(0) });
  return out;
}
