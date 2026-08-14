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
  dispensePrescription,
  fetchPrescriptions,
  receivePrescription,
  seedPharmacyPersonas,
  type PharmacyPrescription,
} from "@/lib/pharmacyClient";

export function PharmacyCarePage() {
  const { push } = useToast();
  const { t } = useLocale();
  const { session, isAuthenticated, isLoading: authLoading } = useAuth();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [rows, setRows] = useState<PharmacyPrescription[]>([]);
  const [rx, setRx] = useState("RX-1001");
  const [patientRef, setPatientRef] = useState("peer-patient-1");
  const [drugCode, setDrugCode] = useState("AMOX500");
  const [drugName, setDrugName] = useState("Amoxicillin 500mg");
  const [qty, setQty] = useState("20");

  const load = useCallback(async () => {
    if (!session) {
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      try {
        await seedPharmacyPersonas(session);
      } catch {
        /* optional */
      }
      setRows((await fetchPrescriptions(session)).items ?? []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load pharmacy");
    } finally {
      setLoading(false);
    }
  }, [session]);

  useEffect(() => {
    if (!authLoading) void load();
  }, [authLoading, load]);

  async function onReceive() {
    if (!session) return;
    try {
      await receivePrescription(session, {
        rx_number: rx,
        patient_ref: patientRef,
        drug_code: drugCode,
        drug_name: drugName,
        quantity: Number(qty),
      });
      setRows((await fetchPrescriptions(session)).items ?? []);
      push({ message: "Prescription received" });
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Receive failed" });
    }
  }

  async function onDispense(id: string) {
    if (!session) return;
    try {
      await dispensePrescription(session, id);
      setRows((await fetchPrescriptions(session)).items ?? []);
      push({ message: "Dispensed" });
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Dispense failed" });
    }
  }

  return (
    <PageLayout
      title={t("pharmacy.title")}
      subtitle={t("pharmacy.subtitle")}
      breadcrumb={[
        { label: t("nav.group.healthcare"), href: "/healthcare/hospital" },
        { label: t("pharmacy.title") },
      ]}
      actions={
        <button type="button" className="mp-btn" onClick={() => void load()} disabled={loading || !session}>
          {t("desk.refresh")}
        </button>
      }
    >
      <DeskChrome>
        <ProgressBar value={session ? 100 : 30} label={t("pharmacy.title")} />
        {authLoading || loading ? <SkeletonTable rows={3} /> : null}
        {!authLoading && (!isAuthenticated || !session) ? (
          <EmptyState
            title={t("desk.signInRequired")}
            description={t("desk.signInRequired")}
            action={
              <Link className="mp-btn mp-btn-primary" href="/login?returnTo=/healthcare/pharmacy">
                {t("dashboard.signIn")}
              </Link>
            }
          />
        ) : null}
        {error ? <DeskAlert>{error}</DeskAlert> : null}
        {session ? (
          <>
            <DeskPanel title="Receive">
              <DeskFormRow>
                <div className="mp-field">
                  <label htmlFor="rx">Rx</label>
                  <input id="rx" className="mp-input" value={rx} onChange={(e) => setRx(e.target.value)} />
                </div>
                <div className="mp-field">
                  <label htmlFor="patient">Patient ref</label>
                  <input
                    id="patient"
                    className="mp-input"
                    value={patientRef}
                    onChange={(e) => setPatientRef(e.target.value)}
                  />
                </div>
                <div className="mp-field">
                  <label htmlFor="drug">Drug</label>
                  <input id="drug" className="mp-input" value={drugCode} onChange={(e) => setDrugCode(e.target.value)} />
                </div>
                <div className="mp-field">
                  <label htmlFor="drugName">Name</label>
                  <input
                    id="drugName"
                    className="mp-input"
                    value={drugName}
                    onChange={(e) => setDrugName(e.target.value)}
                  />
                </div>
                <div className="mp-field">
                  <label htmlFor="qty">Qty</label>
                  <input id="qty" className="mp-input" value={qty} onChange={(e) => setQty(e.target.value)} />
                </div>
                <DeskToolbar>
                  <button type="button" className="mp-btn mp-btn-primary" onClick={() => void onReceive()}>
                    Receive
                  </button>
                </DeskToolbar>
              </DeskFormRow>
            </DeskPanel>
            <DeskPanel title="Prescriptions">
              {rows.length === 0 ? (
                <EmptyState title="No prescriptions" description="Receive an Rx with a peer patient_ref." />
              ) : (
                <DataTable
                  columns={[
                    { key: "rx_number", header: "Rx" },
                    { key: "drug_code", header: "Drug" },
                    { key: "status", header: "Status" },
                    { key: "action", header: "Action" },
                  ]}
                  rows={rows.map((r) => ({
                    id: r.id,
                    rx_number: r.rx_number,
                    drug_code: r.drug_code,
                    status: r.status,
                    action:
                      r.status === "received" ? (
                        <button type="button" className="mp-btn" onClick={() => void onDispense(r.id)}>
                          Dispense
                        </button>
                      ) : (
                        "—"
                      ),
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
