import {
  type ApiSession,
  apiGet,
  apiPost,
  clearSession,
  createClientLogin,
  isAuthFailure,
  loadSession as loadHospitalSession,
  saveSession as saveHospitalSession,
} from "./clientAuth";

export type { ApiSession };
export { isAuthFailure };

export const loginHospitalSession = createClientLogin("Hospital Admin");
export { loadHospitalSession, saveHospitalSession };

export function clearHospitalSession(): void {
  clearSession();
}

export type HospitalPatient = {
  id: string;
  mrn: string;
  first_name: string;
  last_name: string;
  full_name?: string;
  date_of_birth: string;
  [key: string]: unknown;
};

export type HospitalAdmission = {
  id: string;
  patient_id: string;
  ward: string;
  status: string;
  bed_id?: string | null;
  discharged_at?: string | null;
  [key: string]: unknown;
};

export type HospitalBed = {
  id: string;
  ward: string;
  room: string;
  bed_code: string;
  status: string;
  current_admission_id?: string | null;
  [key: string]: unknown;
};

export type HospitalEncounter = {
  id: string;
  patient_id: string;
  admission_id: string;
  status: string;
  procedure_codes?: string[];
  diagnosis_codes?: string[];
  [key: string]: unknown;
};

export type HospitalDashboard = {
  as_of?: string;
  summary: {
    patient_count: number;
    bed_count: number;
    available_beds: number;
    occupied_beds: number;
    active_admissions: number;
    admission_count: number;
    encounter_count: number;
    open_encounters: number;
    completed_encounters: number;
  };
  headline?: Record<string, unknown>;
};

type Page<T> = { items: T[]; total: number; limit: number; offset: number };

export async function seedHospitalPersonas(
  session: ApiSession,
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/identity/personas/hospital/seed", session, {});
}

export async function seedHospitalDemo(session: ApiSession): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/hospital/seed", session, {});
}

export async function fetchHospitalDashboard(session: ApiSession): Promise<HospitalDashboard> {
  return apiGet("/api/v1/hospital/dashboard", session);
}

export async function fetchHospitalPatients(
  session: ApiSession,
): Promise<Page<HospitalPatient>> {
  return apiGet("/api/v1/hospital/patients", session);
}

export async function fetchHospitalAdmissions(
  session: ApiSession,
): Promise<Page<HospitalAdmission>> {
  return apiGet("/api/v1/hospital/admissions", session);
}

export async function fetchHospitalBeds(
  session: ApiSession,
): Promise<Page<HospitalBed>> {
  return apiGet("/api/v1/hospital/beds", session);
}

export async function fetchHospitalEncounters(
  session: ApiSession,
): Promise<Page<HospitalEncounter>> {
  return apiGet("/api/v1/hospital/encounters", session);
}

export async function registerHospitalPatient(
  session: ApiSession,
  body: {
    mrn: string;
    first_name: string;
    last_name: string;
    date_of_birth: string;
  },
): Promise<HospitalPatient> {
  return apiPost("/api/v1/hospital/patients", session, body);
}

export async function admitHospitalPatient(
  session: ApiSession,
  body: { patient_id: string; ward: string; bed_id?: string },
): Promise<HospitalAdmission> {
  return apiPost("/api/v1/hospital/admissions", session, body);
}

export async function createHospitalBed(
  session: ApiSession,
  body: { ward: string; room: string; bed_code: string },
): Promise<HospitalBed> {
  return apiPost("/api/v1/hospital/beds", session, body);
}

export async function assignHospitalBed(
  session: ApiSession,
  admissionId: string,
  body: { bed_id: string },
): Promise<HospitalAdmission> {
  return apiPost(`/api/v1/hospital/admissions/${admissionId}/assign-bed`, session, body);
}

export async function transferHospitalAdmission(
  session: ApiSession,
  admissionId: string,
  body: { to_ward: string; to_bed_id?: string },
): Promise<HospitalAdmission> {
  return apiPost(`/api/v1/hospital/admissions/${admissionId}/transfer`, session, body);
}

