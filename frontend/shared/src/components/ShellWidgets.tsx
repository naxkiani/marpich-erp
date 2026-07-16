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
  const [reply, setReply] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSend() {
    const text = prompt.trim();
    if (!text || loading) return;
    setLoading(true);
    setError(null);
    setReply(null);
    try {
      const tenantId =
        (typeof window !== "undefined" &&
          (localStorage.getItem("marpich.tenantId") ||
            localStorage.getItem("tenantId") ||
            "demo")) ||
        "demo";
      const token =
        typeof window !== "undefined"
          ? localStorage.getItem("marpich.accessToken") ||
            localStorage.getItem("access_token") ||
            ""
          : "";
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
        "X-Tenant-ID": tenantId,
      };
      if (token) headers.Authorization = `Bearer ${token}`;
      const res = await fetch(`${API_URL}/api/v1/ai/assist`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          module_id: "platform",
          surface: "assistant",
          prompt: text,
        }),
      });
      if (!res.ok) {
        const body = await res.text();
        throw new Error(body || `AI assist failed (${res.status})`);
      }
      const json = (await res.json()) as { data?: { reply?: string } };
      setReply(json.data?.reply ?? "No reply returned.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "AI assist failed");
    } finally {
      setLoading(false);
    }
  }

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
            disabled={loading}
          />
          <button
            type="button"
            className="mp-btn mp-btn-primary"
            disabled={!prompt.trim() || loading}
            onClick={() => void onSend()}
          >
            {loading ? "Sending…" : "Send"}
          </button>
          {error ? (
            <p role="alert" className="mp-error">
              {error}
            </p>
          ) : null}
          {reply ? <pre className="mp-ai-reply">{reply}</pre> : null}
        </aside>
      ) : null}
    </>
  );
}
