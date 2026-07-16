"use client";

import { PageLayout } from "@marpich/core";
import { DataTable, EmptyState, ProgressBar, SkeletonTable, useToast } from "@marpich/shared";
import { useCallback, useEffect, useState } from "react";
import {
  encryptDemoCiphertext,
  issueLiveKitToken,
  listMessengerMessages,
  loadMessengerSession,
  loginMessengerSession,
  openMessengerConversation,
  saveMessengerSession,
  sendMessengerMessage,
  type ApiSession,
  type MessengerMessage,
} from "@/lib/messengerClient";

export function MessengerCarePage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("messenger-demo");
  const [email, setEmail] = useState("messenger@demo.dev");
  const [password, setPassword] = useState("SecurePass123!");

  const [conversationId, setConversationId] = useState("");
  const [e2ee, setE2ee] = useState(true);
  const [livekitToken, setLivekitToken] = useState("");
  const [livekitSimulated, setLivekitSimulated] = useState(true);
  const [livekitRoom, setLivekitRoom] = useState("");
  const [passphrase, setPassphrase] = useState("demo-e2ee-passphrase");
  const [draft, setDraft] = useState("Hello secure room");
  const [messages, setMessages] = useState<MessengerMessage[]>([]);

  const refreshMessages = useCallback(
    async (active: ApiSession, cid: string) => {
      if (!cid) return;
      const rows = await listMessengerMessages(active, cid);
      setMessages(rows);
    },
    [],
  );

  useEffect(() => {
    const existing = loadMessengerSession();
    if (!existing) {
      setLoading(false);
      return;
    }
    setSession(existing);
    setTenantId(existing.tenantId);
    setLoading(false);
    setProgress(100);
  }, []);

  async function onLogin() {
    try {
      const next = await loginMessengerSession(tenantId, email, password);
      saveMessengerSession(next);
      setSession(next);
      push({ message: `Connected to messenger tenant ${next.tenantId}` });
      setProgress(100);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    }
  }

  async function onOpen() {
    if (!session) return;
    setProgress(50);
    try {
      const conv = await openMessengerConversation(session, {
        title: "Ops room",
        member_ids: ["peer-demo"],
        e2ee_enabled: e2ee,
        issue_livekit_token: true,
      });
      setConversationId(conv.id);
      setLivekitToken(String(conv.livekit_token || ""));
      setLivekitSimulated(Boolean(conv.livekit_simulated));
      setLivekitRoom(String(conv.livekit_room_name || ""));
      push({
        message: conv.livekit_simulated
          ? "Conversation opened (LiveKit simulated)"
          : "Conversation opened (LiveKit JWT)",
      });
      await refreshMessages(session, conv.id);
      setProgress(100);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Open failed" });
      setProgress(100);
    }
  }

  async function onSend() {
    if (!session || !conversationId) return;
    try {
      if (e2ee) {
        const ciphertext = await encryptDemoCiphertext(draft, passphrase);
        await sendMessengerMessage(session, conversationId, {
          ciphertext,
          ciphertext_type: "application/x-marpich-e2ee",
        });
      } else {
        await sendMessengerMessage(session, conversationId, { body: draft });
      }
      push({ message: e2ee ? "Ciphertext stored (server never saw plaintext)" : "Message sent" });
      await refreshMessages(session, conversationId);
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Send failed" });
    }
  }

  async function onToken() {
    if (!session || !conversationId) return;
    try {
      const tok = await issueLiveKitToken(session, conversationId);
      setLivekitToken(tok.token);
      setLivekitSimulated(tok.simulated);
      setLivekitRoom(tok.room_name);
      push({
        message: tok.simulated ? "Simulated LiveKit token" : "Real LiveKit AccessToken issued",
      });
    } catch (err) {
      push({ message: err instanceof Error ? err.message : "Token failed" });
    }
  }

  return (
    <PageLayout
      title="Messenger"
      subtitle="P5.3 — client E2EE ciphertext + LiveKit AccessToken via Integration connector."
      breadcrumb={[{ label: "Enterprise", href: "/enterprise/document-studio" }, { label: "Messenger" }]}
    >
      <ProgressBar value={progress} label="Loading messenger" />

      {!session ? (
        <section className="mp-stack" aria-label="Sign in">
          <h2>Session</h2>
          <label>
            Tenant
            <input value={tenantId} onChange={(e) => setTenantId(e.target.value)} />
          </label>
          <label>
            Email
            <input value={email} onChange={(e) => setEmail(e.target.value)} />
          </label>
          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <button type="button" className="mp-btn" onClick={() => void onLogin()}>
            Sign in
          </button>
        </section>
      ) : null}

      {error ? <p role="alert">{error}</p> : null}

      {loading ? (
        <SkeletonTable rows={3} />
      ) : session ? (
        <>
          <section className="mp-stack" aria-label="Conversation">
            <h2>Open conversation</h2>
            <label>
              <input
                type="checkbox"
                checked={e2ee}
                onChange={(e) => setE2ee(e.target.checked)}
              />{" "}
              E2EE (client ciphertext)
            </label>
            <label>
              Demo passphrase
              <input value={passphrase} onChange={(e) => setPassphrase(e.target.value)} />
            </label>
            <div className="mp-row">
              <button type="button" className="mp-btn" onClick={() => void onOpen()}>
                Open + LiveKit token
              </button>
              <button
                type="button"
                className="mp-btn"
                onClick={() => void onToken()}
                disabled={!conversationId}
              >
                Refresh LiveKit token
              </button>
            </div>
            {conversationId ? (
              <p>
                Conversation <code>{conversationId.slice(0, 8)}</code> · room{" "}
                <code>{livekitRoom || "—"}</code> ·{" "}
                {livekitSimulated ? "simulated" : "real JWT"}
              </p>
            ) : null}
            {livekitToken ? (
              <p>
                Token preview: <code>{livekitToken.slice(0, 28)}…</code>
              </p>
            ) : null}
          </section>

          <section className="mp-stack" aria-label="Compose">
            <h2>Send</h2>
            <label>
              Message
              <textarea value={draft} onChange={(e) => setDraft(e.target.value)} rows={3} />
            </label>
            <button
              type="button"
              className="mp-btn"
              onClick={() => void onSend()}
              disabled={!conversationId}
            >
              {e2ee ? "Encrypt & send" : "Send plaintext"}
            </button>
          </section>

          {messages.length === 0 ? (
            <EmptyState
              title="No messages"
              description="Open a conversation and send ciphertext (E2EE) or plaintext."
            />
          ) : (
            <DataTable
              columns={[
                { key: "created_at", header: "When" },
                { key: "payload", header: "Payload" },
                { key: "kind", header: "Kind" },
              ]}
              rows={messages.map((m) => ({
                id: m.id,
                created_at: m.created_at.slice(0, 19),
                payload: m.ciphertext
                  ? `${m.ciphertext.slice(0, 40)}…`
                  : m.body,
                kind: m.ciphertext ? "ciphertext" : "plaintext",
              }))}
            />
          )}
        </>
      ) : null}
    </PageLayout>
  );
}
