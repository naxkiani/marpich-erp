/** Runtime application registry for ONE NAV + Command Palette (Wave 01+). */

import { matchesAnyPermission } from "./permissions";

export type NavGroupId =
  | "home"
  | "healthcare"
  | "education"
  | "commerce"
  | "workforce"
  | "collaboration"
  | "platform"
  | "security"
  | "administration"
  | "account";

export type AppNavItem = {
  id: string;
  label: string;
  /** i18n key — falls back to label */
  labelKey?: string;
  href: string;
  group: NavGroupId;
  keywords?: string[];
  /** Any-of permission codes required to show this app (omit = always visible when authenticated). */
  permission?: string | string[];
  /**
   * Industry-pack module IDs that unlock this app in the shell.
   * Omit = always eligible (Home / Account / core platform desks).
   * Match if tenant.enabled_modules intersects this list.
   */
  moduleIds?: string[];
};

export type PermissionPredicate = (code: string) => boolean;

export type ModuleLaunchStatus = "ready" | "coming_soon";

export type ModuleLaunchEntry = {
  moduleId: string;
  href: string | null;
  navId?: string;
  status: ModuleLaunchStatus;
  label: string;
};

export type PackLaunchEntry = {
  packId: string;
  href: string | null;
  status: ModuleLaunchStatus;
  primaryModuleIds?: string[];
};

export const NAV_GROUP_LABELS: Record<NavGroupId, string> = {
  home: "Home",
  healthcare: "Healthcare",
  education: "Education",
  commerce: "Commerce & Finance",
  workforce: "Workforce",
  collaboration: "Collaboration",
  platform: "Platform",
  security: "Security",
  administration: "Administration",
  account: "Account",
};

export const NAV_GROUP_LABEL_KEYS: Record<NavGroupId, string> = {
  home: "nav.group.home",
  healthcare: "nav.group.healthcare",
  education: "nav.group.education",
  commerce: "nav.group.commerce",
  workforce: "nav.group.workforce",
  collaboration: "nav.group.collaboration",
  platform: "nav.group.platform",
  security: "nav.group.security",
  administration: "nav.group.administration",
  account: "nav.group.account",
};

