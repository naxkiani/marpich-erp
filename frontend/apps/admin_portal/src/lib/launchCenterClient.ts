import { type ApiSession, apiGet, apiPost } from "./clientAuth";

export type LaunchCenterWorkspace = {
  P395_STATUS: string;
  PRODUCTION_LOCK: string;
  G26_READY: boolean;
  G26_STATUS: string;
  P0: number;
  P313: string;
  P313_REENTRY_READY: boolean;
  PRODUCTION_CERTIFIED: boolean;
  GO_LIVE_READY: boolean;
  GO_LIVE_AUTHORIZATION: string;
  ACTIVE_APPLICATIONS: number;
  PRODUCTION_TRAFFIC: string;
  environments_total: number;
  environments_ready: number;
  environments_blocked: number;
  active_jobs: number;
  failed_jobs: number;
  DIGEST: string;
  IMAGE: string;
  RELEASE: string;
  COMMIT: string;
  sections: string[];
  wizard: string[];
  roles: string[];
  providers: Record<string, { status: string; credentials: string; regions: string }>;
  releases: Array<{
    RELEASE_ID: string;
    VERSION?: string;
    COMMIT_SHA?: string;
    IMAGE?: string;
    IMAGE_DIGEST?: string;
    SECURITY?: string;
    SECURITY_STATUS?: string;
    SBOM?: string;
    SBOM_ID?: string;
    TEST_STATUS?: string;
    PROMOTION_STATUS?: string;
    TEST?: string;
    PROMOTION?: string;
    selectable?: boolean;
    latest_rejected?: boolean;
  }>;
  environments?: Array<Record<string, unknown>>;
  jobs?: Array<Record<string, unknown>>;
  backups?: Array<Record<string, unknown>>;
  restores?: Array<Record<string, unknown>>;
  plans?: Array<Record<string, unknown>>;
  profiles?: Record<string, Record<string, string>>;
  sizes?: Record<string, Record<string, string>>;
  cost?: { TOTAL?: string; zero_cost_invented?: boolean };
  health?: { LIVE?: string; READY?: string; status?: string };
  demo_mode?: { enabled?: boolean; label?: string; is_production?: boolean };
  go_live_button?: boolean;
  p0_override?: boolean;
  g26_override?: boolean;
  plan?: Record<string, unknown>;
  credentials?: Record<string, unknown>;
  dependencies?: Array<Record<string, string>>;
  autonomous_operations?: {
    kill_switch?: boolean;
    PRODUCTION_AUTOMATION_LOCK?: string;
  };
  control_plane?: {
    environment?: string;
    provider?: string;
    region?: string;
    profile?: string;
    status?: string;
    release?: string;
    deployment?: string;
    database?: string;
    network?: string;
    DNS?: string;
    TLS?: string;
    backup?: string;
    restore?: string;
    observability?: string;
    security?: string;
    cost?: string;
    capacity?: string;
    drift?: string;
  };
  [key: string]: unknown;
};

export type LaunchCenterPlan = Record<string, unknown> & {
  STATUS?: string;
  executed?: boolean;
};

export const SECRET_KEYS = ["password", "token", "secret", "private_key", "credential", "connection_string"];

export function productionExecutionLocked(data: Pick<LaunchCenterWorkspace, "PRODUCTION_LOCK" | "G26_READY" | "PRODUCTION_CERTIFIED" | "GO_LIVE_AUTHORIZATION"> | null): boolean {
  if (!data) return true;
  return (
    data.PRODUCTION_LOCK === "ACTIVE" ||
    data.G26_READY !== true ||
    data.PRODUCTION_CERTIFIED !== true ||
    data.GO_LIVE_AUTHORIZATION !== "APPROVED"
  );
}

export function releaseSelectable(row: { selectable?: boolean; IMAGE_DIGEST?: string; latest_rejected?: boolean }): boolean {
  if (row.latest_rejected) return false;
  if (row.selectable === false) return false;
  const digest = row.IMAGE_DIGEST ?? "";
  return Boolean(digest) && digest !== "NOT_AVAILABLE" && digest !== "latest";
}

export function demoLabel(data: LaunchCenterWorkspace | null): string {
  return data?.demo_mode?.label === "SIMULATED" ? "SIMULATED" : "SIMULATED";
}

export function redactSecretFields(payload: Record<string, unknown>): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(payload)) {
    const lower = key.toLowerCase();
    if (SECRET_KEYS.some((marker) => lower.includes(marker))) {
      out[key] = "REDACTED";
      continue;
    }
    out[key] = value;
  }
  return out;
}

export async function fetchLaunchCenterStatus(session: ApiSession): Promise<LaunchCenterWorkspace> {
  return apiGet<LaunchCenterWorkspace>("/api/v1/launch-center/status", session);
}

export async function fetchLaunchCenterProviders(session: ApiSession): Promise<{
  providers: LaunchCenterWorkspace["providers"];
  credentials: Record<string, unknown>;
}> {
  return apiGet("/api/v1/launch-center/providers", session);
}

export async function createLaunchCenterPlan(
  session: ApiSession,
  body: { provider: string; environment: string; profile: string; release?: string },
): Promise<LaunchCenterPlan> {
  return apiPost("/api/v1/launch-center/deployments/plan", session, body);
}

export async function validateLaunchCenterPlan(
  session: ApiSession,
  body: { provider: string; environment: string; profile: string; release?: string },
): Promise<LaunchCenterPlan> {
  return apiPost("/api/v1/launch-center/deployments/validate", session, body);
}

export async function requestLaunchCenterProvision(
  session: ApiSession,
  body: { provider: string; environment: string; profile: string; release?: string },
): Promise<LaunchCenterPlan> {
  return apiPost("/api/v1/launch-center/deployments", session, body);
}

export async function verifyLaunchCenterDeployment(
  session: ApiSession,
  body: { provider: string; environment: string; profile: string; release?: string },
): Promise<LaunchCenterPlan> {
  return apiPost("/api/v1/launch-center/deployments/verify", session, body);
}
