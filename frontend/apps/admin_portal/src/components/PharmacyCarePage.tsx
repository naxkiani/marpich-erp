"use client";

import { PageLayout } from "@marpich/core";
import {
  AdvancedFilterBar,
  DataTable,
  EmptyState,
  ProgressBar,
  SkeletonTable,
  StepProgress,
  useAutosave,
  useLocale,
  useToast,
} from "@marpich/shared";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  counselPrescription,
  dispensePrescription,
  fetchDispenses,
  fetchPrescriptions,
  loadPharmacySession,
  loginPharmacySession,
  receivePrescription,
  savePharmacySession,
  seedPharmacyPersonas,
  type ApiSession,
  type PharmacyDispense,
  type PharmacyPrescription,
} from "@/lib/pharmacyClient";

const DRAFT_KEY = "marpich.pharmacy.care.draft";

type TabId = "overview" | "prescriptions" | "dispenses";

function StatusChip({ status }: { status: string }) {
  const tone =
    status === "counselled" || status === "dispensed"
      ? "ok"
      : status === "received"
        ? "warn"
        : "muted";
  return (
    <span className={`mp-pharm-chip mp-pharm-chip--${tone}`} data-status={status}>
      {status}
    </span>
  );
}

export function PharmacyCarePage() {
  const { push } = useToast();
  const { t } = useLocale();
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("pharmacy-demo");
  const [email, setEmail] = useState("pharmacy@demo.dev");
  const [password, setPassword] = useState("SecurePass123!");
  const [tab, setTab] = useState<TabId>("overview");
  const [filterQ, setFilterQ] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [draftReady, setDraftReady] = useState(false);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const [rows, setRows] = useState<PharmacyPrescription[]>([]);
  const [dispenses, setDispenses] = useState<PharmacyDispense[]>([]);

  const [rx, setRx] = useState("RX-1001");
  const [patientRef, setPatientRef] = useState("peer-patient-1");
  const [drugCode, setDrugCode] = useState("AMOX500");
  const [drugName, setDrugName] = useState("Amoxicillin 500mg");
  const [qty, setQty] = useState("20");
  const [encounterRef, setEncounterRef] = useState("");
  const [counselNotes, setCounselNotes] = useState("");

  const formDraft = useMemo(
    () => ({
      filterQ,
      statusFilter,
      tab,
      rx,
      patientRef,
      drugCode,
      drugName,
      qty,
      encounterRef,
      counselNotes,
    }),
    [
      counselNotes,
      drugCode,
      drugName,
      encounterRef,
      filterQ,
      patientRef,
      qty,
      rx,
      statusFilter,
      tab,
    ],
  );

  const persistDraft = useCallback(
    async (values: typeof formDraft) => {
      if (!draftReady) return;
      try {
        localStorage.setItem(DRAFT_KEY, JSON.stringify(values));
      } catch {
        /* ignore */
      }
    },
    [draftReady],
  );

  const { saving: draftSaving } = useAutosave(formDraft, persistDraft, 900);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(DRAFT_KEY);
      if (raw) {
        const parsed = JSON.parse(raw) as Partial<typeof formDraft>;
        if (typeof parsed.filterQ === "string") setFilterQ(parsed.filterQ);
        if (typeof parsed.statusFilter === "string") setStatusFilter(parsed.statusFilter);
        if (
          parsed.tab === "overview" ||
          parsed.tab === "prescriptions" ||
          parsed.tab === "dispenses"
        ) {
          setTab(parsed.tab);
        }
        if (typeof parsed.rx === "string") setRx(parsed.rx);
        if (typeof parsed.patientRef === "string") setPatientRef(parsed.patientRef);
        if (typeof parsed.drugCode === "string") setDrugCode(parsed.drugCode);
        if (typeof parsed.drugName === "string") setDrugName(parsed.drugName);
        if (typeof parsed.qty === "string") setQty(parsed.qty);
        if (typeof parsed.encounterRef === "string") setEncounterRef(parsed.encounterRef);
        if (typeof parsed.counselNotes === "string") setCounselNotes(parsed.counselNotes);
      }
    } catch {
      /* ignore */
    }
    setDraftReady(true);
  }, []);

  const loadData = useCallback(async (active: ApiSession) => {
    setLoading(true);
    setProgress(40);
    setError(null);
    try {
      const [rxPage, dispPage] = await Promise.all([
        fetchPrescriptions(active),
        fetchDispenses(active),
      ]);
      setRows(rxPage.items ?? []);
      setDispenses(dispPage.items ?? []);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("pharmacy.loadFailed"));
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [t]);

  useEffect(() => {
    const existing = loadPharmacySession();
    if (!existing) {
      setLoading(false);
      return;
    }
    setSession(existing);
    setTenantId(existing.tenantId);
    void loadData(existing);
  }, [loadData]);

  const selected = rows.find((r) => r.id === selectedId) ?? null;

  const lifecycleStep = useMemo(() => {
    if (!selected) return 0;
    if (selected.status === "counselled") return 2;
    if (selected.status === "dispensed") return 1;
    return 0;
  }, [selected]);

  const workflowSteps = useMemo(
    () => [
      t("pharmacy.step.received"),
      t("pharmacy.step.dispensed"),
      t("pharmacy.step.counselled"),
    ],
    [t],
  );

  const filtered = useMemo(() => {
    const q = filterQ.trim().toLowerCase();
    return rows.filter((r) => {
      if (statusFilter !== "all" && r.status !== statusFilter) return false;
      if (!q) return true;
      return (
        r.rx_number.toLowerCase().includes(q) ||
        r.drug_code.toLowerCase().includes(q) ||
        r.patient_ref.toLowerCase().includes(q) ||
        r.drug_name.toLowerCase().includes(q)
      );
    });
  }, [filterQ, rows, statusFilter]);

  const stats = useMemo(
    () => ({
      prescriptions: rows.length,
      pending: rows.filter((r) => r.status === "received").length,
      dispensed: rows.filter((r) => r.status === "dispensed" || r.status === "counselled")
        .length,
      records: dispenses.length,
    }),
    [dispenses.length, rows],
  );

  async function runAction(label: string, fn: () => Promise<void>) {
    if (!session || busy) return;
    setBusy(true);
    setError(null);
    try {
      await fn();
      push({ message: label });
      await loadData(session);
    } catch (err) {
      const msg = err instanceof Error ? err.message : t("pharmacy.failed");
      setError(msg);
      push({ message: msg });
    } finally {
      setBusy(false);
    }
  }

  async function onLogin() {
    try {
      const next = await loginPharmacySession(tenantId, email, password);
      savePharmacySession(next);
      setSession(next);
      try {
        await seedPharmacyPersonas(next);
      } catch {
        /* optional */
      }
      push({ message: t("pharmacy.connected") });
      await loadData(next);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("pharmacy.connectFailed"));
    }
  }

  return (
    <PageLayout
      title={t("pharmacy.title")}
      subtitle={t("pharmacy.subtitle")}
      breadcrumb={[
        { label: t("pharmacy.breadcrumb"), href: "/healthcare/clinic" },
        { label: t("pharmacy.pharmacy") },
      ]}
      actions={
        session ? (
          <button
            type="button"
            className="mp-btn"
            disabled={loading || busy}
            onClick={() => void loadData(session)}
          >
            {t("common.refresh")}
          </button>
        ) : null
      }
    >
      <ProgressBar
        value={progress}
        label={loading ? t("pharmacy.loading") : t("pharmacy.ready")}
      />
      {error ? (
        <p className="mp-pharm-alert" role="alert">
          {error}
        </p>
      ) : null}

      {!session ? (
        <section className="mp-stack" aria-label={t("pharmacy.session")}>
          <p className="mp-field-help">{t("pharmacy.connectHelp")}</p>
          <label>
            {t("pharmacy.tenant")}
            <input value={tenantId} onChange={(e) => setTenantId(e.target.value)} />
          </label>
          <label>
            {t("pharmacy.email")}
            <input value={email} onChange={(e) => setEmail(e.target.value)} />
          </label>
          <label>
            {t("pharmacy.password")}
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <button type="button" className="mp-btn mp-btn-primary" onClick={() => void onLogin()}>
            {t("pharmacy.connect")}
          </button>
        </section>
      ) : (
        <div className="mp-desk-shell">
          <aside className="mp-desk-rail" aria-label={t("pharmacy.rail")}>
            <section className="mp-desk-rail-card">
              <header className="mp-desk-rail-head">
                <h2>{t("pharmacy.workflow")}</h2>
              </header>
              <div className="mp-desk-rail-body">
                <StepProgress steps={workflowSteps} current={lifecycleStep} />
                {draftSaving ? (
                  <p className="mp-field-help" aria-live="polite">
                    {t("pharmacy.draftSaved")}…
                  </p>
                ) : (
                  <p className="mp-field-help">{t("pharmacy.eventHint")}</p>
                )}
              </div>
            </section>
            <section className="mp-desk-rail-card" aria-label={t("pharmacy.metrics")}>
              <header className="mp-desk-rail-head">
                <h2>{t("pharmacy.metrics")}</h2>
              </header>
              <div className="mp-desk-rail-body">
                <div className="mp-desk-status-row">
                  <span>{t("pharmacy.stat.prescriptions")}</span>
                  <strong>{stats.prescriptions}</strong>
                </div>
                <div className="mp-desk-status-row">
                  <span>{t("pharmacy.stat.pending")}</span>
                  <strong>{stats.pending}</strong>
                </div>
                <div className="mp-desk-status-row">
                  <span>{t("pharmacy.stat.dispensed")}</span>
                  <strong>{stats.dispensed}</strong>
                </div>
                <div className="mp-desk-status-row">
                  <span>{t("pharmacy.stat.dispenseRecords")}</span>
                  <strong>{stats.records}</strong>
                </div>
              </div>
            </section>
          </aside>

          <div className="mp-desk-content">
            <div className="mp-desk-cats" role="tablist" aria-label={t("pharmacy.rail")}>
              {(
                [
                  ["overview", "pharmacy.tab.overview"],
                  ["prescriptions", "pharmacy.tab.prescriptions"],
                  ["dispenses", "pharmacy.tab.dispenses"],
                ] as const
              ).map(([id, key]) => (
                <button
                  key={id}
                  type="button"
                  role="tab"
                  aria-selected={tab === id}
                  className={tab === id ? "mp-btn mp-btn-primary" : "mp-btn"}
                  onClick={() => setTab(id)}
                >
                  {t(key)}
                </button>
              ))}
            </div>

            {loading ? (
              <SkeletonTable rows={5} />
            ) : tab === "overview" ? (
              <section className="mp-stack">
                <p className="mp-field-help">{t("pharmacy.overviewHelp")}</p>
                <h2>{t("pharmacy.receive")}</h2>
                <label>
                  {t("pharmacy.field.rx")}
                  <input value={rx} onChange={(e) => setRx(e.target.value)} />
                </label>
                <label>
                  {t("pharmacy.field.patientRef")}
                  <input value={patientRef} onChange={(e) => setPatientRef(e.target.value)} />
                </label>
                <p className="mp-field-help">{t("pharmacy.patientRefHelp")}</p>
                <label>
                  {t("pharmacy.field.drugCode")}
                  <input value={drugCode} onChange={(e) => setDrugCode(e.target.value)} />
                </label>
                <label>
                  {t("pharmacy.field.drugName")}
                  <input value={drugName} onChange={(e) => setDrugName(e.target.value)} />
                </label>
                <label>
                  {t("pharmacy.field.quantity")}
                  <input value={qty} onChange={(e) => setQty(e.target.value)} />
                </label>
                <label>
                  {t("pharmacy.field.encounterRef")}
                  <input
                    value={encounterRef}
                    onChange={(e) => setEncounterRef(e.target.value)}
                    placeholder={t("pharmacy.field.encounterRefHint")}
                  />
                </label>
                <button
                  type="button"
                  className="mp-btn mp-btn-primary"
                  disabled={busy}
                  onClick={() =>
                    void runAction(t("pharmacy.rxReceived"), async () => {
                      const created = await receivePrescription(session, {
                        rx_number: rx,
                        patient_ref: patientRef,
                        drug_code: drugCode,
                        drug_name: drugName,
                        quantity: Number(qty),
                        ...(encounterRef.trim()
                          ? { source_encounter_ref: encounterRef.trim() }
                          : {}),
                      });
                      setSelectedId(created.id);
                      setTab("prescriptions");
                    })
                  }
                >
                  {t("pharmacy.receive")}
                </button>
              </section>
            ) : tab === "prescriptions" ? (
              <>
                <div className="mp-desk-toolbar" role="search">
                  <AdvancedFilterBar
                    filters={[
                      { id: "q", label: t("pharmacy.filter"), type: "text" },
                      { id: "status", label: t("pharmacy.field.status"), type: "text" },
                    ]}
                    onChange={(values) => {
                      setFilterQ(values.q ?? "");
                      setStatusFilter((values.status ?? "").toLowerCase().trim() || "all");
                    }}
                  />
                </div>
                {filtered.length === 0 ? (
                  <EmptyState
                    title={t("pharmacy.noPrescriptions")}
                    description={t("pharmacy.noPrescriptionsHint")}
                  />
                ) : (
                  <DataTable
                    columns={[
                      { key: "rx_number", header: t("pharmacy.field.rx") },
                      { key: "drug", header: t("pharmacy.field.drug") },
                      { key: "status", header: t("pharmacy.field.status") },
                      { key: "action", header: t("pharmacy.field.action") },
                    ]}
                    rows={filtered.map((r) => ({
                      id: r.id,
                      rx_number: r.rx_number,
                      drug: `${r.drug_code} · ${r.drug_name}`,
                      status: <StatusChip status={r.status} />,
                      action:
                        r.status === "received" ? (
                          <button
                            type="button"
                            className="mp-btn"
                            disabled={busy}
                            onClick={() => {
                              setSelectedId(r.id);
                              void runAction(t("pharmacy.dispensedEvent"), async () => {
                                await dispensePrescription(session, r.id);
                              });
                            }}
                          >
                            {t("pharmacy.dispense")}
                          </button>
                        ) : r.status === "dispensed" ? (
                          <button
                            type="button"
                            className="mp-btn mp-btn-primary"
                            disabled={busy}
                            onClick={() => setSelectedId(r.id)}
                          >
                            {t("pharmacy.counsel")}
                          </button>
                        ) : (
                          "—"
                        ),
                    }))}
                    selectable
                    onSelectionChange={(ids) => {
                      if (ids[0]) setSelectedId(ids[0]);
                    }}
                  />
                )}
                {selected ? (
                  <section className="mp-pharm-panel" aria-label={t("pharmacy.rxDetail")}>
                    <header>{t("pharmacy.rxDetail")}</header>
                    <dl className="mp-pharm-dl">
                      <div>
                        <dt>{t("pharmacy.field.rx")}</dt>
                        <dd>{selected.rx_number}</dd>
                      </div>
                      <div>
                        <dt>{t("pharmacy.field.status")}</dt>
                        <dd>
                          <StatusChip status={selected.status} />
                        </dd>
                      </div>
                      <div>
                        <dt>{t("pharmacy.field.patientRef")}</dt>
                        <dd>{selected.patient_ref}</dd>
                      </div>
                    </dl>
                    {selected.status === "dispensed" ? (
                      <div className="mp-stack">
                        <label>
                          {t("pharmacy.field.counselNotes")}
                          <textarea
                            value={counselNotes}
                            onChange={(e) => setCounselNotes(e.target.value)}
                            rows={3}
                          />
                        </label>
                        <button
                          type="button"
                          className="mp-btn mp-btn-primary"
                          disabled={busy}
                          onClick={() =>
                            void runAction(t("pharmacy.counselledEvent"), async () => {
                              await counselPrescription(session, selected.id, {
                                notes: counselNotes || undefined,
                              });
                              setCounselNotes("");
                            })
                          }
                        >
                          {t("pharmacy.counsel")}
                        </button>
                      </div>
                    ) : null}
                    {selected.status === "received" ? (
                      <p className="mp-field-help">{t("pharmacy.selectRxHint")}</p>
                    ) : null}
                  </section>
                ) : null}
              </>
            ) : dispenses.length === 0 ? (
              <EmptyState
                title={t("pharmacy.noDispenses")}
                description={t("pharmacy.noDispensesHint")}
              />
            ) : (
              <DataTable
                columns={[
                  { key: "prescription_id", header: t("pharmacy.field.rxId") },
                  { key: "qty", header: t("pharmacy.field.quantity") },
                  { key: "at", header: t("pharmacy.field.dispensedAt") },
                ]}
                rows={dispenses.map((d) => ({
                  id: d.id,
                  prescription_id: d.prescription_id,
                  qty: d.quantity_dispensed,
                  at: d.dispensed_at ?? "—",
                }))}
              />
            )}
          </div>
        </div>
      )}

      <style jsx>{`
        .mp-pharm-alert {
          color: var(--mp-danger, #b45309);
        }
        .mp-pharm-chip {
          display: inline-block;
          padding: 0.15rem 0.5rem;
          border-radius: 999px;
          font-size: 0.8rem;
          text-transform: lowercase;
          background: var(--mp-bg-muted);
        }
        .mp-pharm-chip--ok {
          background: color-mix(in srgb, #2f9e6b 22%, transparent);
        }
        .mp-pharm-chip--warn {
          background: color-mix(in srgb, #c47a2c 24%, transparent);
        }
        .mp-pharm-panel {
          margin-block-start: 1rem;
          padding: 0.85rem 1rem;
          border: 1px solid color-mix(in srgb, currentColor 14%, transparent);
          border-radius: var(--mp-radius-sm, 8px);
        }
        .mp-pharm-panel header {
          font-weight: 600;
          margin-block-end: 0.65rem;
        }
        .mp-pharm-dl {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
          gap: 0.65rem 1rem;
          margin: 0 0 0.75rem;
        }
        .mp-pharm-dl dt {
          font-size: 0.75rem;
          opacity: 0.75;
          margin: 0;
        }
        .mp-pharm-dl dd {
          margin: 0.15rem 0 0;
          font-weight: 600;
        }
      `}</style>
    </PageLayout>
  );
}
