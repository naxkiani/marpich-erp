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
  fetchLabOrders,
  fetchLabSamples,
  finalizeLabResult,
  loadLaboratorySession,
  loginLaboratorySession,
  placeLabOrder,
  receiveLabSample,
  saveLaboratorySession,
  seedLaboratoryPersonas,
  type ApiSession,
  type LabOrder,
  type LabSample,
} from "@/lib/laboratoryClient";

const DRAFT_KEY = "marpich.laboratory.care.draft";

type TabId = "overview" | "orders" | "samples" | "results";

function StatusChip({ status }: { status: string }) {
  const tone =
    status === "finalized"
      ? "ok"
      : status === "sample_received"
        ? "warn"
        : status === "ordered"
          ? "neutral"
          : "muted";
  return (
    <span className={`mp-lab-chip mp-lab-chip--${tone}`} data-status={status}>
      {status}
    </span>
  );
}

export function LaboratoryCarePage() {
  const { push } = useToast();
  const { t } = useLocale();
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("laboratory-demo");
  const [email, setEmail] = useState("lab@demo.dev");
  const [password, setPassword] = useState("SecurePass123!");
  const [tab, setTab] = useState<TabId>("overview");
  const [filterQ, setFilterQ] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [draftReady, setDraftReady] = useState(false);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const [orders, setOrders] = useState<LabOrder[]>([]);
  const [samples, setSamples] = useState<LabSample[]>([]);

  const [orderNumber, setOrderNumber] = useState("LAB-2001");
  const [patientRef, setPatientRef] = useState("peer-patient-1");
  const [testCode, setTestCode] = useState("CBC");
  const [encounterRef, setEncounterRef] = useState("");
  const [specimenType, setSpecimenType] = useState("whole_blood");
  const [resultValue, setResultValue] = useState("5.2");
  const [resultUnit, setResultUnit] = useState("10^9/L");

  const formDraft = useMemo(
    () => ({
      filterQ,
      statusFilter,
      tab,
      orderNumber,
      patientRef,
      testCode,
      encounterRef,
      specimenType,
      resultValue,
      resultUnit,
    }),
    [
      encounterRef,
      filterQ,
      orderNumber,
      patientRef,
      resultUnit,
      resultValue,
      specimenType,
      statusFilter,
      tab,
      testCode,
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
          parsed.tab === "orders" ||
          parsed.tab === "samples" ||
          parsed.tab === "results"
        ) {
          setTab(parsed.tab);
        }
        if (typeof parsed.orderNumber === "string") setOrderNumber(parsed.orderNumber);
        if (typeof parsed.patientRef === "string") setPatientRef(parsed.patientRef);
        if (typeof parsed.testCode === "string") setTestCode(parsed.testCode);
        if (typeof parsed.encounterRef === "string") setEncounterRef(parsed.encounterRef);
        if (typeof parsed.specimenType === "string") setSpecimenType(parsed.specimenType);
        if (typeof parsed.resultValue === "string") setResultValue(parsed.resultValue);
        if (typeof parsed.resultUnit === "string") setResultUnit(parsed.resultUnit);
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
      const [orderPage, samplePage] = await Promise.all([
        fetchLabOrders(active),
        fetchLabSamples(active),
      ]);
      setOrders(orderPage.items ?? []);
      setSamples(samplePage.items ?? []);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("laboratory.loadFailed"));
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [t]);

  useEffect(() => {
    const existing = loadLaboratorySession();
    if (!existing) {
      setLoading(false);
      return;
    }
    setSession(existing);
    setTenantId(existing.tenantId);
    void loadData(existing);
  }, [loadData]);

  const selected = orders.find((o) => o.id === selectedId) ?? null;

  const lifecycleStep = useMemo(() => {
    if (!selected) return 0;
    if (selected.status === "finalized") return 2;
    if (selected.status === "sample_received") return 1;
    return 0;
  }, [selected]);

  const workflowSteps = useMemo(
    () => [
      t("laboratory.step.ordered"),
      t("laboratory.step.sample"),
      t("laboratory.step.finalized"),
    ],
    [t],
  );

  const filteredOrders = useMemo(() => {
    const q = filterQ.trim().toLowerCase();
    return orders.filter((o) => {
      if (statusFilter !== "all" && o.status !== statusFilter) return false;
      if (!q) return true;
      return (
        o.order_number.toLowerCase().includes(q) ||
        o.test_code.toLowerCase().includes(q) ||
        o.patient_ref.toLowerCase().includes(q) ||
        (o.result_value ?? "").toLowerCase().includes(q)
      );
    });
  }, [filterQ, orders, statusFilter]);

  const finalized = useMemo(
    () => orders.filter((o) => o.status === "finalized"),
    [orders],
  );

  const stats = useMemo(
    () => ({
      orders: orders.length,
      pending: orders.filter((o) => o.status !== "finalized").length,
      finalized: finalized.length,
      samples: samples.length,
    }),
    [finalized.length, orders, samples.length],
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
      const msg = err instanceof Error ? err.message : t("laboratory.failed");
      setError(msg);
      push({ message: msg });
    } finally {
      setBusy(false);
    }
  }

  async function onLogin() {
    try {
      const next = await loginLaboratorySession(tenantId, email, password);
      saveLaboratorySession(next);
      setSession(next);
      try {
        await seedLaboratoryPersonas(next);
      } catch {
        /* optional */
      }
      push({ message: t("laboratory.connected") });
      await loadData(next);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("laboratory.connectFailed"));
    }
  }

  return (
    <PageLayout
      title={t("laboratory.title")}
      subtitle={t("laboratory.subtitle")}
      breadcrumb={[
        { label: t("laboratory.breadcrumb"), href: "/healthcare/clinic" },
        { label: t("laboratory.laboratory") },
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
        label={loading ? t("laboratory.loading") : t("laboratory.ready")}
      />
      {error ? (
        <p className="mp-lab-alert" role="alert">
          {error}
        </p>
      ) : null}

      {!session ? (
        <section className="mp-stack" aria-label={t("laboratory.session")}>
          <p className="mp-field-help">{t("laboratory.connectHelp")}</p>
          <label>
            {t("laboratory.tenant")}
            <input value={tenantId} onChange={(e) => setTenantId(e.target.value)} />
          </label>
          <label>
            {t("laboratory.email")}
            <input value={email} onChange={(e) => setEmail(e.target.value)} />
          </label>
          <label>
            {t("laboratory.password")}
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <button type="button" className="mp-btn mp-btn-primary" onClick={() => void onLogin()}>
            {t("laboratory.connect")}
          </button>
        </section>
      ) : (
        <div className="mp-desk-shell">
          <aside className="mp-desk-rail" aria-label={t("laboratory.rail")}>
            <section className="mp-desk-rail-card">
              <header className="mp-desk-rail-head">
                <h2>{t("laboratory.workflow")}</h2>
              </header>
              <div className="mp-desk-rail-body">
                <StepProgress steps={workflowSteps} current={lifecycleStep} />
                {draftSaving ? (
                  <p className="mp-field-help" aria-live="polite">
                    {t("laboratory.draftSaved")}…
                  </p>
                ) : (
                  <p className="mp-field-help">{t("laboratory.eventHint")}</p>
                )}
              </div>
            </section>
            <section className="mp-desk-rail-card" aria-label={t("laboratory.metrics")}>
              <header className="mp-desk-rail-head">
                <h2>{t("laboratory.metrics")}</h2>
              </header>
              <div className="mp-desk-rail-body">
                <div className="mp-desk-status-row">
                  <span>{t("laboratory.stat.orders")}</span>
                  <strong>{stats.orders}</strong>
                </div>
                <div className="mp-desk-status-row">
                  <span>{t("laboratory.stat.pending")}</span>
                  <strong>{stats.pending}</strong>
                </div>
                <div className="mp-desk-status-row">
                  <span>{t("laboratory.stat.finalized")}</span>
                  <strong>{stats.finalized}</strong>
                </div>
                <div className="mp-desk-status-row">
                  <span>{t("laboratory.stat.samples")}</span>
                  <strong>{stats.samples}</strong>
                </div>
              </div>
            </section>
          </aside>

          <div className="mp-desk-content">
            <div className="mp-desk-cats" role="tablist" aria-label={t("laboratory.rail")}>
              {(
                [
                  ["overview", "laboratory.tab.overview"],
                  ["orders", "laboratory.tab.orders"],
                  ["samples", "laboratory.tab.samples"],
                  ["results", "laboratory.tab.results"],
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
                <p className="mp-field-help">{t("laboratory.overviewHelp")}</p>
                <h2>{t("laboratory.placeOrder")}</h2>
                <label>
                  {t("laboratory.field.orderNumber")}
                  <input value={orderNumber} onChange={(e) => setOrderNumber(e.target.value)} />
                </label>
                <label>
                  {t("laboratory.field.patientRef")}
                  <input value={patientRef} onChange={(e) => setPatientRef(e.target.value)} />
                </label>
                <p className="mp-field-help">{t("laboratory.patientRefHelp")}</p>
                <label>
                  {t("laboratory.field.testCode")}
                  <input value={testCode} onChange={(e) => setTestCode(e.target.value)} />
                </label>
                <label>
                  {t("laboratory.field.encounterRef")}
                  <input
                    value={encounterRef}
                    onChange={(e) => setEncounterRef(e.target.value)}
                    placeholder={t("laboratory.field.encounterRefHint")}
                  />
                </label>
                <button
                  type="button"
                  className="mp-btn mp-btn-primary"
                  disabled={busy}
                  onClick={() =>
                    void runAction(t("laboratory.orderPlaced"), async () => {
                      const created = await placeLabOrder(session, {
                        order_number: orderNumber,
                        patient_ref: patientRef,
                        test_code: testCode,
                        ...(encounterRef.trim()
                          ? { source_encounter_ref: encounterRef.trim() }
                          : {}),
                      });
                      setSelectedId(created.id);
                      setTab("orders");
                    })
                  }
                >
                  {t("laboratory.placeOrder")}
                </button>
              </section>
            ) : tab === "orders" ? (
              <>
                <AdvancedFilterBar
                  filters={[
                    { id: "q", label: t("laboratory.filter"), type: "text" },
                    { id: "status", label: t("laboratory.field.status"), type: "text" },
                  ]}
                  onChange={(values) => {
                    setFilterQ(values.q ?? "");
                    setStatusFilter((values.status ?? "").toLowerCase().trim() || "all");
                  }}
                />
                {filteredOrders.length === 0 ? (
                  <EmptyState
                    title={t("laboratory.noOrders")}
                    description={t("laboratory.noOrdersHint")}
                  />
                ) : (
                  <DataTable
                    columns={[
                      { key: "order_number", header: t("laboratory.field.orderNumber") },
                      { key: "test_code", header: t("laboratory.field.testCode") },
                      { key: "status", header: t("laboratory.field.status") },
                      { key: "result", header: t("laboratory.field.result") },
                      { key: "action", header: t("laboratory.field.action") },
                    ]}
                    rows={filteredOrders.map((o) => ({
                      id: o.id,
                      order_number: o.order_number,
                      test_code: o.test_code,
                      status: <StatusChip status={o.status} />,
                      result: o.result_value
                        ? `${o.result_value}${o.result_unit ? ` ${o.result_unit}` : ""}`
                        : "—",
                      action:
                        o.status === "ordered" ? (
                          <button
                            type="button"
                            className="mp-btn"
                            disabled={busy}
                            onClick={() => {
                              setSelectedId(o.id);
                              void runAction(t("laboratory.sampleReceived"), async () => {
                                await receiveLabSample(session, {
                                  order_id: o.id,
                                  accession_number: `ACC-${Date.now().toString().slice(-6)}`,
                                  specimen_type: specimenType || "whole_blood",
                                });
                              });
                            }}
                          >
                            {t("laboratory.receiveSample")}
                          </button>
                        ) : o.status === "sample_received" ? (
                          <button
                            type="button"
                            className="mp-btn mp-btn-primary"
                            disabled={busy}
                            onClick={() => setSelectedId(o.id)}
                          >
                            {t("laboratory.finalizeResult")}
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
                  <section className="mp-lab-panel" aria-label={t("laboratory.orderDetail")}>
                    <header>{t("laboratory.orderDetail")}</header>
                    <dl className="mp-lab-dl">
                      <div>
                        <dt>{t("laboratory.field.orderNumber")}</dt>
                        <dd>{selected.order_number}</dd>
                      </div>
                      <div>
                        <dt>{t("laboratory.field.status")}</dt>
                        <dd>
                          <StatusChip status={selected.status} />
                        </dd>
                      </div>
                      <div>
                        <dt>{t("laboratory.field.patientRef")}</dt>
                        <dd>{selected.patient_ref}</dd>
                      </div>
                    </dl>
                    {selected.status === "sample_received" ? (
                      <div className="mp-stack">
                        <label>
                          {t("laboratory.field.resultValue")}
                          <input
                            value={resultValue}
                            onChange={(e) => setResultValue(e.target.value)}
                          />
                        </label>
                        <label>
                          {t("laboratory.field.resultUnit")}
                          <input
                            value={resultUnit}
                            onChange={(e) => setResultUnit(e.target.value)}
                          />
                        </label>
                        <button
                          type="button"
                          className="mp-btn mp-btn-primary"
                          disabled={busy}
                          onClick={() =>
                            void runAction(t("laboratory.resultFinalizedEvent"), async () => {
                              await finalizeLabResult(session, selected.id, {
                                result_value: resultValue,
                                result_unit: resultUnit || undefined,
                              });
                            })
                          }
                        >
                          {t("laboratory.finalizeResult")}
                        </button>
                      </div>
                    ) : selected.status === "ordered" ? (
                      <div className="mp-stack">
                        <label>
                          {t("laboratory.field.specimen")}
                          <input
                            value={specimenType}
                            onChange={(e) => setSpecimenType(e.target.value)}
                          />
                        </label>
                        <p className="mp-field-help">{t("laboratory.selectOrderHint")}</p>
                      </div>
                    ) : null}
                  </section>
                ) : null}
              </>
            ) : tab === "samples" ? (
              samples.length === 0 ? (
                <EmptyState
                  title={t("laboratory.noSamples")}
                  description={t("laboratory.noSamplesHint")}
                />
              ) : (
                <DataTable
                  columns={[
                    { key: "accession", header: t("laboratory.field.accession") },
                    { key: "specimen", header: t("laboratory.field.specimen") },
                    { key: "order_id", header: t("laboratory.field.orderId") },
                    { key: "at", header: t("laboratory.field.receivedAt") },
                  ]}
                  rows={samples.map((s) => ({
                    id: s.id,
                    accession: s.accession_number,
                    specimen: s.specimen_type,
                    order_id: s.order_id,
                    at: s.received_at ?? "—",
                  }))}
                />
              )
            ) : finalized.length === 0 ? (
              <EmptyState
                title={t("laboratory.noResults")}
                description={t("laboratory.noResultsHint")}
              />
            ) : (
              <DataTable
                columns={[
                  { key: "order_number", header: t("laboratory.field.orderNumber") },
                  { key: "test_code", header: t("laboratory.field.testCode") },
                  { key: "result", header: t("laboratory.field.result") },
                ]}
                rows={finalized.map((o) => ({
                  id: o.id,
                  order_number: o.order_number,
                  test_code: o.test_code,
                  result: `${o.result_value ?? ""}${o.result_unit ? ` ${o.result_unit}` : ""}`,
                }))}
              />
            )}
          </div>
        </div>
      )}

      <style jsx>{`
        .mp-lab-alert {
          color: var(--mp-danger, #b45309);
        }
        .mp-lab-chip {
          display: inline-block;
          padding: 0.15rem 0.5rem;
          border-radius: 999px;
          font-size: 0.8rem;
          text-transform: lowercase;
          background: var(--mp-bg-muted);
        }
        .mp-lab-chip--ok {
          background: color-mix(in srgb, #2f9e6b 22%, transparent);
        }
        .mp-lab-chip--warn {
          background: color-mix(in srgb, #c47a2c 24%, transparent);
        }
        .mp-lab-panel {
          margin-block-start: 1rem;
          padding: 0.85rem 1rem;
          border: 1px solid color-mix(in srgb, currentColor 14%, transparent);
          border-radius: var(--mp-radius-sm, 8px);
        }
        .mp-lab-panel header {
          font-weight: 600;
          margin-block-end: 0.65rem;
        }
        .mp-lab-dl {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
          gap: 0.65rem 1rem;
          margin: 0 0 0.75rem;
        }
        .mp-lab-dl dt {
          font-size: 0.75rem;
          opacity: 0.75;
          margin: 0;
        }
        .mp-lab-dl dd {
          margin: 0.15rem 0 0;
          font-weight: 600;
        }
      `}</style>
    </PageLayout>
  );
}
