"use client";

import { PageLayout } from "@marpich/core";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast } from "@marpich/shared";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  deployEisArtifact,
  fetchEisArtifacts,
  fetchEisCatalog,
  fetchEisCitizenWorkspace,
  fetchEisDashboard,
  fetchEisDeployments,
  fetchEisDesigner,
  fetchEisDeveloperPortal,
  fetchEisMarketplace,
  fetchEisTestRuns,
  loadEisSession,
  loginEisSession,
  publishEisArtifact,
  saveEisSession,
  seedEis,
  testEisArtifact,
  type ApiSession,
  type EisCatalog,
  type EisCitizenWorkspace,
  type EisDashboard,
  type EisDesignerGraph,
  type EisDeveloperPortal,
} from "@/lib/enterpriseIntegrationStudioClient";

const CAPABILITY_LABELS: Record<string, string> = {
  visual_api_builder: "Visual API Builder",
  visual_connector_builder: "Visual Connector Builder",
  visual_workflow_builder: "Visual Workflow Builder",
  visual_event_designer: "Visual Event Designer",
  data_mapping: "Data Mapping",
  transformation: "Transformation",
  testing: "Testing",
  mock_services: "Mock Services",
  api_documentation: "API Documentation",
  connector_marketplace: "Connector Marketplace",
  versioning: "Versioning",
  deployment: "Deployment",
  developer_portal: "Developer Portal",
  citizen_developer_workspace: "Citizen Developer Workspace",
};

const NODE_COLORS: Record<string, string> = {
  start: "#22c55e",
  end: "#6366f1",
  gateway: "#0ea5e9",
  action: "#0ea5e9",
  transform: "#8b5cf6",
  mapping: "#a855f7",
  route: "#14b8a6",
  auth: "#f59e0b",
  connector: "#3b82f6",
  event: "#ec4899",
  human: "#f97316",
  notification: "#64748b",
  source: "#22c55e",
  filter: "#eab308",
};

function StudioDesignerCanvas({ graph }: { graph: EisDesignerGraph }) {
  const nodeMap = useMemo(() => new Map(graph.nodes.map((n) => [n.id, n])), [graph.nodes]);
  const width = Math.max(...graph.nodes.map((n) => n.x), 400) + 180;
  const height = Math.max(...graph.nodes.map((n) => n.y), 200) + 80;

  function edgePath(fromId: string, toId: string): string {
    const from = nodeMap.get(fromId);
    const to = nodeMap.get(toId);
    if (!from || !to) return "";
    const x1 = from.x + 120;
    const y1 = from.y + 22;
    const x2 = to.x;
    const y2 = to.y + 22;
    return `M ${x1} ${y1} L ${x2} ${y2}`;
  }

  return (
    <div className="eis-designer-canvas">
      <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label={`Designer: ${graph.name}`}>
        <defs>
          <marker id="eis-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill="#0ea5e9" />
          </marker>
        </defs>
        {graph.edges.map((e) => (
          <path
            key={`${e.from}-${e.to}`}
            d={edgePath(e.from, e.to)}
            className="eis-edge"
            markerEnd="url(#eis-arrow)"
          />
        ))}
        {graph.nodes.map((node) => (
          <g key={node.id} transform={`translate(${node.x}, ${node.y})`}>
            <rect width={120} height={44} rx={8} fill={NODE_COLORS[node.type] ?? "#94a3b8"} />
            <text x={60} y={18} textAnchor="middle" className="eis-node-label">
              {node.label}
            </text>
            <text x={60} y={34} textAnchor="middle" className="eis-node-type">
              {node.type}
            </text>
          </g>
        ))}
      </svg>
    </div>
  );
}

