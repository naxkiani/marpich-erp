import { API_URL } from "./config";
import { authHeaders } from "./session";
import type { AuthSession } from "./types";

const BFF_PREFIX = "/api/backend";

function requestUrl(path: string): string {
  if (typeof window !== "undefined") return `${BFF_PREFIX}${path}`;
  return `${API_URL}${path}`;
}

async function parseError(res: Response): Promise<string> {
  const body = await res.json().catch(() => ({}));
  const detail = body.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail) && detail[0]?.msg) return String(detail[0].msg);
  return body.message ?? `HTTP ${res.status}`;
}

async function apiFetch(path: string, session: AuthSession, init: RequestInit): Promise<Response> {
  return fetch(requestUrl(path), {
    ...init,
    credentials: "same-origin",
    headers: { ...authHeaders(session), ...(init.headers as Record<string, string> | undefined) },
  });
}

export async function apiGet<T>(path: string, session: AuthSession): Promise<T> {
  const res = await apiFetch(path, session, { method: "GET" });
  if (!res.ok) throw new Error(await parseError(res));
  const json = await res.json();
  return json.data as T;
}

export async function apiPost<T>(path: string, session: AuthSession, body: unknown = {}): Promise<T> {
  const res = await apiFetch(path, session, { method: "POST", body: JSON.stringify(body) });
  if (!res.ok) throw new Error(await parseError(res));
  const json = await res.json();
  return json.data as T;
}

export async function apiDelete<T>(path: string, session: AuthSession): Promise<T> {
  const res = await apiFetch(path, session, { method: "DELETE" });
  if (!res.ok) throw new Error(await parseError(res));
  const json = await res.json();
  return json.data as T;
}

export async function apiPut<T>(path: string, session: AuthSession, body: unknown = {}): Promise<T> {
  const res = await apiFetch(path, session, { method: "PUT", body: JSON.stringify(body) });
  if (!res.ok) throw new Error(await parseError(res));
  const json = await res.json();
  return json.data as T;
}

export async function apiPatch<T>(path: string, session: AuthSession, body: unknown = {}): Promise<T> {
  const res = await apiFetch(path, session, { method: "PATCH", body: JSON.stringify(body) });
  if (!res.ok) throw new Error(await parseError(res));
  const json = await res.json();
  return json.data as T;
}
