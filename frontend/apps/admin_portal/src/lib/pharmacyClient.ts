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
};

export type PharmacyDispense = {
  id: string;
  prescription_id: string;
  quantity_dispensed: number;
};

type Page<T> = { items: T[]; total: number };

export async function seedPharmacyPersonas(session: ApiSession) {
  return apiPost("/api/v1/identity/personas/pharmacy/seed", session, {});
}

export async function fetchPrescriptions(session: ApiSession): Promise<Page<PharmacyPrescription>> {
  return apiGet("/api/v1/pharmacy/prescriptions", session);
}

export async function receivePrescription(
  session: ApiSession,
  body: {
    rx_number: string;
    patient_ref: string;
    drug_code: string;
    drug_name: string;
    quantity: number;
  },
): Promise<PharmacyPrescription> {
  return apiPost("/api/v1/pharmacy/prescriptions", session, body);
}

export async function dispensePrescription(
  session: ApiSession,
  prescription_id: string,
): Promise<PharmacyDispense> {
  return apiPost("/api/v1/pharmacy/dispenses", session, { prescription_id });
}