export function EnterpriseIntegrationStudioDashboardPage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(15);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("eis-demo");
  const [email, setEmail] = useState("admin@eis.dev");
  const [password, setPassword] = useState("SecurePass123!");

  const [catalog, setCatalog] = useState<EisCatalog | null>(null);
  const [dashboard, setDashboard] = useState<EisDashboard | null>(null);
  const [developerPortal, setDeveloperPortal] = useState<EisDeveloperPortal | null>(null);
  const [citizenWorkspace, setCitizenWorkspace] = useState<EisCitizenWorkspace | null>(null);
  const [artifacts, setArtifacts] = useState<Array<Record<string, unknown>>>([]);
  const [marketplace, setMarketplace] = useState<Array<Record<string, unknown>>>([]);
  const [deployments, setDeployments] = useState<Array<Record<string, unknown>>>([]);
  const [testRuns, setTestRuns] = useState<Array<Record<string, unknown>>>([]);
  const [designerGraph, setDesignerGraph] = useState<EisDesignerGraph | null>(null);
  const [designerTab, setDesignerTab] = useState<"api" | "connector" | "workflow" | "event">("api");
  const [lastAction, setLastAction] = useState<string | null>(null);

  const loadData = useCallback(async (active: ApiSession) => {
    setLoading(true);
    setProgress(30);
    setError(null);
    try {
      const [cat, dash, portal, citizen, arts, mkt, deps, tests] = await Promise.all([
        fetchEisCatalog(active),
        fetchEisDashboard(active),
        fetchEisDeveloperPortal(active),
        fetchEisCitizenWorkspace(active),
        fetchEisArtifacts(active),
        fetchEisMarketplace(active),
        fetchEisDeployments(active),
        fetchEisTestRuns(active),
      ]);
      setCatalog(cat);
      setDashboard(dash);
      setDeveloperPortal(portal);
      setCitizenWorkspace(citizen);
      setArtifacts(arts);
      setMarketplace(mkt);
      setDeployments(deps);
      setTestRuns(tests);

      const match = arts.find((a) => String(a.artifact_type) === designerTab);
      if (match?.artifact_ref) {
        const graph = await fetchEisDesigner(active, String(match.artifact_ref));
        setDesignerGraph(graph);
      } else {
        setDesignerGraph(null);
      }
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load integration studio dashboard");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [designerTab]);

  useEffect(() => {
    const stored = loadEisSession();
    if (stored) {
      setSession(stored);
      void loadData(stored);
      return;
    }
    setLoading(false);
    setProgress(100);
  }, [loadData]);

  useEffect(() => {
    if (!session) return;
    const match = artifacts.find((a) => String(a.artifact_type) === designerTab);
    if (!match?.artifact_ref) {
      setDesignerGraph(null);
      return;
    }
    void fetchEisDesigner(session, String(match.artifact_ref))
      .then(setDesignerGraph)
      .catch(() => setDesignerGraph(null));
  }, [session, artifacts, designerTab]);

  const stats = useMemo(() => {
    if (!dashboard) return [];
    const s = dashboard.summary;
    return [
      { label: "Projects", value: s.projects, tone: "ok" as const },
      { label: "Artifacts", value: s.artifacts, tone: "ok" as const },
      { label: "Live deployments", value: s.deployments_live, tone: "ok" as const },
      { label: "Tests passed", value: s.tests_passed, tone: "ok" as const },
      { label: "Marketplace", value: s.marketplace_listings, tone: "ok" as const },
      { label: "Citizen projects", value: s.citizen_projects, tone: "ok" as const },
      { label: "Versions", value: s.versions, tone: "ok" as const },
      { label: "Capabilities", value: s.capabilities, tone: "ok" as const },
    ];
  }, [dashboard]);

  const capabilityRows = useMemo(() => {
    if (!catalog) return [];
    return catalog.capabilities.map((c) => ({
      capability: CAPABILITY_LABELS[c.capability] ?? c.label,
      key: c.capability,
    }));
  }, [catalog]);

  const artifactRows = useMemo(
    () =>
      artifacts.map((a) => ({
        ref: String(a.artifact_ref ?? "—"),
        name: String(a.name ?? "—"),
        type: String(a.artifact_type ?? "—"),
        status: String(a.status ?? "—"),
        version: String(a.version ?? "—"),
      })),
    [artifacts],
  );

  const marketplaceRows = useMemo(
    () =>
      marketplace.map((m) => ({
        ref: String(m.listing_ref ?? "—"),
        name: String(m.name ?? "—"),
        publisher: String(m.publisher ?? "—"),
        version: String(m.version ?? "—"),
        type: String(m.connector_type ?? "—"),
      })),
    [marketplace],
  );

  async function onConnect() {
    try {
      const next = await loginEisSession(tenantId, email, password);
      setSession(next);
      saveEisSession(next);
      push({ message: `Connected to tenant ${tenantId}` });
      await loadData(next);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Connection failed" });
    }
  }

  async function runAction(label: string, fn: (s: ApiSession) => Promise<unknown>) {
    if (!session) return;
    try {
      await fn(session);
      setLastAction(label);
      await loadData(session);
      push({ message: `${label} completed` });
    } catch (err) {
      push({ message: err instanceof Error ? err.message : `${label} failed` });
    }
  }

  const firstArtifactRef = artifacts[0]?.artifact_ref ? String(artifacts[0].artifact_ref) : null;

  return (
    <PageLayout
      title="Enterprise Integration Studio"
      breadcrumb={[
        { label: "Marpich", href: "/" },
        { label: "Enterprise", href: "/modules" },
        { label: "Integration Studio" },
      ]}
      actions={
        session ? (
          <>
            <button type="button" className="mp-btn" onClick={() => void runAction("Seed", seedEis)}>
              Seed
            </button>
            {firstArtifactRef ? (
              <>
                <button
                  type="button"
                  className="mp-btn"
                  onClick={() => void runAction("Test", (s) => testEisArtifact(s, firstArtifactRef))}
                >
                  Test latest
                </button>
                <button
                  type="button"
                  className="mp-btn"
                  onClick={() => void runAction("Publish", (s) => publishEisArtifact(s, firstArtifactRef))}
                >
                  Publish
                </button>
                <button
                  type="button"
                  className="mp-btn mp-btn-primary"
                  onClick={() => void runAction("Deploy", (s) => deployEisArtifact(s, firstArtifactRef))}
                >
                  Deploy
                </button>
              </>
            ) : null}
            <button type="button" className="mp-btn" onClick={() => session && void loadData(session)} disabled={loading}>
              Refresh
            </button>
          </>
        ) : null
      }
    >
      <p className="eis-subtitle">
        Visual API, connector, workflow, and event designers with data mapping, transformation, testing, mock services, documentation, marketplace, versioning, deployment, developer portal, and citizen workspace.
      </p>

      <ProgressBar value={progress} label={loading ? "Loading integration studio…" : "Dashboard ready"} />

      {!session ? (
        <section className="eis-connect" aria-labelledby="connect-heading">
          <h2 id="connect-heading">Connect to API</h2>
          <div className="eis-form">
            <label>
              Tenant ID
              <input className="mp-input" value={tenantId} onChange={(e) => setTenantId(e.target.value)} />
            </label>
            <label>
              Email
              <input className="mp-input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            </label>
            <label>
              Password
              <input className="mp-input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            </label>
            <button type="button" className="mp-btn mp-btn-primary" onClick={() => void onConnect()}>
              Connect
            </button>
          </div>
        </section>
      ) : null}

      {error ? <p className="eis-error" role="alert">{error}</p> : null}
      {session && loading ? <SkeletonTable rows={4} cols={4} /> : null}

      {session && dashboard && !loading ? (
        <>
          <p className="eis-muted">
            Tenant <strong>{session.tenantId}</strong>
            {lastAction ? ` · Last action: ${lastAction}` : ""}
          </p>

          <div className="eis-stats">
            {stats.map((stat) => (
              <article key={stat.label} className="eis-stat">
                <span className="eis-stat-value">{stat.value}</span>
                <span className="eis-stat-label">{stat.label}</span>
              </article>
            ))}
          </div>

          <section aria-labelledby="designer-heading">
            <h2 id="designer-heading">Visual designers</h2>
            <div className="eis-tabs" role="tablist">
              {(["api", "connector", "workflow", "event"] as const).map((tab) => (
                <button
                  key={tab}
                  type="button"
                  role="tab"
                  aria-selected={designerTab === tab}
                  className={`eis-tab${designerTab === tab ? " eis-tab-active" : ""}`}
                  onClick={() => setDesignerTab(tab)}
                >
                  {tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>
            {designerGraph ? (
              <StudioDesignerCanvas graph={designerGraph} />
            ) : (
              <EmptyState title="No designer graph" description="Seed defaults to load sample artifacts." />
            )}
          </section>

          <div className="eis-grid">
            <section aria-labelledby="portal-heading">
              <h2 id="portal-heading">{developerPortal?.title ?? "Developer Portal"}</h2>
              {developerPortal ? (
                <>
                  <p className="eis-muted">SDK: {developerPortal.sdk_languages.join(", ")}</p>
                  <ul className="eis-links">
                    {developerPortal.quick_links.map((link) => (
                      <li key={link.path}>{link.label}</li>
                    ))}
                  </ul>
                </>
              ) : null}
            </section>

            <section aria-labelledby="citizen-heading">
              <h2 id="citizen-heading">{citizenWorkspace?.title ?? "Citizen Workspace"}</h2>
              {citizenWorkspace ? (
                <>
                  <p className="eis-muted">Guided: {citizenWorkspace.guided_steps.join(" → ")}</p>
                  <div className="eis-templates">
                    {citizenWorkspace.templates.map((t) => (
                      <span key={t.id} className="eis-template-chip">
                        {t.label}
                      </span>
                    ))}
                  </div>
                </>
              ) : null}
            </section>
          </div>

          <div className="eis-grid">
            <section aria-labelledby="capabilities-heading">
              <h2 id="capabilities-heading">Capabilities ({catalog?.capabilities.length ?? 0})</h2>
              <DataTable
                columns={[
                  { key: "capability", header: "Capability", sortable: true },
                  { key: "key", header: "Key", sortable: true },
                ]}
                rows={capabilityRows}
              />
            </section>

            <section aria-labelledby="marketplace-heading">
              <h2 id="marketplace-heading">Connector marketplace ({marketplace.length})</h2>
              {marketplaceRows.length ? (
                <DataTable
                  columns={[
                    { key: "name", header: "Name", sortable: true },
                    { key: "publisher", header: "Publisher", sortable: true },
                    { key: "version", header: "Version", sortable: true },
                    { key: "type", header: "Type", sortable: true },
                  ]}
                  rows={marketplaceRows}
                />
              ) : (
                <EmptyState title="No listings" description="Run Seed to load marketplace connectors." />
              )}
            </section>
          </div>

          <section aria-labelledby="artifacts-heading">
            <h2 id="artifacts-heading">Artifacts ({artifacts.length})</h2>
            {artifactRows.length ? (
              <DataTable
                columns={[
                  { key: "ref", header: "Ref", sortable: true },
                  { key: "name", header: "Name", sortable: true },
                  { key: "type", header: "Type", sortable: true },
                  { key: "status", header: "Status", sortable: true },
                  { key: "version", header: "Version", sortable: true },
                ]}
                rows={artifactRows}
              />
            ) : (
              <EmptyState
                title="No artifacts"
                description="Seed defaults to create sample APIs, connectors, workflows, and events."
                action={
                  <button type="button" className="mp-btn mp-btn-primary" onClick={() => void runAction("Seed", seedEis)}>
                    Seed defaults
                  </button>
                }
              />
            )}
          </section>

          <div className="eis-grid">
            <section aria-labelledby="deployments-heading">
              <h2 id="deployments-heading">Deployments ({deployments.length})</h2>
              {deployments.length ? (
                <DataTable
                  columns={[
                    { key: "ref", header: "Ref", sortable: true },
                    { key: "artifact", header: "Artifact", sortable: true },
                    { key: "env", header: "Environment", sortable: true },
                    { key: "status", header: "Status", sortable: true },
                  ]}
                  rows={deployments.map((d) => ({
                    ref: String(d.deployment_ref ?? "—"),
                    artifact: String(d.artifact_ref ?? "—"),
                    env: String(d.environment ?? "—"),
                    status: String(d.status ?? "—"),
                  }))}
                />
              ) : (
                <EmptyState title="No deployments" description="Publish and deploy an artifact to sandbox." />
              )}
            </section>

            <section aria-labelledby="tests-heading">
              <h2 id="tests-heading">Test runs ({testRuns.length})</h2>
              {testRuns.length ? (
                <DataTable
                  columns={[
                    { key: "ref", header: "Ref", sortable: true },
                    { key: "artifact", header: "Artifact", sortable: true },
                    { key: "status", header: "Status", sortable: true },
                    { key: "duration", header: "Duration", sortable: true },
                  ]}
                  rows={testRuns.slice(0, 10).map((t) => ({
                    ref: String(t.test_ref ?? "—"),
                    artifact: String(t.artifact_ref ?? "—"),
                    status: String(t.status ?? "—"),
                    duration: `${t.duration_ms ?? 0}ms`,
                  }))}
                />
              ) : (
                <EmptyState title="No test runs" description="Run a mock test on an artifact." />
              )}
            </section>
          </div>
        </>
      ) : null}

      <style jsx>{`
        .eis-subtitle { color: var(--mp-text-muted, #64748b); margin: 0 0 1rem; }
        .eis-connect { margin: 1rem 0 1.5rem; padding: 1rem; border: 1px solid var(--mp-border, #e2e8f0); border-radius: 8px; }
        .eis-form { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.75rem; align-items: end; margin-top: 0.75rem; }
        label { display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.85rem; }
        .eis-muted { color: var(--mp-text-muted, #64748b); margin: 0.5rem 0; }
        .eis-error { color: #b91c1c; margin: 0.75rem 0; }
        .eis-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 0.75rem; margin: 1rem 0; }
        .eis-stat { padding: 1rem; border-radius: 8px; background: var(--mp-surface-2, #f8fafc); border: 1px solid var(--mp-border, #e2e8f0); }
        .eis-stat-value { display: block; font-size: 1.2rem; font-weight: 700; }
        .eis-stat-label { font-size: 0.75rem; color: var(--mp-text-muted, #64748b); }
        .eis-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; margin-bottom: 1.5rem; }
        .eis-tabs { display: flex; gap: 0.5rem; margin-bottom: 0.75rem; }
        .eis-tab { padding: 0.4rem 0.75rem; border: 1px solid var(--mp-border, #e2e8f0); border-radius: 6px; background: #fff; cursor: pointer; }
        .eis-tab-active { background: #0ea5e9; color: #fff; border-color: #0ea5e9; }
        .eis-designer-canvas { overflow-x: auto; border: 1px solid var(--mp-border, #e2e8f0); border-radius: 8px; background: #f8fafc; margin-bottom: 1.5rem; }
        .eis-edge { fill: none; stroke: #0ea5e9; stroke-width: 2; }
        .eis-node-label { fill: #fff; font-size: 11px; font-weight: 600; }
        .eis-node-type { fill: rgba(255,255,255,0.85); font-size: 9px; }
        .eis-links { margin: 0.5rem 0; padding-left: 1.25rem; font-size: 0.9rem; }
        .eis-templates { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
        .eis-template-chip { padding: 0.25rem 0.6rem; border-radius: 999px; background: #ede9fe; color: #5b21b6; font-size: 0.8rem; }
        h2 { margin: 0 0 0.75rem; font-size: 1.1rem; }
        @media (max-width: 960px) { .eis-grid { grid-template-columns: 1fr; } }
      `}</style>
    </PageLayout>
  );
}
