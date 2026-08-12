import { apiGet, apiPost, getStoredSession, type AuthSession } from "@marpich/auth-provider";

export type ApiSession = AuthSession;

export type PurchaseRequisition = {
  id: string;
  sku: string;
  quantity: string;
  quantity_available: string;
  reorder_threshold: string;
  status: string;
  reason: string;
};

export type Page<T> = { items: T[]; total: number; limit: number; offset: number };

export function loadProcurementSession(): ApiSession | null {
  return getStoredSession();
}

export async function fetchRequisitions(session: ApiSession): Promise<Page<PurchaseRequisition>> {
  return apiGet<Page<PurchaseRequisition>>("/api/v1/procurement/requisitions?limit=50", session);
}

export async function submitRequisition(
  session: ApiSession,
  requisitionId: string,
): Promise<PurchaseRequisition> {
  return apiPost<PurchaseRequisition>(
    `/api/v1/procurement/requisitions/${requisitionId}/submit`,
    session,
    {},
  );
}

export async function approveRequisition(
  session: ApiSession,
  requisitionId: string,
): Promise<PurchaseRequisition> {
  return apiPost<PurchaseRequisition>(
    `/api/v1/procurement/requisitions/${requisitionId}/approve`,
    session,
    {},
  );
}
