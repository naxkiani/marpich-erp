"use client";

import { useEffect, useState } from "react";
import { useLocale } from "../i18n/LocaleProvider";
import { getPlatformAuthHeaders, platformApiUrl } from "../platform/session";

type Notification = { id: string; title: string; body?: string; read?: boolean; status?: string };

export function NotificationCenter() {
  const { t } = useLocale();
  const [open, setOpen] = useState(false);
  const [items, setItems] = useState<Notification[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    const headers = getPlatformAuthHeaders();
    if (!headers) {
      setItems([]);
      setError("Sign in to view notifications.");
      return;
    }
    setError(null);
    fetch(platformApiUrl("/api/v1/notifications/inbox"), { headers, credentials: "same-origin" })
      .then(async (r) => {
        if (!r.ok) throw new Error(`inbox ${r.status}`);
        return r.json();
      })
      .then((payload) => {
        const raw = Array.isArray(payload) ? payload : payload.data ?? payload.items ?? [];
        const list = (Array.isArray(raw) ? raw : []).map((n: Notification) => ({
          ...n,
          read: n.read ?? n.status === "read",
        }));
        setItems(list);
      })
      .catch(() => {
        setItems([]);
        setError("Unable to load notifications.");
      });
  }, [open]);

  async function markRead(id: string) {
    const headers = getPlatformAuthHeaders();
    if (!headers) return;
    await fetch(platformApiUrl(`/api/v1/notifications/inbox/${encodeURIComponent(id)}/read`), {
      method: "PATCH",
      headers,
      credentials: "same-origin",
    }).catch(() => undefined);
    setItems((prev) => prev.map((n) => (n.id === id ? { ...n, read: true, status: "read" } : n)));
  }

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
        <span aria-hidden="true">●</span>
        {unread > 0 ? <span className="mp-badge">{unread}</span> : null}
      </button>
      {open ? (
        <div className="mp-panel mp-animate-in" role="region" aria-label={t("shell.notifications")}>
          <header className="mp-panel-header">
            <span>{t("shell.notifications")}</span>
            <a className="mp-link" href="/enterprise/notifications">
              Open desk
            </a>
          </header>
          {error ? <p className="mp-search-muted">{error}</p> : null}
          <ul>
            {items.map((n) => (
              <li key={n.id}>
                <button type="button" className="mp-search-hit" onClick={() => void markRead(n.id)}>
                  <strong>{n.title}</strong>
                  {n.body ? <span>{n.body}</span> : null}
                </button>
              </li>
            ))}
            {!error && items.length === 0 ? (
              <li className="mp-search-muted">Inbox empty</li>
            ) : null}
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
      const headers = getPlatformAuthHeaders();
      if (!headers) {
        throw new Error("Sign in required for AI Copilot.");
      }
      const res = await fetch(platformApiUrl("/api/v1/ai/assist"), {
        method: "POST",
        headers,
        credentials: "same-origin",
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
        {t("shell.ai")}
      </button>
      {open ? (
        <aside className="mp-ai-panel mp-animate-in" aria-label={t("shell.ai")}>
          <header>{t("shell.ai")}</header>
          <p className="mp-field-help" role="note">
            {t("shell.ai.disclaimer")}
          </p>
          <textarea
            className="mp-textarea"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder={t("shell.ai.placeholder")}
            rows={4}
            disabled={loading}
          />
          <button
            type="button"
            className="mp-btn mp-btn-primary"
            disabled={!prompt.trim() || loading}
            onClick={() => void onSend()}
          >
            {loading ? t("shell.ai.sending") : t("shell.ai.send")}
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
