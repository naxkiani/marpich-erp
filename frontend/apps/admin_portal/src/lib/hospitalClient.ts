import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadHospitalSession,
  saveSession as saveHospitalSession,
} from "./clientAuth";

export type { ApiSession };

export const loginHospitalSession = createClientLogin("Hospital Admin");
export { loadHospitalSession, saveHospitalSession };

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

type Page<T> = { items: T[]; total: number; limit: number; offset: number };

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
  body: { patient_id: string; ward: string },
): Promise<HospitalAdmission> {
  return apiPost("/api/v1/hospital/admissions", session, body);
}

export async function startHospitalEncounter(
  session: ApiSession,
  body: { admission_id: string },
): Promise<HospitalEncounter> {
  return apiPost("/api/v1/hospital/encounters", session, body);
}

export async function completeHospitalEncounter(
  session: ApiSession,
  encounterId: string,
  body: { procedure_codes?: string[]; diagnosis_codes?: string[] } = {},
): Promise<HospitalEncounter> {
  return apiPost(`/api/v1/hospital/encounters/${encounterId}/complete`, session, body);
}

export async function seedHospitalPersonas(
  session: ApiSession,
): Promise<Record<string, unknown>> {
  return apiPost("/api/v1/identity/personas/hospital/seed", session, {});
}
