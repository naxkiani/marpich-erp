import { apiGet, apiPost, getStoredSession, type AuthSession } from "@marpich/auth-provider";

export type ApiSession = AuthSession;

export type ArInvoice = {
  id: string;
  sales_order_id: string;
  contact_id: string;
  title: string;
  amount: string;
  currency: string;
  status: string;
  issued_at?: string | null;
  paid_at?: string | null;
};

export type Page<T> = { items: T[]; total: number; limit: number; offset: number };

export function loadAccountingSession(): ApiSession | null {
  return getStoredSession();
}

export async function fetchArInvoices(session: ApiSession): Promise<Page<ArInvoice>> {
  return apiGet<Page<ArInvoice>>("/api/v1/accounting/invoices?limit=50", session);
}

export async function issueArInvoice(session: ApiSession, invoiceId: string): Promise<ArInvoice> {
  return apiPost<ArInvoice>(`/api/v1/accounting/invoices/${invoiceId}/issue`, session, {});
}

export async function receiveArPayment(
  session: ApiSession,
  invoiceId: string,
): Promise<ArInvoice> {
  return apiPost<ArInvoice>(
    `/api/v1/accounting/invoices/${invoiceId}/receive-payment`,
    session,
    {},
  );
}
