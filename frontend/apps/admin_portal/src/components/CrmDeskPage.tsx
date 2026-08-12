"use client";

import { PageLayout } from "@marpich/core";
import { useAuth } from "@marpich/auth-provider";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast } from "@marpich/shared";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import {
  createCrmContact,
  createCrmOpportunity,
  fetchCrmContacts,
  fetchCrmOpportunities,
  loseCrmOpportunity,
  winCrmOpportunity,
  type CrmContact,
  type CrmOpportunity,
} from "@/lib/crmClient";

export function CrmDeskPage() {
  const { push } = useToast();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [contacts, setContacts] = useState<CrmContact[]>([]);
  const [opportunities, setOpportunities] = useState<CrmOpportunity[]>([]);

  const [email, setEmail] = useState("buyer@acme.io");
  const [fullName, setFullName] = useState("Ada Buyer");
  const [company, setCompany] = useState("Acme");
  const [title, setTitle] = useState("Enterprise license");
  const [amount, setAmount] = useState("25000.00");
  const [selectedContactId, setSelectedContactId] = useState("");

  const loadData = useCallback(async () => {
    if (!session) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setProgress(40);
    setError(null);
    try {
      const [c, o] = await Promise.all([fetchCrmContacts(session), fetchCrmOpportunities(session)]);
      setContacts(c.items ?? []);
      setOpportunities(o.items ?? []);
      if (!selectedContactId && c.items?.[0]?.id) setSelectedContactId(c.items[0].id);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load CRM");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [session, selectedContactId]);

  useEffect(() => {
    if (!authLoading) void loadData();
  }, [authLoading, loadData]);

  async function onCreateContact() {
    if (!session) return;
    try {
      await createCrmContact(session, { email, full_name: fullName, company });
      push({ message: "Contact created" });
      await loadData();
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Create failed" });
    }
  }

  async function onCreateOpportunity() {
    if (!session || !selectedContactId) return;
    try {
      await createCrmOpportunity(session, {
        contact_id: selectedContactId,
        title,
        amount,
        currency: "USD",
      });
      push({ message: "Opportunity opened" });
      await loadData();
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Create failed" });
    }
  }

  if (authLoading) {
    return (
      <PageLayout title="CRM" subtitle="Customer Management">
        <SkeletonTable rows={4} />
      </PageLayout>
    );
  }

  if (!isAuthenticated || !session) {
    return (
      <PageLayout title="CRM" subtitle="Customer Management">
        <EmptyState
          title="Sign in required"
          description="Authenticate to manage contacts and opportunities."
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
    <PageLayout title="CRM" subtitle="Contacts · Opportunities (CAP-ENT-001)">
      <ProgressBar value={progress} />
      {error ? <p className="mp-error">{error}</p> : null}

      <section className="mp-stack" style={{ marginBlock: "1rem" }}>
        <h2>New contact</h2>
        <div className="mp-form-row">
          <input className="mp-input" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
          <input
            className="mp-input"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            placeholder="Full name"
          />
          <input
            className="mp-input"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            placeholder="Company"
          />
          <button type="button" className="mp-btn mp-btn-accent" onClick={() => void onCreateContact()}>
            Create contact
          </button>
        </div>
      </section>

      <section className="mp-stack" style={{ marginBlock: "1rem" }}>
        <h2>New opportunity</h2>
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
          <button type="button" className="mp-btn mp-btn-accent" onClick={() => void onCreateOpportunity()}>
            Open opportunity
          </button>
        </div>
      </section>

      {loading ? (
        <SkeletonTable rows={5} />
      ) : (
        <>
          <h2>Contacts</h2>
          {contacts.length === 0 ? (
            <EmptyState title="No contacts" description="Create a contact to start the pipeline." />
          ) : (
            <DataTable
              columns={[
                { key: "full_name", header: "Name" },
                { key: "email", header: "Email" },
                { key: "company", header: "Company" },
                { key: "status", header: "Status" },
              ]}
              rows={contacts}
            />
          )}

          <h2 style={{ marginBlockStart: "1.5rem" }}>Opportunities</h2>
          {opportunities.length === 0 ? (
            <EmptyState title="No opportunities" description="Open an opportunity against a contact." />
          ) : (
            <DataTable
              columns={[
                { key: "title", header: "Title" },
                { key: "amount", header: "Amount" },
                { key: "currency", header: "CCY" },
                { key: "stage", header: "Stage" },
                {
                  key: "id",
                  header: "Actions",
                  render: (row: CrmOpportunity) =>
                    row.stage === "won" || row.stage === "lost" ? (
                      <span className="mp-nav-muted">Closed</span>
                    ) : (
                      <span className="mp-form-row">
                        <button
                          type="button"
                          className="mp-btn"
                          onClick={() =>
                            void winCrmOpportunity(session, row.id).then(loadData).catch((err) =>
                              push({
                                message: err instanceof Error ? err.message : "Win failed",
                              }),
                            )
                          }
                        >
                          Win
                        </button>
                        <button
                          type="button"
                          className="mp-btn"
                          onClick={() =>
                            void loseCrmOpportunity(session, row.id, "Not a fit")
                              .then(loadData)
                              .catch((err) =>
                                push({
                                  message: err instanceof Error ? err.message : "Lose failed",
                                }),
                              )
                          }
                        >
                          Lose
                        </button>
                      </span>
                    ),
                },
              ]}
              rows={opportunities}
            />
          )}
        </>
      )}
    </PageLayout>
  );
}
