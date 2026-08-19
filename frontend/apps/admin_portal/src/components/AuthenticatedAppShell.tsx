"use client";

import { useAuth } from "@marpich/auth-provider";
import { AppShell } from "@marpich/core";
import {
  APPLICATION_NAV,
  TenantModulesProvider,
  filterApplicationNav,
  useLocale,
  useTenantModules,
  type CommandItem,
} from "@marpich/shared";
import { useMemo, type ReactNode } from "react";
import { ShellNav } from "./ShellNav";

function ShellWithCommands({ children }: { children: ReactNode }) {
  const { hasPermission, isAuthenticated } = useAuth();
  const { enabledModules, snapshot } = useTenantModules();
  const { t } = useLocale();

  const commands = useMemo<CommandItem[]>(() => {
    const moduleGate = snapshot ? enabledModules : undefined;
    const apps = isAuthenticated
      ? filterApplicationNav(hasPermission, APPLICATION_NAV, moduleGate)
      : APPLICATION_NAV.filter((i) => i.group === "home" || i.id === "security");
    return [
      ...apps.map((app) => ({
        id: `nav-${app.id}`,
        label: `${t("nav.open")} ${app.labelKey ? t(app.labelKey) : app.label}`,
        onSelect: () => {
          window.location.href = app.href;
        },
      })),
      {
        id: "theme",
        label: t("nav.toggleTheme"),
        onSelect: () =>
          document.documentElement.dataset.theme === "dark"
            ? (document.documentElement.dataset.theme = "light")
            : (document.documentElement.dataset.theme = "dark"),
      },
      {
        id: "ask-ai",
        label: t("nav.askAi"),
        onSelect: () => {
          document.querySelector<HTMLButtonElement>(".mp-btn-accent")?.click();
        },
      },
    ];
  }, [enabledModules, hasPermission, isAuthenticated, snapshot, t]);

  return (
    <AppShell nav={<ShellNav />} commands={commands}>
      {children}
    </AppShell>
  );
}

export function AuthenticatedAppShell({ children }: { children: ReactNode }) {
  const { isAuthenticated, session } = useAuth();

  return (
    <TenantModulesProvider
      isAuthenticated={isAuthenticated}
      tenantId={session?.tenantId}
    >
      <ShellWithCommands>{children}</ShellWithCommands>
    </TenantModulesProvider>
  );
}
