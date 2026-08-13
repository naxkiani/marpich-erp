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
  convertSalesQuotation,
  createSalesQuotation,
  fetchSalesOrders,
  fetchSalesQuotations,
  sendSalesQuotation,
  type SalesOrder,
  type SalesQuotation,
} from "@/lib/salesClient";
import { fetchCrmContacts, type CrmContact } from "@/lib/crmClient";

export function SalesDeskPage() {
  const { push } = useToast();
  const { t } = useLocale();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [quotations, setQuotations] = useState<SalesQuotation[]>([]);
  const [orders, setOrders] = useState<SalesOrder[]>([]);
  const [contacts, setContacts] = useState<CrmContact[]>([]);

  const [selectedContactId, setSelectedContactId] = useState("");
  const [title, setTitle] = useState("Professional services");
  const [amount, setAmount] = useState("10000.00");

  const loadData = useCallback(async () => {
    if (!session) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setProgress(40);
    setError(null);
    try {
      const [q, o, c] = await Promise.all([
        fetchSalesQuotations(session),
        fetchSalesOrders(session),
        fetchCrmContacts(session).catch(() => ({ items: [] as CrmContact[], total: 0, limit: 50, offset: 0 })),
      ]);
      setQuotations(q.items ?? []);
      setOrders(o.items ?? []);
      setContacts(c.items ?? []);
      if (!selectedContactId && c.items?.[0]?.id) setSelectedContactId(c.items[0].id);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load Sales");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [session, selectedContactId]);

  useEffect(() => {
    if (!authLoading) void loadData();
  }, [authLoading, loadData]);

  async function onCreateQuotation() {
    if (!session || !selectedContactId) return;
    try {
      await createSalesQuotation(session, {
        contact_id: selectedContactId,
        title,
        amount,
        currency: "USD",
      });
      push({ message: "Quotation drafted" });
      await loadData();
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Create failed" });
    }
  }

  if (authLoading) {
    return (
      <PageLayout title="Sales" subtitle="Quotations & Orders">
        <SkeletonTable rows={4} />
      </PageLayout>
    );
  }

  if (!isAuthenticated || !session) {
    return (
      <PageLayout title="Sales" subtitle="Quotations & Orders">
        <EmptyState
          title="Sign in required"
          description="Authenticate to manage quotations and orders."
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
    <PageLayout title="Sales" subtitle="Quotations · Orders (CAP-ENT-002)">
      <DeskChrome>
      <ProgressBar value={progress} />
      {error ? <DeskAlert>{error}</DeskAlert> : null}

      <p className="mp-nav-muted" style={{ marginBlock: "0.75rem" }}>
        Won CRM opportunities auto-create draft quotations.{" "}
        <Link href="/crm">Open CRM</Link>
      </p>

      <section className="mp-stack" style={{ marginBlock: "1rem" }}>
        <h2>New quotation</h2>
        <div className="mp-form-row">
          <select
            className="mp-input"
            value={selectedContactId}
            onChange={(e) => setSelectedContactId(e.target.value)}
          >
            <option value="">Select contact</option>
            {contacts.map((c) => (
              <option key={c.id} value={c.id}>
                {c.full_name} ({c.email})
              </option>
            ))}
          </select>
          <input className="mp-input" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Title" />
          <input className="mp-input" value={amount} onChange={(e) => setAmount(e.target.value)} placeholder="Amount" />
          <button type="button" className="mp-btn mp-btn-accent" onClick={() => void onCreateQuotation()}>
            Draft quotation
          </button>
        </div>
      </section>

      {loading ? (
        <SkeletonTable rows={5} />
      ) : (
        <>
          <h2>Quotations</h2>
          {quotations.length === 0 ? (
            <EmptyState
              title="No quotations"
              description="Win a CRM opportunity or draft a quotation manually."
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
                  render: (row: SalesQuotation) => {
                    if (row.status === "draft") {
                      return (
                        <button
                          type="button"
                          className="mp-btn"
                          onClick={() =>
                            void sendSalesQuotation(session, row.id)
                              .then(loadData)
                              .catch((err) =>
                                push({
                                  message: err instanceof Error ? err.message : "Send failed",
                                }),
                              )
                          }
                        >
                          Send
                        </button>
                      );
                    }
                    if (row.status === "sent" || row.status === "accepted") {
                      return (
                        <button
                          type="button"
                          className="mp-btn"
                          onClick={() =>
                            void convertSalesQuotation(session, row.id)
                              .then(loadData)
                              .catch((err) =>
                                push({
                                  message: err instanceof Error ? err.message : "Convert failed",
                                }),
                              )
                          }
                        >
                          Convert to order
                        </button>
                      );
                    }
                    return <span className="mp-nav-muted">{row.status}</span>;
                  },
                },
              ]}
              rows={quotations}
            />
          )}

          <h2 style={{ marginBlockStart: "1.5rem" }}>Orders</h2>
          {orders.length === 0 ? (
            <EmptyState title="No orders" description="Convert an accepted quotation to place an order." />
          ) : (
            <DataTable
              columns={[
                { key: "title", header: "Title" },
                { key: "amount", header: "Amount" },
                { key: "currency", header: "CCY" },
                { key: "status", header: "Status" },
                { key: "quotation_id", header: "Quotation" },
              ]}
              rows={orders}
            />
          )}
        </>
      )}
          </DeskChrome>
    </PageLayout>
  );
}
