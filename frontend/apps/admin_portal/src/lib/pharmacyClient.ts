import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadPharmacySession,
  saveSession as savePharmacySession,
} from "./clientAuth";

export type { ApiSession };
export const loginPharmacySession = createClientLogin("Pharmacy Admin");
export { loadPharmacySession, savePharmacySession };

export type PharmacyPrescription = {
  id: string;
  rx_number: string;
  patient_ref: string;
  drug_code: string;
  drug_name: string;
  quantity: number;
  status: string;
  source_encounter_ref?: string | null;
  counseling_notes?: string | null;
  counselled_at?: string | null;
};

export type PharmacyDispense = {
  id: string;
  prescription_id: string;
  patient_ref?: string;
  drug_code?: string;
  quantity_dispensed: number;
  dispensed_at?: string;
};

type Page<T> = { items: T[]; total: number; limit?: number; offset?: number };

export async function seedPharmacyPersonas(session: ApiSession) {
  return apiPost("/api/v1/identity/personas/pharmacy/seed", session, {});
}

export async function fetchPrescriptions(session: ApiSession): Promise<Page<PharmacyPrescription>> {
  return apiGet("/api/v1/pharmacy/prescriptions", session);
}

export async function fetchDispenses(session: ApiSession): Promise<Page<PharmacyDispense>> {
  return apiGet("/api/v1/pharmacy/dispenses", session);
}

export async function receivePrescription(
  session: ApiSession,
  body: {
    rx_number: string;
    patient_ref: string;
    drug_code: string;
    drug_name: string;
    quantity: number;
    source_encounter_ref?: string;
  },
): Promise<PharmacyPrescription> {
  return apiPost("/api/v1/pharmacy/prescriptions", session, body);
}

export async function dispensePrescription(
  session: ApiSession,
  prescription_id: string,
  quantity_dispensed?: number,
): Promise<PharmacyDispense> {
  return apiPost("/api/v1/pharmacy/dispenses", session, {
    prescription_id,
    ...(quantity_dispensed != null ? { quantity_dispensed } : {}),
  });
}

/** CAP-HLT-008 counsel step after dispense. */
export async function counselPrescription(
  session: ApiSession,
  prescriptionId: string,
  body: { notes?: string } = {},
): Promise<PharmacyPrescription> {
  return apiPost(`/api/v1/pharmacy/prescriptions/${prescriptionId}/counsel`, session, body);
}
