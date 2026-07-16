"use client";

import { PageLayout } from "@marpich/core";
import {
  DataTable,
  EmptyState,
  ProgressBar,
  SkeletonTable,
  useToast,
} from "@marpich/shared";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  askCopilot,
  fetchComplianceControls,
  fetchIntelligenceDashboard,
  fetchMesh,
  listProviders,
  loadFederationSession,
  loginFederationSession,
  predictIdentityRisk,
  saveFederationSession,
  seedFederation,
  type ApiSession,
  type IntelligenceDashboard,
} from "@/lib/federationClient";

export function FederationAdminPage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("federation-admin");
  const [email, setEmail] = useState("fed-admin@enterprise.dev");
  const [password, setPassword] = useState("SecurePass123!");
  const [dashboard, setDashboard] = useState<IntelligenceDashboard | null>(null);
  const [providers, setProviders] = useState<Array<Record<string, unknown>>>([]);
  const [mesh, setMesh] = useState<Record<string, unknown> | null>(null);
  const [prediction, setPrediction] = useState<Record<string, unknown> | null>(null);
  const [copilotAnswer, setCopilotAnswer] = useState<Record<string, unknown> | null>(null);
  const [compliance, setCompliance] = useState<Record<string, unknown> | null>(null);
  const [question, setQuestion] = useState("Explain trust score and policy suggestions");

  const loadData = useCallback(async (active: ApiSession) => {
    setLoading(true);
    setProgress(35);
    setError(null);
    try {
      await seedFederation(active);
      setProgress(55);
      const [dash, prov, meshData, complianceData] = await Promise.all([
        fetchIntelligenceDashboard(active),
        listProviders(active),
        fetchMesh(active),
        fetchComplianceControls(active),
      ]);
      setDashboard(dash);
      setProviders(Array.isArray(prov) ? prov : []);
      setMesh(meshData);
      setCompliance(complianceData);
      setProgress(100);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load federation admin");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const existing = loadFederationSession();
    if (existing) {
      setSession(existing);
      void loadData(existing);
    } else {
      setLoading(false);
    }
  }, [loadData]);

  async function onLogin(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      const next = await loginFederationSession(tenantId, email, password);
      saveFederationSession(next);
      setSession(next);
      await loadData(next);
      push({ title: "Signed in", description: "Federation admin session ready" });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    }
  }

  async function onPredict() {
    if (!session) return;
    try {
      const result = await predictIdentityRisk(session, {
        failed_logins: 2,
        device_confidence: 0.4,
        behavior_confidence: 0.5,
        geo_risk: 0.3,
      });
      setPrediction(result);
      push({ title: "Prediction complete", description: String(result.classification ?? "ok") });
    } catch (err) {
      push({ title: "Prediction failed", description: err instanceof Error ? err.message : "error" });
    }
  }

  async function onCopilot() {
    if (!session) return;
    try {
      const answer = await askCopilot(session, question);
      setCopilotAnswer(answer);
    } catch (err) {
      push({ title: "Copilot failed", description: err instanceof Error ? err.message : "error" });
    }
  }

  const providerRows = useMemo(
    () =>
      providers.map((p) => ({
        ref: String(p.provider_ref ?? ""),
        name: String(p.name ?? ""),
        protocol: String(p.protocol ?? ""),
        enabled: String(p.enabled ?? false),
      })),
    [providers],
  );

  return (
    <PageLayout
      title="Identity Federation Administration"
      breadcrumb={[
        { label: "Marpich", href: "/" },
        { label: "Enterprise" },
        { label: "Federation" },
      ]}
    >
      <div className="space-y-6" dir="auto">
        {!session && (
          <form className="mp-form max-w-xl space-y-3" onSubmit={onLogin}>
            <h2 className="text-lg font-semibold">Admin sign-in</h2>
            <label className="block">
              Tenant
              <input className="mp-input w-full" value={tenantId} onChange={(e) => setTenantId(e.target.value)} />
            </label>
            <label className="block">
              Email
              <input className="mp-input w-full" value={email} onChange={(e) => setEmail(e.target.value)} />
            </label>
            <label className="block">
              Password
              <input
                type="password"
                className="mp-input w-full"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </label>
            <button type="submit" className="mp-btn">
              Continue
            </button>
          </form>
        )}

        {loading && (
          <div className="space-y-3" aria-busy="true">
            <ProgressBar value={progress} />
            <SkeletonTable rows={5} />
          </div>
        )}

        {error && (
          <EmptyState title="Unable to load federation admin" description={error} />
        )}

        {session && !loading && dashboard && (
          <>
            <section className="grid gap-4 md:grid-cols-4" aria-label="Federation KPIs">
              <article className="mp-stat">
                <h3>Providers</h3>
                <p>{String((dashboard.analytics.federation_trends as { providers?: number }).providers ?? 0)}</p>
              </article>
              <article className="mp-stat">
                <h3>Failed logins</h3>
                <p>{dashboard.analytics.failed_logins}</p>
              </article>
              <article className="mp-stat">
                <h3>AI models</h3>
                <p>{dashboard.models.length}</p>
              </article>
              <article className="mp-stat">
                <h3>Quality gates</h3>
                <p>{dashboard.quality_gates.length}</p>
              </article>
            </section>

            <section aria-label="Identity providers">
              <div className="mb-3 flex flex-wrap gap-2">
                <h2 className="text-lg font-semibold">Identity Providers</h2>
              </div>
              {providerRows.length === 0 ? (
                <EmptyState title="No providers" description="Register an IdP to begin federation." />
              ) : (
                <DataTable
                  columns={[
                    { key: "ref", header: "Ref" },
                    { key: "name", header: "Name" },
                    { key: "protocol", header: "Protocol" },
                    { key: "enabled", header: "Enabled" },
                  ]}
                  rows={providerRows}
                />
              )}
            </section>

            <section className="grid gap-4 lg:grid-cols-2" aria-label="AI intelligence">
              <div className="space-y-3">
                <h2 className="text-lg font-semibold">AI Identity Prediction</h2>
                <button type="button" className="mp-btn" onClick={() => void onPredict()}>
                  Run risk prediction
                </button>
                {prediction && (
                  <pre className="overflow-auto rounded border p-3 text-sm" aria-live="polite">
                    {JSON.stringify(prediction, null, 2)}
                  </pre>
                )}
              </div>
              <div className="space-y-3">
                <h2 className="text-lg font-semibold">Identity Copilot</h2>
                <label className="block">
                  Ask
                  <input
                    className="mp-input w-full"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                  />
                </label>
                <button type="button" className="mp-btn" onClick={() => void onCopilot()}>
                  Ask copilot
                </button>
                {copilotAnswer && (
                  <pre className="overflow-auto rounded border p-3 text-sm" aria-live="polite">
                    {JSON.stringify(copilotAnswer, null, 2)}
                  </pre>
                )}
              </div>
            </section>

            <section aria-label="AI insights">
              <h2 className="mb-2 text-lg font-semibold">AI Insights</h2>
              <ul className="space-y-2">
                {(dashboard.analytics.ai_insights ?? []).map((insight) => (
                  <li key={`${insight.type}-${insight.message}`} className="rounded border p-3">
                    <strong>{insight.severity}</strong> — {insight.message}
                    <div className="text-sm opacity-80">{insight.recommendation}</div>
                  </li>
                ))}
              </ul>
            </section>

            <section className="grid gap-4 lg:grid-cols-2" aria-label="Mesh and compliance">
              <div>
                <h2 className="mb-2 text-lg font-semibold">Identity Fabric Mesh</h2>
                <pre className="overflow-auto rounded border p-3 text-sm">
                  {JSON.stringify(mesh?.health ?? mesh, null, 2)}
                </pre>
              </div>
              <div>
                <h2 className="mb-2 text-lg font-semibold">Compliance Center</h2>
                <pre className="overflow-auto rounded border p-3 text-sm">
                  {JSON.stringify(compliance, null, 2)}
                </pre>
              </div>
            </section>
          </>
        )}
      </div>
    </PageLayout>
  );
}