/** Canonical module_id → app launch map (industry_packs.json ids). */
export const MODULE_LAUNCH_CATALOG: ModuleLaunchEntry[] = [
  { moduleId: "platform.crm", href: "/crm", navId: "crm", status: "ready", label: "CRM" },
  { moduleId: "platform.inventory", href: "/inventory", navId: "inventory", status: "ready", label: "Inventory" },
  { moduleId: "inventory.management", href: "/inventory", navId: "inventory", status: "ready", label: "Inventory" },
  { moduleId: "platform.finance", href: "/accounting", navId: "accounting", status: "ready", label: "Finance / Accounting" },
  { moduleId: "finance.accounting", href: "/accounting", navId: "accounting", status: "ready", label: "Accounting" },
  { moduleId: "finance.tax", href: "/tax", navId: "tax", status: "ready", label: "Tax" },
  { moduleId: "tax.management", href: "/tax", navId: "tax", status: "ready", label: "Tax" },
  { moduleId: "platform.hr", href: "/hr", navId: "human_resources", status: "ready", label: "Human Resources" },
  { moduleId: "government.procurement", href: "/procurement", navId: "procurement", status: "ready", label: "Procurement" },
  { moduleId: "healthcare.patient-management", href: "/healthcare/hospital", navId: "hospital", status: "ready", label: "Patient Management" },
  { moduleId: "healthcare.clinical", href: "/healthcare/hospital", navId: "hospital", status: "ready", label: "Clinical" },
  { moduleId: "healthcare.billing", href: "/accounting", navId: "accounting", status: "ready", label: "Healthcare Billing" },
  { moduleId: "healthcare.appointments", href: "/healthcare/clinic", navId: "clinic", status: "ready", label: "Appointments" },
  { moduleId: "healthcare.pharmacy", href: "/healthcare/pharmacy", navId: "pharmacy", status: "ready", label: "Pharmacy" },
  { moduleId: "healthcare.laboratory", href: "/healthcare/laboratory", navId: "laboratory", status: "ready", label: "Laboratory" },
  { moduleId: "healthcare.radiology", href: null, status: "coming_soon", label: "Radiology" },
  { moduleId: "education.student-information", href: "/education/university", navId: "university", status: "ready", label: "Student Information" },
  { moduleId: "education.academics", href: "/education/university", navId: "university", status: "ready", label: "Academics" },
  { moduleId: "education.admissions", href: "/education/university", navId: "university", status: "ready", label: "Admissions" },
  { moduleId: "education.grading", href: null, status: "coming_soon", label: "Grading" },
  { moduleId: "education.attendance", href: null, status: "coming_soon", label: "Attendance" },
  { moduleId: "education.library", href: null, status: "coming_soon", label: "Library" },
  { moduleId: "education.research", href: null, status: "coming_soon", label: "Research" },
  { moduleId: "finance.core-banking", href: "/banking/analytics", navId: "banking", status: "ready", label: "Core Banking" },
  { moduleId: "finance.islamic-products", href: "/banking/analytics", navId: "banking", status: "ready", label: "Islamic Products" },
  { moduleId: "finance.lending", href: "/banking/analytics", navId: "banking", status: "ready", label: "Lending" },
  { moduleId: "finance.forex", href: null, status: "coming_soon", label: "Forex" },
  { moduleId: "finance.treasury", href: null, status: "coming_soon", label: "Treasury" },
  { moduleId: "platform.documents", href: "/enterprise/document-studio", navId: "documents", status: "ready", label: "Documents" },
  { moduleId: "platform.workflow", href: "/enterprise/workflows", navId: "workflow", status: "ready", label: "Workflow" },
  { moduleId: "platform.identity", href: "/account/security", navId: "security", status: "ready", label: "Identity" },
  { moduleId: "platform.core", href: "/", navId: "dashboard", status: "ready", label: "Core Platform" },
  { moduleId: "logistics.warehouse", href: null, status: "coming_soon", label: "Warehouse" },
  { moduleId: "manufacturing.mrp", href: null, status: "coming_soon", label: "MRP" },
  { moduleId: "manufacturing.production", href: null, status: "coming_soon", label: "Production" },
  { moduleId: "retail.pos", href: "/sales", navId: "sales", status: "ready", label: "POS / Sales" },
  { moduleId: "retail.catalog", href: "/inventory", navId: "inventory", status: "ready", label: "Catalog" },
  { moduleId: "construction.projects", href: null, status: "coming_soon", label: "Projects" },
  { moduleId: "real-estate.listings", href: null, status: "coming_soon", label: "Listings" },
  { moduleId: "hospitality.reservations", href: null, status: "coming_soon", label: "Reservations" },
  { moduleId: "government.citizen-services", href: null, status: "coming_soon", label: "Citizen Services" },
  { moduleId: "ngo.programs", href: null, status: "coming_soon", label: "NGO Programs" },
];

export const PACK_LAUNCH_CATALOG: PackLaunchEntry[] = [
  { packId: "hospital", href: "/healthcare/hospital", status: "ready", primaryModuleIds: ["healthcare.patient-management"] },
  { packId: "clinic", href: "/healthcare/clinic", status: "ready", primaryModuleIds: ["healthcare.appointments"] },
  { packId: "pharmacy", href: "/healthcare/pharmacy", status: "ready", primaryModuleIds: ["healthcare.pharmacy"] },
  { packId: "laboratory", href: "/healthcare/laboratory", status: "ready", primaryModuleIds: ["healthcare.laboratory"] },
  { packId: "university", href: "/education/university", status: "ready", primaryModuleIds: ["education.student-information"] },
  { packId: "school", href: null, status: "coming_soon" },
  { packId: "bank", href: "/banking/analytics", status: "ready", primaryModuleIds: ["finance.core-banking"] },
  { packId: "islamic_bank", href: "/banking/analytics", status: "ready", primaryModuleIds: ["finance.islamic-products"] },
  { packId: "microfinance", href: "/banking/analytics", status: "ready", primaryModuleIds: ["finance.lending"] },
  { packId: "currency_exchange", href: null, status: "coming_soon" },
  { packId: "tax_consulting", href: "/tax", status: "ready", primaryModuleIds: ["finance.tax", "tax.management"] },
  { packId: "accounting_firm", href: "/accounting", status: "ready", primaryModuleIds: ["finance.accounting", "platform.finance"] },
  { packId: "hr_company", href: "/hr", status: "ready", primaryModuleIds: ["platform.hr"] },
  { packId: "retail", href: "/sales", status: "ready", primaryModuleIds: ["retail.pos", "platform.crm"] },
  { packId: "pos", href: "/sales", status: "ready", primaryModuleIds: ["retail.pos"] },
  { packId: "warehouse", href: null, status: "coming_soon" },
  { packId: "manufacturing", href: null, status: "coming_soon" },
  { packId: "logistics", href: null, status: "coming_soon" },
  { packId: "transportation", href: null, status: "coming_soon" },
  { packId: "construction", href: null, status: "coming_soon" },
  { packId: "engineering", href: null, status: "coming_soon" },
  { packId: "hotel", href: null, status: "coming_soon" },
  { packId: "restaurant", href: null, status: "coming_soon" },
  { packId: "real_estate", href: null, status: "coming_soon" },
  { packId: "property_management", href: null, status: "coming_soon" },
  { packId: "government", href: null, status: "coming_soon" },
  { packId: "municipality", href: null, status: "coming_soon" },
  { packId: "ngo", href: null, status: "coming_soon" },
];

