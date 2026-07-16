"use client";

import { PageLayout } from "@marpich/core";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast } from "@marpich/shared";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  executeEcfOperation,
  fetchEcfCatalog,
  fetchEcfConnectorCatalog,
  fetchEcfConnectors,
  fetchEcfDashboard,
  fetchEcfExecutions,
  fetchEcfSdk,
  loadEcfSession,
  loginEcfSession,
  saveEcfSession,
  seedEcf,
  testEcfConnector,
  type ApiSession,
  type EcfCatalog,
  type EcfDashboard,
} from "@/lib/enterpriseConnectorFrameworkClient";

const CAPABILITY_LABELS: Record<string, string> = {
  core_banking_systems: "Core Banking Systems",
  payment_gateways: "Payment Gateways",
  government_services: "Government Services",
  tax_authorities: "Tax Authorities",
  central_banks: "Central Banks",
  erp_systems: "ERP Systems",
  crm_systems: "CRM Systems",
  moodle: "Moodle",
  google_classroom: "Google Classroom",
  microsoft_365: "Microsoft 365",
  google_workspace: "Google Workspace",
  ldap: "LDAP",
  active_directory: "Active Directory",
  azure_ad: "Azure AD",
  email: "Email",
  sms: "SMS",
  whatsapp_business_api: "WhatsApp Business API",
  push_notifications: "Push Notifications",
  cloud_storage: "Cloud Storage",
  document_management_systems: "Document Management Systems",
  plugin_architecture: "Plug-in Architecture",
  connector_sdk: "Connector SDK",
  connector_monitoring: "Connector Monitoring",
  connector_management_console: "Connector Management Console",
};

