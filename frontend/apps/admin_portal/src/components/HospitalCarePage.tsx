"use client";

import { PageLayout } from "@marpich/core";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast } from "@marpich/shared";
import { useCallback, useEffect, useState } from "react";
import {
  admitHospitalPatient,
  completeHospitalEncounter,
  fetchHospitalAdmissions,
  fetchHospitalEncounters,
  fetchHospitalPatients,
  loadHospitalSession,
  loginHospitalSession,
  registerHospitalPatient,
  saveHospitalSession,
  seedHospitalPersonas,
  startHospitalEncounter,
  type ApiSession,
  type HospitalAdmission,
  type HospitalEncounter,
  type HospitalPatient,
} from "@/lib/hospitalClient";

export function HospitalCarePage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("hospital-demo");
  const [email, setEmail] = useState("hospital@demo.dev");
  const [password, setPassword] = useState("SecurePass123!");

  const [patients, setPatients] = useState<HospitalPatient[]>([]);
  const [admissions, setAdmissions] = useState<HospitalAdmission[]>([]);
  const [encounters, setEncounters] = useState<HospitalEncounter[]>([]);

  const [mrn, setMrn] = useState("MRN-1001");
  const [firstName, setFirstName] = useState("Ali");
  const [lastName, setLastName] = useState("Rezaei");
  const [dob, setDob] = useState("1975-01-20");
  const [ward, setWard] = useState("ICU-1");
  const [selectedPatientId, setSelectedPatientId] = useState("");
  const [selectedAdmissionId, setSelectedAdmissionId] = useState("");

  const loadData = useCallback(async (active: ApiSession) => {
    setLoading(true);
    setProgress(40);
    setError(null);
    try {
      const [p, a, e] = await Promise.all([
        fetchHospitalPatients(active),
        fetchHospitalAdmissions(active),
        fetchHospitalEncounters(active),
      ]);
      setPatients(p.items ?? []);
      setAdmissions(a.items ?? []);
      setEncounters(e.items ?? []);
      if (!selectedPatientId && p.items?.[0]?.id) setSelectedPatientId(p.items[0].id);
      if (!selectedAdmissionId && a.items?.[0]?.id) setSelectedAdmissionId(a.items[0].id);
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load hospital data");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [selectedAdmissionId, selectedPatientId]);

  useEffect(() => {
    const existing = loadHospitalSession();
    if (!existing) {
      setLoading(false);
      return;
    }
    setSession(existing);
    setTenantId(existing.tenantId);
    void loadData(existing);
  }, [loadData]);

  async function onLogin() {
    try {
      const next = await loginHospitalSession(tenantId, email, password);
      saveHospitalSession(next);
      setSession(next);
      try {
        await seedHospitalPersonas(next);
      } catch {
        /* optional */
      }
      push({ message: `Connected to hospital tenant ${next.tenantId}` });
      await loadData(next);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    }
  }

  async function onRegister() {
    if (!session) return;
    try {
      const created = await registerHospitalPatient(session, {
        mrn,
        first_name: firstName,
        last_name: lastName,
        date_of_birth: dob,
      });
      setSelectedPatientId(created.id);
      push({ message: `Patient registered: ${created.mrn}` });
      await loadData(session);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Register failed" });
    }
  }

  async function onAdmit() {
    if (!session || !selectedPatientId) return;
    try {
      const adm = await admitHospitalPatient(session, {
        patient_id: selectedPatientId,
        ward,
      });
      setSelectedAdmissionId(adm.id);
      push({ message: `Admitted to ${ward}` });
      await loadData(session);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Admit failed" });
    }
  }

  async function onEncounter() {
    if (!session || !selectedAdmissionId) return;
    try {
      const enc = await startHospitalEncounter(session, {
        admission_id: selectedAdmissionId,
      });
      await completeHospitalEncounter(session, enc.id, {
        procedure_codes: ["99223"],
        diagnosis_codes: ["J18.9"],
      });
      push({ message: "Encounter completed" });
      await loadData(session);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Encounter failed" });
    }
  }

  return (
    <PageLayout
      title="Hospital Care"
      subtitle="CAP-HLT-001 acute lifecycle — register, admit, encounter (separate from clinic ambulatory)."
      breadcrumb={[
        { label: "Healthcare", href: "/healthcare/clinic" },
        { label: "Hospital" },
      ]}
    >
      <ProgressBar value={progress} label="Loading hospital" />

      {!session ? (
        <section className="mp-stack" aria-label="Sign in">
          <h2>Session</h2>
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
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <button type="button" className="mp-btn" onClick={() => void onLogin()}>
            Sign in
          </button>
        </section>
      ) : null}

      {error ? <p role="alert">{error}</p> : null}

      {loading ? (
        <SkeletonTable rows={4} />
      ) : session ? (
        <>
          <section className="mp-stack" aria-label="Acute care actions">
            <h2>Register → Admit → Encounter</h2>
            <label>
              MRN
              <input value={mrn} onChange={(e) => setMrn(e.target.value)} />
            </label>
            <label>
              First name
              <input value={firstName} onChange={(e) => setFirstName(e.target.value)} />
            </label>
            <label>
              Last name
              <input value={lastName} onChange={(e) => setLastName(e.target.value)} />
            </label>
            <label>
              DOB
              <input value={dob} onChange={(e) => setDob(e.target.value)} />
            </label>
            <label>
              Ward
              <input value={ward} onChange={(e) => setWard(e.target.value)} />
            </label>
            <div className="mp-row">
              <button type="button" className="mp-btn" onClick={() => void onRegister()}>
                Register
              </button>
              <button type="button" className="mp-btn" onClick={() => void onAdmit()}>
                Admit
              </button>
              <button type="button" className="mp-btn" onClick={() => void onEncounter()}>
                Start + complete encounter
              </button>
            </div>
            <label>
              Patient
              <select
                value={selectedPatientId}
                onChange={(e) => setSelectedPatientId(e.target.value)}
              >
                <option value="">—</option>
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.mrn} — {p.full_name ?? `${p.first_name} ${p.last_name}`}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Admission
              <select
                value={selectedAdmissionId}
                onChange={(e) => setSelectedAdmissionId(e.target.value)}
              >
                <option value="">—</option>
                {admissions.map((a) => (
                  <option key={a.id} value={a.id}>
                    {a.ward} ({a.status})
                  </option>
                ))}
              </select>
            </label>
          </section>

          {patients.length === 0 ? (
            <EmptyState
              title="No hospital patients"
              description="Register with MRN to start CAP-HLT-001 acute lifecycle."
            />
          ) : (
            <DataTable
              columns={[
                { key: "mrn", header: "MRN" },
                { key: "full_name", header: "Name" },
                { key: "date_of_birth", header: "DOB" },
              ]}
              rows={patients.map((p) => ({
                id: p.id,
                mrn: p.mrn,
                full_name: p.full_name ?? `${p.first_name} ${p.last_name}`,
                date_of_birth: p.date_of_birth,
              }))}
            />
          )}

          <h2>Admissions</h2>
          {admissions.length === 0 ? (
            <EmptyState title="No admissions" description="Admit a registered patient to a ward." />
          ) : (
            <DataTable
              columns={[
                { key: "ward", header: "Ward" },
                { key: "status", header: "Status" },
                { key: "patient_id", header: "Patient" },
              ]}
              rows={admissions.map((a) => ({
                id: a.id,
                ward: a.ward,
                status: a.status,
                patient_id: a.patient_id.slice(0, 8),
              }))}
            />
          )}

          <h2>Encounters</h2>
          {encounters.length === 0 ? (
            <EmptyState
              title="No encounters"
              description="Start an encounter from an active admission (not walk-in)."
            />
          ) : (
            <DataTable
              columns={[
                { key: "id", header: "Encounter" },
                { key: "status", header: "Status" },
                { key: "codes", header: "Dx / Proc" },
              ]}
              rows={encounters.map((e) => ({
                id: e.id.slice(0, 8),
                status: e.status,
                codes: [
                  ...(e.diagnosis_codes ?? []),
                  ...(e.procedure_codes ?? []),
                ].join(", ") || "—",
              }))}
            />
          )}
        </>
      ) : null}
    </PageLayout>
  );
}
