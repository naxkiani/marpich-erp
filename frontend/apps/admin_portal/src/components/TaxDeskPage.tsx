"use client";

import { PageLayout } from "@marpich/core";
import { useAuth } from "@marpich/auth-provider";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast,
  DeskAlert,
  DeskChrome,
  useLocale} from "@marpich/shared";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import {
  fetchTaxLiabilities,
  fetchTaxReturns,
  fileTaxReturn,
  type TaxLiability,
  type TaxReturn,
} from "@/lib/taxClient";

export function TaxDeskPage() {
  const { push } = useToast();
  const { t } = useLocale();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [liabilities, setLiabilities] = useState<TaxLiability[]>([]);
  const [returns, setReturns] = useState<TaxReturn[]>([]);
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
      const [l, r] = await Promise.all([
        fetchTaxLiabilities(session),
        fetchTaxReturns(session),
      ]);
      setLiabilities(l.items ?? []);
      setReturns(r.items ?? []);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tax");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    if (!authLoading) void loadData();
  }, [authLoading, loadData]);

  async function onFileReturn() {
    if (!session) return;
    try {
      await fileTaxReturn(session, periodLabel);
      push({ message: "Tax return filed" });
      await loadData();
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "File failed" });
    }
  }

  if (authLoading) {
    return (
      <PageLayout title="Tax" subtitle="Tax Processing">
        <SkeletonTable rows={4} />
      </PageLayout>
    );
  }

  if (!isAuthenticated || !session) {
    return (
      <PageLayout title="Tax" subtitle="Tax Processing">
        <EmptyState
          title="Sign in required"
          description="Authenticate to manage tax returns."
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
    <PageLayout title="Tax" subtitle="Liabilities & Returns (CAP-ENT-026)">
      <DeskChrome>
      <ProgressBar value={progress} />
      {error ? <DeskAlert>{error}</DeskAlert> : null}

      <p className="mp-nav-muted" style={{ marginBlock: "0.75rem" }}>
        Payroll runs create tax liabilities. File a return to emit{" "}
        <code>tax.return.filed</code>. <Link href="/payroll">Open Payroll</Link>
      </p>

      <div style={{ display: "flex", gap: "0.5rem", marginBlockEnd: "1rem", flexWrap: "wrap" }}>
        <input
          className="mp-input"
          value={periodLabel}
          onChange={(e) => setPeriodLabel(e.target.value)}
          placeholder="Period label"
          aria-label="Period label"
        />
        <button type="button" className="mp-btn mp-btn-accent" onClick={() => void onFileReturn()}>
          File tax return
        </button>
      </div>

      {loading ? (
        <SkeletonTable rows={5} />
      ) : (
        <>
          <h2 className="mp-section-title">Liabilities</h2>
          {liabilities.length === 0 ? (
            <EmptyState
              title="No liabilities"
              description="Complete a payroll run to calculate tax liabilities."
              action={
                <Link className="mp-btn" href="/payroll">
                  Open Payroll
                </Link>
              }
            />
          ) : (
            <DataTable
              columns={[
                { key: "period_label", header: "Period" },
                { key: "taxable_base", header: "Base" },
                { key: "tax_amount", header: "Tax" },
                { key: "currency", header: "CCY" },
                { key: "status", header: "Status" },
              ]}
              rows={liabilities}
            />
          )}

          <h2 className="mp-section-title" style={{ marginBlockStart: "1.5rem" }}>
            Returns
          </h2>
          {returns.length === 0 ? (
            <EmptyState title="No returns" description="File open liabilities for a period." />
          ) : (
            <DataTable
              columns={[
                { key: "period_label", header: "Period" },
                { key: "liability_count", header: "Liabilities" },
                { key: "total_tax", header: "Total tax" },
                { key: "status", header: "Status" },
              ]}
              rows={returns}
            />
          )}
        </>
      )}
          </DeskChrome>
    </PageLayout>
  );
}
