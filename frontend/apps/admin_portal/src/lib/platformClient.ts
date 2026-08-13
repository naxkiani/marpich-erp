import { API_URL } from "@marpich/auth-provider";
import {
  activatableModulesForPack,
  isPackComingSoon,
  launchHrefForModule,
  launchHrefForPack as sharedLaunchHrefForPack,
} from "@marpich/shared";
import { type ApiSession, apiGet, apiPost } from "./clientAuth";

export {
  activatableModulesForPack,
  isPackComingSoon,
  launchHrefForModule,
};

export type ModuleJewel =
  | "forest"
  | "royal"
  | "emerald"
  | "gold"
  | "orange"
  | "purple"
  | "silver";

export type ModuleCategory =
  | "healthcare"
  | "education"
  | "finance"
  | "commerce"
  | "government"
  | "operations"
  | "platform";

export type IndustryPack = {
  pack_id: string;
  display_name: string;
  description: string;
  required_modules: string[];
  optional_modules: string[];
  compliance_frameworks?: string[];
  default_locale?: string;
};

export type PlatformTenant = {
  id: string;
  slug: string;
  name: string;
  industry_pack: string;
  tier: string;
  status: string;
  enabled_modules: string[];
  locale?: string;
  timezone?: string;
  data_region?: string;
  created_at?: string;
  updated_at?: string;
};

export type PlatformLaunchLink = {
  id: string;
  href: string;
  labelKey: string;
};

const JEWELS: ModuleJewel[] = [
  "forest",
  "royal",
  "emerald",
  "gold",
  "orange",
  "purple",
  "silver",
];

const PACK_JEWELS: Record<string, ModuleJewel> = {
  hospital: "emerald",
  clinic: "royal",
  pharmacy: "forest",
  laboratory: "purple",
  university: "royal",
  school: "royal",
  bank: "gold",
  islamic_bank: "gold",
  microfinance: "gold",
  currency_exchange: "gold",
  tax_consulting: "gold",
  accounting_firm: "gold",
  government: "forest",
  municipality: "forest",
  ngo: "forest",
  retail: "orange",
  pos: "orange",
  hotel: "orange",
  restaurant: "orange",
  manufacturing: "purple",
  logistics: "purple",
  warehouse: "purple",
  transportation: "purple",
  construction: "orange",
  engineering: "purple",
  real_estate: "orange",
  property_management: "orange",
  hr_company: "silver",
};

const PACK_CATEGORIES: Record<string, ModuleCategory> = {
  hospital: "healthcare",
  clinic: "healthcare",
  pharmacy: "healthcare",
  laboratory: "healthcare",
  university: "education",
  school: "education",
  bank: "finance",
  islamic_bank: "finance",
  microfinance: "finance",
  currency_exchange: "finance",
  tax_consulting: "finance",
  accounting_firm: "finance",
  government: "government",
  municipality: "government",
  ngo: "government",
  retail: "commerce",
  pos: "commerce",
  hotel: "commerce",
  restaurant: "commerce",
  real_estate: "commerce",
  property_management: "commerce",
  manufacturing: "operations",
  logistics: "operations",
  warehouse: "operations",
  transportation: "operations",
  construction: "operations",
  engineering: "operations",
  hr_company: "operations",
};

export const PLATFORM_LAUNCH_LINKS: PlatformLaunchLink[] = [
  { id: "hospital", href: "/healthcare/hospital", labelKey: "dashboard.launch.hospital" },
  { id: "clinic", href: "/healthcare/clinic", labelKey: "dashboard.launch.clinic" },
  { id: "pharmacy", href: "/healthcare/pharmacy", labelKey: "dashboard.launch.pharmacy" },
  { id: "laboratory", href: "/healthcare/laboratory", labelKey: "dashboard.launch.laboratory" },
  { id: "university", href: "/education/university", labelKey: "dashboard.launch.university" },
  { id: "banking", href: "/banking/analytics", labelKey: "dashboard.launch.banking" },
  { id: "crm", href: "/crm", labelKey: "nav.app.crm" },
  { id: "sales", href: "/sales", labelKey: "nav.app.sales" },
  { id: "inventory", href: "/inventory", labelKey: "nav.app.inventory" },
  { id: "accounting", href: "/accounting", labelKey: "nav.app.accounting" },
  { id: "procurement", href: "/procurement", labelKey: "nav.app.procurement" },
  { id: "hr", href: "/hr", labelKey: "nav.app.hr" },
  { id: "payroll", href: "/payroll", labelKey: "nav.app.payroll" },
  { id: "tax", href: "/tax", labelKey: "nav.app.tax" },
  { id: "documents", href: "/enterprise/document-studio", labelKey: "dashboard.launch.documents" },
  { id: "messenger", href: "/enterprise/messenger", labelKey: "dashboard.launch.messenger" },
  { id: "observability", href: "/enterprise/observability", labelKey: "dashboard.launch.observability" },
  { id: "scheduler", href: "/enterprise/scheduler", labelKey: "dashboard.launch.scheduler" },
  { id: "integration", href: "/enterprise/integration-studio", labelKey: "dashboard.launch.integration" },
];

