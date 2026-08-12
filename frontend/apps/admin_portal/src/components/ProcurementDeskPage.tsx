"use client";

import { PageLayout } from "@marpich/core";
import { useAuth } from "@marpich/auth-provider";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast } from "@marpich/shared";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import {
  approveRequisition,
  fetchRequisitions,
  receiveRequisition,
  submitRequisition,
  type PurchaseRequisition,
} from "@/lib/procurementClient";

export function ProcurementDeskPage() {
  const { push } = useToast();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [requisitions, setRequisitions] = useState<PurchaseRequisition[]>([]);

  const loadData = useCallback(async () => {
    if (!session) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setProgress(40);
    setError(null);
    try {
      const page = await fetchRequisitions(session);
      setRequisitions(page.items ?? []);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load requisitions");
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
      <PageLayout title="Procurement" subtitle="Purchase requisitions">
        <SkeletonTable rows={4} />
      </PageLayout>
    );
  }

  if (!isAuthenticated || !session) {
    return (
      <PageLayout title="Procurement" subtitle="Purchase requisitions">
        <EmptyState
          title="Sign in required"
          description="Authenticate to manage purchase requisitions."
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
    <PageLayout title="Procurement" subtitle="Requisitions (CAP-ENT-040)">
      <ProgressBar value={progress} />
      {error ? <p className="mp-error">{error}</p> : null}

      <p className="mp-nav-muted" style={{ marginBlock: "0.75rem" }}>
        Low available stock after sales reservations auto-creates draft requisitions.{" "}
        <Link href="/inventory">Open Inventory</Link>
      </p>

      {loading ? (
        <SkeletonTable rows={5} />
      ) : requisitions.length === 0 ? (
        <EmptyState
          title="No requisitions"
          description="Place a sales order when stock is near the reorder threshold."
        />
      ) : (
        <DataTable
          columns={[
            { key: "sku", header: "SKU" },
            { key: "quantity", header: "Reorder qty" },
            { key: "quantity_available", header: "Available" },
            { key: "status", header: "Status" },
            {
              key: "id",
              header: "Actions",
              render: (row: PurchaseRequisition) => {
                if (row.status === "draft") {
                  return (
                    <button
                      type="button"
                      className="mp-btn"
                      onClick={() =>
                        void submitRequisition(session, row.id)
                          .then(loadData)
                          .catch((err) =>
                            push({
                              message: err instanceof Error ? err.message : "Submit failed",
                            }),
                          )
                      }
                    >
                      Submit
                    </button>
                  );
                }
                if (row.status === "submitted") {
                  return (
                    <button
                      type="button"
                      className="mp-btn"
                      onClick={() =>
                        void approveRequisition(session, row.id)
                          .then(loadData)
                          .catch((err) =>
                            push({
                              message: err instanceof Error ? err.message : "Approve failed",
                            }),
                          )
                      }
                    >
                      Approve PO
                    </button>
                  );
                }
                if (row.status === "approved") {
                  return (
                    <button
                      type="button"
                      className="mp-btn"
                      onClick={() =>
                        void receiveRequisition(session, row.id)
                          .then(loadData)
                          .catch((err) =>
                            push({
                              message: err instanceof Error ? err.message : "Receive failed",
                            }),
                          )
                      }
                    >
                      Receive goods
                    </button>
                  );
                }
                return <span className="mp-nav-muted">{row.status}</span>;
              },
            },
          ]}
          rows={requisitions}
        />
      )}
    </PageLayout>
  );
}