export function EnterpriseConnectorFrameworkDashboardPage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(15);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("ecf-demo");
  const [email, setEmail] = useState("admin@ecf.dev");
  const [password, setPassword] = useState("SecurePass123!");

  const [catalog, setCatalog] = useState<EcfCatalog | null>(null);
  const [dashboard, setDashboard] = useState<EcfDashboard | null>(null);
  const [connectors, setConnectors] = useState<Array<Record<string, unknown>>>([]);
  const [connectorCatalog, setConnectorCatalog] = useState<Array<Record<string, unknown>>>([]);
  const [sdkInfo, setSdkInfo] = useState<Record<string, unknown> | null>(null);
  const [executions, setExecutions] = useState<Array<Record<string, unknown>>>([]);
  const [lastAction, setLastAction] = useState<string | null>(null);

  const loadData = useCallback(async (active: ApiSession) => {
    setLoading(true);
    setProgress(30);
    setError(null);
    try {
      const [cat, dash, conns, catEntries, sdk, execs] = await Promise.all([
        fetchEcfCatalog(active),
        fetchEcfDashboard(active),
        fetchEcfConnectors(active),
        fetchEcfConnectorCatalog(active),
        fetchEcfSdk(active),
        fetchEcfExecutions(active),
      ]);
      setCatalog(cat);
      setDashboard(dash);
      setConnectors(conns);
      setConnectorCatalog(catEntries.entries);
      setSdkInfo(sdk);
      setExecutions(execs);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load connector framework console");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const stored = loadEcfSession();
    if (stored) {
      setSession(stored);
      void loadData(stored);
      return;
    }
    setLoading(false);
    setProgress(100);
  }, [loadData]);

  const stats = useMemo(() => {
    if (!dashboard) return [];
    const s = dashboard.summary;
    return [
      { label: "Capabilities", value: s.capabilities, tone: "ok" as const },
      { label: "Instances", value: s.connector_instances, tone: "ok" as const },
      { label: "Active", value: s.active_instances, tone: "ok" as const },
      { label: "SDK types", value: s.sdk_registered_types, tone: "ok" as const },
      { label: "Success rate", value: `${s.success_rate_pct}%`, tone: s.success_rate_pct < 90 ? "warn" : "ok" },
      { label: "Plugin bindings", value: s.plugin_bindings, tone: "ok" as const },
      { label: "Healthy", value: s.healthy_connectors, tone: "ok" as const },
      { label: "Executions", value: s.executions_total, tone: "ok" as const },
    ];
  }, [dashboard]);

  const capabilityRows = useMemo(() => {
    if (!catalog) return [];
    return catalog.capabilities.map((c) => ({
      capability: CAPABILITY_LABELS[c.capability] ?? c.label,
      key: c.capability,
    }));
  }, [catalog]);

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      const active = await loginEcfSession(tenantId, email, password);
      setSession(active);
      saveEcfSession(active);
      await loadData(active);
      push({ title: "Signed in", variant: "success" });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
      setLoading(false);
    }
  }

  async function runSeed() {
    if (!session) return;
    const result = await seedEcf(session);
    setLastAction(`Seeded ${result.connector_instances} connector instances`);
    await loadData(session);
    push({ title: "Connectors seeded", variant: "success" });
  }

  async function runTest() {
    if (!session) return;
    const bank = connectors.find((c) => c.connector_type === "bank_api");
    if (!bank) return;
    const result = await testEcfConnector(session, String(bank.instance_ref));
    setLastAction(`Health check: connected=${String(result.connected)}`);
    await loadData(session);
    push({ title: "Connection tested", variant: "success" });
  }

  async function runExecute() {
    if (!session) return;
    const bank = connectors.find((c) => c.connector_type === "bank_api");
    if (!bank) return;
    const result = await executeEcfOperation(session, String(bank.instance_ref), "balance_inquiry", { account_ref: "ACC-1" });
    setLastAction(`Executed ${result.operation} — ${result.status}`);
    await loadData(session);
    push({ title: "Operation executed", variant: "success" });
  }

  return (
    <PageLayout title="Enterprise Connector Framework" breadcrumbs={[{ label: "Enterprise" }, { label: "Connector Framework" }]}>
      <div className="ecf-console">
        <ProgressBar value={progress} />
        {error ? <p className="ecf-error">{error}</p> : null}

        {!session ? (
          <form className="ecf-login" onSubmit={handleLogin}>
            <p className="ecf-muted">Sign in to open the connector management console.</p>
            <label>Tenant<input value={tenantId} onChange={(e) => setTenantId(e.target.value)} /></label>
            <label>Email<input value={email} onChange={(e) => setEmail(e.target.value)} /></label>
            <label>Password<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></label>
            <button type="submit">Sign in</button>
          </form>
        ) : null}

        {session && loading ? <SkeletonTable rows={6} /> : null}

        {session && !loading && dashboard ? (
          <>
            <section className="ecf-stats">
              {stats.map((s) => (
                <div key={s.label} className={`ecf-stat ecf-stat--${s.tone}`}>
                  <span>{s.label}</span>
                  <strong>{s.value}</strong>
                </div>
              ))}
            </section>

            <section className="ecf-actions">
              <button type="button" onClick={() => void runSeed()}>Seed connectors</button>
              <button type="button" onClick={() => void runTest()} disabled={!connectors.length}>Test bank API</button>
              <button type="button" onClick={() => void runExecute()} disabled={!connectors.length}>Execute balance inquiry</button>
            </section>
            {lastAction ? <p className="ecf-muted">Last action: {lastAction}</p> : null}
            {sdkInfo ? <p className="ecf-muted">SDK: {String(sdkInfo.package)} — {String(sdkInfo.total)} registered types</p> : null}

            <section>
              <h2>Capabilities</h2>
              <DataTable columns={[{ key: "capability", header: "Capability" }, { key: "key", header: "Key" }]} rows={capabilityRows} empty={<EmptyState title="No capabilities" />} />
            </section>

            <section>
              <h2>Connector catalog</h2>
              <DataTable
                columns={[
                  { key: "connector_type", header: "Type" },
                  { key: "display_name", header: "Name" },
                  { key: "category", header: "Category" },
                  { key: "sdk_registered", header: "SDK" },
                ]}
                rows={connectorCatalog.slice(0, 24).map((e) => ({
                  connector_type: String(e.connector_type ?? ""),
                  display_name: String(e.display_name ?? ""),
                  category: String(e.category ?? ""),
                  sdk_registered: e.sdk_registered ? "Yes" : "No",
                }))}
                empty={<EmptyState title="No catalog entries" />}
              />
            </section>

            <section>
              <h2>Connector instances</h2>
              <DataTable
                columns={[
                  { key: "instance_ref", header: "Ref" },
                  { key: "connector_type", header: "Type" },
                  { key: "display_name", header: "Name" },
                  { key: "status", header: "Status" },
                ]}
                rows={connectors.slice(0, 20).map((c) => ({
                  instance_ref: String(c.instance_ref ?? ""),
                  connector_type: String(c.connector_type ?? ""),
                  display_name: String(c.display_name ?? ""),
                  status: String(c.status ?? ""),
                }))}
                empty={<EmptyState title="No instances — seed first" />}
              />
            </section>

            <section>
              <h2>Recent executions</h2>
              <DataTable
                columns={[
                  { key: "execution_ref", header: "Ref" },
                  { key: "connector_type", header: "Type" },
                  { key: "operation", header: "Operation" },
                  { key: "status", header: "Status" },
                ]}
                rows={executions.slice(0, 15).map((e) => ({
                  execution_ref: String(e.execution_ref ?? ""),
                  connector_type: String(e.connector_type ?? ""),
                  operation: String(e.operation ?? ""),
                  status: String(e.status ?? ""),
                }))}
                empty={<EmptyState title="No executions yet" />}
              />
            </section>
          </>
        ) : null}
      </div>
    </PageLayout>
  );
}
