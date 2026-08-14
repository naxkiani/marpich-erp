"use client";

import { PageLayout } from "@marpich/core";
import {
  DeskAlert,
  DeskChrome,
  DeskPanel,
  EmptyState,
  ProgressBar,
  useLocale,
  useToast,
} from "@marpich/shared";
import { authHeaders, useAuth } from "@marpich/auth-provider";
import { useCallback, useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

type PolicyRow = {
  id?: string;
  key?: string;
  domain?: string;
  version?: number;
  status?: string;
  [key: string]: unknown;
};

export function PolicyDeskPage() {
  const { t } = useLocale();
  const { push } = useToast();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [policies, setPolicies] = useState<PolicyRow[]>([]);
  const [evalResult, setEvalResult] = useState<string | null>(null);
  const [domain, setDomain] = useState("privacy");
  const [policyKey, setPolicyKey] = useState("export_pii");

  const load = useCallback(async () => {
    if (!session) {
      setLoading(false);
      setError("Sign in required.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const headers = authHeaders(session);
      const res = await fetch(`${API_URL}/api/v1/policies`, { headers });
      if (!res.ok) throw new Error(`Policies unavailable (${res.status})`);
      const json = await res.json();
      const data = json.data ?? json;
      const items = Array.isArray(data) ? data : (data.items ?? []);
      setPolicies(items);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load policies");
      setPolicies([]);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    if (!authLoading) void load();
  }, [authLoading, load]);

  const runEvaluate = async () => {
    if (!session) return;
    setEvalResult(null);
    try {
      const res = await fetch(`${API_URL}/api/v1/policies/evaluate`, {
        method: "POST",
        headers: { ...authHeaders(session), "Content-Type": "application/json" },
        body: JSON.stringify({ domain, policy_key: policyKey, facts: { resource: "demo" } }),
      });
      const json = await res.json().catch(() => ({}));
      setEvalResult(`${res.status}: ${JSON.stringify(json.data ?? json)}`);
      if (res.ok) push({ message: "Policy evaluated" });
    } catch (err) {
      setEvalResult(err instanceof Error ? err.message : "Evaluate failed");
    }
  };

  if (authLoading || loading) {
    return (
      <PageLayout title={t("nav.policy") || "Policy"}>
        <ProgressBar />
      </PageLayout>
    );
  }

  if (!isAuthenticated) {
    return (
      <PageLayout title={t("nav.policy") || "Policy"}>
        <EmptyState title="Sign in required" description="Policy Engine requires a session." />
      </PageLayout>
    );
  }

  return (
    <PageLayout title={t("nav.policy") || "Policy & Compliance"}>
      <DeskChrome>
        {error ? <DeskAlert>{error}</DeskAlert> : null}
        <DeskPanel title="Evaluate">
          <div style={{ display: "flex", flexWrap: "wrap", gap: "0.75rem", alignItems: "end" }}>
            <label>
              Domain
              <input value={domain} onChange={(e) => setDomain(e.target.value)} />
            </label>
            <label>
              Policy key
              <input value={policyKey} onChange={(e) => setPolicyKey(e.target.value)} />
            </label>
            <button type="button" onClick={() => void runEvaluate()}>
              Evaluate
            </button>
          </div>
          {evalResult ? <pre style={{ marginTop: "1rem", whiteSpace: "pre-wrap" }}>{evalResult}</pre> : null}
        </DeskPanel>
        <DeskPanel title="Policies">
          {policies.length === 0 ? (
            <EmptyState title="No policies listed" description="Create policies via Policy Engine API." />
          ) : (
            <ul>
              {policies.map((p, i) => (
                <li key={String(p.id ?? p.key ?? i)}>
                  {String(p.domain ?? "")}/{String(p.key ?? p.id ?? "policy")} v{String(p.version ?? "?")}{" "}
                  {p.status ? `(${String(p.status)})` : ""}
                </li>
              ))}
            </ul>
          )}
        </DeskPanel>
      </DeskChrome>
    </PageLayout>
  );
}
