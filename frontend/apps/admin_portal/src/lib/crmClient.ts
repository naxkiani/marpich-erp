import { apiGet, apiPost, getStoredSession, type AuthSession } from "@marpich/auth-provider";

export type ApiSession = AuthSession;

export type CrmContact = {
  id: string;
  email: string;
  full_name: string;
  company?: string | null;
  phone?: string | null;
  status: string;
};

export type CrmOpportunity = {
  id: string;
  contact_id: string;
  title: string;
  amount: string;
  currency: string;
  stage: string;
  closed_at?: string | null;
};

export type Page<T> = { items: T[]; total: number; limit: number; offset: number };

export function loadCrmSession(): ApiSession | null {
  return getStoredSession();
}

export async function fetchCrmContacts(session: ApiSession): Promise<Page<CrmContact>> {
  return apiGet<Page<CrmContact>>("/api/v1/crm/contacts?limit=50", session);
}

export async function createCrmContact(
  session: ApiSession,
  payload: { email: string; full_name: string; company?: string; phone?: string },
): Promise<CrmContact> {
  return apiPost<CrmContact>("/api/v1/crm/contacts", session, payload);
}

export async function fetchCrmOpportunities(session: ApiSession): Promise<Page<CrmOpportunity>> {
  return apiGet<Page<CrmOpportunity>>("/api/v1/crm/opportunities?limit=50", session);
}

export async function createCrmOpportunity(
  session: ApiSession,
  payload: { contact_id: string; title: string; amount: string; currency?: string },
): Promise<CrmOpportunity> {
  return apiPost<CrmOpportunity>("/api/v1/crm/opportunities", session, payload);
}

export async function winCrmOpportunity(session: ApiSession, opportunityId: string): Promise<CrmOpportunity> {
  return apiPost<CrmOpportunity>(`/api/v1/crm/opportunities/${opportunityId}/win`, session, {});
}

export async function loseCrmOpportunity(
  session: ApiSession,
  opportunityId: string,
  reason?: string,
): Promise<CrmOpportunity> {
  return apiPost<CrmOpportunity>(`/api/v1/crm/opportunities/${opportunityId}/lose`, session, {
    reason: reason ?? null,
  });
}