function hashPack(packId: string): number {
  let h = 0;
  for (let i = 0; i < packId.length; i += 1) {
    h = (h * 31 + packId.charCodeAt(i)) >>> 0;
  }
  return h;
}

export function jewelForPack(packId: string, index = 0): ModuleJewel {
  if (PACK_JEWELS[packId]) return PACK_JEWELS[packId];
  return JEWELS[(hashPack(packId) + index) % JEWELS.length] ?? "silver";
}

export function packInitials(name: string): string {
  const parts = name
    .trim()
    .split(/[\s/_-]+/)
    .filter(Boolean);
  if (parts.length === 0) return "?";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return `${parts[0][0] ?? ""}${parts[1][0] ?? ""}`.toUpperCase();
}

export function categoryForPack(packId: string): ModuleCategory {
  return PACK_CATEGORIES[packId] ?? "platform";
}

export function launchHrefForPack(packId: string): string | null {
  return sharedLaunchHrefForPack(packId);
}

export async function fetchPlatformTenant(
  session: ApiSession,
  slug: string,
): Promise<PlatformTenant> {
  return apiGet<PlatformTenant>(`/api/v1/platform/tenants/${encodeURIComponent(slug)}`, session);
}

async function publicGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const detail = (body as { detail?: string; message?: string }).detail;
    throw new Error(
      typeof detail === "string"
        ? detail
        : (body as { message?: string }).message ?? `HTTP ${res.status}`,
    );
  }
  const json = (await res.json()) as { data: T };
  return json.data;
}

async function publicPost<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const parsed = await res.json().catch(() => ({}));
    const detail = (parsed as { detail?: string; message?: string }).detail;
    throw new Error(
      typeof detail === "string"
        ? detail
        : (parsed as { message?: string }).message ?? `HTTP ${res.status}`,
    );
  }
  const json = (await res.json()) as { data: T };
  return json.data;
}

export async function fetchIndustryPacks(): Promise<IndustryPack[]> {
  return publicGet<IndustryPack[]>("/api/v1/platform/industry-packs");
}

export async function fetchPlatformTenants(session: ApiSession): Promise<PlatformTenant[]> {
  return apiGet<PlatformTenant[]>("/api/v1/platform/tenants", session);
}

export async function provisionPlatformTenant(
  session: ApiSession | null | undefined,
  body: {
    name: string;
    slug: string;
    industry_pack: string;
    tier?: string;
    optional_modules?: string[];
    locale?: string;
    timezone?: string;
    data_region?: string;
  },
): Promise<PlatformTenant> {
  if (session) {
    return apiPost<PlatformTenant>("/api/v1/platform/tenants", session, body);
  }
  return publicPost<PlatformTenant>("/api/v1/platform/tenants", body);
}

export async function activatePlatformModule(
  session: ApiSession,
  slug: string,
  moduleId: string,
): Promise<PlatformTenant> {
  return apiPost<PlatformTenant>(
    `/api/v1/platform/tenants/${encodeURIComponent(slug)}/modules`,
    session,
    { module_id: moduleId },
  );
}

export async function suspendPlatformTenant(
  session: ApiSession,
  slug: string,
): Promise<PlatformTenant> {
  return apiPost<PlatformTenant>(
    `/api/v1/platform/tenants/${encodeURIComponent(slug)}/suspend`,
    session,
    {},
  );
}
