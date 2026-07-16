"use client";

import { PageLayout } from "@marpich/core";
import { DataTable, EmptyState, ProgressBar, useToast } from "@marpich/shared";
import { useEffect, useState } from "react";
import {
  fetchLabOrders,
  finalizeLabResult,
  loadLaboratorySession,
  loginLaboratorySession,
  placeLabOrder,
  receiveLabSample,
  saveLaboratorySession,
  seedLaboratoryPersonas,
  type ApiSession,
  type LabOrder,
} from "@/lib/laboratoryClient";

export function LaboratoryCarePage() {
  const { push } = useToast();
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("laboratory-demo");
  const [email, setEmail] = useState("lab@demo.dev");
  const [password, setPassword] = useState("SecurePass123!");
  const [rows, setRows] = useState<LabOrder[]>([]);
  const [orderNumber, setOrderNumber] = useState("LAB-2001");
  const [patientRef, setPatientRef] = useState("peer-patient-1");
  const [testCode, setTestCode] = useState("CBC");
  const [selectedId, setSelectedId] = useState("");

  useEffect(() => {
    const existing = loadLaboratorySession();
    if (existing) {
      setSession(existing);
      setTenantId(existing.tenantId);
      void fetchLabOrders(existing).then((p) => setRows(p.items ?? []));
    }
  }, []);

  async function refresh(active: ApiSession) {
    const page = await fetchLabOrders(active);
    setRows(page.items ?? []);
  }

  async function onLogin() {
    const next = await loginLaboratorySession(tenantId, email, password);
    saveLaboratorySession(next);
    setSession(next);
    try {
      await seedLaboratoryPersonas(next);
    } catch {
      /* optional */
    }
    await refresh(next);
    push({ message: `Laboratory tenant ${next.tenantId}` });
  }

  async function onOrder() {
    if (!session) return;
    const order = await placeLabOrder(session, {
      order_number: orderNumber,
      patient_ref: patientRef,
      test_code: testCode,
    });
    setSelectedId(order.id);
    await refresh(session);
    push({ message: "Order placed" });
  }

  async function onSample() {
    if (!session || !selectedId) return;
    await receiveLabSample(session, {
      order_id: selectedId,
      accession_number: `ACC-${Date.now().toString().slice(-6)}`,
      specimen_type: "whole_blood",
    });
    await refresh(session);
    push({ message: "Sample received" });
  }

  async function onResult() {
    if (!session || !selectedId) return;
    await finalizeLabResult(session, selectedId, {
      result_value: "5.2",
      result_unit: "10^9/L",
    });
    await refresh(session);
    push({ message: "Result available" });
  }

  return (
    <PageLayout
      title="Laboratory"
      subtitle="CAP-HLT-007 stub — order → sample → result (separate from hospital/clinic/pharmacy)."
      breadcrumb={[{ label: "Healthcare", href: "/healthcare/clinic" }, { label: "Laboratory" }]}
    >
      <ProgressBar value={session ? 100 : 30} label="Laboratory" />
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
            <h2>Order → Sample → Result</h2>
            <label>
              Order #
              <input value={orderNumber} onChange={(e) => setOrderNumber(e.target.value)} />
            </label>
            <label>
              Patient ref
              <input value={patientRef} onChange={(e) => setPatientRef(e.target.value)} />
            </label>
            <label>
              Test
              <input value={testCode} onChange={(e) => setTestCode(e.target.value)} />
            </label>
            <div className="mp-row">
              <button type="button" className="mp-btn" onClick={() => void onOrder()}>
                Place order
              </button>
              <button type="button" className="mp-btn" onClick={() => void onSample()}>
                Receive sample
              </button>
              <button type="button" className="mp-btn" onClick={() => void onResult()}>
                Finalize result
              </button>
            </div>
            <label>
              Selected order
              <select value={selectedId} onChange={(e) => setSelectedId(e.target.value)}>
                <option value="">—</option>
                {rows.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.order_number} ({r.status})
                  </option>
                ))}
              </select>
            </label>
          </section>
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
        </>
      )}
    </PageLayout>
  );
}
