"use client";

import {
  AIAssistantPanel,
  APPLICATION_NAV,
  Breadcrumb,
  CommandPalette,
  DirectionProvider,
  GlobalSearch,
  HelpButton,
  KeyboardShortcutsDialog,
  LocaleProvider,
  LocaleSwitcher,
  NotificationCenter,
  ThemeProvider,
  ThemeToggle,
  ToastProvider,
  UndoToast,
  useGlobalKeyboardShortcuts,
  useLocale,
  type BreadcrumbItem,
  type CommandItem,
} from "@marpich/shared";
import { useCallback, useMemo, useState, type ReactNode } from "react";

export function MarpichProviders({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider>
      <LocaleProvider>
        <ToastProvider>
          <DirectionProvider>{children}</DirectionProvider>
          <UndoToast />
        </ToastProvider>
      </LocaleProvider>
    </ThemeProvider>
  );
}

export function AppShell({
  children,
  nav,
  commands: commandsProp,
}: {
  children: ReactNode;
  nav?: ReactNode;
  /** When provided (e.g. AuthZ-filtered), replaces default registry commands. */
  commands?: CommandItem[];
}) {
  const { t } = useLocale();
  const [commandOpen, setCommandOpen] = useState(false);
  const [shortcutsOpen, setShortcutsOpen] = useState(false);
  const [navOpen, setNavOpen] = useState(false);

  const defaultCommands = useMemo<CommandItem[]>(
    () => [
      ...APPLICATION_NAV.map((app) => ({
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
    ],
    [],
  );
  const commands = commandsProp ?? defaultCommands;

  const onCommandPalette = useCallback(() => setCommandOpen(true), []);
  const onFocusSearch = useCallback(() => {
    document.getElementById("global-search")?.focus();
  }, []);
  const onShowShortcuts = useCallback(() => setShortcutsOpen(true), []);

  useGlobalKeyboardShortcuts({ onCommandPalette, onFocusSearch, onShowShortcuts });

  return (
    <div className={`mp-shell${navOpen ? " mp-nav-open" : ""}`}>
      <a href="#main-content" className="sr-only">
        {t("shell.skipToContent")}
      </a>
      {navOpen ? (
        <button
          type="button"
          className="mp-nav-backdrop"
          aria-label={t("shell.closeNav")}
          onClick={() => setNavOpen(false)}
        />
      ) : null}
      <header className="mp-shell-header">
        <button
          type="button"
          className="mp-btn mp-nav-toggle"
          aria-label={t("shell.openNav")}
          aria-expanded={navOpen}
          onClick={() => setNavOpen((v) => !v)}
        >
          {t("shell.menu")}
        </button>
        <div className="mp-shell-brand">
          <strong>{t("app.name")}</strong>
        </div>
        <GlobalSearch />
        <div className="mp-shell-actions">
          <button
            type="button"
            className="mp-btn"
            onClick={() => setCommandOpen(true)}
            aria-label={t("shell.commandPalette")}
          >
            ⌘K
          </button>
          <NotificationCenter />
          <HelpButton />
          <AIAssistantPanel />
          <LocaleSwitcher />
          <ThemeToggle />
        </div>
      </header>
      <div className="mp-shell-body">
        {nav ? (
          <aside className="mp-shell-sidebar" id="mp-shell-sidebar">
            {nav}
          </aside>
        ) : null}
        <main id="main-content" className="mp-shell-main">
          {children}
        </main>
      </div>
      <CommandPalette open={commandOpen} onOpenChange={setCommandOpen} items={commands} />
      <KeyboardShortcutsDialog open={shortcutsOpen} onOpenChange={setShortcutsOpen} />
    </div>
  );
}

export function PageLayout({
  title,
  subtitle,
  breadcrumb,
  actions,
  children,
}: {
  title: string;
  subtitle?: string;
  breadcrumb?: BreadcrumbItem[];
  actions?: ReactNode;
  children: ReactNode;
}) {
  return (
    <div className="mp-page">
      <header className="mp-page-header">
        <div>
          {breadcrumb ? <Breadcrumb items={breadcrumb} /> : null}
          <h1>{title}</h1>
          {subtitle ? <p className="mp-page-subtitle">{subtitle}</p> : null}
        </div>
        {actions ? <div className="mp-page-actions">{actions}</div> : null}
      </header>
      <div className="mp-page-content">{children}</div>
    </div>
  );
}
