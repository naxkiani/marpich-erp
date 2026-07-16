import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadTaxRuleSession,
  saveSession as saveTaxRuleSession,
} from "./clientAuth";

export type { ApiSession };

export const loginTaxRuleSession = createClientLogin("Tax Rule Admin");
export { loadTaxRuleSession, saveTaxRuleSession };
export const loginTaxCalcSession = loginTaxRuleSession;
export type BuilderCatalog = {
  scope_dimensions: string[];
  builder: Record<string, unknown>;
  condition_operators: string[];
  hardcoded_business_rules: boolean;
};

export type ConfigurableTaxRule = {
  id: string;
  rule_ref: string;
  name: string;
  tax_type: string;
  description: string;
  active_version: number | null;
  version_count: number;
};

export type TaxRuleVersion = {
  id: string;
  rule_id: string;
  version: number;
  status: string;
  effective_from: string;
  expires_at: string | null;
  priority: number;
  scope: Record<string, unknown>;
  conditions: Array<{ field: string; operator: string; value: unknown }>;
  rules: Array<{ outcome: string; parameters: Record<string, unknown> }>;
  exceptions: Array<{
    id?: string;
    name?: string;
    conditions: Array<{ field: string; operator: string; value: unknown }>;
    rules: Array<{ outcome: string; parameters: Record<string, unknown> }>;
  }>;
  approval_required: boolean;
};

export type RuleDetail = ConfigurableTaxRule & { versions: TaxRuleVersion[] };

export type EvaluateResult = {
  matched: boolean;
  rule_ref?: string;
  version?: number;
  priority?: number;
  outcome?: string;
  parameters: Record<string, unknown>;
  evaluation_trace?: unknown[];
  hardcoded_business_rules: boolean;
};

export type TestRunResult = {
  rule_ref: string;
  version: number;
  total: number;
  passed: number;
  failed: number;
  all_passed: boolean;
  results: Array<{
    name: string;
    passed: boolean;
    expected: Record<string, unknown>;
    actual: Record<string, unknown>;
  }>;
};



export function fetchBuilderCatalog(session: ApiSession) {
  return apiGet<BuilderCatalog>("/api/v1/tax/rule-engine/builder-catalog", session);
}

export function fetchTaxRules(session: ApiSession) {
  return apiGet<ConfigurableTaxRule[]>("/api/v1/tax/rule-engine/rules", session);
}

export function fetchTaxRuleDetail(session: ApiSession, ruleId: string) {
  return apiGet<RuleDetail>(`/api/v1/tax/rule-engine/rules/${ruleId}`, session);
}

export function createTaxRule(
  session: ApiSession,
  payload: {
    name: string;
    tax_type: string;
    priority: number;
    scope: Record<string, unknown>;
    conditions: unknown[];
    rules: unknown[];
    exceptions: unknown[];
    approval_required?: boolean;
  },
) {
  return apiPost<{ rule: ConfigurableTaxRule; version: TaxRuleVersion }>(
    "/api/v1/tax/rule-engine/rules",
    session,
    payload,
  );
}

export function activateTaxRuleVersion(session: ApiSession, ruleId: string, version: number) {
  return apiPost<TaxRuleVersion>(
    `/api/v1/tax/rule-engine/rules/${ruleId}/versions/${version}/activate`,
    session,
    {},
  );
}

export function simulateTaxRule(
  session: ApiSession,
  payload: { facts: Record<string, unknown>; rule_id?: string; version?: number },
) {
  return apiPost<EvaluateResult & { mode?: string }>(
    "/api/v1/tax/rule-engine/simulate",
    session,
    payload,
  );
}

export function runTaxRuleTests(
  session: ApiSession,
  ruleId: string,
  version: number,
  testCases: Array<{ name: string; facts: Record<string, unknown>; expect: Record<string, unknown> }>,
) {
  return apiPost<TestRunResult>(
    `/api/v1/tax/rule-engine/rules/${ruleId}/versions/${version}/test`,
    session,
    { test_cases: testCases },
  );
}

export function evaluateTaxRules(
  session: ApiSession,
  payload: { facts: Record<string, unknown>; tax_type?: string },
) {
  return apiPost<EvaluateResult>("/api/v1/tax/rule-engine/evaluate", session, payload);
}

export type CalculationResult = {
  tax_type: string;
  calculation_mode: string;
  base_amount: number;
  tax_amount: number;
  total_amount: number;
  effective_rate: number;
  audit_ref?: string;
  explanation: { summary: string; narrative: string[]; steps: unknown[] };
  validation: { status: string; confidence: number; findings: unknown[] };
  ai_validation: { insights: string[]; answer?: string };
  hardcoded_business_rules: boolean;
};


export function computeTax(
  session: ApiSession,
  payload: {
    amount: number;
    tax_type: string;
    jurisdiction: string;
    calculation_mode?: string;
    components?: unknown[];
  },
) {
  return apiPost<CalculationResult>("/api/v1/tax/calculation/compute", session, payload);
}

