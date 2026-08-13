"use client";

import { PageLayout } from "@marpich/core";
import { useAuth } from "@marpich/auth-provider";
import {
  DataTable,
  DeskAlert,
  DeskChrome,
  DeskFormRow,
  DeskMetrics,
  DeskPanel,
  DeskToolbar,
  EmptyState,
  ProgressBar,
  SkeletonTable,
  useLocale,
  useToast,
} from "@marpich/shared";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import {
  createCrmContact,
  createCrmOpportunity,
  fetchCrmContacts,
  fetchCrmOpportunities,
  loseCrmOpportunity,
  winCrmOpportunity,
  type CrmOpportunity,
} from "@/lib/crmClient";

export function CrmDeskPage() {
  const { push } = useToast();
  const { t } = useLocale();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [contacts, setContacts] = useState<
    Array<{ id: string; full_name: string; email: string; company?: string | null; status: string }>
  >([]);
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
      <PageLayout title={t("nav.app.crm")} subtitle="CAP-ENT-001">
        <SkeletonTable rows={4} />
      </PageLayout>
    );
  }

  if (!isAuthenticated || !session) {
    return (
      <PageLayout title={t("nav.app.crm")} subtitle="CAP-ENT-001">
        <EmptyState
          title={t("desk.signInRequired")}
          description={t("desk.signInRequired")}
          action={
            <Link className="mp-btn mp-btn-primary" href="/login?returnTo=/crm">
              {t("dashboard.signIn")}
            </Link>
          }
        />
      </PageLayout>
    );
  }

  return (
    <PageLayout
      title={t("nav.app.crm")}
      subtitle="Contacts · Opportunities (CAP-ENT-001)"
      actions={
        <button type="button" className="mp-btn" onClick={() => void loadData()} disabled={loading}>
          {t("desk.refresh")}
        </button>
      }
    >
      <DeskChrome>
        <ProgressBar value={progress} label={loading ? t("desk.loading") : t("desk.ready")} />
        {error ? <DeskAlert>{error}</DeskAlert> : null}
        <DeskMetrics
          items={[
            { label: "Contacts", value: contacts.length },
            { label: "Opportunities", value: opportunities.length },
            {
              label: "Open",
              value: opportunities.filter((o) => o.stage !== "won" && o.stage !== "lost").length,
            },
          ]}
        />

        <DeskPanel title="New contact">
          <DeskFormRow>
            <div className="mp-field">
              <label htmlFor="crm-email">Email</label>
              <input id="crm-email" className="mp-input" value={email} onChange={(e) => setEmail(e.target.value)} />
            </div>
            <div className="mp-field">
              <label htmlFor="crm-name">Full name</label>
              <input
                id="crm-name"
                className="mp-input"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            </div>
            <div className="mp-field">
              <label htmlFor="crm-company">Company</label>
              <input
                id="crm-company"
                className="mp-input"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
              />
            </div>
            <DeskToolbar>
              <button type="button" className="mp-btn mp-btn-primary" onClick={() => void onCreateContact()}>
                Create contact
              </button>
            </DeskToolbar>
          </DeskFormRow>
        </DeskPanel>

        <DeskPanel title="New opportunity">
          <DeskFormRow>
            <div className="mp-field">
              <label htmlFor="crm-contact">Contact</label>
              <select
                id="crm-contact"
                className="mp-select"
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
            </div>
            <div className="mp-field">
              <label htmlFor="crm-title">Title</label>
              <input id="crm-title" className="mp-input" value={title} onChange={(e) => setTitle(e.target.value)} />
            </div>
            <div className="mp-field">
              <label htmlFor="crm-amount">Amount</label>
              <input id="crm-amount" className="mp-input" value={amount} onChange={(e) => setAmount(e.target.value)} />
            </div>
            <DeskToolbar>
              <button type="button" className="mp-btn mp-btn-primary" onClick={() => void onCreateOpportunity()}>
                Open opportunity
              </button>
            </DeskToolbar>
          </DeskFormRow>
        </DeskPanel>

        {loading ? (
          <SkeletonTable rows={5} />
        ) : (
          <>
            <DeskPanel title="Contacts">
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
            </DeskPanel>

            <DeskPanel title="Opportunities">
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
                                void winCrmOpportunity(session, row.id)
                                  .then(loadData)
                                  .catch((err) =>
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
            </DeskPanel>
          </>
        )}
      </DeskChrome>
    </PageLayout>
  );
}
