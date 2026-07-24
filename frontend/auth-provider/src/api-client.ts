import { API_URL } from "./config";
import { authHeaders } from "./session";
import type { AuthSession } from "./types";

async function parseError(res: Response): Promise<string> {
  const body = await res.json().catch(() => ({}));
  const detail = body.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail) && detail[0]?.msg) return String(detail[0].msg);
  return body.message ?? `HTTP ${res.status}`;
}

export async function apiGet<T>(path: string, session: AuthSession): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, { headers: authHeaders(session) });
  if (!res.ok) throw new Error(await parseError(res));
  const json = await res.json();
  return json.data as T;
}

export async function apiPost<T>(path: string, session: AuthSession, body: unknown = {}): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: authHeaders(session),
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(await parseError(res));
  const json = await res.json();
  return json.data as T;
}

export async function apiDelete<T>(path: string, session: AuthSession): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "DELETE",
    headers: authHeaders(session),
  });
  if (!res.ok) throw new Error(await parseError(res));
  const json = await res.json();
  return json.data as T;
}

export async function apiPut<T>(path: string, session: AuthSession, body: unknown = {}): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "PUT",
    headers: authHeaders(session),
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(await parseError(res));
  const json = await res.json();
  return json.data as T;
}

export async function apiPatch<T>(path: string, session: AuthSession, body: unknown = {}): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "PATCH",
    headers: authHeaders(session),
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(await parseError(res));
  const json = await res.json();
  return json.data as T;
}