export function explainTax(session: ApiSession, payload: Record<string, unknown>) {
  return apiPost<{ explanation: CalculationResult["explanation"] }>(
    "/api/v1/tax/calculation/explain",
    session,
    payload,
  );
}

export function validateTax(session: ApiSession, payload: Record<string, unknown>) {
  return apiPost<{ validation: CalculationResult["validation"]; ai_validation: CalculationResult["ai_validation"] }>(
    "/api/v1/tax/calculation/validate",
    session,
    payload,
  );
}

export function fetchCalculationAudit(session: ApiSession) {
  return apiGet<Array<{ audit_ref: string; tax_type: string; tax_amount: number; created_at: string }>>(
    "/api/v1/tax/calculation/audit",
    session,
  );
}

export function fetchCalculationCatalog(session: ApiSession) {
  return apiGet<{ tax_types: unknown[]; calculation_modes: unknown[] }>(
    "/api/v1/tax/calculation/catalog",
    session,
  );
}

// --- Withholding Tax Platform ---

export type WithholdingCategory = {
  category: string;
  label: string;
  policy_key: string;
};

export type WithholdingTransaction = {
  transaction_ref: string;
  category: string;
  payee_ref: string;
  payee_name: string;
  base_amount: number;
  withholding_amount: number;
  currency: string;
  jurisdiction: string;
  period: string;
  status: string;
  policy_key: string;
  audit_ref?: string;
  created_at: string;
};

export type WithholdingDashboard = {
  policy_driven: boolean;
  hardcoded_business_rules: boolean;
  totals: {
    transactions: number;
    pending_approvals: number;
    certificates: number;
    credits: number;
    settlements: number;
    refunds: number;
  };
  by_category: Array<{ category: string; count: number; amount: number }>;
};

export type WithholdingReport = {
  report_type: string;
  period: string;
  category: string;
  transaction_count: number;
  total_base: number;
  total_withheld: number;
  rows: Array<Record<string, unknown>>;
};

export function fetchWithholdingCatalog(session: ApiSession) {
  return apiGet<WithholdingCategory[]>("/api/v1/tax/withholding-platform/catalog", session);
}

export function fetchWithholdingDashboard(session: ApiSession) {
  return apiGet<WithholdingDashboard>("/api/v1/tax/withholding-platform/dashboard", session);
}

export function fetchWithholdingTransactions(session: ApiSession) {
  return apiGet<WithholdingTransaction[]>("/api/v1/tax/withholding-platform/transactions", session);
}

export function createWithholdingTransaction(
  session: ApiSession,
  payload: {
    category: string;
    payee_ref: string;
    payee_name?: string;
    base_amount: number;
    currency?: string;
    jurisdiction: string;
    period: string;
    source_ref?: string;
    auto_post_gl?: boolean;
  },
) {
  return apiPost<{ transaction: WithholdingTransaction; approval?: unknown; gl_post?: unknown }>(
    "/api/v1/tax/withholding-platform/transactions",
    session,
    payload,
  );
}

export function fetchWithholdingApprovals(session: ApiSession) {
  return apiGet<Array<{ approval_ref: string; transaction_ref: string; status: string }>>(
    "/api/v1/tax/withholding-platform/approvals",
    session,
  );
}

export function approveWithholding(
  session: ApiSession,
  approvalRef: string,
  payload?: { approver_id?: string; auto_post_gl?: boolean },
) {
  return apiPost<{ transaction: WithholdingTransaction }>(
    `/api/v1/tax/withholding-platform/approvals/${approvalRef}/approve`,
    session,
    payload ?? {},
  );
}

export function issueWithholdingCertificate(session: ApiSession, transactionRef: string) {
  return apiPost<{ certificate: unknown; tax_credit: unknown }>(
    `/api/v1/tax/withholding-platform/transactions/${transactionRef}/certificate`,
    session,
    {},
  );
}

export function fetchWithholdingCertificates(session: ApiSession) {
  return apiGet<Array<Record<string, unknown>>>("/api/v1/tax/withholding-platform/certificates", session);
}

export function fetchWithholdingCredits(session: ApiSession) {
  return apiGet<Array<Record<string, unknown>>>("/api/v1/tax/withholding-platform/credits", session);
}

export function createWithholdingSettlement(
  session: ApiSession,
  payload: { period: string; currency?: string },
) {
  return apiPost<{ settlement: Record<string, unknown> }>(
    "/api/v1/tax/withholding-platform/settlements",
    session,
    payload,
  );
}

export function postWithholdingSettlement(session: ApiSession, settlementRef: string) {
  return apiPost<{ settlement: Record<string, unknown> }>(
    `/api/v1/tax/withholding-platform/settlements/${settlementRef}/post`,
    session,
    {},
  );
}

export function fetchWithholdingSettlements(session: ApiSession) {
  return apiGet<Array<Record<string, unknown>>>("/api/v1/tax/withholding-platform/settlements", session);
}

