"use client";

import { PageLayout } from "@marpich/core";
import { useAuth } from "@marpich/auth-provider";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast } from "@marpich/shared";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import {
  createPayrollRun,
  fetchPayrollEmployees,
  fetchPayrollRuns,
  type PayrollEmployee,
  type PayrollRun,
} from "@/lib/payrollClient";

export function PayrollDeskPage() {
  const { push } = useToast();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [employees, setEmployees] = useState<PayrollEmployee[]>([]);
  const [runs, setRuns] = useState<PayrollRun[]>([]);
  const [periodLabel, setPeriodLabel] = useState("2026-08");

  const loadData = useCallback(async () => {
    if (!session) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setProgress(40);
    setError(null);
    try {
      const [e, r] = await Promise.all([
        fetchPayrollEmployees(session),
        fetchPayrollRuns(session),
      ]);
      setEmployees(e.items ?? []);
      setRuns(r.items ?? []);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load payroll");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    if (!authLoading) void loadData();
  }, [authLoading, loadData]);

  async function onCreateRun() {
    if (!session) return;
    try {
      await createPayrollRun(session, periodLabel);
      push({ message: "Payroll run completed" });
      await loadData();
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Run failed" });
    }
  }

  if (authLoading) {
    return (
      <PageLayout title="Payroll" subtitle="Payroll Lifecycle">
        <SkeletonTable rows={4} />
      </PageLayout>
    );
  }

  if (!isAuthenticated || !session) {
    return (
      <PageLayout title="Payroll" subtitle="Payroll Lifecycle">
        <EmptyState
          title="Sign in required"
          description="Authenticate to manage payroll."
          action={
            <Link className="mp-btn mp-btn-accent" href="/login">
              Sign in
            </Link>
          }
        />
      </PageLayout>
    );
  }

  return (
    <PageLayout title="Payroll" subtitle="Runs (CAP-ENT-015)">
      <ProgressBar value={progress} />
      {error ? <p className="mp-error">{error}</p> : null}

      <p className="mp-nav-muted" style={{ marginBlock: "0.75rem" }}>
        HR hires project into payroll employees. Complete a run to emit{" "}
        <code>payroll.run.completed</code>. <Link href="/hr">Open HR</Link>
      </p>

      <div style={{ display: "flex", gap: "0.5rem", marginBlockEnd: "1rem", flexWrap: "wrap" }}>
        <input
          className="mp-input"
          value={periodLabel}
          onChange={(e) => setPeriodLabel(e.target.value)}
          placeholder="Period label"
          aria-label="Period label"
        />
        <button type="button" className="mp-btn mp-btn-accent" onClick={() => void onCreateRun()}>
          Complete pay run
        </button>
      </div>

      {loading ? (
        <SkeletonTable rows={5} />
      ) : (
        <>
          <h2 className="mp-section-title">Projected employees</h2>
          {employees.length === 0 ? (
            <EmptyState
              title="No payroll employees"
              description="Hire an employee in HR to project into payroll."
              action={
                <Link className="mp-btn" href="/hr">
                  Open HR
                </Link>
              }
            />
          ) : (
            <DataTable
              columns={[
                { key: "full_name", header: "Name" },
                { key: "email", header: "Email" },
                { key: "base_salary", header: "Base" },
                { key: "currency", header: "CCY" },
                { key: "status", header: "Status" },
              ]}
              rows={employees}
            />
          )}

          <h2 className="mp-section-title" style={{ marginBlockStart: "1.5rem" }}>
            Pay runs
          </h2>
          {runs.length === 0 ? (
            <EmptyState title="No runs" description="Complete a pay run for active employees." />
          ) : (
            <DataTable
              columns={[
                { key: "period_label", header: "Period" },
                { key: "employee_count", header: "Employees" },
                { key: "total_gross", header: "Gross" },
                { key: "total_net", header: "Net" },
                { key: "status", header: "Status" },
              ]}
              rows={runs}
            />
          )}
        </>
      )}
    </PageLayout>
  );
}
