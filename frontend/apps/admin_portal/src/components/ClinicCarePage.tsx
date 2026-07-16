"use client";

import { PageLayout } from "@marpich/core";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast } from "@marpich/shared";
import { useCallback, useEffect, useState } from "react";
import {
  completeClinicEncounter,
  fetchClinicAppointments,
  fetchClinicEncounters,
  fetchClinicPatients,
  loadClinicSession,
  loginClinicSession,
  registerClinicPatient,
  saveClinicSession,
  scheduleClinicAppointment,
  seedClinicPersonas,
  startClinicEncounter,
  type ApiSession,
  type ClinicAppointment,
  type ClinicEncounter,
  type ClinicPatient,
} from "@/lib/clinicClient";

export function ClinicCarePage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("clinic-demo");
  const [email, setEmail] = useState("clinic@demo.dev");
  const [password, setPassword] = useState("SecurePass123!");

  const [patients, setPatients] = useState<ClinicPatient[]>([]);
  const [encounters, setEncounters] = useState<ClinicEncounter[]>([]);
  const [appointments, setAppointments] = useState<ClinicAppointment[]>([]);

  const [patientNumber, setPatientNumber] = useState("CLN-3001");
  const [firstName, setFirstName] = useState("Sara");
  const [lastName, setLastName] = useState("Ahmadi");
  const [dob, setDob] = useState("1988-03-12");
  const [provider, setProvider] = useState("Dr. Karimi");
  const [selectedPatientId, setSelectedPatientId] = useState<string>("");

  const loadData = useCallback(async (active: ApiSession) => {
    setLoading(true);
    setProgress(40);
    setError(null);
    try {
      const [p, e, a] = await Promise.all([
        fetchClinicPatients(active),
        fetchClinicEncounters(active),
        fetchClinicAppointments(active),
      ]);
      setPatients(p.items ?? []);
      setEncounters(e.items ?? []);
      setAppointments(a.items ?? []);
      if (!selectedPatientId && p.items?.[0]?.id) {
        setSelectedPatientId(p.items[0].id);
      }
      setProgress(100);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load clinic data");
      setProgress(100);
    } finally {
      setLoading(false);
    }
  }, [selectedPatientId]);

  useEffect(() => {
    const existing = loadClinicSession();
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
      const next = await loginClinicSession(tenantId, email, password);
      saveClinicSession(next);
      setSession(next);
      try {
        await seedClinicPersonas(next);
      } catch {
        /* seed may require roles.write — admin often already has * */
      }
      push({ message: `Connected to clinic tenant ${next.tenantId}` });
      await loadData(next);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    }
  }

  async function onRegisterPatient() {
    if (!session) return;
    try {
      const created = await registerClinicPatient(session, {
        patient_number: patientNumber,
        first_name: firstName,
        last_name: lastName,
        date_of_birth: dob,
      });
      setSelectedPatientId(created.id);
      push({ message: `Patient registered: ${created.full_name ?? created.patient_number}` });
      await loadData(session);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Register failed" });
    }
  }

  async function onSchedule() {
    if (!session || !selectedPatientId) return;
    try {
      await scheduleClinicAppointment(session, {
        patient_id: selectedPatientId,
        provider_name: provider,
        scheduled_at: new Date().toISOString(),
      });
      push({ message: "Appointment scheduled" });
      await loadData(session);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Schedule failed" });
    }
  }

  async function onWalkInEncounter() {
    if (!session || !selectedPatientId) return;
    try {
      const enc = await startClinicEncounter(session, { patient_id: selectedPatientId });
      await completeClinicEncounter(session, enc.id, ["Z00.0"]);
      push({ message: "Walk-in encounter completed" });
      await loadData(session);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Encounter failed" });
    }
  }

  return (
    <PageLayout
      title="Clinic Care"
      subtitle="CAP-HLT-002/003 outpatient patients, appointments, and encounters — separate from hospital acute care."
      breadcrumb={[
        { label: "Healthcare", href: "/healthcare/clinic" },
        { label: "Clinic" },
      ]}
    >
      <ProgressBar value={progress} label="Loading clinic" />

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
          <section className="mp-stack" aria-label="Register patient">
            <h2>Register patient</h2>
            <label>
              Number
              <input value={patientNumber} onChange={(e) => setPatientNumber(e.target.value)} />
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
              Date of birth
              <input value={dob} onChange={(e) => setDob(e.target.value)} />
            </label>
            <div className="mp-row">
              <button type="button" className="mp-btn" onClick={() => void onRegisterPatient()}>
                Register
              </button>
              <button type="button" className="mp-btn" onClick={() => void onSchedule()}>
                Schedule appointment
              </button>
              <button type="button" className="mp-btn" onClick={() => void onWalkInEncounter()}>
                Walk-in encounter
              </button>
            </div>
            <label>
              Selected patient
              <select
                value={selectedPatientId}
                onChange={(e) => setSelectedPatientId(e.target.value)}
              >
                <option value="">—</option>
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.patient_number} — {p.full_name ?? `${p.first_name} ${p.last_name}`}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Provider
              <input value={provider} onChange={(e) => setProvider(e.target.value)} />
            </label>
          </section>

          {patients.length === 0 ? (
            <EmptyState
              title="No patients yet"
              description="Register an outpatient to start CAP-HLT-002 care lifecycle."
            />
          ) : (
            <DataTable
              columns={[
                { key: "patient_number", header: "Number" },
                { key: "full_name", header: "Name" },
                { key: "date_of_birth", header: "DOB" },
              ]}
              rows={patients.map((p) => ({
                id: p.id,
                patient_number: p.patient_number,
                full_name: p.full_name ?? `${p.first_name} ${p.last_name}`,
                date_of_birth: p.date_of_birth,
              }))}
            />
          )}

          <h2>Encounters</h2>
          {encounters.length === 0 ? (
            <EmptyState title="No encounters" description="Start a walk-in or appointment visit." />
          ) : (
            <DataTable
              columns={[
                { key: "id", header: "Encounter" },
                { key: "patient_id", header: "Patient" },
                { key: "status", header: "Status" },
                { key: "codes", header: "Dx" },
              ]}
              rows={encounters.map((e) => ({
                id: e.id.slice(0, 8),
                patient_id: e.patient_id.slice(0, 8),
                status: e.status,
                codes: (e.diagnosis_codes ?? []).join(", ") || "—",
              }))}
            />
          )}

          <h2>Appointments</h2>
          {appointments.length === 0 ? (
            <EmptyState title="No appointments" description="Schedule from a registered patient." />
          ) : (
            <DataTable
              columns={[
                { key: "provider_name", header: "Provider" },
                { key: "scheduled_at", header: "When" },
                { key: "status", header: "Status" },
              ]}
              rows={appointments.map((a) => ({
                id: a.id,
                provider_name: a.provider_name,
                scheduled_at: a.scheduled_at,
                status: a.status,
              }))}
            />
          )}
        </>
      ) : null}
    </PageLayout>
  );
}
