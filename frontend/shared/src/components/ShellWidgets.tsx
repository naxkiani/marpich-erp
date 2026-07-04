"use client";

import { useEffect, useState } from "react";
import { useLocale } from "../i18n/LocaleProvider";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

type Notification = { id: string; title: string; body?: string; read?: boolean };

export function NotificationCenter() {
  const { t } = useLocale();
  const [open, setOpen] = useState(false);
  const [items, setItems] = useState<Notification[]>([]);

  useEffect(() => {
    if (!open) return;
    fetch(`${API_URL}/api/v1/notifications/inbox`)
      .then((r) => (r.ok ? r.json() : []))
      .then((data) => setItems(Array.isArray(data) ? data : data.items ?? []))
      .catch(() =>
        setItems([
          { id: "1", title: "Welcome to Marpich", body: "Platform shell is ready." },
        ]),
      );
  }, [open]);

  const unread = items.filter((n) => !n.read).length;

  return (
    <div className="mp-notification-center">
      <button
        type="button"
        className="mp-icon-btn"
        aria-label={t("shell.notifications")}
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
      >
        🔔
        {unread > 0 ? <span className="mp-badge">{unread}</span> : null}
      </button>
      {open ? (
        <div className="mp-panel mp-animate-in" role="region" aria-label={t("shell.notifications")}>
          <header>{t("shell.notifications")}</header>
          <ul>
            {items.map((n) => (
              <li key={n.id}>
                <strong>{n.title}</strong>
                {n.body ? <p>{n.body}</p> : null}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </div>
  );
}

export function HelpButton({ helpUrl = "https://docs.marpich.local" }: { helpUrl?: string }) {
  const { t } = useLocale();
  return (
    <a
      className="mp-icon-btn"
      href={helpUrl}
      target="_blank"
      rel="noreferrer"
      aria-label={t("shell.help")}
      title={t("shell.help")}
    >
      ?
    </a>
  );
}

export function AIAssistantPanel() {
  const { t } = useLocale();
  const [open, setOpen] = useState(false);
  const [prompt, setPrompt] = useState("");

  return (
    <>
      <button
        type="button"
        className="mp-btn mp-btn-accent"
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
      >
        ✨ {t("shell.ai")}
      </button>
      {open ? (
        <aside className="mp-ai-panel mp-animate-in" aria-label={t("shell.ai")}>
          <header>{t("shell.ai")}</header>
          <textarea
            className="mp-textarea"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Ask Marpich AI…"
            rows={4}
          />
          <button type="button" className="mp-btn mp-btn-primary" disabled={!prompt.trim()}>
            Send
          </button>
        </aside>
      ) : null}
    </>
  );
}
