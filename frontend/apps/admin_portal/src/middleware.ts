import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { SESSION_COOKIE_NAME, SESSION_COOKIE_VALUE } from "@marpich/auth-provider";

const PROTECTED_PREFIXES = ["/enterprise", "/tax", "/currency-exchange"];

const PUBLIC_PATHS = new Set(["/login"]);

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const hasSession = request.cookies.get(SESSION_COOKIE_NAME)?.value === SESSION_COOKIE_VALUE;
  const isProtected = PROTECTED_PREFIXES.some((prefix) => pathname.startsWith(prefix));
  const isPublic = PUBLIC_PATHS.has(pathname);

  if (isProtected && !hasSession && !isPublic) {
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
  matcher: ["/enterprise/:path*", "/tax/:path*", "/currency-exchange/:path*", "/login"],
};
