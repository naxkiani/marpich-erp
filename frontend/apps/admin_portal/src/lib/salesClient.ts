import { apiGet, apiPost, getStoredSession, type AuthSession } from "@marpich/auth-provider";

export type ApiSession = AuthSession;

export type SalesQuotation = {
  id: string;
  contact_id: string;
  opportunity_id?: string | null;
  title: string;
  amount: string;
  currency: string;
  status: string;
  sent_at?: string | null;
  accepted_at?: string | null;
};

export type SalesOrder = {
  id: string;
  contact_id: string;
  quotation_id?: string | null;
  opportunity_id?: string | null;
  title: string;
  amount: string;
  currency: string;
  status: string;
};

export type Page<T> = { items: T[]; total: number; limit: number; offset: number };

export function loadSalesSession(): ApiSession | null {
  return getStoredSession();
}

export async function fetchSalesQuotations(session: ApiSession): Promise<Page<SalesQuotation>> {
  return apiGet<Page<SalesQuotation>>("/api/v1/sales/quotations?limit=50", session);
}

export async function fetchSalesOrders(session: ApiSession): Promise<Page<SalesOrder>> {
  return apiGet<Page<SalesOrder>>("/api/v1/sales/orders?limit=50", session);
}

export async function createSalesQuotation(
  session: ApiSession,
  payload: {
    contact_id: string;
    title: string;
    amount: string;
    currency?: string;
    opportunity_id?: string;
  },
): Promise<SalesQuotation> {
  return apiPost<SalesQuotation>("/api/v1/sales/quotations", session, payload);
}

export async function sendSalesQuotation(
  session: ApiSession,
  quotationId: string,
): Promise<SalesQuotation> {
  return apiPost<SalesQuotation>(`/api/v1/sales/quotations/${quotationId}/send`, session, {});
}

export async function convertSalesQuotation(
  session: ApiSession,
  quotationId: string,
): Promise<{ order: SalesOrder; quotation: SalesQuotation }> {
  return apiPost<{ order: SalesOrder; quotation: SalesQuotation }>(
    `/api/v1/sales/quotations/${quotationId}/convert`,
    session,
    {},
  );
}
