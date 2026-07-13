import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadEisSession,
  saveSession as saveEisSession,
} from "./clientAuth";

export type { ApiSession };

export const loginEisSession = createClientLogin("Integration Studio Admin");
export { loadEisSession, saveEisSession };
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
