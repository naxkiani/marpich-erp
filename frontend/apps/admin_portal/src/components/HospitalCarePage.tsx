"use client";

import { useAuth } from "@marpich/auth-provider";
import { PageLayout } from "@marpich/core";
import {
  AdvancedFilterBar,
  DataTable,
  EmptyState,
  ExportButton,
  ProgressBar,
  PrintButton,
  SkeletonTable,
  StepProgress,
  useAutosave,
  useLocale,
  useToast,
} from "@marpich/shared";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  admitHospitalPatient,
  assignHospitalBed,
  clearHospitalSession,
  completeHospitalEncounter,
  createHospitalBed,
  dischargeHospitalAdmission,
  fetchBillings,
  fetchHospitalAdmissions,
  fetchHospitalBeds,
  fetchHospitalCareEvents,
  fetchHospitalDashboard,
  fetchHospitalEncounters,
  fetchHospitalPatients,
  isAuthFailure,
  loadHospitalSession,
  loginHospitalSession,
  registerHospitalPatient,
  saveHospitalSession,
  seedHospitalDemo,
  seedHospitalPersonas,
  startHospitalEncounter,
  transferHospitalAdmission,
  waitForBillingByEncounter,
  type ApiSession,
  type EncounterBilling,
  type HospitalAdmission,
  type HospitalBed,
  type HospitalCareEvent,
  type HospitalDashboard,
  type HospitalEncounter,
  type HospitalPatient,
} from "@/lib/hospitalClient";
import {
  seedPeerCareEvents,
  targetsForCareEventSeed,
  targetsFromPatientsAndEncounters,
} from "@/lib/careEventSeed";

type TabId = "board" | "patients" | "beds" | "admissions" | "encounters";

const DRAFT_KEY = "marpich.hospital.care.draft";

function shortId(id: string): string {
  return id.length > 8 ? `${id.slice(0, 8)}…` : id;
}

function StatusChip({ status }: { status: string }) {
  const tone =
    status === "available" || status === "active"
      ? "ok"
      : status === "occupied"
        ? "warn"
        : status === "discharged" || status === "completed"
          ? "muted"
          : "neutral";
  return (
    <span className={`mp-hosp-chip mp-hosp-chip--${tone}`} data-status={status}>
      {status}
    </span>
  );
}

