import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadFinDsSession,
  saveSession as saveFinDsSession,
} from "./clientAuth";

export type { ApiSession };

export const loginFinDsSession = createClientLogin("MLOps Admin");
export { loadFinDsSession, saveFinDsSession };
export type MLOpsCapability = {
  capability: string;
  label: string;
  layer?: string;
};

export type MLOpsArchitecture = {
  name: string;
  layers: Array<{ layer: string; components: string[]; description: string }>;
  pipeline_flow: string[];
  inference_paths: Record<string, string[]>;
};

export type FinDsDashboard = {
  summary: {
    capabilities: number;
    features_registered: number;
    models_registered: number;
    models_in_production: number;
    experiments_tracked: number;
    pipelines_completed: number;
    approvals_pending: number;
    predictions_run: number;
    drift_alerts: number;
    retraining_recommended: boolean;
    mlops_architecture_layers: number;
    autonomous_posting_forbidden: boolean;
  };
  profile: Record<string, unknown> | null;
  mlops_architecture: MLOpsArchitecture;
  context_snapshot: {
    model_accuracy: number;
    feature_count: number;
    training_samples: number;
  };
  capabilities: MLOpsCapability[];
  recent_monitors: Array<Record<string, unknown>>;
};

export type FinDsCatalog = {
  capabilities: MLOpsCapability[];
  inference_modes: Array<{ mode: string; label: string }>;
  policy_keys: string[];
  mlops_architecture: MLOpsArchitecture;
  explainable_outputs: boolean;
  autonomous_posting_forbidden: boolean;
};

export type FinDsModel = {
  model_ref: string;
  name: string;
  model_type: string;
  version: string;
  status: string;
  framework: string;
  metrics: Record<string, number>;
  artifact_uri: string;
  has_explainable_output: boolean;
};

export type FinDsMonitor = {
  monitor_ref: string;
  model_ref: string;
  drift_score: number;
  drift_severity: string;
  retraining_recommended: boolean;
  has_explainable_output: boolean;
};

export type ExternalRegistryStatus = {
  provider: string;
  configured: boolean;
  connected: boolean;
  mode: string;
  tracking_uri?: string | null;
  message?: string;
};

export type RegistrySyncResult = {
  registry: ExternalRegistryStatus;
  imported_count: number;
  skipped_count: number;
  imported_models: FinDsModel[];
  skipped: string[];
};


export async function fetchFinDsCatalog(session: ApiSession): Promise<FinDsCatalog> {
  return apiGet("/api/v1/financial-data-science/catalog", session);
}

export async function fetchFinDsDashboard(session: ApiSession): Promise<FinDsDashboard> {
  return apiGet("/api/v1/financial-data-science/dashboard", session);
}

export async function fetchFinDsModels(session: ApiSession): Promise<FinDsModel[]> {
  return apiGet("/api/v1/financial-data-science/models", session);
}

export async function fetchFinDsMonitors(session: ApiSession): Promise<FinDsMonitor[]> {
  return apiGet("/api/v1/financial-data-science/monitors", session);
}

export async function fetchExternalRegistryStatus(session: ApiSession): Promise<ExternalRegistryStatus> {
  return apiGet("/api/v1/financial-data-science/registry/status", session);
}

export async function seedFinDs(session: ApiSession): Promise<{ seeded: boolean }> {
  return apiPost("/api/v1/financial-data-science/seed", session);
}

export async function syncExternalRegistry(session: ApiSession): Promise<RegistrySyncResult> {
  return apiPost("/api/v1/financial-data-science/registry/sync", session);
}

export async function detectDrift(session: ApiSession, modelRef: string): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/financial-data-science/monitors/drift", session, { model_ref: modelRef });
}

export async function runRetraining(
  session: ApiSession,
  modelRef: string,
  featureRefs: string[],
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/financial-data-science/retraining/run", session, {
    model_ref: modelRef,
    feature_refs: featureRefs,
  });
}

export async function runBatchPrediction(
  session: ApiSession,
  modelRef: string,
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/financial-data-science/predictions/run", session, {
    model_ref: modelRef,
    inference_mode: "batch",
    inputs: [{ revenue: 1_250_000 }],
  });
}

export async function runPipeline(session: ApiSession): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/financial-data-science/pipelines/run", session, {
    name: "On-demand Training Pipeline",
    model_type: "regression",
    feature_refs: ["revenue_30d", "cash_position", "net_profit_margin"],
  });
}
