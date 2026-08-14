"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { API_URL, loadPlatformSession } from "./session";

export type TenantModulesSnapshot = {
  slug: string;
  name?: string;
  industryPack?: string;
  enabledModules: string[];
};

type TenantModulesContextValue = {
  snapshot: TenantModulesSnapshot | null;
  enabledModules: string[];
  loading: boolean;
  error: string | null;
  refresh: () => Promise<TenantModulesSnapshot | null>;
  setEnabledModules: (slug: string, modules: string[], meta?: Partial<TenantModulesSnapshot>) => void;
};

const TenantModulesContext = createContext<TenantModulesContextValue | null>(null);

async function fetchTenantBySlug(
  slug: string,
  accessToken: string,
): Promise<TenantModulesSnapshot | null> {
  const res = await fetch(`${API_URL}/api/v1/platform/tenants/${encodeURIComponent(slug)}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "X-Tenant-ID": slug,
      "Content-Type": "application/json",
    },
  });
  if (!res.ok) return null;
  const json = (await res.json()) as {
    data?: {
      slug?: string;
      name?: string;
      industry_pack?: string;
      enabled_modules?: string[];
    };
  };
  const data = json.data;
  if (!data?.slug) return null;
  return {
    slug: data.slug,
    name: data.name,
    industryPack: data.industry_pack,
    enabledModules: data.enabled_modules ?? [],
  };
}

export function TenantModulesProvider({
  children,
  tenantId,
  accessToken,
  isAuthenticated,
}: {
  children: ReactNode;
  tenantId?: string | null;
  accessToken?: string | null;
  isAuthenticated: boolean;
}) {
  const [snapshot, setSnapshot] = useState<TenantModulesSnapshot | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    const session = loadPlatformSession();
    const slug = tenantId || session?.tenantId;
    const token = accessToken || session?.accessToken;
    if (!isAuthenticated || !slug || !token) {
      setSnapshot(null);
      return null;
    }
    setLoading(true);
    setError(null);
    try {
      const next = await fetchTenantBySlug(slug, token);
      setSnapshot(next);
      if (!next) setError("Unable to load tenant modules");
      return next;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Tenant modules failed");
      return null;
    } finally {
      setLoading(false);
    }
  }, [accessToken, isAuthenticated, tenantId]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const setEnabledModules = useCallback(
    (slug: string, modules: string[], meta?: Partial<TenantModulesSnapshot>) => {
      setSnapshot((prev) => ({
        slug,
        name: meta?.name ?? prev?.name,
        industryPack: meta?.industryPack ?? prev?.industryPack,
        enabledModules: modules,
      }));
    },
    [],
  );

  const value = useMemo<TenantModulesContextValue>(
    () => ({
      snapshot,
      enabledModules: snapshot?.enabledModules ?? [],
      loading,
      error,
      refresh,
      setEnabledModules,
    }),
    [error, loading, refresh, setEnabledModules, snapshot],
  );

  return <TenantModulesContext.Provider value={value}>{children}</TenantModulesContext.Provider>;
}

export function useTenantModules(): TenantModulesContextValue {
  const ctx = useContext(TenantModulesContext);
  if (!ctx) {
    return {
      snapshot: null,
      enabledModules: [],
      loading: false,
      error: null,
      refresh: async () => null,
      setEnabledModules: () => undefined,
    };
  }
  return ctx;
}