export const APPLICATION_NAV: AppNavItem[] = [
  { id: "dashboard", label: "Dashboard", labelKey: "nav.app.dashboard", href: "/", group: "home", keywords: ["home"] },
  { id: "modules", label: "Modules", labelKey: "nav.app.modules", href: "/modules", group: "home" },
  {
    id: "hospital",
    label: "Hospital",
    labelKey: "nav.app.hospital",
    href: "/healthcare/hospital",
    group: "healthcare",
    permission: "hospital.patients.read",
    moduleIds: ["healthcare.patient-management", "healthcare.clinical", "healthcare.billing"],
  },
  {
    id: "clinic",
    label: "Clinic",
    labelKey: "nav.app.clinic",
    href: "/healthcare/clinic",
    group: "healthcare",
    permission: "clinic.patients.read",
    moduleIds: ["healthcare.patient-management", "healthcare.appointments"],
  },
  {
    id: "pharmacy",
    label: "Pharmacy",
    labelKey: "nav.app.pharmacy",
    href: "/healthcare/pharmacy",
    group: "healthcare",
    permission: "pharmacy.prescriptions.read",
    moduleIds: ["healthcare.pharmacy"],
  },
  {
    id: "laboratory",
    label: "Laboratory",
    labelKey: "nav.app.laboratory",
    href: "/healthcare/laboratory",
    group: "healthcare",
    permission: "laboratory.orders.read",
    moduleIds: ["healthcare.laboratory"],
  },
  {
    id: "university",
    label: "University",
    labelKey: "nav.app.university",
    href: "/education/university",
    group: "education",
    permission: "university.students.read",
    moduleIds: ["education.student-information", "education.academics", "education.admissions"],
  },
  {
    id: "banking",
    label: "Banking Analytics",
    labelKey: "nav.app.banking",
    href: "/banking/analytics",
    group: "commerce",
    permission: "banking.analytics.read",
    moduleIds: ["finance.core-banking", "finance.islamic-products", "finance.lending"],
  },
  {
    id: "crm",
    label: "CRM",
    labelKey: "nav.app.crm",
    href: "/crm",
    group: "commerce",
    keywords: ["contacts", "opportunities", "customers"],
    permission: ["crm.contacts.read", "crm.opportunities.read"],
    moduleIds: ["platform.crm"],
  },
  {
    id: "sales",
    label: "Sales",
    labelKey: "nav.app.sales",
    href: "/sales",
    group: "commerce",
    keywords: ["quotations", "orders", "quotes"],
    permission: ["sales.quotations.read", "sales.orders.read"],
    moduleIds: ["platform.crm", "retail.pos"],
  },
  {
    id: "inventory",
    label: "Inventory",
    labelKey: "nav.app.inventory",
    href: "/inventory",
    group: "commerce",
    keywords: ["stock", "sku", "warehouse"],
    permission: "inventory.stock.read",
    moduleIds: ["platform.inventory", "inventory.management", "retail.catalog"],
  },
  {
    id: "accounting",
    label: "Accounting",
    labelKey: "nav.app.accounting",
    href: "/accounting",
    group: "commerce",
    keywords: ["invoices", "ar", "receivable", "billing"],
    permission: "accounting.invoice.read",
    moduleIds: ["platform.finance", "finance.accounting", "healthcare.billing"],
  },
  {
    id: "procurement",
    label: "Procurement",
    labelKey: "nav.app.procurement",
    href: "/procurement",
    group: "commerce",
    keywords: ["requisitions", "purchase", "po", "vendor"],
    permission: "procurement.requisitions.read",
    moduleIds: ["government.procurement", "platform.inventory"],
  },
  {
    id: "human_resources",
    label: "Human Resources",
    labelKey: "nav.app.hr",
    href: "/hr",
    group: "workforce",
    keywords: ["employees", "hr", "hire", "terminate", "workforce"],
    permission: "human_resources.employees.read",
    moduleIds: ["platform.hr"],
  },
  {
    id: "payroll",
    label: "Payroll",
    labelKey: "nav.app.payroll",
    href: "/payroll",
    group: "workforce",
    keywords: ["payslip", "salary", "pay run", "compensation"],
    permission: ["payroll.employees.read", "payroll.runs.read"],
    moduleIds: ["platform.hr"],
  },
  {
    id: "tax",
    label: "Tax",
    labelKey: "nav.app.tax",
    href: "/tax",
    group: "workforce",
    keywords: ["tax return", "liability", "vat", "withholding"],
    permission: ["tax.liabilities.read", "tax.returns.read"],
    moduleIds: ["finance.tax", "tax.management"],
  },
  {
    id: "documents",
    label: "Document Studio",
    labelKey: "nav.app.documents",
    href: "/enterprise/document-studio",
    group: "collaboration",
    permission: "documents.read",
    moduleIds: ["platform.documents"],
  },
  {
    id: "messenger",
    label: "Messenger",
    labelKey: "nav.app.messenger",
    href: "/enterprise/messenger",
    group: "collaboration",
    permission: "messenger.messages.read",
  },
  {
    id: "notifications",
    label: "Notifications",
    labelKey: "nav.app.notifications",
    href: "/enterprise/notifications",
    group: "platform",
    keywords: ["inbox"],
  },
  {
    id: "audit",
    label: "Audit",
    labelKey: "nav.app.audit",
    href: "/enterprise/audit",
    group: "platform",
    permission: "audit.entries.read",
  },
  {
    id: "workflow",
    label: "Workflows",
    labelKey: "nav.app.workflow",
    href: "/enterprise/workflows",
    group: "platform",
    keywords: ["tasks", "approvals"],
    permission: ["workflow.instances.read", "workflow.definitions.read", "workflow.tasks.complete"],
    moduleIds: ["platform.workflow"],
  },
  {
    id: "federation",
    label: "Federation",
    labelKey: "nav.app.federation",
    href: "/enterprise/federation",
    group: "security",
    permission: "federation.read",
  },
  { id: "security", label: "My Security", labelKey: "nav.mySecurity", href: "/account/security", group: "account" },
  {
    id: "plugins",
    label: "Plugins",
    labelKey: "nav.app.plugins",
    href: "/enterprise/plugins",
    group: "administration",
    permission: ["plugins.read", "plugins.marketplace.read"],
  },
  {
    id: "connectors",
    label: "Connectors",
    labelKey: "nav.app.connectors",
    href: "/enterprise/connector-framework",
    group: "administration",
    permission: ["enterprise_connector_framework.read", "integration.connectors.read"],
  },
  {
    id: "observability",
    label: "Observability",
    labelKey: "nav.app.observability",
    href: "/enterprise/observability",
    group: "administration",
    permission: "enterprise_observability.read",
  },
  {
    id: "scheduler",
    label: "Scheduler",
    labelKey: "nav.app.scheduler",
    href: "/enterprise/scheduler",
    group: "administration",
    permission: "enterprise_scheduler.read",
  },
  {
    id: "integration-studio",
    label: "Integration Studio",
    labelKey: "nav.app.integrationStudio",
    href: "/enterprise/integration-studio",
    group: "administration",
    permission: "enterprise_integration_studio.read",
  },
];

