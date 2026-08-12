/** Runtime application registry for ONE NAV + Command Palette (Wave 01). */

export type NavGroupId = "home" | "applications" | "platform" | "security" | "administration" | "account";

export type AppNavItem = {
  id: string;
  label: string;
  href: string;
  group: NavGroupId;
  keywords?: string[];
};

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
  { id: "hospital", label: "Hospital", href: "/healthcare/hospital", group: "applications" },
  { id: "clinic", label: "Clinic", href: "/healthcare/clinic", group: "applications" },
  { id: "pharmacy", label: "Pharmacy", href: "/healthcare/pharmacy", group: "applications" },
  { id: "laboratory", label: "Laboratory", href: "/healthcare/laboratory", group: "applications" },
  { id: "university", label: "University", href: "/education/university", group: "applications" },
  { id: "banking", label: "Banking Analytics", href: "/banking/analytics", group: "applications" },
  { id: "documents", label: "Document Studio", href: "/enterprise/document-studio", group: "applications" },
  { id: "messenger", label: "Messenger", href: "/enterprise/messenger", group: "applications" },
  { id: "notifications", label: "Notifications", href: "/enterprise/notifications", group: "platform", keywords: ["inbox"] },
  { id: "audit", label: "Audit", href: "/enterprise/audit", group: "platform" },
  { id: "workflow", label: "Workflows", href: "/enterprise/workflows", group: "platform", keywords: ["tasks", "approvals"] },
  { id: "federation", label: "Federation", href: "/enterprise/federation", group: "security" },
  { id: "security", label: "My Security", href: "/account/security", group: "account" },
  { id: "plugins", label: "Plugins", href: "/enterprise/plugins", group: "administration" },
  { id: "connectors", label: "Connectors", href: "/enterprise/connector-framework", group: "administration" },
  { id: "observability", label: "Observability", href: "/enterprise/observability", group: "administration" },
  { id: "scheduler", label: "Scheduler", href: "/enterprise/scheduler", group: "administration" },
  { id: "integration-studio", label: "Integration Studio", href: "/enterprise/integration-studio", group: "administration" },
];

export const NAV_GROUP_ORDER: NavGroupId[] = [
  "home",
  "applications",
  "platform",
  "security",
  "administration",
  "account",
];

export function groupedApplicationNav(): { group: NavGroupId; label: string; items: AppNavItem[] }[] {
  return NAV_GROUP_ORDER.map((group) => ({
    group,
    label: NAV_GROUP_LABELS[group],
    items: APPLICATION_NAV.filter((i) => i.group === group),
  })).filter((g) => g.items.length > 0);
}

export function searchApplicationNav(query: string): AppNavItem[] {
  const q = query.trim().toLowerCase();
  if (!q) return [];
  return APPLICATION_NAV.filter((item) => {
    const hay = [item.label, item.id, item.href, ...(item.keywords ?? [])].join(" ").toLowerCase();
    return hay.includes(q);
  }).slice(0, 8);
}
