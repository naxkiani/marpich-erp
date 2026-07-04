"use client";

import {
  AIAssistantPanel,
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
}: {
  children: ReactNode;
  nav?: ReactNode;
}) {
  const { t } = useLocale();
  const [commandOpen, setCommandOpen] = useState(false);
  const [shortcutsOpen, setShortcutsOpen] = useState(false);

  const commands = useMemo<CommandItem[]>(
    () => [
      {
        id: "home",
        label: "Go to Dashboard",
        shortcut: "G D",
        onSelect: () => {
          window.location.href = "/";
        },
      },
      {
        id: "theme",
        label: "Toggle theme",
        onSelect: () => document.documentElement.dataset.theme === "dark"
          ? (document.documentElement.dataset.theme = "light")
          : (document.documentElement.dataset.theme = "dark"),
      },
    ],
    [],
  );

  const onCommandPalette = useCallback(() => setCommandOpen(true), []);
  const onFocusSearch = useCallback(() => {
    document.getElementById("global-search")?.focus();
  }, []);
  const onShowShortcuts = useCallback(() => setShortcutsOpen(true), []);

  useGlobalKeyboardShortcuts({ onCommandPalette, onFocusSearch, onShowShortcuts });

  return (
    <div className="mp-shell">
      <a href="#main-content" className="sr-only">
        Skip to content
      </a>
      <header className="mp-shell-header">
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
        {nav ? <aside className="mp-shell-sidebar">{nav}</aside> : null}
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
  breadcrumb,
  actions,
  children,
}: {
  title: string;
  breadcrumb: BreadcrumbItem[];
  actions?: ReactNode;
  children: ReactNode;
}) {
  return (
    <div className="mp-page mp-animate-in">
      <header className="mp-page-header">
        <div>
          <Breadcrumb items={breadcrumb} />
          <h1>{title}</h1>
        </div>
        {actions ? <div className="mp-page-actions">{actions}</div> : null}
      </header>
      <div className="mp-page-content">{children}</div>
    </div>
  );
}