export function requestWithholdingRefund(
  session: ApiSession,
  payload: {
    payee_ref: string;
    refund_amount: number;
    currency?: string;
    reason?: string;
    source_transaction_ref?: string;
  },
) {
  return apiPost<{ refund: Record<string, unknown> }>("/api/v1/tax/withholding-platform/refunds", session, payload);
}

export function approveWithholdingRefund(
  session: ApiSession,
  refundRef: string,
  payload?: { approver_id?: string },
) {
  return apiPost<{ refund: Record<string, unknown> }>(
    `/api/v1/tax/withholding-platform/refunds/${refundRef}/approve`,
    session,
    payload ?? {},
  );
}

export function fetchWithholdingRefunds(session: ApiSession) {
  return apiGet<Array<Record<string, unknown>>>("/api/v1/tax/withholding-platform/refunds", session);
}

export function fetchWithholdingReport(
  session: ApiSession,
  params?: { period?: string; category?: string },
) {
  const qs = new URLSearchParams();
  if (params?.period) qs.set("period", params.period);
  if (params?.category) qs.set("category", params.category);
  const suffix = qs.toString() ? `?${qs.toString()}` : "";
  return apiGet<WithholdingReport>(`/api/v1/tax/withholding-platform/reports${suffix}`, session);
}

// --- Payroll Tax Engine ---

export type PayrollTaxCategory = {
  category: string;
  label: string;
  policy_key: string;
  base_field: string;
};

export type PayrollTaxRun = {
  run_ref: string;
  employee_ref: string;
  employee_name: string;
  period: string;
  gross_pay: number;
  overtime_amount: number;
  bonus_amount: number;
  termination_amount: number;
  total_tax: number;
  status: string;
  created_at: string;
};

export type PayrollTaxDashboard = {
  policy_driven: boolean;
  hardcoded_business_rules: boolean;
  summary: {
    runs: number;
    line_items: number;
    total_tax: number;
    posted_runs: number;
    audit_entries: number;
  };
  by_category: Record<string, number>;
};

export type PayrollTaxReport = {
  report_type: string;
  period: string;
  category_filter: string;
  employee_filter: string;
  run_count: number;
  total_tax: number;
  by_category: Record<string, number>;
};

export function fetchPayrollTaxCatalog(session: ApiSession) {
  return apiGet<PayrollTaxCategory[]>("/api/v1/tax/payroll-tax/catalog", session);
}

export function fetchPayrollTaxDashboard(session: ApiSession) {
  return apiGet<PayrollTaxDashboard>("/api/v1/tax/payroll-tax/dashboard", session);
}

export function fetchPayrollTaxRuns(session: ApiSession) {
  return apiGet<PayrollTaxRun[]>("/api/v1/tax/payroll-tax/runs", session);
}

export function calculatePayrollTaxRun(
  session: ApiSession,
  payload: {
    employee_ref: string;
    employee_name?: string;
    gross_pay: number;
    period: string;
    jurisdiction?: string;
    overtime_amount?: number;
    bonus_amount?: number;
    termination_amount?: number;
    auto_post_gl?: boolean;
  },
) {
  return apiPost<{ run: PayrollTaxRun; line_items: Array<Record<string, unknown>> }>(
    "/api/v1/tax/payroll-tax/runs",
    session,
    payload,
  );
}

export function postPayrollTaxRun(session: ApiSession, runRef: string) {
  return apiPost<{ run: PayrollTaxRun; posting: Record<string, unknown> }>(
    `/api/v1/tax/payroll-tax/runs/${runRef}/post`,
    session,
    {},
  );
}

export function fetchPayrollTaxAudit(session: ApiSession) {
  return apiGet<Array<{ audit_ref: string; run_ref: string; action: string; created_at: string }>>(
    "/api/v1/tax/payroll-tax/audit",
    session,
  );
}

export function fetchPayrollTaxReport(
  session: ApiSession,
  params?: { period?: string; category?: string; employee_ref?: string },
) {
  const qs = new URLSearchParams();
  if (params?.period) qs.set("period", params.period);
  if (params?.category) qs.set("category", params.category);
  if (params?.employee_ref) qs.set("employee_ref", params.employee_ref);
  const suffix = qs.toString() ? `?${qs.toString()}` : "";
  return apiGet<PayrollTaxReport>(`/api/v1/tax/payroll-tax/reports${suffix}`, session);
}

// --- e-Invoice Platform ---

export type DigitalInvoice = {
  invoice_ref: string;
  invoice_number: string;
  version: number;
  buyer_name: string;
  seller_name: string;
  total_amount: number;
  status: string;
  government_format: string;
  qr_code: string;
  digital_signature: string;
  created_at: string;
};

export type EInvoiceDashboard = {
  policy_driven: boolean;
  hardcoded_business_rules: boolean;
  summary: {
    invoices: number;
    submissions: number;
    archives: number;
    issued: number;
    submitted: number;
  };
  capabilities: string[];
};

export function fetchEInvoiceCatalog(session: ApiSession) {
  return apiGet<{ capabilities: Array<{ capability: string; label: string }>; government_formats: string[] }>(
    "/api/v1/tax/einvoice-platform/catalog",
    session,
  );
}

