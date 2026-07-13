const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export type ApiSession = { tenantId: string; accessToken: string };

export type EisCatalog = {
  capabilities: Array<{ capability: string; label: string }>;
  policy_keys: string[];
  artifact_types: string[];
  delegation: Record<string, string | boolean>;
};

export type EisDashboard = {
  summary: {
    capabilities: number;
    projects: number;
    artifacts: number;
    versions: number;
    deployments_live: number;
    tests_passed: number;
    marketplace_listings: number;
    citizen_projects: number;
  };
  profile: Record<string, unknown> | null;
  artifacts_by_type: Record<string, number>;
  recent_tests: Array<Record<string, unknown>>;
  capabilities: Array<{ capability: string; label: string }>;
};

export type EisDesignerGraph = {
  name: string;
  nodes: Array<{ id: string; label: string; type: string; x: number; y: number }>;
  edges: Array<{ from: string; to: string }>;
};

export type EisDeveloperPortal = {
  title: string;
  projects: Array<Record<string, unknown>>;
  artifacts: Array<Record<string, unknown>>;
  marketplace_preview: Array<Record<string, unknown>>;
  quick_links: Array<{ label: string; path: string }>;
  sdk_languages: string[];
};

export type EisCitizenWorkspace = {
  title: string;
  no_code: boolean;
  templates: Array<{ id: string; label: string; artifact_type: string }>;
  projects: Array<Record<string, unknown>>;
  artifacts: Array<Record<string, unknown>>;
  guided_steps: string[];
};

const SESSION_KEY = "marpich_eis_session";

export function loadEisSession(): ApiSession | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.sessionStorage.getItem(SESSION_KEY);
    return raw ? (JSON.parse(raw) as ApiSession) : null;
  } catch {
    return null;
  }
}

export function saveEisSession(session: ApiSession): void {
  window.sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

function headers(session: ApiSession): HeadersInit {
  return {
    "Content-Type": "application/json",
    "X-Tenant-ID": session.tenantId,
    Authorization: `Bearer ${session.accessToken}`,
  };
}

async function apiGet<T>(path: string, session: ApiSession): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, { headers: headers(session) });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? body.message ?? `HTTP ${res.status}`);
  }
  return (await res.json()).data as T;
}

async function apiPost<T>(path: string, session: ApiSession, body: unknown = {}): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: headers(session),
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? `HTTP ${res.status}`);
  }
  return (await res.json()).data as T;
}

export async function loginEisSession(tenantId: string, email: string, password: string): Promise<ApiSession> {
  const tenantHeaders = { "Content-Type": "application/json", "X-Tenant-ID": tenantId };
  await fetch(`${API_URL}/api/v1/auth/register`, {
    method: "POST",
    headers: tenantHeaders,
    body: JSON.stringify({ email, password, display_name: "Integration Studio Admin" }),
  }).catch(() => undefined);
  const login = await fetch(`${API_URL}/api/v1/auth/login`, {
    method: "POST",
    headers: tenantHeaders,
    body: JSON.stringify({ email, password }),
  });
  if (!login.ok) throw new Error("Login failed — check tenant, email, and password");
  const json = await login.json();
  const session: ApiSession = { tenantId, accessToken: json.data.access_token };
  saveEisSession(session);
  return session;
}

export async function fetchEisCatalog(session: ApiSession): Promise<EisCatalog> {
  return apiGet("/api/v1/enterprise-integration-studio/catalog", session);
}

export async function fetchEisDashboard(session: ApiSession): Promise<EisDashboard> {
  return apiGet("/api/v1/enterprise-integration-studio/dashboard", session);
}

export async function fetchEisDeveloperPortal(session: ApiSession): Promise<EisDeveloperPortal> {
  return apiGet("/api/v1/enterprise-integration-studio/developer-portal", session);
}

export async function fetchEisCitizenWorkspace(session: ApiSession): Promise<EisCitizenWorkspace> {
  return apiGet("/api/v1/enterprise-integration-studio/citizen-workspace", session);
}

export async function fetchEisArtifacts(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-integration-studio/artifacts", session);
}

export async function fetchEisMarketplace(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-integration-studio/marketplace", session);
}

export async function fetchEisDesigner(session: ApiSession, artifactRef: string): Promise<EisDesignerGraph> {
  return apiGet(`/api/v1/enterprise-integration-studio/artifacts/${artifactRef}/designer`, session);
}

export async function fetchEisDeployments(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-integration-studio/deployments", session);
}

export async function fetchEisTestRuns(session: ApiSession): Promise<Array<Record<string, unknown>>> {
  return apiGet("/api/v1/enterprise-integration-studio/test-runs", session);
}

export async function seedEis(session: ApiSession): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/enterprise-integration-studio/seed", session);
}

export async function testEisArtifact(session: ApiSession, artifactRef: string): Promise<Record<string, unknown>> {
  return apiPost(`/api/v1/enterprise-integration-studio/artifacts/${artifactRef}/test`, session, { use_mock: true });
}

export async function publishEisArtifact(session: ApiSession, artifactRef: string): Promise<Record<string, unknown>> {
  return apiPost(`/api/v1/enterprise-integration-studio/artifacts/${artifactRef}/publish`, session);
}

export async function deployEisArtifact(session: ApiSession, artifactRef: string): Promise<Record<string, unknown>> {
  return apiPost(`/api/v1/enterprise-integration-studio/artifacts/${artifactRef}/deploy`, session, {
    environment: "sandbox",
  });
}
