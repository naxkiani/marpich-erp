"use client";

import { PageLayout } from "@marpich/core";
import {
  DataTable,
  DeskAlert,
  DeskChrome,
  DeskMetrics,
  DeskPanel,
  EmptyState,
  ProgressBar,
  SkeletonTable,
  useLocale,
  useToast,
} from "@marpich/shared";
import { authHeaders, useAuth } from "@marpich/auth-provider";
import { useCallback, useEffect, useMemo, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

type WorkflowTask = {
  id: string;
  name?: string;
  status?: string;
  instance_id?: string;
  assignee_id?: string;
  created_at?: string;
  [key: string]: unknown;
};

type WorkflowDefinition = {
  key: string;
  name?: string;
  version?: number;
};

export function WorkflowDeskPage() {
  const { t } = useLocale();
  const { push } = useToast();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tasks, setTasks] = useState<WorkflowTask[]>([]);
  const [definitions, setDefinitions] = useState<WorkflowDefinition[]>([]);
  const [page, setPage] = useState(0);
  const pageSize = 10;

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
      const [tasksRes, defsRes] = await Promise.all([
        fetch(`${API_URL}/api/v1/workflow/tasks`, { headers }),
        fetch(`${API_URL}/api/v1/workflow/definitions`, { headers }),
      ]);
      if (!tasksRes.ok) throw new Error(`Tasks unavailable (${tasksRes.status})`);
      if (!defsRes.ok) throw new Error(`Definitions unavailable (${defsRes.status})`);
      const tasksJson = await tasksRes.json();
      const defsJson = await defsRes.json();
      const taskList = (tasksJson.data ?? tasksJson) as WorkflowTask[];
      const defList = (defsJson.data ?? defsJson) as WorkflowDefinition[];
      setTasks(Array.isArray(taskList) ? taskList : []);
      setDefinitions(Array.isArray(defList) ? defList : []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load workflows");
      setTasks([]);
      setDefinitions([]);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    if (!authLoading) void load();
  }, [authLoading, load]);

  async function completeTask(taskId: string, outcome: "approved" | "rejected") {
    if (!session) return;
    const res = await fetch(`${API_URL}/api/v1/workflow/tasks/${encodeURIComponent(taskId)}/complete`, {
      method: "POST",
      headers: authHeaders(session),
      body: JSON.stringify({ outcome, comment: `Completed via Task Center (${outcome})` }),
    });
    if (!res.ok) {
      push({ message: `Complete failed: ${await res.text()}` });
      return;
    }
    push({ message: `Task ${outcome}` });
    await load();
  }

  const pageRows = useMemo(() => {
    const start = page * pageSize;
    return tasks.slice(start, start + pageSize);
  }, [tasks, page]);

  const pageCount = Math.max(1, Math.ceil(tasks.length / pageSize));

  return (
    <PageLayout
      title="Workflow Task Center"
      subtitle="Human tasks and definitions from the MEOS Workflow platform (P260)."
      breadcrumb={[
        { label: t("app.name"), href: "/" },
        { label: "Platform" },
        { label: "Workflows" },
      ]}
      actions={
        <button type="button" className="mp-btn" onClick={() => void load()} disabled={loading}>
          Refresh
        </button>
      }
    >
      <DeskChrome>
      <ProgressBar value={loading ? 40 : 100} label={loading ? t("desk.loading") : t("desk.ready")} />
      <DeskMetrics items={[
        { label: "Tasks", value: tasks.length },
        { label: "Definitions", value: definitions.length },
      ]} />
      {!isAuthenticated && !authLoading ? (
        <EmptyState title={t("desk.signInRequired")} description={t("desk.signInRequired")} />
      ) : null}
      {error ? (
        <DeskAlert>{error}</DeskAlert>
      ) : null}

      <section className="mp-panel" style={{ padding: "1rem", marginBottom: "1rem" }}>
        <h2 style={{ marginTop: 0, fontSize: "1rem" }}>Definitions ({definitions.length})</h2>
        {loading ? (
          <SkeletonTable rows={3} />
        ) : definitions.length === 0 ? (
          <EmptyState title="No definitions" description="Deploy a workflow definition via API to get started." />
        ) : (
          <ul>
            {definitions.map((d) => (
              <li key={d.key}>
                <strong>{d.name ?? d.key}</strong>
                {d.version != null ? <span> · v{d.version}</span> : null}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section>
        <h2 style={{ fontSize: "1rem" }}>My tasks ({tasks.length})</h2>
        {loading ? (
          <SkeletonTable rows={5} />
        ) : tasks.length === 0 ? (
          <EmptyState title="No open tasks" description="Assigned workflow tasks will appear here." />
        ) : (
          <>
            <DataTable
              columns={[
                { key: "name", header: "Task", render: (row) => String(row.name ?? row.id) },
                { key: "status", header: "Status" },
                { key: "instance_id", header: "Instance" },
                {
                  key: "actions",
                  header: "Actions",
                  render: (row) => (
                    <span style={{ display: "inline-flex", gap: "0.35rem" }}>
                      <button
                        type="button"
                        className="mp-btn mp-btn-primary"
                        onClick={() => void completeTask(String(row.id), "approved")}
                      >
                        Approve
                      </button>
                      <button
                        type="button"
                        className="mp-btn"
                        onClick={() => void completeTask(String(row.id), "rejected")}
                      >
                        Reject
                      </button>
                    </span>
                  ),
                },
              ]}
              rows={pageRows}
            />
            <div style={{ display: "flex", gap: "0.5rem", marginTop: "0.75rem", alignItems: "center" }}>
              <button
                type="button"
                className="mp-btn"
                disabled={page <= 0}
                onClick={() => setPage((p) => Math.max(0, p - 1))}
              >
                Previous
              </button>
              <span className="mp-nav-muted">
                Page {page + 1} / {pageCount}
              </span>
              <button
                type="button"
                className="mp-btn"
                disabled={page + 1 >= pageCount}
                onClick={() => setPage((p) => p + 1)}
              >
                Next
              </button>
            </div>
          </>
        )}
      </section>
      </DeskChrome>
    </PageLayout>
  );
}