export function fetchEInvoiceDashboard(session: ApiSession) {
  return apiGet<EInvoiceDashboard>("/api/v1/tax/einvoice-platform/dashboard", session);
}

export function fetchEInvoices(session: ApiSession) {
  return apiGet<DigitalInvoice[]>("/api/v1/tax/einvoice-platform/invoices", session);
}

export function createDigitalInvoice(
  session: ApiSession,
  payload: {
    buyer_ref: string;
    buyer_name?: string;
    seller_ref: string;
    seller_name?: string;
    subtotal: number;
    tax_amount: number;
    jurisdiction?: string;
    line_items?: Array<Record<string, unknown>>;
  },
) {
  return apiPost<{ invoice: DigitalInvoice }>("/api/v1/tax/einvoice-platform/invoices", session, payload);
}

export function validateEInvoice(session: ApiSession, invoiceRef: string) {
  return apiPost<{ invoice: DigitalInvoice; validation: Record<string, unknown> }>(
    `/api/v1/tax/einvoice-platform/invoices/${invoiceRef}/validate`,
    session,
    {},
  );
}

export function signEInvoice(session: ApiSession, invoiceRef: string, signerId: string) {
  return apiPost<{ invoice: DigitalInvoice }>(
    `/api/v1/tax/einvoice-platform/invoices/${invoiceRef}/sign`,
    session,
    { signer_id: signerId },
  );
}

export function issueEInvoice(session: ApiSession, invoiceRef: string) {
  return apiPost<{ invoice: DigitalInvoice }>(
    `/api/v1/tax/einvoice-platform/invoices/${invoiceRef}/issue`,
    session,
    {},
  );
}

export function submitEInvoice(session: ApiSession, invoiceRef: string) {
  return apiPost<{ invoice: DigitalInvoice; submission: Record<string, unknown> }>(
    `/api/v1/tax/einvoice-platform/invoices/${invoiceRef}/submit`,
    session,
    {},
  );
}

export function verifyEInvoice(session: ApiSession, invoiceRef: string) {
  return apiGet<{ verification: { verified: boolean } }>(
    `/api/v1/tax/einvoice-platform/invoices/${invoiceRef}/verify`,
    session,
  );
}

export function fetchEInvoiceReport(session: ApiSession, params?: { status?: string }) {
  const qs = new URLSearchParams();
  if (params?.status) qs.set("status", params.status);
  const suffix = qs.toString() ? `?${qs.toString()}` : "";
  return apiGet<{ report_type: string; invoice_count: number; total_amount: number }>(
    `/api/v1/tax/einvoice-platform/reports${suffix}`,
    session,
  );
}

// --- Government Tax Integration ---

export type GovTaxRequest = {
  request_ref: string;
  operation_type: string;
  jurisdiction: string;
  status: string;
  connector_id: string;
  attempt_count: number;
  acknowledgement_ref: string;
  created_at: string;
};

export type GovTaxDashboard = {
  policy_driven: boolean;
  hardcoded_business_rules: boolean;
  country_specific_integrations_forbidden: boolean;
  summary: {
    requests: number;
    acknowledgements: number;
    failed: number;
    retry_scheduled: number;
    audit_entries: number;
  };
};

export function fetchGovTaxCatalog(session: ApiSession) {
  return apiGet<{ capabilities: Array<{ capability: string; label: string }>; country_specific_integrations_forbidden: boolean }>(
    "/api/v1/tax/gov-integration/catalog",
    session,
  );
}

export function fetchGovTaxDashboard(session: ApiSession) {
  return apiGet<GovTaxDashboard>("/api/v1/tax/gov-integration/dashboard", session);
}

export function fetchGovTaxRequests(session: ApiSession) {
  return apiGet<GovTaxRequest[]>("/api/v1/tax/gov-integration/requests", session);
}

export function fetchGovTaxConnector(session: ApiSession, operationType: string, jurisdiction: string) {
  return apiGet<{ connector: Record<string, unknown>; policy_driven: boolean }>(
    `/api/v1/tax/gov-integration/connectors/${operationType}?jurisdiction=${encodeURIComponent(jurisdiction)}`,
    session,
  );
}

export function submitGovTaxRegistration(
  session: ApiSession,
  payload: { jurisdiction?: string; payload: Record<string, unknown>; simulate_failure?: boolean },
) {
  return apiPost<{ request: GovTaxRequest; acknowledgement?: Record<string, unknown> }>(
    "/api/v1/tax/gov-integration/registration",
    session,
    payload,
  );
}

export function submitGovTaxReturn(
  session: ApiSession,
  payload: { jurisdiction?: string; payload: Record<string, unknown> },
) {
  return apiPost<{ request: GovTaxRequest }>("/api/v1/tax/gov-integration/returns", session, payload);
}

export function submitGovTaxPayment(
  session: ApiSession,
  payload: { jurisdiction?: string; payload: Record<string, unknown> },
) {
  return apiPost<{ request: GovTaxRequest }>("/api/v1/tax/gov-integration/payments", session, payload);
}

