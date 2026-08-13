"use client";

import Link from "next/link";
import { PageLayout } from "@marpich/core";
import { useAuth } from "@marpich/auth-provider";
import {
  DataTable,
  DeskAlert,
  DeskChrome,
  DeskFormRow,
  DeskPanel,
  DeskToolbar,
  EmptyState,
  ProgressBar,
  SkeletonTable,
  useLocale,
  useToast,
} from "@marpich/shared";
import { useCallback, useEffect, useState } from "react";
import {
  fetchLabOrders,
  finalizeLabResult,
  placeLabOrder,
  receiveLabSample,
  seedLaboratoryPersonas,
  type LabOrder,
} from "@/lib/laboratoryClient";

export function LaboratoryCarePage() {
  const { push } = useToast();
  const { t } = useLocale();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [rows, setRows] = useState<LabOrder[]>([]);
  const [orderNumber, setOrderNumber] = useState("LAB-2001");
  const [patientRef, setPatientRef] = useState("peer-patient-1");
  const [testCode, setTestCode] = useState("CBC");
  const [selectedId, setSelectedId] = useState("");

  const refresh = useCallback(async () => {
    if (!session) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      try {
        await seedLaboratoryPersonas(session);
      } catch {
        /* optional */
      }
      const page = await fetchLabOrders(session);
      setRows(page.items ?? []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load laboratory");
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    if (!authLoading) void refresh();
  }, [authLoading, refresh]);

  async function onOrder() {
    if (!session) return;
    try {
      const order = await placeLabOrder(session, {
        order_number: orderNumber,
        patient_ref: patientRef,
        test_code: testCode,
      });
      setSelectedId(order.id);
      await refresh();
      push({ message: "Order placed" });
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Order failed" });
    }
  }

  async function onSample() {
    if (!session || !selectedId) return;
    try {
      await receiveLabSample(session, {
        order_id: selectedId,
        accession_number: `ACC-${Date.now().toString().slice(-6)}`,
        specimen_type: "whole_blood",
      });
      await refresh();
      push({ message: "Sample received" });
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Sample failed" });
    }
  }

  async function onResult() {
    if (!session || !selectedId) return;
    try {
      await finalizeLabResult(session, selectedId, {
        result_value: "5.2",
        result_unit: "10^9/L",
      });
      await refresh();
      push({ message: "Result available" });
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Result failed" });
    }
  }

  return (
    <PageLayout
      title={t("laboratory.title")}
      subtitle={t("laboratory.subtitle")}
      breadcrumb={[
        { label: t("nav.group.healthcare"), href: "/healthcare/hospital" },
        { label: t("laboratory.title") },
      ]}
      actions={
        <button type="button" className="mp-btn" onClick={() => void refresh()} disabled={loading || !session}>
          {t("desk.refresh")}
        </button>
      }
    >
      <DeskChrome>
        <ProgressBar value={session ? 100 : 30} label={t("laboratory.title")} />
        {authLoading || loading ? <SkeletonTable rows={3} /> : null}
        {!authLoading && (!isAuthenticated || !session) ? (
          <EmptyState
            title={t("desk.signInRequired")}
            description={t("desk.signInRequired")}
            action={
              <Link className="mp-btn mp-btn-primary" href="/login?returnTo=/healthcare/laboratory">
                {t("dashboard.signIn")}
              </Link>
            }
          />
        ) : null}
        {error ? <DeskAlert>{error}</DeskAlert> : null}
        {session ? (
          <>
            <DeskPanel title="Order → Sample → Result">
              <DeskFormRow>
                <div className="mp-field">
                  <label htmlFor="lab-order">Order #</label>
                  <input
                    id="lab-order"
                    className="mp-input"
                    value={orderNumber}
                    onChange={(e) => setOrderNumber(e.target.value)}
                  />
                </div>
                <div className="mp-field">
                  <label htmlFor="lab-patient">Patient ref</label>
                  <input
                    id="lab-patient"
                    className="mp-input"
                    value={patientRef}
                    onChange={(e) => setPatientRef(e.target.value)}
                  />
                </div>
                <div className="mp-field">
                  <label htmlFor="lab-test">Test</label>
                  <input
                    id="lab-test"
                    className="mp-input"
                    value={testCode}
                    onChange={(e) => setTestCode(e.target.value)}
                  />
                </div>
                <div className="mp-field">
                  <label htmlFor="lab-selected">Selected order</label>
                  <select
                    id="lab-selected"
                    className="mp-select"
                    value={selectedId}
                    onChange={(e) => setSelectedId(e.target.value)}
                  >
                    <option value="">—</option>
                    {rows.map((r) => (
                      <option key={r.id} value={r.id}>
                        {r.order_number} ({r.status})
                      </option>
                    ))}
                  </select>
                </div>
                <DeskToolbar>
                  <button type="button" className="mp-btn mp-btn-primary" onClick={() => void onOrder()}>
                    Place order
                  </button>
                  <button type="button" className="mp-btn" onClick={() => void onSample()}>
                    Receive sample
                  </button>
                  <button type="button" className="mp-btn" onClick={() => void onResult()}>
                    Finalize result
                  </button>
                </DeskToolbar>
              </DeskFormRow>
            </DeskPanel>
            <DeskPanel title="Orders">
              {rows.length === 0 ? (
                <EmptyState title="No lab orders" description="Place an order with a peer patient_ref." />
              ) : (
                <DataTable
                  columns={[
                    { key: "order_number", header: "Order" },
                    { key: "test_code", header: "Test" },
                    { key: "status", header: "Status" },
                    { key: "result_value", header: "Result" },
                  ]}
                  rows={rows.map((r) => ({
                    id: r.id,
                    order_number: r.order_number,
                    test_code: r.test_code,
                    status: r.status,
                    result_value: r.result_value ?? "—",
                  }))}
                />
              )}
            </DeskPanel>
          </>
        ) : null}
      </DeskChrome>
    </PageLayout>
  );
}
