import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadLaboratorySession,
  saveSession as saveLaboratorySession,
} from "./clientAuth";

export type { ApiSession };
export const loginLaboratorySession = createClientLogin("Laboratory Admin");
export { loadLaboratorySession, saveLaboratorySession };

export type LabOrder = {
  id: string;
  order_number: string;
  patient_ref: string;
  test_code: string;
  status: string;
  result_value?: string | null;
  result_unit?: string | null;
  source_encounter_ref?: string | null;
  finalized_at?: string | null;
};

export type LabSample = {
  id: string;
  order_id: string;
  accession_number: string;
  specimen_type: string;
  patient_ref: string;
  received_at?: string;
};

type Page<T> = { items: T[]; total: number; limit?: number; offset?: number };

export async function seedLaboratoryPersonas(session: ApiSession) {
  return apiPost("/api/v1/identity/personas/laboratory/seed", session, {});
}

export async function fetchLabOrders(session: ApiSession): Promise<Page<LabOrder>> {
  return apiGet("/api/v1/laboratory/orders", session);
}

export async function fetchLabSamples(session: ApiSession): Promise<Page<LabSample>> {
  return apiGet("/api/v1/laboratory/samples", session);
}

export async function placeLabOrder(
  session: ApiSession,
  body: {
    order_number: string;
    patient_ref: string;
    test_code: string;
    source_encounter_ref?: string;
  },
): Promise<LabOrder> {
  return apiPost("/api/v1/laboratory/orders", session, body);
}

export async function receiveLabSample(
  session: ApiSession,
  body: { order_id: string; accession_number: string; specimen_type: string },
): Promise<LabSample> {
  return apiPost("/api/v1/laboratory/samples", session, body);
}

export async function finalizeLabResult(
  session: ApiSession,
  orderId: string,
  body: { result_value: string; result_unit?: string },
): Promise<LabOrder> {
  return apiPost(`/api/v1/laboratory/orders/${orderId}/results`, session, body);
}
