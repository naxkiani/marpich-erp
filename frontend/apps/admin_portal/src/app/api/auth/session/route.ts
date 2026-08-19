import { NextResponse } from "next/server";
import { isJwtSessionCookieValid, SESSION_COOKIE_NAME } from "@marpich/auth-provider";
import {
  ACCESS_COOKIE,
  ACCESS_MAX_AGE,
  REFRESH_COOKIE,
  REFRESH_MAX_AGE,
  cookieBase,
  sameOrigin,
} from "@/lib/bffAuth";

async function jwtOk(token: string, tokenType: string): Promise<boolean> {
  const secret = process.env.JWT_SECRET?.trim() || process.env.MARPICH_JWT_SECRET?.trim();
  const requireSignature =
    process.env.MARPICH_REQUIRE_JWT_VERIFY === "1" ||
    (process.env.MARPICH_REQUIRE_JWT_VERIFY !== "0" && process.env.NODE_ENV === "production");
  return isJwtSessionCookieValid(token, {
    secret,
    requireSignature,
    issuer: process.env.JWT_ISSUER?.trim() || "marpich-identity",
    tokenType,
  });
}

export async function POST(request: Request) {
  if (!sameOrigin(request)) {
    return NextResponse.json({ ok: false }, { status: 403 });
  }
  const body = (await request.json().catch(() => null)) as {
    accessToken?: unknown;
    refreshToken?: unknown;
  } | null;
  const accessToken = typeof body?.accessToken === "string" ? body.accessToken.trim() : "";
  const refreshToken = typeof body?.refreshToken === "string" ? body.refreshToken.trim() : "";
  if (!(await jwtOk(accessToken, "access"))) {
    return NextResponse.json({ ok: false }, { status: 401 });
  }
  const res = NextResponse.json({ ok: true });
  res.cookies.set({ name: ACCESS_COOKIE, value: accessToken, ...cookieBase(ACCESS_MAX_AGE) });
  if (refreshToken) {
    res.cookies.set({ name: REFRESH_COOKIE, value: refreshToken, ...cookieBase(REFRESH_MAX_AGE) });
  }
  return res;
}

export async function DELETE(request: Request) {
  if (!sameOrigin(request)) {
    return NextResponse.json({ ok: false }, { status: 403 });
  }
  const res = NextResponse.json({ ok: true });
  res.cookies.set({ name: ACCESS_COOKIE, value: "", ...cookieBase(0) });
  res.cookies.set({ name: REFRESH_COOKIE, value: "", ...cookieBase(0) });
  res.cookies.set({ name: SESSION_COOKIE_NAME, value: "", ...cookieBase(0) });
  return res;
}
