import { apiGet, apiPost, getStoredSession, type AuthSession } from "@marpich/auth-provider";

export type ApiSession = AuthSession;

export type PayrollEmployee = {
  id: string;
  hr_employee_id: string;
  email: string;
  full_name: string;
  job_title: string;
  department: string;
  status: string;
  base_salary: string;
  currency: string;
};

export type PayrollRun = {
  id: string;
  period_label: string;
  status: string;
  employee_count: number;
  total_gross: string;
  total_net: string;
  currency: string;
  completed_at?: string | null;
};

export type Page<T> = { items: T[]; total: number; limit: number; offset: number };

export function loadPayrollSession(): ApiSession | null {
  return getStoredSession();
}

export async function fetchPayrollEmployees(
  session: ApiSession,
): Promise<Page<PayrollEmployee>> {
  return apiGet<Page<PayrollEmployee>>("/api/v1/payroll/employees?limit=50", session);
}

export async function fetchPayrollRuns(session: ApiSession): Promise<Page<PayrollRun>> {
  return apiGet<Page<PayrollRun>>("/api/v1/payroll/runs?limit=50", session);
}

export async function createPayrollRun(
  session: ApiSession,
  periodLabel: string,
): Promise<PayrollRun> {
  return apiPost<PayrollRun>("/api/v1/payroll/runs", session, { period_label: periodLabel });
}
