"use client";

import { useAuth } from "@marpich/auth-provider";
import { AppShell } from "@marpich/core";
import { APPLICATION_NAV, filterApplicationNav, type CommandItem } from "@marpich/shared";
import { useMemo, type ReactNode } from "react";
import { ShellNav } from "./ShellNav";

export function AuthenticatedAppShell({ children }: { children: ReactNode }) {
  const { hasPermission, isAuthenticated } = useAuth();

  const commands = useMemo<CommandItem[]>(() => {
    const apps = isAuthenticated
      ? filterApplicationNav(hasPermission)
      : APPLICATION_NAV.filter((i) => i.group === "home" || i.id === "security");
    return [
      ...apps.map((app) => ({
        id: `nav-${app.id}`,
        label: `Open ${app.label}`,
        onSelect: () => {
          window.location.href = app.href;
        },
      })),
      {
        id: "theme",
        label: "Toggle theme",
        onSelect: () =>
          document.documentElement.dataset.theme === "dark"
            ? (document.documentElement.dataset.theme = "light")
            : (document.documentElement.dataset.theme = "dark"),
      },
      {
        id: "ask-ai",
        label: "Ask AI",
        onSelect: () => {
          document.querySelector<HTMLButtonElement>(".mp-btn-accent")?.click();
        },
      },
    ];
  }, [hasPermission, isAuthenticated]);

  return (
    <AppShell nav={<ShellNav />} commands={commands}>
      {children}
    </AppShell>
  );
}
