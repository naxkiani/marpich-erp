/** Runtime application registry for ONE NAV + Command Palette (Wave 01). */

import { matchesAnyPermission } from "./permissions";

export type NavGroupId =
  | "home"
  | "applications"
  | "platform"
  | "security"
  | "administration"
  | "account";

export type AppNavItem = {
  id: string;
  label: string;
  href: string;
  group: NavGroupId;
  keywords?: string[];
  /** Any-of permission codes required to show this app (omit = always visible when authenticated). */
  permission?: string | string[];
};

export type PermissionPredicate = (code: string) => boolean;

export const NAV_GROUP_LABELS: Record<NavGroupId, string> = {
  home: "Home",
  applications: "Applications",
  platform: "Platform",
  security: "Security",
  administration: "Administration",
  account: "Account",
};

export const APPLICATION_NAV: AppNavItem[] = [
  { id: "dashboard", label: "Dashboard", href: "/", group: "home", keywords: ["home"] },
  { id: "modules", label: "Modules", href: "/modules", group: "home" },
  {
    id: "hospital",
    label: "Hospital",
    href: "/healthcare/hospital",
    group: "applications",
    permission: "hospital.patients.read",
  },
  {
    id: "clinic",
    label: "Clinic",
    href: "/healthcare/clinic",
    group: "applications",
    permission: "clinic.patients.read",
  },
  {
    id: "pharmacy",
    label: "Pharmacy",
    href: "/healthcare/pharmacy",
    group: "applications",
    permission: "pharmacy.prescriptions.read",
  },
  {
    id: "laboratory",
    label: "Laboratory",
    href: "/healthcare/laboratory",
    group: "applications",
    permission: "laboratory.orders.read",
  },
  {
    id: "university",
    label: "University",
    href: "/education/university",
    group: "applications",
    permission: "university.students.read",
  },
  { id: "banking", label: "Banking Analytics", href: "/banking/analytics", group: "applications", permission: "banking.analytics.read" },
  {
    id: "crm",
    label: "CRM",
    href: "/crm",
    group: "applications",
    keywords: ["contacts", "opportunities", "customers"],
    permission: ["crm.contacts.read", "crm.opportunities.read"],
  },
  {
    id: "sales",
    label: "Sales",
    href: "/sales",
    group: "applications",
    keywords: ["quotations", "orders", "quotes"],
    permission: ["sales.quotations.read", "sales.orders.read"],
  },
  {
    id: "inventory",
    label: "Inventory",
    href: "/inventory",
    group: "applications",
    keywords: ["stock", "sku", "warehouse"],
    permission: "inventory.stock.read",
  },
  {
    id: "accounting",
    label: "Accounting",
    href: "/accounting",
    group: "applications",
    keywords: ["invoices", "ar", "receivable", "billing"],
    permission: "accounting.invoice.read",
  },
  {
    id: "procurement",
    label: "Procurement",
    href: "/procurement",
    group: "applications",
    keywords: ["requisitions", "purchase", "po", "vendor"],
    permission: "procurement.requisitions.read",
  },
  {
    id: "human_resources",
    label: "Human Resources",
    href: "/hr",
    group: "applications",
    keywords: ["employees", "hr", "hire", "terminate", "workforce"],
    permission: "human_resources.employees.read",
  },
  {
    id: "payroll",
    label: "Payroll",
    href: "/payroll",
    group: "applications",
    keywords: ["payslip", "salary", "pay run", "compensation"],
    permission: ["payroll.employees.read", "payroll.runs.read"],
  },
  {
    id: "documents",
    label: "Document Studio",
    href: "/enterprise/document-studio",
    group: "applications",
    permission: "documents.read",
  },
  {
    id: "messenger",
    label: "Messenger",
    href: "/enterprise/messenger",
    group: "applications",
    permission: "messenger.messages.read",
  },
  {
    id: "notifications",
    label: "Notifications",
    href: "/enterprise/notifications",
    group: "platform",
    keywords: ["inbox"],
  },
  {
    id: "audit",
    label: "Audit",
    href: "/enterprise/audit",
    group: "platform",
    permission: "audit.entries.read",
  },
  {
    id: "workflow",
    label: "Workflows",
    href: "/enterprise/workflows",
    group: "platform",
    keywords: ["tasks", "approvals"],
    permission: ["workflow.instances.read", "workflow.definitions.read", "workflow.tasks.complete"],
  },
  {
    id: "federation",
    label: "Federation",
    href: "/enterprise/federation",
    group: "security",
    permission: "federation.read",
  },
  { id: "security", label: "My Security", href: "/account/security", group: "account" },
  {
    id: "plugins",
    label: "Plugins",
    href: "/enterprise/plugins",
    group: "administration",
    permission: ["plugins.read", "plugins.marketplace.read"],
  },
  {
    id: "connectors",
    label: "Connectors",
    href: "/enterprise/connector-framework",
    group: "administration",
    permission: ["enterprise_connector_framework.read", "integration.connectors.read"],
  },
  {
    id: "observability",
    label: "Observability",
    href: "/enterprise/observability",
    group: "administration",
    permission: "enterprise_observability.read",
  },
  {
    id: "scheduler",
    label: "Scheduler",
    href: "/enterprise/scheduler",
    group: "administration",
    permission: "enterprise_scheduler.read",
  },
  {
    id: "integration-studio",
    label: "Integration Studio",
    href: "/enterprise/integration-studio",
    group: "administration",
    permission: "enterprise_integration_studio.read",
  },
];

export const NAV_GROUP_ORDER: NavGroupId[] = [
  "home",
  "applications",
  "platform",
  "security",
  "administration",
  "account",
];

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

export function filterApplicationNav(
  can: PermissionPredicate | readonly string[] | undefined,
  items: AppNavItem[] = APPLICATION_NAV,
): AppNavItem[] {
  return items.filter((item) => canAccessApp(item, can));
}

export function groupedApplicationNav(
  can?: PermissionPredicate | readonly string[],
): { group: NavGroupId; label: string; items: AppNavItem[] }[] {
  const visible = can === undefined ? APPLICATION_NAV : filterApplicationNav(can);
  return NAV_GROUP_ORDER.map((group) => ({
    group,
    label: NAV_GROUP_LABELS[group],
    items: visible.filter((i) => i.group === group),
  })).filter((g) => g.items.length > 0);
}

export function searchApplicationNav(
  query: string,
  can?: PermissionPredicate | readonly string[],
): AppNavItem[] {
  const q = query.trim().toLowerCase();
  if (!q) return [];
  const pool = can === undefined ? APPLICATION_NAV : filterApplicationNav(can);
  return pool
    .filter((item) => {
      const hay = [item.label, item.id, item.href, ...(item.keywords ?? [])].join(" ").toLowerCase();
      return hay.includes(q);
    })
    .slice(0, 8);
}