export async function dischargeHospitalAdmission(
  session: ApiSession,
  admissionId: string,
): Promise<HospitalAdmission> {
  return apiPost(`/api/v1/hospital/admissions/${admissionId}/discharge`, session, {});
}

export async function startHospitalEncounter(
  session: ApiSession,
  body: { admission_id: string },
): Promise<HospitalEncounter> {
  return apiPost("/api/v1/hospital/encounters", session, body);
}

export async function documentHospitalEncounter(
  session: ApiSession,
  encounterId: string,
  body: { procedure_codes?: string[]; diagnosis_codes?: string[] } = {},
): Promise<HospitalEncounter> {
  return apiPost(`/api/v1/hospital/encounters/${encounterId}/document`, session, body);
}

export async function completeHospitalEncounter(
  session: ApiSession,
  encounterId: string,
  body: { procedure_codes?: string[]; diagnosis_codes?: string[] } = {},
): Promise<HospitalEncounter> {
  return apiPost(`/api/v1/hospital/encounters/${encounterId}/complete`, session, body);
}

export type EncounterBilling = {
  id: string;
  external_encounter_id: string;
  patient_ref: string;
  procedure_codes?: string[];
  line_items?: Array<{ code?: string; amount?: number; [key: string]: unknown }>;
  total_amount: number;
  currency?: string;
  status: string;
  correlation_id?: string;
  [key: string]: unknown;
};

export async function fetchBillingByEncounter(
  session: ApiSession,
  encounterId: string,
): Promise<EncounterBilling> {
  return apiGet(`/api/v1/accounting/billings/by-encounter/${encounterId}`, session);
}

/** Poll briefly — in-process bus is sync, but UI may race with refresh. */
export async function waitForBillingByEncounter(
  session: ApiSession,
  encounterId: string,
  options: { attempts?: number; delayMs?: number } = {},
): Promise<EncounterBilling | null> {
  const attempts = options.attempts ?? 5;
  const delayMs = options.delayMs ?? 80;
  for (let i = 0; i < attempts; i += 1) {
    try {
      return await fetchBillingByEncounter(session, encounterId);
    } catch {
      await new Promise((r) => setTimeout(r, delayMs));
    }
  }
  return null;
}

export async function fetchBillings(session: ApiSession): Promise<EncounterBilling[]> {
  const data = await apiGet<EncounterBilling[] | { items: EncounterBilling[] }>(
    "/api/v1/accounting/billings",
    session,
  );
  if (Array.isArray(data)) return data;
  return data.items ?? [];
}

export type HospitalCareEvent = {
  id: string;
  tenant_id: string;
  source_event_id: string;
  source_context: string;
  event_kind: string;
  peer_id: string;
  patient_id: string;
  admission_id?: string | null;
  encounter_id?: string | null;
  summary: Record<string, unknown>;
  correlation_id?: string | null;
  occurred_at: string;
};

export async function fetchHospitalCareEvents(
  session: ApiSession,
  options: {
    patientId?: string;
    admissionId?: string;
    encounterId?: string;
    limit?: number;
  } = {},
): Promise<HospitalCareEvent[]> {
  const params = new URLSearchParams();
  if (options.patientId) params.set("patient_id", options.patientId);
  if (options.admissionId) params.set("admission_id", options.admissionId);
  if (options.encounterId) params.set("encounter_id", options.encounterId);
  if (options.limit) params.set("limit", String(options.limit));
  const qs = params.toString();
  const path = qs ? `/api/v1/hospital/care-events?${qs}` : "/api/v1/hospital/care-events";
  const data = await apiGet<{ items: HospitalCareEvent[]; total?: number } | HospitalCareEvent[]>(
    path,
    session,
  );
  if (Array.isArray(data)) return data;
  return data.items ?? [];
}
