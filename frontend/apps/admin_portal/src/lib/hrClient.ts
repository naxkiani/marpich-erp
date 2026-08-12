import { apiGet, apiPost, getStoredSession, type AuthSession } from "@marpich/auth-provider";

export type ApiSession = AuthSession;

export type HrEmployee = {
  id: string;
  email: string;
  full_name: string;
  job_title: string;
  department: string;
  employee_number: string;
  status: string;
  hired_at?: string;
  terminated_at?: string | null;
};

export type Page<T> = { items: T[]; total: number; limit: number; offset: number };

export function loadHrSession(): ApiSession | null {
  return getStoredSession();
}

export async function fetchEmployees(session: ApiSession): Promise<Page<HrEmployee>> {
  return apiGet<Page<HrEmployee>>("/api/v1/human-resources/employees?limit=50", session);
}

export async function hireEmployee(
  session: ApiSession,
  body: {
    email: string;
    full_name: string;
    job_title?: string;
    department?: string;
    employee_number?: string;
  },
): Promise<HrEmployee> {
  return apiPost<HrEmployee>("/api/v1/human-resources/employees", session, body);
}

export async function terminateEmployee(
  session: ApiSession,
  employeeId: string,
  reason?: string,
): Promise<HrEmployee> {
  return apiPost<HrEmployee>(
    `/api/v1/human-resources/employees/${employeeId}/terminate`,
    session,
    { reason: reason ?? "" },
  );
}