export const NAV_GROUP_ORDER: NavGroupId[] = [
  "home",
  "healthcare",
  "education",
  "commerce",
  "workforce",
  "collaboration",
  "platform",
  "security",
  "administration",
  "account",
];

const MODULE_LAUNCH_BY_ID = new Map(MODULE_LAUNCH_CATALOG.map((e) => [e.moduleId, e]));
const PACK_LAUNCH_BY_ID = new Map(PACK_LAUNCH_CATALOG.map((e) => [e.packId, e]));

export function launchEntryForModule(moduleId: string): ModuleLaunchEntry | undefined {
  return MODULE_LAUNCH_BY_ID.get(moduleId);
}

export function launchHrefForModule(moduleId: string): string | null {
  const entry = MODULE_LAUNCH_BY_ID.get(moduleId);
  if (!entry || entry.status !== "ready") return null;
  return entry.href;
}

export function packLaunchEntry(packId: string): PackLaunchEntry | undefined {
  return PACK_LAUNCH_BY_ID.get(packId);
}

export function launchHrefForPack(packId: string): string | null {
  const entry = PACK_LAUNCH_BY_ID.get(packId);
  if (!entry || entry.status !== "ready") return null;
  return entry.href;
}

export function isPackComingSoon(packId: string): boolean {
  const entry = PACK_LAUNCH_BY_ID.get(packId);
  return !entry || entry.status === "coming_soon" || !entry.href;
}