export function retryGovTaxRequest(session: ApiSession, requestRef: string) {
  return apiPost<{ request: GovTaxRequest }>(
    `/api/v1/tax/gov-integration/requests/${requestRef}/retry`,
    session,
    {},
  );
}

export function checkGovTaxCompliance(session: ApiSession, jurisdiction: string) {
  return apiPost<{ compliance: { overall_compliant: boolean; registration_status: string } }>(
    "/api/v1/tax/gov-integration/compliance/check",
    session,
    { jurisdiction },
  );
}

export function fetchGovTaxAudit(session: ApiSession) {
  return apiGet<Array<{ audit_ref: string; request_ref: string; action: string; created_at: string }>>(
    "/api/v1/tax/gov-integration/audit",
    session,
  );
}

export function fetchGovTaxReport(session: ApiSession) {
  return apiGet<{ report_type: string; request_count: number; completed: number; failed: number }>(
    "/api/v1/tax/gov-integration/reports",
    session,
  );
}

// --- Enterprise Tax Reporting ---

export type TaxReportRecord = {
  report_ref: string;
  report_type: string;
  period: string;
  jurisdiction: string;
  summary: Record<string, unknown>;
  created_at: string;
};

export type TaxReportingDashboard = {
  policy_driven: boolean;
  hardcoded_business_rules: boolean;
  summary: {
    reports_generated: number;
    exports_created: number;
    report_types_available: number;
    export_formats: string[];
  };
  capabilities: string[];
  source_data: Record<string, number>;
};

export function fetchTaxReportingCatalog(session: ApiSession) {
  return apiGet<{ reports: Array<{ report_type: string; label: string }>; export_formats: string[] }>(
    "/api/v1/tax/reporting/catalog",
    session,
  );
}

export function fetchTaxReportingDashboard(session: ApiSession) {
  return apiGet<TaxReportingDashboard>("/api/v1/tax/reporting/dashboard", session);
}

export function fetchTaxReports(session: ApiSession) {
  return apiGet<TaxReportRecord[]>("/api/v1/tax/reporting/reports", session);
}

export function generateTaxReport(
  session: ApiSession,
  payload: {
    report_type: string;
    period?: string;
    jurisdiction?: string;
    organization_id?: string;
    branch_id?: string;
  },
) {
  return apiPost<{ report: TaxReportRecord }>("/api/v1/tax/reporting/reports", session, payload);
}

export function exportTaxReport(session: ApiSession, reportRef: string, format: string) {
  return apiPost<{ export: { export_ref: string; format: string; content: unknown } }>(
    `/api/v1/tax/reporting/reports/${reportRef}/export`,
    session,
    { format },
  );
}

export type TaxAuditEntry = {
  entry_ref: string;
  event_type: string;
  subject_ref: string;
  user_id: string;
  timestamp: string;
  policy_version: number | null;
  policy_key: string;
  approval_ref: string;
  digital_signature: string;
  entry_hash: string;
  previous_hash: string;
  immutable: boolean;
};

export type TaxComplianceReport = {
  report_ref: string;
  period: string;
  jurisdiction: string;
  compliant: boolean;
  findings: Array<{ severity: string; code: string; message: string }>;
  audit_entry_count: number;
  summary: Record<string, unknown>;
  created_at: string;
};

export type TaxAuditDashboard = {
  policy_driven: boolean;
  hardcoded_business_rules: boolean;
  immutable_audit: boolean;
  summary: {
    total_entries: number;
    compliance_reports: number;
    chain_valid: boolean;
    event_types: number;
    unique_users: number;
  };
  by_event_type: Record<string, number>;
  tracks: string[];
};

export function fetchTaxAuditCatalog(session: ApiSession) {
  return apiGet<{
    tracks: Array<{ track: string; label: string }>;
    event_types: string[];
    immutable_audit: boolean;
  }>("/api/v1/tax/audit-platform/catalog", session);
}

export function fetchTaxAuditDashboard(session: ApiSession) {
  return apiGet<TaxAuditDashboard>("/api/v1/tax/audit-platform/dashboard", session);
}

export function fetchTaxAuditHistory(session: ApiSession, eventType?: string) {
  const qs = eventType ? `?event_type=${encodeURIComponent(eventType)}` : "";
  return apiGet<TaxAuditEntry[]>(`/api/v1/tax/audit-platform/history${qs}`, session);
}

export function verifyTaxAuditChain(session: ApiSession) {
  return apiGet<{ valid: boolean; entries_checked: number; broken_at: string | null }>(
    "/api/v1/tax/audit-platform/verify",
    session,
  );
}

export function recordTaxAuditEvent(
  session: ApiSession,
  payload: {
    event_type: string;
    subject_ref: string;
    user_id?: string;
    payload?: Record<string, unknown>;
    policy_key?: string;
    policy_version?: number;
    approval_ref?: string;
    digital_signature?: string;
  },
) {
  return apiPost<{ entry: TaxAuditEntry }>("/api/v1/tax/audit-platform/events", session, payload);
}

