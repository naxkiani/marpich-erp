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
import { loadPlatformSession } from "./session";

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

async function fetchTenantBySlug(slug: string): Promise<TenantModulesSnapshot | null> {
  const res = await fetch(`/api/backend/api/v1/platform/tenants/${encodeURIComponent(slug)}`, {
    credentials: "same-origin",
    headers: {
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
  isAuthenticated,
}: {
  children: ReactNode;
  tenantId?: string | null;
  isAuthenticated: boolean;
}) {
  const [snapshot, setSnapshot] = useState<TenantModulesSnapshot | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    const session = loadPlatformSession();
    const slug = tenantId || session?.tenantId;
    if (!isAuthenticated || !slug) {
      setSnapshot(null);
      return null;
    }
    setLoading(true);
    setError(null);
    try {
      const next = await fetchTenantBySlug(slug);
      setSnapshot(next);
      if (!next) setError("Unable to load tenant modules");
      return next;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Tenant modules failed");
      return null;
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, tenantId]);

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