export function canAccessApp(
  item: AppNavItem,
  can: PermissionPredicate | readonly string[] | undefined,
): boolean {
  if (!item.permission) return true;
  if (!can) return false;
  if (typeof can === "function") {
    const codes = typeof item.permission === "string" ? [item.permission] : item.permission;
    return codes.some((code) => can(code));
  }
  return matchesAnyPermission(can, item.permission);
}

/** True when the app is unlocked by tenant enabled_modules (or has no module gate). */
export function isModuleEnabledForApp(
  item: AppNavItem,
  enabledModules: readonly string[] | null | undefined,
): boolean {
  if (!item.moduleIds || item.moduleIds.length === 0) return true;
  if (!enabledModules || enabledModules.length === 0) return false;
  const enabled = new Set(enabledModules);
  return item.moduleIds.some((id) => enabled.has(id));
}

export function filterApplicationNav(
  can: PermissionPredicate | readonly string[] | undefined,
  items: AppNavItem[] = APPLICATION_NAV,
  enabledModules?: readonly string[] | null,
): AppNavItem[] {
  return items.filter((item) => {
    if (!canAccessApp(item, can)) return false;
    if (enabledModules === undefined) return true;
    return isModuleEnabledForApp(item, enabledModules);
  });
}

export function groupedApplicationNav(
  can?: PermissionPredicate | readonly string[],
  enabledModules?: readonly string[] | null,
): { group: NavGroupId; label: string; labelKey: string; items: AppNavItem[] }[] {
  const visible =
    can === undefined && enabledModules === undefined
      ? APPLICATION_NAV
      : filterApplicationNav(can, APPLICATION_NAV, enabledModules);
  return NAV_GROUP_ORDER.map((group) => ({
    group,
    label: NAV_GROUP_LABELS[group],
    labelKey: NAV_GROUP_LABEL_KEYS[group],
    items: visible.filter((i) => i.group === group),
  })).filter((g) => g.items.length > 0);
}

export function searchApplicationNav(
  query: string,
  can?: PermissionPredicate | readonly string[],
  enabledModules?: readonly string[] | null,
): AppNavItem[] {
  const q = query.trim().toLowerCase();
  if (!q) return [];
  const pool =
    can === undefined && enabledModules === undefined
      ? APPLICATION_NAV
      : filterApplicationNav(can, APPLICATION_NAV, enabledModules);
  return pool
    .filter((item) => {
      const hay = [item.label, item.id, item.href, ...(item.keywords ?? [])].join(" ").toLowerCase();
      return hay.includes(q);
    })
    .slice(0, 8);
}

export function activatableModulesForPack(
  pack: { required_modules?: string[]; optional_modules?: string[]; requiredModules?: string[]; optionalModules?: string[] },
  enabledModules: readonly string[],
): string[] {
  const required = pack.required_modules ?? pack.requiredModules ?? [];
  const optional = pack.optional_modules ?? pack.optionalModules ?? [];
  const enabled = new Set(enabledModules);
  return [...required, ...optional].filter((m) => !enabled.has(m));
}
