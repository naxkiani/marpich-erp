import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadClinicSession,
  saveSession as saveClinicSession,
} from "./clientAuth";

export type { ApiSession };

export const loginClinicSession = createClientLogin("Clinic Admin");
export { loadClinicSession, saveClinicSession };

export type ClinicPatient = {
  id: string;
  patient_number: string;
  first_name: string;
  last_name: string;
  full_name?: string;
  date_of_birth: string;
  [key: string]: unknown;
};

export type ClinicEncounter = {
  id: string;
  patient_id: string;
  appointment_id?: string | null;
  status: string;
  diagnosis_codes?: string[];
  [key: string]: unknown;
};

export type ClinicAppointment = {
  id: string;
  patient_id: string;
  provider_name: string;
  scheduled_at: string;
  status: string;
  [key: string]: unknown;
};

type Page<T> = { items: T[]; total: number; limit: number; offset: number };

export async function fetchClinicPatients(session: ApiSession): Promise<Page<ClinicPatient>> {
  return apiGet("/api/v1/clinic/patients", session);
}

export async function fetchClinicEncounters(session: ApiSession): Promise<Page<ClinicEncounter>> {
  return apiGet("/api/v1/clinic/encounters", session);
}

export async function fetchClinicAppointments(
  session: ApiSession,
): Promise<Page<ClinicAppointment>> {
  return apiGet("/api/v1/clinic/appointments", session);
}

export async function registerClinicPatient(
  session: ApiSession,
  body: {
    patient_number: string;
    first_name: string;
    last_name: string;
    date_of_birth: string;
  },
): Promise<ClinicPatient> {
  return apiPost("/api/v1/clinic/patients", session, body);
}

export async function scheduleClinicAppointment(
  session: ApiSession,
  body: { patient_id: string; provider_name: string; scheduled_at: string },
): Promise<ClinicAppointment> {
  return apiPost("/api/v1/clinic/appointments", session, body);
}

export async function startClinicEncounter(
  session: ApiSession,
  body: { appointment_id?: string; patient_id?: string },
): Promise<ClinicEncounter> {
  return apiPost("/api/v1/clinic/encounters", session, body);
}

export async function completeClinicEncounter(
  session: ApiSession,
  encounterId: string,
  diagnosis_codes: string[] = [],
): Promise<ClinicEncounter> {
  return apiPost(`/api/v1/clinic/encounters/${encounterId}/complete`, session, {
    diagnosis_codes,
  });
}

export async function seedClinicPersonas(session: ApiSession): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/identity/personas/clinic/seed", session, {});
}