export function HospitalCarePage() {
  const { t } = useLocale();
  const { push } = useToast();
  const {
    session: authSession,
    isAuthenticated,
    isLoading: authLoading,
    login,
    logout,
  } = useAuth();

  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [needsReconnect, setNeedsReconnect] = useState(false);
  const [localSession, setLocalSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("hospital-demo");
  const [email, setEmail] = useState("hospital@demo.dev");
  const [password, setPassword] = useState("SecurePass123!");

  const [dashboard, setDashboard] = useState<HospitalDashboard | null>(null);
  const [patients, setPatients] = useState<HospitalPatient[]>([]);
  const [admissions, setAdmissions] = useState<HospitalAdmission[]>([]);
  const [encounters, setEncounters] = useState<HospitalEncounter[]>([]);
  const [beds, setBeds] = useState<HospitalBed[]>([]);
  const [billingsByEncounter, setBillingsByEncounter] = useState<
    Record<string, EncounterBilling>
  >({});
  const [careEvents, setCareEvents] = useState<HospitalCareEvent[]>([]);
  const [selectedEncounterId, setSelectedEncounterId] = useState("");

  const session = needsReconnect ? null : localSession ?? (isAuthenticated ? authSession : null);
  const loadGen = useRef(0);

  const resetAuthState = useCallback(async () => {
    // Block retries from authSession before clearing storage / calling logout.
    setNeedsReconnect(true);
    clearHospitalSession();
    setLocalSession(null);
    setDashboard(null);
    setPatients([]);
    setAdmissions([]);
    setEncounters([]);
    setBeds([]);
    setBillingsByEncounter({});
    setCareEvents([]);
    setSelectedEncounterId("");
    try {
      await logout();
    } catch {
      /* session may already be invalid */
    }
  }, [logout]);

  const [mrn, setMrn] = useState("MRN-1001");
  const [firstName, setFirstName] = useState("Ali");
  const [lastName, setLastName] = useState("Rezaei");
  const [dob, setDob] = useState("1975-01-20");
  const [ward, setWard] = useState("ICU-1");
  const [room, setRoom] = useState("101");
  const [bedCode, setBedCode] = useState("A");
  const [selectedPatientId, setSelectedPatientId] = useState("");
  const [selectedAdmissionId, setSelectedAdmissionId] = useState("");
  const [selectedBedId, setSelectedBedId] = useState("");
  const [tab, setTab] = useState<TabId>("board");
  const [filterWard, setFilterWard] = useState("");
  const [filterStatus, setFilterStatus] = useState("");
  const [confirmDischarge, setConfirmDischarge] = useState(false);
  const [draftReady, setDraftReady] = useState(false);

  const draft = useMemo(
    () => ({ mrn, firstName, lastName, dob, ward, room, bedCode }),
    [mrn, firstName, lastName, dob, ward, room, bedCode],
  );

  const persistDraft = useCallback(async (values: typeof draft) => {
    if (!draftReady) return;
    try {
      localStorage.setItem(DRAFT_KEY, JSON.stringify(values));
    } catch {
      /* ignore quota */
    }
  }, [draftReady]);

  const { saving: draftSaving } = useAutosave(draft, persistDraft, 900);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(DRAFT_KEY);
      if (raw) {
        const parsed = JSON.parse(raw) as Partial<typeof draft>;
        if (parsed.mrn) setMrn(parsed.mrn);
        if (parsed.firstName) setFirstName(parsed.firstName);
        if (parsed.lastName) setLastName(parsed.lastName);
        if (parsed.dob) setDob(parsed.dob);
        if (parsed.ward) setWard(parsed.ward);
        if (parsed.room) setRoom(parsed.room);
        if (parsed.bedCode) setBedCode(parsed.bedCode);
      }
    } catch {
      /* ignore */
    } finally {
      setDraftReady(true);
    }
  }, []);

  const loadData = useCallback(
    async (active: ApiSession) => {
      const gen = ++loadGen.current;
      setLoading(true);
      setProgress(40);
      setError(null);
      try {
        // Probe auth with a single call first so a dead JWT does not fan out 5 errors.
        const dash = await fetchHospitalDashboard(active);
        if (gen !== loadGen.current) return;
        const [p, a, e, b] = await Promise.all([
          fetchHospitalPatients(active),
          fetchHospitalAdmissions(active),
          fetchHospitalEncounters(active),
          fetchHospitalBeds(active),
        ]);
        if (gen !== loadGen.current) return;
        const patientItems = p.items ?? [];
        const admissionItems = a.items ?? [];
        const bedItems = b.items ?? [];
        setDashboard(dash);
        setPatients(patientItems);
        setAdmissions(admissionItems);
        setEncounters(e.items ?? []);
        setBeds(bedItems);
        try {
          const billings = await fetchBillings(active);
          if (gen !== loadGen.current) return;
          const map: Record<string, EncounterBilling> = {};
          for (const b of billings) {
            if (b.external_encounter_id) map[b.external_encounter_id] = b;
          }
          setBillingsByEncounter(map);
        } catch {
          /* billing permission optional — clinical UI still works */
          if (gen === loadGen.current) setBillingsByEncounter({});
        }
        try {
          const events = await fetchHospitalCareEvents(active, { limit: 50 });
          if (gen === loadGen.current) setCareEvents(events);
        } catch {
          if (gen === loadGen.current) setCareEvents([]);
        }
        setSelectedPatientId((prev) => prev || patientItems[0]?.id || "");
        setSelectedAdmissionId((prev) => {
          if (prev && admissionItems.some((x) => x.id === prev)) return prev;
          const activeAdm = admissionItems.find((x) => x.status === "active");
          return activeAdm?.id || admissionItems[0]?.id || "";
        });
        setSelectedBedId((prev) => {
          if (prev && bedItems.some((x) => x.id === prev)) return prev;
          const free = bedItems.find((x) => x.status === "available");
          return free?.id || bedItems[0]?.id || "";
        });
        setSelectedEncounterId((prev) => {
          const encItems = e.items ?? [];
          if (prev && encItems.some((x) => x.id === prev)) return prev;
          return encItems[0]?.id || "";
        });
        setNeedsReconnect(false);
        setProgress(100);
      } catch (err) {
        if (gen !== loadGen.current) return;
        const message = err instanceof Error ? err.message : t("hospital.loadFailed");
        setProgress(100);
        if (isAuthFailure(message)) {
          await resetAuthState();
          setError(t("hospital.sessionExpired"));
        } else {
          setError(message);
        }
      } finally {
        if (gen === loadGen.current) setLoading(false);
      }
    },
    [resetAuthState, t],
  );

  useEffect(() => {
    if (authLoading) return;
    if (needsReconnect) {
      setLoading(false);
      setProgress(100);
      return;
    }
    const stored = loadHospitalSession();
    if (stored) {
      setLocalSession(stored);
      setTenantId(stored.tenantId);
      void loadData(stored);
      return;
    }
    if (authSession && isAuthenticated) {
      void loadData(authSession);
      return;
    }
    setLoading(false);
    setProgress(100);
  }, [authLoading, authSession, isAuthenticated, loadData, needsReconnect]);

  const selectedAdmission = useMemo(
    () => admissions.find((a) => a.id === selectedAdmissionId) ?? null,
    [admissions, selectedAdmissionId],
  );

  const availableBeds = useMemo(
    () => beds.filter((b) => b.status === "available"),
    [beds],
  );

  const occupancy = useMemo(() => {
    const summary = dashboard?.summary;
    const available =
      summary?.available_beds ?? beds.filter((b) => b.status === "available").length;
    const occupied =
      summary?.occupied_beds ?? beds.filter((b) => b.status === "occupied").length;
    const total = summary?.bed_count ?? beds.length;
    const active =
      summary?.active_admissions ?? admissions.filter((a) => a.status === "active").length;
    const patientsCount = summary?.patient_count ?? patients.length;
    const encountersCount = summary?.encounter_count ?? encounters.length;
    const openEncounters =
      summary?.open_encounters ??
      encounters.filter((e) => e.status === "in_progress" || e.status === "open").length;
    return {
      available,
      occupied,
      total,
      active,
      patients: patientsCount,
      encounters: encountersCount,
      openEncounters,
    };
  }, [admissions, beds, dashboard, encounters, patients.length]);

  const lifecycleStep = useMemo(() => {
    if (!patients.length) return 0;
    if (!beds.length) return 1;
    if (!selectedAdmission) return 2;
    if (selectedAdmission.status === "discharged") return 4;
    if (selectedAdmission.bed_id) return 3;
    return 2;
  }, [patients.length, beds.length, selectedAdmission]);

  const patientNameById = useMemo(() => {
    const map = new Map<string, string>();
    for (const p of patients) {
      map.set(p.id, p.full_name ?? `${p.first_name} ${p.last_name}`);
    }
    return map;
  }, [patients]);

  const bedLabelById = useMemo(() => {
    const map = new Map<string, string>();
    for (const b of beds) {
      map.set(b.id, `${b.ward}/${b.room}/${b.bed_code}`);
    }
    return map;
  }, [beds]);

  const bedsByWard = useMemo(() => {
    const groups = new Map<string, HospitalBed[]>();
    for (const bed of beds) {
      if (filterWard && !bed.ward.toLowerCase().includes(filterWard.toLowerCase())) continue;
      if (filterStatus && bed.status !== filterStatus) continue;
      const list = groups.get(bed.ward) ?? [];
      list.push(bed);
      groups.set(bed.ward, list);
    }
    return [...groups.entries()].sort(([a], [b]) => a.localeCompare(b));
  }, [beds, filterWard, filterStatus]);

  const filteredAdmissions = useMemo(() => {
    return admissions.filter((a) => {
      if (filterWard && !a.ward.toLowerCase().includes(filterWard.toLowerCase())) return false;
      if (filterStatus && a.status !== filterStatus) return false;
      return true;
    });
  }, [admissions, filterWard, filterStatus]);

  const exportRows = useMemo(
    () =>
      beds.map((b) => ({
        ward: b.ward,
        room: b.room,
        bed: b.bed_code,
        status: b.status,
        admission: b.current_admission_id ?? "",
      })),
    [beds],
  );

  const canActOnAdmission = selectedAdmission?.status === "active";
  const steps = [
    t("hospital.step.register"),
    t("hospital.step.bed"),
    t("hospital.step.admit"),
    t("hospital.step.transfer"),
    t("hospital.step.discharge"),
  ];

  async function runAction(label: string, fn: () => Promise<void>) {
    if (!session || busy) return;
    setBusy(true);
    setError(null);
    try {
      await fn();
      push({ message: label });
      await loadData(session);
    } catch (err) {
      const msg = err instanceof Error ? err.message : label;
      setError(msg);
      push({ message: msg });
      if (isAuthFailure(msg)) {
        await resetAuthState();
        setError(t("hospital.sessionExpired"));
      }
    } finally {
      setBusy(false);
    }
  }

  async function onConnect() {
    setBusy(true);
    setError(null);
    try {
      const next = await loginHospitalSession(tenantId, email, password);
      setLocalSession(next);
      saveHospitalSession(next);
      setNeedsReconnect(false);
      try {
        await login({
          tenantId,
          email,
          password,
          displayName: "Hospital Admin",
          registerIfMissing: true,
        });
      } catch {
        /* module session is enough */
      }
      try {
        await seedHospitalPersonas(next);
      } catch {
        /* optional */
      }
      try {
        await seedHospitalDemo(next);
      } catch {
        /* dashboard GET also seeds */
      }
      try {
        const [p, e, existing] = await Promise.all([
          fetchHospitalPatients(next),
          fetchHospitalEncounters(next),
          fetchHospitalCareEvents(next, { limit: 10 }),
        ]);
        if ((existing?.length ?? 0) === 0) {
          const seeded = await seedPeerCareEvents(
            next,
            targetsFromPatientsAndEncounters(p.items ?? [], e.items ?? []),
            { maxPatients: 2 },
          );
          if (seeded.labResults + seeded.dispenses > 0) {
            push({
              message: `${t("hospital.careEventsSeeded")}: lab ${seeded.labResults}, rx ${seeded.dispenses}`,
            });
          }
        }
      } catch {
        /* optional — clinical UI still works without peer care seed */
      }
      push({ message: t("hospital.connected") });
      await loadData(next);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("hospital.connectFailed"));
    } finally {
      setBusy(false);
    }
  }

  async function onSeedCareEvents() {
    if (!session || busy) return;
    if (patients.length === 0 || encounters.length === 0) {
      push({ message: t("hospital.seedCareEventsEmpty") });
      return;
    }
    setBusy(true);
    setError(null);
    try {
      const targets = targetsForCareEventSeed(
        patients,
        encounters,
        selectedEncounterId || undefined,
      );
      const seeded = await seedPeerCareEvents(session, targets, {
        maxPatients: selectedEncounterId ? 1 : 2,
        uniqueKey: Date.now().toString(36).slice(-5),
      });
      if (seeded.errors.length) {
        push({
          message: `${t("hospital.seedCareEventsFailed")}: ${seeded.errors[0]}`,
        });
      } else if (seeded.labResults + seeded.dispenses === 0) {
        push({
          message: `${t("hospital.careEventsSeeded")}: skipped ${seeded.skipped}`,
        });
      } else {
        push({
          message: `${t("hospital.careEventsSeeded")}: lab ${seeded.labResults}, rx ${seeded.dispenses}`,
        });
      }
      await loadData(session);
    } catch (err) {
      const message = err instanceof Error ? err.message : t("hospital.seedCareEventsFailed");
      setError(message);
      push({ message });
      if (isAuthFailure(message)) {
        await resetAuthState();
        setError(t("hospital.sessionExpired"));
      }
    } finally {
      setBusy(false);
    }
  }

  const tabs: { id: TabId; label: string }[] = [
    { id: "board", label: t("hospital.tab.board") },
    { id: "patients", label: t("hospital.tab.patients") },
    { id: "beds", label: t("hospital.tab.beds") },
    { id: "admissions", label: t("hospital.tab.admissions") },
    { id: "encounters", label: t("hospital.tab.encounters") },
  ];

  return (
    <PageLayout
      title={t("hospital.title")}
      subtitle={t("hospital.subtitle")}
      breadcrumb={[
        { label: t("hospital.breadcrumb.healthcare"), href: "/healthcare/clinic" },
        { label: t("hospital.breadcrumb.hospital") },
      ]}
      actions={
        session ? (
          <>
            <ExportButton label={t("common.export")} rows={exportRows} filename="hospital-beds.csv" />
            <PrintButton label={t("common.print")} />
            <button
              type="button"
              className="mp-btn"
              disabled={loading || busy}
              onClick={() => void loadData(session)}
            >
              {t("common.refresh")}
            </button>
          </>
        ) : null
      }
    >
      <ProgressBar
        value={progress}
        label={loading ? t("hospital.loading") : t("hospital.ready")}
      />

      {!session ? (
        <section className="mp-stack mp-hosp-section" aria-label={t("hospital.session")}>
          <h2>{t("hospital.connectHint")}</h2>
          <p className="mp-field-help">{t("hospital.connectHelp")}</p>
          <div className="mp-form mp-hosp-form-grid">
            <div className="mp-field">
              <label htmlFor="hosp-tenant">{t("hospital.tenant")}</label>
              <input
                id="hosp-tenant"
                className="mp-input"
                value={tenantId}
                onChange={(e) => setTenantId(e.target.value)}
                autoComplete="organization"
              />
            </div>
            <div className="mp-field">
              <label htmlFor="hosp-email">{t("hospital.email")}</label>
              <input
                id="hosp-email"
                className="mp-input"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="username"
              />
            </div>
            <div className="mp-field">
              <label htmlFor="hosp-password">{t("hospital.password")}</label>
              <input
                id="hosp-password"
                className="mp-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
              />
            </div>
          </div>
          <button
            type="button"
            className="mp-btn mp-btn-primary"
            disabled={busy}
            onClick={() => void onConnect()}
          >
            {t("hospital.connect")}
          </button>
        </section>
      ) : null}

      {error ? (
        <p className="mp-hosp-alert" role="alert">
          {error}
        </p>
      ) : null}

      {loading && session ? (
        <SkeletonTable rows={5} cols={4} />
      ) : session ? (
        <div className="mp-hosp-layout">
          <aside className="mp-hosp-aside" aria-label={t("hospital.careActions")}>
            <StepProgress steps={steps} current={lifecycleStep} />
            {draftSaving ? (
              <p className="mp-field-help" aria-live="polite">
                {t("hospital.draftSaved")}…
              </p>
            ) : null}

            <section className="mp-hosp-section" aria-labelledby="hosp-register-h">
              <h2 id="hosp-register-h">{t("hospital.register")}</h2>
              <div className="mp-form mp-hosp-form-grid">
                <div className="mp-field">
                  <label htmlFor="hosp-mrn">MRN</label>
                  <input
                    id="hosp-mrn"
                    className="mp-input"
                    value={mrn}
                    onChange={(e) => setMrn(e.target.value)}
                  />
                </div>
                <div className="mp-field">
                  <label htmlFor="hosp-fn">First name</label>
                  <input
                    id="hosp-fn"
                    className="mp-input"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                  />
                </div>
                <div className="mp-field">
                  <label htmlFor="hosp-ln">Last name</label>
                  <input
                    id="hosp-ln"
                    className="mp-input"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                  />
                </div>
                <div className="mp-field">
                  <label htmlFor="hosp-dob">DOB</label>
                  <input
                    id="hosp-dob"
                    className="mp-input"
                    type="date"
                    value={dob}
                    onChange={(e) => setDob(e.target.value)}
                  />
                </div>
              </div>
              <button
                type="button"
                className="mp-btn mp-btn-primary"
                disabled={busy}
                onClick={() =>
                  void runAction(`Patient registered: ${mrn}`, async () => {
                    const created = await registerHospitalPatient(session, {
                      mrn,
                      first_name: firstName,
                      last_name: lastName,
                      date_of_birth: dob,
                    });
                    setSelectedPatientId(created.id);
                    setTab("patients");
                  })
                }
              >
                {t("hospital.register")}
              </button>
            </section>

            <section className="mp-hosp-section" aria-labelledby="hosp-bed-h">
              <h2 id="hosp-bed-h">{t("hospital.createBed")}</h2>
              <div className="mp-form mp-hosp-form-grid">
                <div className="mp-field">
                  <label htmlFor="hosp-ward">{t("hospital.filterWard")}</label>
                  <input
                    id="hosp-ward"
                    className="mp-input"
                    value={ward}
                    onChange={(e) => setWard(e.target.value)}
                  />
                </div>
                <div className="mp-field">
                  <label htmlFor="hosp-room">Room</label>
                  <input
                    id="hosp-room"
                    className="mp-input"
                    value={room}
                    onChange={(e) => setRoom(e.target.value)}
                  />
                </div>
                <div className="mp-field">
                  <label htmlFor="hosp-bedcode">Bed</label>
                  <input
                    id="hosp-bedcode"
                    className="mp-input"
                    value={bedCode}
                    onChange={(e) => setBedCode(e.target.value)}
                  />
                </div>
              </div>
              <button
                type="button"
                className="mp-btn"
                disabled={busy}
                onClick={() =>
                  void runAction(`Bed ${ward}/${room}/${bedCode} created`, async () => {
                    const bed = await createHospitalBed(session, {
                      ward,
                      room,
                      bed_code: bedCode,
                    });
                    setSelectedBedId(bed.id);
                    setTab("board");
                  })
                }
              >
                {t("hospital.createBed")}
              </button>
            </section>

            <section className="mp-hosp-section" aria-labelledby="hosp-actions-h">
              <h2 id="hosp-actions-h">{t("hospital.careActions")}</h2>
              <div className="mp-form mp-hosp-form-grid">
                <div className="mp-field">
                  <label htmlFor="hosp-patient">Patient</label>
                  <select
                    id="hosp-patient"
                    className="mp-select"
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
                </div>
                <div className="mp-field">
                  <label htmlFor="hosp-sel-bed">Bed</label>
                  <select
                    id="hosp-sel-bed"
                    className="mp-select"
                    value={selectedBedId}
                    onChange={(e) => setSelectedBedId(e.target.value)}
                  >
                    <option value="">—</option>
                    {beds.map((b) => (
                      <option key={b.id} value={b.id}>
                        {b.ward}/{b.room}/{b.bed_code} ({b.status})
                      </option>
                    ))}
                  </select>
                </div>
                <div className="mp-field">
                  <label htmlFor="hosp-admission">Admission</label>
                  <select
                    id="hosp-admission"
                    className="mp-select"
                    value={selectedAdmissionId}
                    onChange={(e) => setSelectedAdmissionId(e.target.value)}
                  >
                    <option value="">—</option>
                    {admissions.map((a) => (
                      <option key={a.id} value={a.id}>
                        {a.ward} · {a.status}
                        {a.bed_id ? ` · ${bedLabelById.get(a.bed_id) ?? shortId(a.bed_id)}` : ""}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="mp-hosp-actions" role="group" aria-label={t("hospital.careActions")}>
                <button
                  type="button"
                  className="mp-btn mp-btn-primary"
                  disabled={busy || !selectedPatientId}
                  onClick={() =>
                    void runAction(`Admitted to ${ward}`, async () => {
                      const adm = await admitHospitalPatient(session, {
                        patient_id: selectedPatientId,
                        ward,
                        bed_id: selectedBedId || undefined,
                      });
                      setSelectedAdmissionId(adm.id);
                      setTab("admissions");
                    })
                  }
                >
                  {t("hospital.admit")}
                </button>
                <button
                  type="button"
                  className="mp-btn"
                  disabled={busy || !canActOnAdmission || !selectedBedId}
                  onClick={() =>
                    void runAction("Bed assigned", async () => {
                      await assignHospitalBed(session, selectedAdmissionId, {
                        bed_id: selectedBedId,
                      });
                    })
                  }
                >
                  {t("hospital.assignBed")}
                </button>
                <button
                  type="button"
                  className="mp-btn"
                  disabled={busy || !canActOnAdmission}
                  onClick={() =>
                    void runAction(`Transferred to ${ward}`, async () => {
                      await transferHospitalAdmission(session, selectedAdmissionId, {
                        to_ward: ward,
                        to_bed_id: selectedBedId || undefined,
                      });
                    })
                  }
                >
                  {t("hospital.transfer")}
                </button>
                <button
                  type="button"
                  className="mp-btn"
                  disabled={busy || !canActOnAdmission}
                  onClick={() =>
                    void runAction(t("hospital.billingPosted"), async () => {
                      const enc = await startHospitalEncounter(session, {
                        admission_id: selectedAdmissionId,
                      });
                      await completeHospitalEncounter(session, enc.id, {
                        procedure_codes: ["99223"],
                        diagnosis_codes: ["J18.9"],
                      });
                      const billing = await waitForBillingByEncounter(session, enc.id);
                      if (billing) {
                        setBillingsByEncounter((prev) => ({
                          ...prev,
                          [enc.id]: billing,
                        }));
                        setSelectedEncounterId(enc.id);
                        push({
                          message: `${t("hospital.billingPosted")}: ${billing.total_amount} ${billing.currency ?? "USD"}`,
                        });
                      } else {
                        push({ message: t("hospital.billingPending") });
                      }
                      setTab("encounters");
                    })
                  }
                >
                  {t("hospital.encounter")}
                </button>
                <button
                  type="button"
                  className="mp-btn mp-btn-danger"
                  disabled={busy || !canActOnAdmission}
                  onClick={() => setConfirmDischarge(true)}
                >
                  {t("hospital.discharge")}
                </button>
              </div>
              {availableBeds.length === 0 && beds.length > 0 ? (
                <p className="mp-field-help">{t("hospital.occupied")}: {occupancy.occupied}</p>
              ) : null}
            </section>
          </aside>

          <div className="mp-hosp-main">
            <section
              className="mp-hosp-occupancy"
              aria-label={t("hospital.occupancy")}
              aria-live="polite"
            >
              <div>
                <span className="mp-hosp-metric-label">{t("hospital.stat.patients")}</span>
                <strong>{occupancy.patients}</strong>
              </div>
              <div>
                <span className="mp-hosp-metric-label">{t("hospital.available")}</span>
                <strong>{occupancy.available}</strong>
              </div>
              <div>
                <span className="mp-hosp-metric-label">{t("hospital.occupied")}</span>
                <strong>{occupancy.occupied}</strong>
              </div>
              <div>
                <span className="mp-hosp-metric-label">{t("hospital.totalBeds")}</span>
                <strong>{occupancy.total}</strong>
              </div>
              <div>
                <span className="mp-hosp-metric-label">{t("hospital.activeAdmissions")}</span>
                <strong>{occupancy.active}</strong>
              </div>
              <div>
                <span className="mp-hosp-metric-label">{t("hospital.stat.openEncounters")}</span>
                <strong>{occupancy.openEncounters}</strong>
              </div>
            </section>

            <AdvancedFilterBar
              filters={[
                { id: "ward", label: t("hospital.filterWard"), type: "text" },
                { id: "status", label: t("hospital.filterStatus"), type: "text" },
              ]}
              onChange={(values) => {
                setFilterWard(values.ward ?? "");
                setFilterStatus((values.status ?? "").toLowerCase().trim());
              }}
            />

            <div className="mp-hosp-tabs" role="tablist" aria-label={t("hospital.title")}>
              {tabs.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  role="tab"
                  id={`hosp-tab-${item.id}`}
                  aria-selected={tab === item.id}
                  aria-controls={`hosp-panel-${item.id}`}
                  className={`mp-btn ${tab === item.id ? "mp-btn-primary" : "mp-btn-ghost"}`}
                  onClick={() => setTab(item.id)}
                >
                  {item.label}
                </button>
              ))}
            </div>

            <div
              role="tabpanel"
              id={`hosp-panel-${tab}`}
              aria-labelledby={`hosp-tab-${tab}`}
              className="mp-hosp-panel mp-animate-in"
            >
              {tab === "board" ? (
                beds.length === 0 ? (
                  <EmptyState
                    title={t("hospital.noBeds")}
                    description={t("hospital.noBedsHint")}
                    action={
                      <button
                        type="button"
                        className="mp-btn mp-btn-primary"
                        onClick={() =>
                          document.getElementById("hosp-bed-h")?.scrollIntoView({
                            behavior: "smooth",
                          })
                        }
                      >
                        {t("hospital.createBed")}
                      </button>
                    }
                  />
                ) : (
                  <div className="mp-hosp-board">
                    {bedsByWard.length === 0 ? (
                      <EmptyState
                        title={t("common.filter")}
                        description={`${t("hospital.filterWard")} / ${t("hospital.filterStatus")}`}
                      />
                    ) : (
                      bedsByWard.map(([wardName, wardBeds]) => (
                        <section key={wardName} aria-labelledby={`ward-${wardName}`}>
                          <h3 id={`ward-${wardName}`}>{wardName}</h3>
                          <div className="mp-hosp-bed-grid" role="list">
                            {wardBeds.map((bed) => {
                              const selected = bed.id === selectedBedId;
                              return (
                                <button
                                  key={bed.id}
                                  type="button"
                                  role="listitem"
                                  className={`mp-hosp-bed ${selected ? "mp-hosp-bed--selected" : ""} mp-hosp-bed--${bed.status}`}
                                  aria-pressed={selected}
                                  aria-label={`${bed.ward} ${bed.room} ${bed.bed_code} ${bed.status}`}
                                  onClick={() => {
                                    setSelectedBedId(bed.id);
                                    setWard(bed.ward);
                                    setRoom(bed.room);
                                    setBedCode(bed.bed_code);
                                    if (bed.current_admission_id) {
                                      setSelectedAdmissionId(bed.current_admission_id);
                                    }
                                  }}
                                >
                                  <span className="mp-hosp-bed-code">
                                    {bed.room}-{bed.bed_code}
                                  </span>
                                  <StatusChip status={bed.status} />
                                </button>
                              );
                            })}
                          </div>
                        </section>
                      ))
                    )}
                  </div>
                )
              ) : null}

              {tab === "patients" ? (
                patients.length === 0 ? (
                  <EmptyState
                    title={t("hospital.noPatients")}
                    description={t("hospital.noPatientsHint")}
                  />
                ) : (
                  <DataTable
                    columns={[
                      { key: "mrn", header: "MRN", sortable: true },
                      { key: "full_name", header: "Name", sortable: true },
                      { key: "date_of_birth", header: "DOB", sortable: true },
                    ]}
                    rows={patients.map((p) => ({
                      id: p.id,
                      mrn: p.mrn,
                      full_name: p.full_name ?? `${p.first_name} ${p.last_name}`,
                      date_of_birth: p.date_of_birth,
                    }))}
                    selectable
                    onSelectionChange={(ids) => {
                      if (ids[0]) setSelectedPatientId(ids[0]);
                    }}
                  />
                )
              ) : null}

              {tab === "beds" ? (
                beds.length === 0 ? (
                  <EmptyState
                    title={t("hospital.noBeds")}
                    description={t("hospital.noBedsHint")}
                  />
                ) : (
                  <DataTable
                    columns={[
                      { key: "location", header: "Location", sortable: true },
                      {
                        key: "status",
                        header: "Status",
                        sortable: true,
                        render: (row) => <StatusChip status={String(row.status)} />,
                      },
                      { key: "admission", header: "Admission" },
                    ]}
                    rows={beds
                      .filter((b) => {
                        if (filterWard && !b.ward.toLowerCase().includes(filterWard.toLowerCase()))
                          return false;
                        if (filterStatus && b.status !== filterStatus) return false;
                        return true;
                      })
                      .map((b) => ({
                        id: b.id,
                        location: `${b.ward}/${b.room}/${b.bed_code}`,
                        status: b.status,
                        admission: b.current_admission_id
                          ? shortId(b.current_admission_id)
                          : "—",
                      }))}
                    selectable
                    onSelectionChange={(ids) => {
                      if (ids[0]) setSelectedBedId(ids[0]);
                    }}
                  />
                )
              ) : null}

              {tab === "admissions" ? (
                filteredAdmissions.length === 0 ? (
                  <EmptyState
                    title={t("hospital.noAdmissions")}
                    description={t("hospital.noAdmissionsHint")}
                  />
                ) : (
                  <DataTable
                    columns={[
                      { key: "ward", header: t("hospital.filterWard"), sortable: true },
                      {
                        key: "status",
                        header: "Status",
                        sortable: true,
                        render: (row) => <StatusChip status={String(row.status)} />,
                      },
                      { key: "bed", header: "Bed", sortable: true },
                      { key: "patient", header: "Patient", sortable: true },
                      { key: "discharged_at", header: "Discharged" },
                    ]}
                    rows={filteredAdmissions.map((a) => ({
                      id: a.id,
                      ward: a.ward,
                      status: a.status,
                      bed: a.bed_id ? (bedLabelById.get(a.bed_id) ?? shortId(a.bed_id)) : "—",
                      patient: patientNameById.get(a.patient_id) ?? shortId(a.patient_id),
                      discharged_at: a.discharged_at
                        ? String(a.discharged_at).slice(0, 19).replace("T", " ")
                        : "—",
                    }))}
                    selectable
                    onSelectionChange={(ids) => {
                      if (ids[0]) setSelectedAdmissionId(ids[0]);
                    }}
                  />
                )
              ) : null}

              {tab === "encounters" ? (
                encounters.length === 0 ? (
                  <EmptyState
                    title={t("hospital.noEncounters")}
                    description={t("hospital.noEncountersHint")}
                  />
                ) : (
                  <>
                    <div className="mp-hosp-seed-bar">
                      <button
                        type="button"
                        className="mp-btn"
                        disabled={busy}
                        onClick={() => void onSeedCareEvents()}
                      >
                        {t("hospital.seedCareEvents")}
                      </button>
                      <p className="mp-field-help">{t("hospital.seedCareEventsHelp")}</p>
                    </div>
                    <DataTable
                      columns={[
                        { key: "id", header: t("hospital.col.encounter"), sortable: true },
                        {
                          key: "status",
                          header: t("hospital.filterStatus"),
                          sortable: true,
                          render: (row) => <StatusChip status={String(row.status)} />,
                        },
                        { key: "codes", header: t("hospital.col.codes") },
                        {
                          key: "billing",
                          header: t("hospital.billing"),
                          render: (row) => {
                            const b = billingsByEncounter[String(row.id)];
                            if (!b) {
                              return (
                                <span className="mp-hosp-chip mp-hosp-chip--muted">
                                  {t("hospital.billingNone")}
                                </span>
                              );
                            }
                            return (
                              <span className="mp-hosp-chip mp-hosp-chip--ok">
                                {b.total_amount} {b.currency ?? "USD"} · {b.status}
                              </span>
                            );
                          },
                        },
                        {
                          key: "care",
                          header: t("hospital.careEvents"),
                          render: (row) => {
                            const count = careEvents.filter(
                              (ev) => ev.encounter_id === String(row.id),
                            ).length;
                            if (!count) {
                              return (
                                <span className="mp-hosp-chip mp-hosp-chip--muted">
                                  {t("hospital.careEventsNone")}
                                </span>
                              );
                            }
                            return (
                              <span className="mp-hosp-chip mp-hosp-chip--ok">
                                {count}
                              </span>
                            );
                          },
                        },
                      ]}
                      rows={encounters.map((e) => ({
                        id: e.id,
                        status: e.status,
                        codes:
                          [...(e.diagnosis_codes ?? []), ...(e.procedure_codes ?? [])].join(
                            ", ",
                          ) || "—",
                      }))}
                      selectable
                      onSelectionChange={(ids) => {
                        if (ids[0]) setSelectedEncounterId(ids[0]);
                      }}
                    />
                    {selectedEncounterId && billingsByEncounter[selectedEncounterId] ? (
                      <section
                        className="mp-hosp-billing-panel mp-animate-in"
                        aria-label={t("hospital.billing")}
                      >
                        <header>{t("hospital.billingDetail")}</header>
                        <dl className="mp-hosp-billing-dl">
                          <div>
                            <dt>{t("hospital.col.encounter")}</dt>
                            <dd>{shortId(selectedEncounterId)}</dd>
                          </div>
                          <div>
                            <dt>{t("hospital.billingAmount")}</dt>
                            <dd>
                              {billingsByEncounter[selectedEncounterId].total_amount}{" "}
                              {billingsByEncounter[selectedEncounterId].currency ?? "USD"}
                            </dd>
                          </div>
                          <div>
                            <dt>{t("hospital.filterStatus")}</dt>
                            <dd>
                              <StatusChip
                                status={billingsByEncounter[selectedEncounterId].status}
                              />
                            </dd>
                          </div>
                          <div>
                            <dt>{t("hospital.billingCorrelation")}</dt>
                            <dd>
                              {billingsByEncounter[selectedEncounterId].correlation_id || "—"}
                            </dd>
                          </div>
                        </dl>
                        <p className="mp-field-help">{t("hospital.billingEventHint")}</p>
                      </section>
                    ) : null}
                    {selectedEncounterId ? (
                      <section
                        className="mp-hosp-billing-panel mp-animate-in"
                        aria-label={t("hospital.careEvents")}
                      >
                        <header>{t("hospital.careEventsDetail")}</header>
                        {careEvents.filter((ev) => ev.encounter_id === selectedEncounterId)
                          .length === 0 ? (
                          <p className="mp-field-help">{t("hospital.careEventsNone")}</p>
                        ) : (
                          <ul className="mp-hosp-care-list">
                            {careEvents
                              .filter((ev) => ev.encounter_id === selectedEncounterId)
                              .map((ev) => (
                                <li key={ev.id}>
                                  <StatusChip status={ev.event_kind} />{" "}
                                  <span>{ev.source_context}</span>
                                  <span className="mp-hosp-care-summary">
                                    {ev.event_kind === "lab_result"
                                      ? `${String(ev.summary.test_code ?? "")} = ${String(ev.summary.result_value ?? "")}${
                                          ev.summary.result_unit
                                            ? ` ${String(ev.summary.result_unit)}`
                                            : ""
                                        }`
                                      : `${String(ev.summary.drug_code ?? "")} × ${String(ev.summary.quantity_dispensed ?? "")}`}
                                  </span>
                                </li>
                              ))}
                          </ul>
                        )}
                        <p className="mp-field-help">{t("hospital.careEventsHint")}</p>
                      </section>
                    ) : null}
                  </>
                )
              ) : null}
            </div>
          </div>
        </div>
      ) : null}

      {confirmDischarge ? (
        <div
          className="mp-overlay"
          role="presentation"
          onClick={() => setConfirmDischarge(false)}
        >
          <div
            className="mp-panel mp-hosp-confirm mp-animate-in"
            role="alertdialog"
            aria-modal="true"
            aria-labelledby="hosp-discharge-title"
            onClick={(e) => e.stopPropagation()}
          >
            <header id="hosp-discharge-title">{t("hospital.discharge")}</header>
            <p>{t("hospital.confirmDischarge")}</p>
            <div className="mp-hosp-actions">
              <button
                type="button"
                className="mp-btn"
                onClick={() => setConfirmDischarge(false)}
              >
                {t("common.cancel")}
              </button>
              <button
                type="button"
                className="mp-btn mp-btn-primary"
                disabled={busy}
                onClick={() => {
                  setConfirmDischarge(false);
                  void runAction("Patient discharged", async () => {
                    await dischargeHospitalAdmission(session!, selectedAdmissionId);
                    setTab("admissions");
                  });
                }}
              >
                {t("common.confirm")}
              </button>
            </div>
          </div>
        </div>
      ) : null}

      <style jsx>{`
        .mp-hosp-layout {
          display: grid;
          grid-template-columns: minmax(280px, 360px) 1fr;
          gap: 1.25rem;
          align-items: start;
        }
        .mp-hosp-aside,
        .mp-hosp-main {
          display: flex;
          flex-direction: column;
          gap: 1rem;
          min-width: 0;
        }
        .mp-hosp-section {
          padding-block: 0.25rem;
          border-block-end: 1px solid var(--mp-border);
          padding-block-end: 1rem;
        }
        .mp-hosp-section h2,
        .mp-hosp-board h3 {
          margin: 0 0 0.75rem;
          font-size: 1rem;
        }
        .mp-hosp-form-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 0.65rem 0.75rem;
          margin-block-end: 0.75rem;
        }
        .mp-hosp-form-grid .mp-field:last-child:nth-child(odd) {
          grid-column: 1 / -1;
        }
        .mp-hosp-actions {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .mp-hosp-occupancy {
          display: grid;
          grid-template-columns: repeat(4, minmax(0, 1fr));
          gap: 0.75rem;
          padding: 0.85rem 1rem;
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius);
          background: var(--mp-bg-muted);
        }
        .mp-hosp-occupancy strong {
          display: block;
          font-size: 1.35rem;
          line-height: 1.2;
        }
        .mp-hosp-metric-label {
          display: block;
          color: var(--mp-fg-muted);
          font-size: 0.8rem;
          margin-block-end: 0.2rem;
        }
        .mp-hosp-tabs {
          display: flex;
          flex-wrap: wrap;
          gap: 0.4rem;
        }
        .mp-hosp-bed-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(7.5rem, 1fr));
          gap: 0.5rem;
        }
        .mp-hosp-bed {
          display: flex;
          flex-direction: column;
          align-items: flex-start;
          gap: 0.35rem;
          padding: 0.65rem 0.7rem;
          border: 1px solid var(--mp-border);
          border-radius: var(--mp-radius-sm);
          background: var(--mp-bg-elevated);
          cursor: pointer;
          text-align: start;
          transition:
            border-color 180ms ease,
            transform 180ms ease,
            background 180ms ease;
        }
        .mp-hosp-bed:hover {
          border-color: var(--mp-fg-muted);
        }
        .mp-hosp-bed--selected {
          outline: 2px solid var(--mp-accent, var(--mp-primary));
          outline-offset: 1px;
        }
        .mp-hosp-bed--available {
          border-inline-start: 3px solid #2f9e6b;
        }
        .mp-hosp-bed--occupied {
          border-inline-start: 3px solid #c47a2c;
        }
        .mp-hosp-bed-code {
          font-weight: 600;
          font-size: 0.95rem;
        }
        .mp-hosp-chip {
          display: inline-block;
          padding: 0.1rem 0.45rem;
          border-radius: var(--mp-radius-sm);
          font-size: 0.75rem;
          text-transform: lowercase;
          background: var(--mp-bg-muted);
        }
        .mp-hosp-chip--ok {
          background: color-mix(in srgb, #2f9e6b 22%, transparent);
          color: inherit;
        }
        .mp-hosp-chip--warn {
          background: color-mix(in srgb, #c47a2c 24%, transparent);
        }
        .mp-hosp-chip--muted {
          opacity: 0.75;
        }
        .mp-hosp-billing-panel {
          margin-block-start: 1rem;
          padding: 0.85rem 1rem;
          border: 1px solid var(--mp-border, color-mix(in srgb, currentColor 14%, transparent));
          border-radius: var(--mp-radius-sm);
          background: color-mix(in srgb, var(--mp-bg-muted, transparent) 55%, transparent);
        }
        .mp-hosp-seed-bar {
          display: flex;
          flex-wrap: wrap;
          align-items: center;
          gap: 0.75rem;
          margin-block-end: 0.75rem;
        }
        .mp-hosp-seed-bar .mp-field-help {
          margin: 0;
          flex: 1 1 12rem;
        }
        .mp-hosp-billing-panel header {
          font-weight: 600;
          margin-block-end: 0.65rem;
        }
        .mp-hosp-billing-dl {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
          gap: 0.65rem 1rem;
          margin: 0;
        }
        .mp-hosp-billing-dl dt {
          font-size: 0.75rem;
          opacity: 0.75;
          margin: 0;
        }
        .mp-hosp-billing-dl dd {
          margin: 0.15rem 0 0;
          font-weight: 600;
        }
        .mp-hosp-care-list {
          list-style: none;
          margin: 0;
          padding: 0;
          display: grid;
          gap: 0.5rem;
        }
        .mp-hosp-care-list li {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          align-items: center;
        }
        .mp-hosp-care-summary {
          color: var(--mp-muted, #64748b);
          font-size: 0.9em;
        }
        .mp-hosp-alert {
          color: var(--mp-danger, var(--mp-orange));
          margin: 0.5rem 0;
        }
        .mp-hosp-confirm {
          position: relative;
          inset: auto;
          width: min(420px, 92vw);
          margin: 15vh auto 0;
          padding: 0 0 1rem;
        }
        .mp-hosp-confirm p {
          padding: 0.85rem 1rem;
          margin: 0;
        }
        .mp-hosp-confirm .mp-hosp-actions {
          padding-inline: 1rem;
        }
        @media (max-width: 960px) {
          .mp-hosp-layout {
            grid-template-columns: 1fr;
          }
          .mp-hosp-occupancy {
            grid-template-columns: repeat(2, minmax(0, 1fr));
          }
        }
        @media (prefers-reduced-motion: reduce) {
          .mp-hosp-bed {
            transition: none;
          }
        }
      `}</style>
    </PageLayout>
  );
}