export function generateTaxComplianceReport(
  session: ApiSession,
  payload: { period?: string; jurisdiction?: string },
) {
  return apiPost<{ report: TaxComplianceReport }>("/api/v1/tax/audit-platform/compliance", session, payload);
}

export function fetchTaxComplianceReports(session: ApiSession) {
  return apiGet<TaxComplianceReport[]>("/api/v1/tax/audit-platform/compliance", session);
}

export function syncTaxAuditPlatforms(session: ApiSession, userId = "system") {
  return apiPost<{ synced_entries: number; correlation_id: string }>(
    "/api/v1/tax/audit-platform/sync",
    session,
    { user_id: userId },
  );
}

export type TaxWorkflowDefinition = {
  definition_ref: string;
  name: string;
  workflow_type: string;
  approval_mode: string;
  steps: Array<{ step_id: string; level: number; role: string; order: number }>;
  sla_hours: number;
  is_active: boolean;
};

export type TaxWorkflowInstance = {
  instance_ref: string;
  workflow_type: string;
  status: string;
  title: string;
  subject_ref: string;
  amount: number;
  currency: string;
  steps: Array<Record<string, unknown>>;
  digital_signatures: Array<Record<string, unknown>>;
  delegations: Array<Record<string, unknown>>;
  sla_breached: boolean;
  created_at: string;
};

export type TaxWorkflowDesigner = {
  definition_count: number;
  by_workflow_type: Record<string, TaxWorkflowDefinition[]>;
  approval_modes: string[];
  workflow_types: string[];
  definitions: TaxWorkflowDefinition[];
  transitions: Record<string, string[]>;
};

export type TaxWorkflowDashboard = {
  policy_driven: boolean;
  hardcoded_business_rules: boolean;
  summary: {
    total_instances: number;
    pending_approval: number;
    escalated: number;
    sla_breached: number;
    active_definitions: number;
    audit_entries: number;
  };
  by_status: Record<string, number>;
  by_workflow_type: Record<string, number>;
};

export function fetchTaxWorkflowCatalog(session: ApiSession) {
  return apiGet<{ capabilities: Array<{ capability: string; label: string }>; workflow_types: string[] }>(
    "/api/v1/tax/workflow-platform/catalog",
    session,
  );
}

export function fetchTaxWorkflowDesigner(session: ApiSession) {
  return apiGet<TaxWorkflowDesigner>("/api/v1/tax/workflow-platform/designer", session);
}

export function fetchTaxWorkflowDashboard(session: ApiSession) {
  return apiGet<TaxWorkflowDashboard>("/api/v1/tax/workflow-platform/dashboard", session);
}

export function fetchTaxWorkflowInstances(session: ApiSession) {
  return apiGet<TaxWorkflowInstance[]>("/api/v1/tax/workflow-platform/instances", session);
}

export function createTaxWorkflowDefinition(
  session: ApiSession,
  payload: {
    name: string;
    workflow_type: string;
    approval_mode?: string;
    steps: Array<{ step_id: string; level: number; role: string; order: number }>;
    sla_hours?: number;
    description?: string;
  },
) {
  return apiPost<TaxWorkflowDefinition>("/api/v1/tax/workflow-platform/definitions", session, payload);
}

export function createTaxWorkflowInstance(
  session: ApiSession,
  payload: {
    workflow_type: string;
    amount?: number;
    currency?: string;
    subject_ref: string;
    subject_type?: string;
    title: string;
    description?: string;
    definition_ref?: string;
  },
) {
  return apiPost<{ instance: TaxWorkflowInstance }>("/api/v1/tax/workflow-platform/instances", session, payload);
}

export function submitTaxWorkflowInstance(session: ApiSession, instanceRef: string) {
  return apiPost<{ instance: TaxWorkflowInstance }>(
    `/api/v1/tax/workflow-platform/instances/${instanceRef}/submit`,
    session,
    {},
  );
}

export function approveTaxWorkflowStep(
  session: ApiSession,
  instanceRef: string,
  payload: { step_id: string; comment?: string; with_signature?: boolean },
) {
  return apiPost<{ instance: TaxWorkflowInstance }>(
    `/api/v1/tax/workflow-platform/instances/${instanceRef}/approve`,
    session,
    payload,
  );
}

export function executeTaxWorkflowInstance(session: ApiSession, instanceRef: string) {
  return apiPost<{ instance: TaxWorkflowInstance }>(
    `/api/v1/tax/workflow-platform/instances/${instanceRef}/execute`,
    session,
    {},
  );
}

export type TaxSecurityDashboard = {
  policy_driven: boolean;
  hardcoded_business_rules: boolean;
  summary: {
    active_policies: number;
    access_rules: number;
    approval_matrix_entries: number;
    pending_operations: number;
    active_locks: number;
    emergency_locked: boolean;
    audit_entries: number;
    audit_chain_valid: boolean;
  };
  capabilities: string[];
  sensitive_operations: string[];
};

