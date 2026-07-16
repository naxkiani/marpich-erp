"use client";

import { PageLayout } from "@marpich/core";
import { DataTable, EmptyState, ProgressBar, useToast } from "@marpich/shared";
import { useEffect, useState } from "react";
import {
  dispensePrescription,
  fetchPrescriptions,
  loadPharmacySession,
  loginPharmacySession,
  receivePrescription,
  savePharmacySession,
  seedPharmacyPersonas,
  type ApiSession,
  type PharmacyPrescription,
} from "@/lib/pharmacyClient";

export function PharmacyCarePage() {
  const { push } = useToast();
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("pharmacy-demo");
  const [email, setEmail] = useState("pharmacy@demo.dev");
  const [password, setPassword] = useState("SecurePass123!");
  const [rows, setRows] = useState<PharmacyPrescription[]>([]);
  const [rx, setRx] = useState("RX-1001");
  const [patientRef, setPatientRef] = useState("peer-patient-1");
  const [drugCode, setDrugCode] = useState("AMOX500");
  const [drugName, setDrugName] = useState("Amoxicillin 500mg");
  const [qty, setQty] = useState("20");

  useEffect(() => {
    const existing = loadPharmacySession();
    if (existing) {
      setSession(existing);
      setTenantId(existing.tenantId);
      void fetchPrescriptions(existing).then((p) => setRows(p.items ?? []));
    }
  }, []);

  async function onLogin() {
    const next = await loginPharmacySession(tenantId, email, password);
    savePharmacySession(next);
    setSession(next);
    try {
      await seedPharmacyPersonas(next);
    } catch {
      /* optional */
    }
    const page = await fetchPrescriptions(next);
    setRows(page.items ?? []);
    push({ message: `Pharmacy tenant ${next.tenantId}` });
  }

  async function onReceive() {
    if (!session) return;
    await receivePrescription(session, {
      rx_number: rx,
      patient_ref: patientRef,
      drug_code: drugCode,
      drug_name: drugName,
      quantity: Number(qty),
    });
    setRows((await fetchPrescriptions(session)).items ?? []);
    push({ message: "Prescription received" });
  }

  async function onDispense(id: string) {
    if (!session) return;
    await dispensePrescription(session, id);
    setRows((await fetchPrescriptions(session)).items ?? []);
    push({ message: "Dispensed" });
  }

  return (
    <PageLayout
      title="Pharmacy"
      subtitle="CAP-HLT-008 stub — receive prescription → dispense (separate from hospital/clinic/lab)."
      breadcrumb={[{ label: "Healthcare", href: "/healthcare/clinic" }, { label: "Pharmacy" }]}
    >
      <ProgressBar value={session ? 100 : 30} label="Pharmacy" />
      {!session ? (
        <section className="mp-stack">
          <label>
            Tenant
            <input value={tenantId} onChange={(e) => setTenantId(e.target.value)} />
          </label>
          <label>
            Email
            <input value={email} onChange={(e) => setEmail(e.target.value)} />
          </label>
          <label>
            Password
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </label>
          <button type="button" className="mp-btn" onClick={() => void onLogin()}>
            Sign in
          </button>
        </section>
      ) : (
        <>
          <section className="mp-stack">
            <h2>Receive</h2>
            <label>
              Rx
              <input value={rx} onChange={(e) => setRx(e.target.value)} />
            </label>
            <label>
              Patient ref
              <input value={patientRef} onChange={(e) => setPatientRef(e.target.value)} />
            </label>
            <label>
              Drug
              <input value={drugCode} onChange={(e) => setDrugCode(e.target.value)} />
            </label>
            <label>
              Name
              <input value={drugName} onChange={(e) => setDrugName(e.target.value)} />
            </label>
            <label>
              Qty
              <input value={qty} onChange={(e) => setQty(e.target.value)} />
            </label>
            <button type="button" className="mp-btn" onClick={() => void onReceive()}>
              Receive
            </button>
          </section>
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
        </>
      )}
    </PageLayout>
  );
}
