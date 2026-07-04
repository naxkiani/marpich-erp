"use client";

import { useEffect, useState } from "react";
import { useLocale } from "../i18n/LocaleProvider";

const SHORTCUTS = [
  { keys: "⌘/Ctrl + K", action: "Command palette" },
  { keys: "⌘/Ctrl + /", action: "Focus search" },
  { keys: "?", action: "Show shortcuts" },
  { keys: "⌘/Ctrl + S", action: "Save form" },
  { keys: "Esc", action: "Close panel" },
];

export function KeyboardShortcutsDialog({
  open,
  onOpenChange,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}) {
  const { t } = useLocale();
  if (!open) return null;

  return (
    <div className="mp-overlay" role="presentation" onClick={() => onOpenChange(false)}>
      <div
        className="mp-shortcuts-dialog mp-animate-in"
        role="dialog"
        aria-label={t("shell.shortcuts")}
        onClick={(e) => e.stopPropagation()}
      >
        <header>
          <h2>{t("shell.shortcuts")}</h2>
          <button type="button" className="mp-icon-btn" aria-label="Close" onClick={() => onOpenChange(false)}>
            ×
          </button>
        </header>
        <table>
          <tbody>
            {SHORTCUTS.map((s) => (
              <tr key={s.keys}>
                <td>
                  <kbd>{s.keys}</kbd>
                </td>
                <td>{s.action}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export function useGlobalKeyboardShortcuts(handlers: {
  onCommandPalette: () => void;
  onFocusSearch: () => void;
  onShowShortcuts: () => void;
}) {
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      const mod = e.metaKey || e.ctrlKey;
      if (mod && e.key.toLowerCase() === "k") {
        e.preventDefault();
        handlers.onCommandPalette();
      }
      if (mod && e.key === "/") {
        e.preventDefault();
        handlers.onFocusSearch();
      }
      if (e.key === "?" && !e.metaKey && !e.ctrlKey && !e.altKey) {
        const tag = (e.target as HTMLElement)?.tagName;
        if (tag === "INPUT" || tag === "TEXTAREA") return;
        e.preventDefault();
        handlers.onShowShortcuts();
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [handlers]);
}

export function useAutosave<T>(
  value: T,
  onSave: (value: T) => void | Promise<void>,
  delayMs = 800,
) {
  const [saving, setSaving] = useState(false);
  const [savedAt, setSavedAt] = useState<Date | null>(null);

  useEffect(() => {
    const timer = window.setTimeout(async () => {
      setSaving(true);
      try {
        await onSave(value);
        setSavedAt(new Date());
      } finally {
        setSaving(false);
      }
    }, delayMs);
    return () => window.clearTimeout(timer);
  }, [value, onSave, delayMs]);

  return { saving, savedAt };
}