export type TaxSecurityOperation = {
  operation_ref: string;
  operation_type: string;
  status: string;
  subject_ref: string;
  amount: number;
  maker_id: string;
  has_encrypted_payload: boolean;
  digital_signatures: Array<Record<string, unknown>>;
};

export function fetchTaxSecurityCatalog(session: ApiSession) {
  return apiGet<{ capabilities: Array<{ capability: string; label: string }>; sensitive_operations: string[] }>(
    "/api/v1/tax/security-platform/catalog",
    session,
  );
}

export function fetchTaxSecurityDashboard(session: ApiSession) {
  return apiGet<TaxSecurityDashboard>("/api/v1/tax/security-platform/dashboard", session);
}

export function seedTaxSecurityDefaults(session: ApiSession) {
  return apiPost<{ seeded: boolean }>("/api/v1/tax/security-platform/seed", session, {});
}

export function evaluateTaxSecurityAccess(
  session: ApiSession,
  payload: {
    operation_type: string;
    maker_id: string;
    roles?: string[];
    attributes?: Record<string, unknown>;
    amount?: number;
  },
) {
  return apiPost<{ allowed: boolean; reason?: string; checks?: Record<string, unknown> }>(
    "/api/v1/tax/security-platform/evaluate",
    session,
    payload,
  );
}

export function fetchTaxSecurityOperations(session: ApiSession) {
  return apiGet<TaxSecurityOperation[]>("/api/v1/tax/security-platform/operations", session);
}

export function createTaxSecurityOperation(
  session: ApiSession,
  payload: {
    operation_type: string;
    subject_ref: string;
    amount?: number;
    sensitive_payload?: Record<string, unknown>;
  },
) {
  return apiPost<{ operation: TaxSecurityOperation }>("/api/v1/tax/security-platform/operations", session, payload);
}

export function submitTaxSecurityOperation(session: ApiSession, operationRef: string) {
  return apiPost<{ operation: TaxSecurityOperation }>(
    `/api/v1/tax/security-platform/operations/${operationRef}/submit`,
    session,
    {},
  );
}

export function approveTaxSecurityOperation(session: ApiSession, operationRef: string) {
  return apiPost<{ operation: TaxSecurityOperation }>(
    `/api/v1/tax/security-platform/operations/${operationRef}/approve`,
    session,
    {},
  );
}

export function activateTaxEmergencyLock(session: ApiSession, reason: string) {
  return apiPost<{ lock: { lock_ref: string; is_active: boolean } }>(
    "/api/v1/tax/security-platform/emergency-lock",
    session,
    { reason },
  );
}

export function fetchTaxSecurityAudit(session: ApiSession) {
  return apiGet<Array<{ audit_ref: string; action: string; actor_id: string; immutable: boolean }>>(
    "/api/v1/tax/security-platform/audit",
    session,
  );
}

export type TaxAIInsight = {
  title: string;
  recommendation?: string;
  explanation: string;
  evidence: Array<Record<string, unknown>>;
  policy_references: Array<Record<string, unknown>>;
  data_sources: string[];
  confidence?: number;
  explainable: boolean;
  autonomous_execution: boolean;
};

export type TaxAICatalog = {
  capabilities: Array<{ capability: string; label: string; explainable?: boolean }>;
  policy_keys: string[];
  explainable: boolean;
  autonomous_execution: boolean;
};

export type TaxAIExecutiveDashboard = {
  summary: Record<string, unknown>;
  recommendations: TaxAIInsight[];
  compliance: Record<string, unknown>;
  risks: Record<string, unknown>;
  explainable: boolean;
  autonomous_execution: boolean;
};

export function fetchTaxAICatalog(session: ApiSession) {
  return apiGet<TaxAICatalog>("/api/v1/tax/ai-assistant-platform/catalog", session);
}

export function fetchTaxAIDashboard(session: ApiSession) {
  return apiGet<Record<string, unknown>>("/api/v1/tax/ai-assistant-platform/dashboard", session);
}

export function fetchTaxAIExecutiveDashboard(session: ApiSession) {
  return apiGet<TaxAIExecutiveDashboard>("/api/v1/tax/ai-assistant-platform/executive-dashboard", session);
}

export function fetchTaxAIRecommendations(session: ApiSession) {
  return apiGet<{ recommendations: TaxAIInsight[] }>("/api/v1/tax/ai-assistant-platform/recommendations", session);
}

export function fetchTaxAICompliance(session: ApiSession) {
  return apiGet<Record<string, unknown>>("/api/v1/tax/ai-assistant-platform/compliance", session);
}

export function fetchTaxAIRisks(session: ApiSession) {
  return apiGet<Record<string, unknown>>("/api/v1/tax/ai-assistant-platform/risks", session);
}

export function fetchTaxAIAnomalies(session: ApiSession) {
  return apiGet<Record<string, unknown>>("/api/v1/tax/ai-assistant-platform/anomalies", session);
}

