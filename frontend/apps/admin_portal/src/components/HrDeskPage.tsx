"use client";

import { PageLayout } from "@marpich/core";
import { useAuth } from "@marpich/auth-provider";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast } from "@marpich/shared";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import {
  fetchEmployees,
  hireEmployee,
  terminateEmployee,
  type HrEmployee,
} from "@/lib/hrClient";

export function HrDeskPage() {
  const { push } = useToast();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [employees, setEmployees] = useState<HrEmployee[]>([]);

  const [email, setEmail] = useState("ada@acme.io");
  const [fullName, setFullName] = useState("Ada Lovelace");
  const [jobTitle, setJobTitle] = useState("Engineer");
  const [department, setDepartment] = useState("R&D");
  const [employeeNumber, setEmployeeNumber] = useState("E-1001");

  const loadData = useCallback(async () => {
    if (!session) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setProgress(40);
    setError(null);
    try {
      const page = await fetchEmployees(session);
      setEmployees(page.items ?? []);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load employees");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    if (!authLoading) void loadData();
  }, [authLoading, loadData]);

  async function onHire() {
    if (!session) return;
    try {
      await hireEmployee(session, {
        email,
        full_name: fullName,
        job_title: jobTitle,
        department,
        employee_number: employeeNumber,
      });
      push({ message: "Employee hired" });
      await loadData();
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Hire failed" });
    }
  }

  if (authLoading) {
    return (
      <PageLayout title="Human Resources" subtitle="Employee Management">
        <SkeletonTable rows={4} />
      </PageLayout>
    );
  }

  if (!isAuthenticated || !session) {
    return (
      <PageLayout title="Human Resources" subtitle="Employee Management">
        <EmptyState
          title="Sign in required"
          description="Authenticate to manage employees."
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
    <PageLayout title="Human Resources" subtitle="Employees (CAP-ENT-010)">
      <ProgressBar value={progress} />
      {error ? <p className="mp-error">{error}</p> : null}

      <p className="mp-nav-muted" style={{ marginBlock: "0.75rem" }}>
        Hire employees and terminate active records. Emits{" "}
        <code>human_resources.employee.hired</code> / <code>.terminated</code>.
      </p>

      <div
        style={{
          display: "grid",
          gap: "0.5rem",
          marginBlockEnd: "1rem",
          maxInlineSize: "32rem",
        }}
      >
        <input
          className="mp-input"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          aria-label="Email"
        />
        <input
          className="mp-input"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          placeholder="Full name"
          aria-label="Full name"
        />
        <input
          className="mp-input"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          placeholder="Job title"
          aria-label="Job title"
        />
        <input
          className="mp-input"
          value={department}
          onChange={(e) => setDepartment(e.target.value)}
          placeholder="Department"
          aria-label="Department"
        />
        <input
          className="mp-input"
          value={employeeNumber}
          onChange={(e) => setEmployeeNumber(e.target.value)}
          placeholder="Employee number"
          aria-label="Employee number"
        />
        <button type="button" className="mp-btn mp-btn-accent" onClick={() => void onHire()}>
          Hire employee
        </button>
      </div>

      {loading ? (
        <SkeletonTable rows={5} />
      ) : employees.length === 0 ? (
        <EmptyState title="No employees" description="Hire the first employee to get started." />
      ) : (
        <DataTable
          columns={[
            { key: "full_name", header: "Name" },
            { key: "email", header: "Email" },
            { key: "job_title", header: "Title" },
            { key: "department", header: "Dept" },
            { key: "status", header: "Status" },
            {
              key: "id",
              header: "Actions",
              render: (row: HrEmployee) =>
                row.status === "active" ? (
                  <button
                    type="button"
                    className="mp-btn"
                    onClick={() =>
                      void terminateEmployee(session, row.id, "Desk termination")
                        .then(loadData)
                        .catch((err) =>
                          push({
                            message: err instanceof Error ? err.message : "Terminate failed",
                          }),
                        )
                    }
                  >
                    Terminate
                  </button>
                ) : (
                  <span className="mp-nav-muted">{row.status}</span>
                ),
            },
          ]}
          rows={employees}
        />
      )}
    </PageLayout>
  );
}
