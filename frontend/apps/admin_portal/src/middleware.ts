import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { SESSION_COOKIE_NAME, SESSION_COOKIE_VALUE } from "@marpich/auth-provider";

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

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const hasSession = request.cookies.get(SESSION_COOKIE_NAME)?.value === SESSION_COOKIE_VALUE;
  const protectedPath = isProtected(pathname);

  if (protectedPath && !hasSession) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    url.searchParams.set("returnTo", pathname);
    return NextResponse.redirect(url);
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
