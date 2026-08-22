import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { SESSION_COOKIE_NAME, isJwtSessionCookieValid } from "@marpich/auth-provider";

const PROTECTED_PREFIXES = [
  "/",
  "/modules",
  "/enterprise",
  "/banking",
  "/education",
  "/healthcare",
  "/account",
];

const PUBLIC_PATHS = new Set(["/login"]);

function isPublicPath(pathname: string): boolean {
  if (PUBLIC_PATHS.has(pathname)) return true;
  return pathname.startsWith("/login/");
}

function isProtected(pathname: string): boolean {
  if (isPublicPath(pathname)) return false;
  if (pathname === "/" || pathname === "/modules") return true;
  return PROTECTED_PREFIXES.some(
    (prefix) => prefix !== "/" && pathname.startsWith(prefix),
  );
}

function jwtSecretFromEnv(): string | undefined {
  return (
    process.env.JWT_SECRET?.trim() ||
    process.env.MARPICH_JWT_SECRET?.trim() ||
    undefined
  );
}

function requireSignature(): boolean {
  if (process.env.MARPICH_REQUIRE_JWT_VERIFY === "1") return true;
  if (process.env.MARPICH_REQUIRE_JWT_VERIFY === "0") return false;
  return process.env.NODE_ENV === "production";
}

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const raw = request.cookies.get(SESSION_COOKIE_NAME)?.value;
  const secret = jwtSecretFromEnv();
  const hasSession = await isJwtSessionCookieValid(raw, {
    secret,
    requireSignature: requireSignature(),
    issuer: process.env.JWT_ISSUER?.trim() || "marpich-identity",
    tokenType: "access",
  });
  const protectedPath = isProtected(pathname);

  if (protectedPath && !hasSession) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    url.searchParams.set("returnTo", pathname);
    const res = NextResponse.redirect(url);
    if (raw) {
      res.cookies.set(SESSION_COOKIE_NAME, "", { path: "/", maxAge: 0 });
    }
    return res;
  }

  if (pathname === "/login" && hasSession) {
    const returnTo = request.nextUrl.searchParams.get("returnTo");
    const destination = returnTo && returnTo.startsWith("/") ? returnTo : "/";
    return NextResponse.redirect(new URL(destination, request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/",
    "/modules",
    "/modules/:path*",
    "/enterprise/:path*",
    "/banking/:path*",
    "/education/:path*",
    "/healthcare/:path*",
    "/login",
    "/login/:path*",
    "/account/:path*",
  ],
};