export function fetchTaxAIForecast(session: ApiSession) {
  return apiGet<Record<string, unknown>>("/api/v1/tax/ai-assistant-platform/forecast", session);
}

export function fetchTaxAIOptimization(session: ApiSession) {
  return apiGet<{ suggestions: TaxAIInsight[] }>("/api/v1/tax/ai-assistant-platform/optimization", session);
}

export function fetchTaxAIInsights(session: ApiSession, capability = "") {
  const q = capability ? `?capability=${encodeURIComponent(capability)}` : "";
  return apiGet<{ insights: Array<Record<string, unknown>> }>(
    `/api/v1/tax/ai-assistant-platform/insights${q}`,
    session,
  );
}

export function runTaxAIComplianceAssistant(
  session: ApiSession,
  payload: { period: string; provided: string[] },
) {
  return apiPost<Record<string, unknown>>("/api/v1/tax/ai-assistant-platform/compliance-assistant", session, payload);
}

export function checkTaxAIMissingDocuments(
  session: ApiSession,
  payload: { period: string; provided: string[] },
) {
  return apiPost<Record<string, unknown>>("/api/v1/tax/ai-assistant-platform/missing-documents", session, payload);
}

export function explainTaxAIPolicy(
  session: ApiSession,
  payload: { policy_key: string; facts?: Record<string, unknown> },
) {
  return apiPost<Record<string, unknown>>("/api/v1/tax/ai-assistant-platform/explain-policy", session, payload);
}

export function chatTaxAIAssistant(
  session: ApiSession,
  payload: { question: string; session_ref?: string },
) {
  return apiPost<Record<string, unknown>>("/api/v1/tax/ai-assistant-platform/chat", session, payload);
}

export function runTaxAIDocumentOCR(
  session: ApiSession,
  payload: { document_type: string; raw_text: string },
) {
  return apiPost<Record<string, unknown>>("/api/v1/tax/ai-assistant-platform/ocr", session, payload);
}

export type TaxComplianceDashboard = {
  tenant_id: string;
  summary: Record<string, number>;
  packages: Array<Record<string, unknown>>;
  recent_alerts: Array<Record<string, unknown>>;
  upcoming_deadlines: Array<Record<string, unknown>>;
  hardcoded_regulations: boolean;
  policy_driven: boolean;
};

export function fetchTaxComplianceCatalog(session: ApiSession) {
  return apiGet<{
    capabilities: Array<{ capability: string; label: string }>;
    available_packages: Array<Record<string, unknown>>;
    hardcoded_regulations: boolean;
    plugin_installable: boolean;
  }>("/api/v1/tax/compliance-platform/catalog", session);
}

export function fetchTaxComplianceDashboard(session: ApiSession) {
  return apiGet<TaxComplianceDashboard>("/api/v1/tax/compliance-platform/dashboard", session);
}

export function seedTaxComplianceDefaults(session: ApiSession) {
  return apiPost<Record<string, unknown>>("/api/v1/tax/compliance-platform/seed", session, {});
}

export function installTaxCompliancePackage(
  session: ApiSession,
  packageRef: string,
  manifest: Record<string, unknown>,
) {
  return apiPost<Record<string, unknown>>(
    `/api/v1/tax/compliance-platform/packages/${packageRef}/install`,
    session,
    { manifest },
  );
}

export function fetchTaxCompliancePackages(session: ApiSession) {
  return apiGet<Array<Record<string, unknown>>>("/api/v1/tax/compliance-platform/packages", session);
}

export function fetchTaxComplianceRegulations(session: ApiSession, packageRef = "") {
  const q = packageRef ? `?package_ref=${encodeURIComponent(packageRef)}` : "";
  return apiGet<Array<Record<string, unknown>>>(`/api/v1/tax/compliance-platform/regulations${q}`, session);
}

export function runTaxRegulatoryCompliance(session: ApiSession, facts: Record<string, unknown>) {
  return apiPost<Record<string, unknown>>("/api/v1/tax/compliance-platform/regulatory-compliance", session, {
    facts,
  });
}

export function runTaxPolicyCompliance(session: ApiSession, facts: Record<string, unknown>) {
  return apiPost<Record<string, unknown>>("/api/v1/tax/compliance-platform/policy-compliance", session, { facts });
}

export function fetchTaxRegulatoryCalendar(session: ApiSession) {
  return apiGet<Record<string, unknown>>("/api/v1/tax/compliance-platform/regulatory-calendar", session);
}

export function fetchTaxComplianceDeadlines(session: ApiSession) {
  return apiGet<{ deadlines: Array<Record<string, unknown>> }>("/api/v1/tax/compliance-platform/deadlines", session);
}

export function generateTaxComplianceAlerts(session: ApiSession) {
  return apiPost<Record<string, unknown>>("/api/v1/tax/compliance-platform/alerts/generate", session, {});
}

export function fetchTaxComplianceAlerts(session: ApiSession) {
  return apiGet<Array<Record<string, unknown>>>("/api/v1/tax/compliance-platform/alerts", session);
}
