"use client";

import { PageLayout } from "@marpich/core";
import { useAuth } from "@marpich/auth-provider";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast } from "@marpich/shared";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { fetchArInvoices, issueArInvoice, receiveArPayment, type ArInvoice } from "@/lib/accountingClient";

export function AccountingArDeskPage() {
  const { push } = useToast();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [invoices, setInvoices] = useState<ArInvoice[]>([]);

  const loadData = useCallback(async () => {
    if (!session) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setProgress(40);
    setError(null);
    try {
      const page = await fetchArInvoices(session);
      setInvoices(page.items ?? []);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load AR invoices");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    if (!authLoading) void loadData();
  }, [authLoading, loadData]);

  if (authLoading) {
    return (
      <PageLayout title="Accounting" subtitle="Accounts Receivable">
        <SkeletonTable rows={4} />
      </PageLayout>
    );
  }

  if (!isAuthenticated || !session) {
    return (
      <PageLayout title="Accounting" subtitle="Accounts Receivable">
        <EmptyState
          title="Sign in required"
          description="Authenticate to manage AR invoices."
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
    <PageLayout title="Accounting" subtitle="AR Invoices (CAP-ENT-023)">
      <ProgressBar value={progress} />
      {error ? <p className="mp-error">{error}</p> : null}

      <p className="mp-nav-muted" style={{ marginBlock: "0.75rem" }}>
        Placed sales orders create draft invoices. Issue posts AR; record payment clears AR and emits{" "}
        <code>accounting.payment.received</code>. <Link href="/sales">Open Sales</Link>
      </p>

      {loading ? (
        <SkeletonTable rows={5} />
      ) : invoices.length === 0 ? (
        <EmptyState
          title="No invoices"
          description="Convert a sales quotation to an order to draft an AR invoice."
        />
      ) : (
        <DataTable
          columns={[
            { key: "title", header: "Title" },
            { key: "amount", header: "Amount" },
            { key: "currency", header: "CCY" },
            { key: "status", header: "Status" },
            {
              key: "id",
              header: "Actions",
              render: (row: ArInvoice) => {
                if (row.status === "draft") {
                  return (
                    <button
                      type="button"
                      className="mp-btn"
                      onClick={() =>
                        void issueArInvoice(session, row.id)
                          .then(loadData)
                          .catch((err) =>
                            push({
                              message: err instanceof Error ? err.message : "Issue failed",
                            }),
                          )
                      }
                    >
                      Issue
                    </button>
                  );
                }
                if (row.status === "issued") {
                  return (
                    <button
                      type="button"
                      className="mp-btn"
                      onClick={() =>
                        void receiveArPayment(session, row.id)
                          .then(loadData)
                          .catch((err) =>
                            push({
                              message: err instanceof Error ? err.message : "Payment failed",
                            }),
                          )
                      }
                    >
                      Record payment
                    </button>
                  );
                }
                return <span className="mp-nav-muted">{row.status}</span>;
              },
            },
          ]}
          rows={invoices}
        />
      )}
    </PageLayout>
  );
}
