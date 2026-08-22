import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { ACCESS_COOKIE, backendApiUrl } from "@/lib/bffAuth";

async function proxy(request: NextRequest, path: string[]): Promise<Response> {
  const joined = `/${path.join("/")}`;
  if (!joined.startsWith("/api/v1/")) {
    return NextResponse.json({ detail: "BFF proxy only allows /api/v1/" }, { status: 400 });
  }
  const jar = await cookies();
  const accessToken = jar.get(ACCESS_COOKIE)?.value ?? "";
  if (!accessToken) {
    return NextResponse.json({ detail: "Not authenticated" }, { status: 401 });
  }
  const target = new URL(joined, `${backendApiUrl()}/`);
  target.search = request.nextUrl.search;
  const headers = new Headers();
  const tenant = request.headers.get("x-tenant-id");
  if (tenant) headers.set("X-Tenant-ID", tenant);
  const contentType = request.headers.get("content-type");
  if (contentType) headers.set("Content-Type", contentType);
  const correlation = request.headers.get("x-correlation-id") || request.headers.get("x-request-id");
  if (correlation) {
    headers.set("X-Correlation-ID", correlation);
    headers.set("X-Request-ID", correlation);
  }
  headers.set("Authorization", `Bearer ${accessToken}`);

  const init: RequestInit = { method: request.method, headers };
  if (request.method !== "GET" && request.method !== "HEAD") {
    init.body = await request.arrayBuffer();
  }
  const upstream = await fetch(target, init);
  const body = await upstream.arrayBuffer();
  const outHeaders = new Headers();
  const pass = ["content-type", "x-request-id", "x-correlation-id"];
  for (const key of pass) {
    const value = upstream.headers.get(key);
    if (value) outHeaders.set(key, value);
  }
  return new NextResponse(body, { status: upstream.status, headers: outHeaders });
}

export async function GET(request: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const { path } = await ctx.params;
  return proxy(request, path);
}

export async function POST(request: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const { path } = await ctx.params;
  return proxy(request, path);
}

export async function PUT(request: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const { path } = await ctx.params;
  return proxy(request, path);
}

export async function PATCH(request: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const { path } = await ctx.params;
  return proxy(request, path);
}

export async function DELETE(request: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const { path } = await ctx.params;
  return proxy(request, path);
}
