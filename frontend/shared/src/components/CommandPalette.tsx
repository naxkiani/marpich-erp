"use client";

import { useEffect, useMemo, useState } from "react";
import { useLocale } from "../i18n/LocaleProvider";

export type CommandItem = {
  id: string;
  label: string;
  group?: string;
  shortcut?: string;
  onSelect: () => void;
};

export function CommandPalette({
  open,
  onOpenChange,
  items,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  items: CommandItem[];
}) {
  const { t } = useLocale();
  const [query, setQuery] = useState("");

  useEffect(() => {
    if (!open) setQuery("");
  }, [open]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return items;
    return items.filter((item) => item.label.toLowerCase().includes(q));
  }, [items, query]);

  if (!open) return null;

  return (
    <div className="mp-overlay" role="presentation" onClick={() => onOpenChange(false)}>
      <div
        className="mp-command-palette mp-animate-in"
        role="dialog"
        aria-label={t("shell.commandPalette")}
        onClick={(e) => e.stopPropagation()}
      >
        <input
          autoFocus
          className="mp-input mp-command-input"
          placeholder={t("shell.commandPalette")}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <ul className="mp-command-list" role="listbox">
          {filtered.map((item) => (
            <li key={item.id}>
              <button
                type="button"
                className="mp-command-item"
                onClick={() => {
                  item.onSelect();
                  onOpenChange(false);
                }}
              >
                <span>{item.label}</span>
                {item.shortcut ? <kbd>{item.shortcut}</kbd> : null}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
