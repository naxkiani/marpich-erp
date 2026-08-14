import { apiGet, apiPost, getStoredSession, type AuthSession } from "@marpich/auth-provider";

export type ApiSession = AuthSession;

export type TaxLiability = {
  id: string;
  payroll_run_id: string;
  period_label: string;
  taxable_base: string;
  tax_amount: string;
  currency: string;
  status: string;
};

export type TaxReturn = {
  id: string;
  period_label: string;
  status: string;
  liability_count: number;
  total_tax: string;
  currency: string;
  filed_at?: string | null;
};

export type Page<T> = { items: T[]; total: number; limit: number; offset: number };

export function loadTaxSession(): ApiSession | null {
  return getStoredSession();
}

export async function fetchTaxLiabilities(session: ApiSession): Promise<Page<TaxLiability>> {
  return apiGet<Page<TaxLiability>>("/api/v1/tax/liabilities?limit=50", session);
}

export async function fetchTaxReturns(session: ApiSession): Promise<Page<TaxReturn>> {
  return apiGet<Page<TaxReturn>>("/api/v1/tax/returns?limit=50", session);
}

export async function fileTaxReturn(
  session: ApiSession,
  periodLabel: string,
): Promise<TaxReturn> {
  return apiPost<TaxReturn>("/api/v1/tax/returns/file", session, {
    period_label: periodLabel,
  });
}
