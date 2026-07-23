"use client";

import { PageLayout } from "@marpich/core";
import {
  AdvancedFilterBar,
  DataTable,
  EmptyState,
  ExportButton,
  PrintButton,
  ProgressBar,
  SkeletonTable,
  StepProgress,
  useAutosave,
  useLocale,
  useToast,
} from "@marpich/shared";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  listDeliveries,
  listInbox,
  listTemplates,
  loadNotificationsSession,
  loginNotificationsSession,
  markInboxRead,
  saveNotificationsSession,
  sendNotification,
  type ApiSession,
  type InboxMessage,
  type NotificationDelivery,
  type NotificationTemplate,
} from "@/lib/notificationsClient";

const DRAFT_KEY = "marpich.notifications.desk.draft";

type TabId = "inbox" | "compose" | "templates" | "deliveries";

function StatusChip({ status }: { status: string }) {
  const tone =
    status === "unread" || status === "pending"
      ? "warn"
      : status === "read" || status === "sent" || status === "ok"
        ? "ok"
        : status === "failed"
          ? "bad"
          : "muted";
  return (
    <span className={`ntf-chip ntf-chip--${tone}`} data-status={status}>
      {status}
    </span>
  );
}

export function NotificationsDeskPage() {
  const { push } = useToast();
  const { t } = useLocale();
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState(20);
  const [error, setError] = useState<string | null>(null);
  const [session, setSession] = useState<ApiSession | null>(null);
  const [tenantId, setTenantId] = useState("notifications-demo");
  const [email, setEmail] = useState("notify@demo.dev");
  const [password, setPassword] = useState("SecurePass123!");
  const [tab, setTab] = useState<TabId>("inbox");
  const [filterQ, setFilterQ] = useState("");
  const [unreadOnly, setUnreadOnly] = useState(false);
  const [draftReady, setDraftReady] = useState(false);
  const [lastAction, setLastAction] = useState<string | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const [inbox, setInbox] = useState<InboxMessage[]>([]);
  const [templates, setTemplates] = useState<NotificationTemplate[]>([]);
  const [deliveries, setDeliveries] = useState<NotificationDelivery[]>([]);

  const [channel, setChannel] = useState<"inbox" | "email">("inbox");
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [category, setCategory] = useState("general");
  const [recipientEmail, setRecipientEmail] = useState("");

  const formDraft = useMemo(
    () => ({
      filterQ,
      unreadOnly,
      tab,
      channel,
      title,
      body,
      category,
      recipientEmail,
    }),
    [body, category, channel, filterQ, recipientEmail, tab, title, unreadOnly],
  );

  const persistDraft = useCallback(
    async (values: typeof formDraft) => {
      if (!draftReady) return;
      try {
        localStorage.setItem(DRAFT_KEY, JSON.stringify(values));
      } catch {
        /* ignore */
      }
    },
    [draftReady],
  );

  const { saving: draftSaving } = useAutosave(formDraft, persistDraft, 900);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(DRAFT_KEY);
      if (raw) {
        const parsed = JSON.parse(raw) as Partial<typeof formDraft>;
        if (typeof parsed.filterQ === "string") setFilterQ(parsed.filterQ);
        if (typeof parsed.unreadOnly === "boolean") setUnreadOnly(parsed.unreadOnly);
        if (
          parsed.tab === "inbox" ||
          parsed.tab === "compose" ||
          parsed.tab === "templates" ||
          parsed.tab === "deliveries"
        ) {
          setTab(parsed.tab);
        }
        if (parsed.channel === "inbox" || parsed.channel === "email") setChannel(parsed.channel);
        if (typeof parsed.title === "string") setTitle(parsed.title);
        if (typeof parsed.body === "string") setBody(parsed.body);
        if (typeof parsed.category === "string" && parsed.category.trim()) {
          setCategory(parsed.category);
        }
        if (typeof parsed.recipientEmail === "string") setRecipientEmail(parsed.recipientEmail);
      }
    } catch {
      /* ignore */
    } finally {
      setDraftReady(true);
    }
  }, []);

  const loadData = useCallback(
    async (active: ApiSession, preferUnread = unreadOnly) => {
      setLoading(true);
      setProgress(40);
      setError(null);
      try {
        const [messages, tpl, dels] = await Promise.all([
          listInbox(active, preferUnread),
          listTemplates(active).catch(() => [] as NotificationTemplate[]),
          listDeliveries(active).catch(() => [] as NotificationDelivery[]),
        ]);
        setInbox(messages);
        setTemplates(tpl);
        setDeliveries(dels);
        setSelectedId((prev) => {
          if (prev && messages.some((m) => m.id === prev)) return prev;
          return messages[0]?.id ?? null;
        });
        setProgress(100);
      } catch (err) {
        setError(err instanceof Error ? err.message : t("notifications.loadFailed"));
        setProgress(100);
      } finally {
        setLoading(false);
      }
    },
    [t, unreadOnly],
  );

  useEffect(() => {
    const existing = loadNotificationsSession();
    if (!existing) {
      setLoading(false);
      setProgress(100);
      return;
    }
    setSession(existing);
    setTenantId(existing.tenantId);
    void loadData(existing);
    // eslint-disable-next-line react-hooks/exhaustive-deps -- mount once
  }, []);

  const unreadCount = useMemo(
    () => inbox.filter((m) => m.status === "unread").length,
    [inbox],
  );

  const lifecycleStep = useMemo(() => {
    if (!session) return 0;
    if (inbox.length === 0 && deliveries.length === 0) return 1;
    if (tab === "compose" && title.trim() && body.trim()) return 2;
    if (deliveries.length > 0 || lastAction === "send") return 3;
    return 1;
  }, [body, deliveries.length, inbox.length, lastAction, session, tab, title]);

  const workflowSteps = useMemo(
    () => [
      { id: "connect", label: t("notifications.step.connect") },
      { id: "browse", label: t("notifications.step.browse") },
      { id: "compose", label: t("notifications.step.compose") },
      { id: "deliver", label: t("notifications.step.deliver") },
    ],
    [t],
  );

  const q = filterQ.toLowerCase().trim();

  const inboxRows = useMemo(
    () =>
      inbox
        .filter((m) => {
          if (!q) return true;
          const hay = `${m.title} ${m.body} ${m.category} ${m.status}`.toLowerCase();
          return hay.includes(q);
        })
        .map((m) => ({
          id: m.id,
          title: m.title,
          category: m.category,
          status: m.status,
          channel: m.channel,
          created: m.created_at.slice(0, 19).replace("T", " "),
        })),
    [inbox, q],
  );

  const templateRows = useMemo(
    () =>
      templates
        .filter((tpl) => {
          if (!q) return true;
          const hay = `${tpl.key} ${tpl.category} ${tpl.description}`.toLowerCase();
          return hay.includes(q);
        })
        .map((tpl) => ({
          id: tpl.key,
          key: tpl.key,
          channel: tpl.channel,
          category: tpl.category,
          description: tpl.description,
        })),
    [q, templates],
  );

  const deliveryRows = useMemo(
    () =>
      deliveries
        .filter((d) => {
          if (!q) return true;
          const hay = `${d.channel} ${d.recipient} ${d.template_key} ${d.status}`.toLowerCase();
          return hay.includes(q);
        })
        .map((d) => ({
          id: d.id,
          channel: d.channel,
          recipient: d.recipient,
          template: d.template_key,
          status: d.status,
          created: d.created_at.slice(0, 19).replace("T", " "),
        })),
    [deliveries, q],
  );

  const selectedMessage = useMemo(
    () => inbox.find((m) => m.id === selectedId) ?? null,
    [inbox, selectedId],
  );

  const exportRows = useMemo(() => {
    if (tab === "templates") return templateRows;
    if (tab === "deliveries") return deliveryRows;
    return inboxRows;
  }, [deliveryRows, inboxRows, tab, templateRows]);

  async function onConnect() {
    setBusy(true);
    setError(null);
    try {
      const next = await loginNotificationsSession(tenantId, email, password);
      saveNotificationsSession(next);
      setSession(next);
      setLastAction("connect");
      push({ message: t("notifications.connected") });
      await loadData(next);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("notifications.connectFailed"));
    } finally {
      setBusy(false);
    }
  }

  async function onRefresh() {
    if (!session) return;
    await loadData(session, unreadOnly);
    setLastAction("refresh");
  }

  async function onMarkRead(messageId: string) {
    if (!session) return;
    try {
      await markInboxRead(session, messageId);
      setLastAction("mark_read");
      push({ message: t("notifications.markedRead") });
      await loadData(session, unreadOnly);
    } catch (err) {
      push({
        message: err instanceof Error ? err.message : t("notifications.markReadFailed"),
      });
    }
  }

  async function onSend() {
    if (!session) return;
    if (!title.trim() || !body.trim()) {
      push({ message: t("notifications.composeRequired") });
      return;
    }
    if (channel === "email" && !recipientEmail.trim()) {
      push({ message: t("notifications.emailRequired") });
      return;
    }
    setBusy(true);
    try {
      await sendNotification(session, {
        channel,
        title: title.trim(),
        body: body.trim(),
        category: category.trim() || "general",
        user_id: null,
        recipient_email: channel === "email" ? recipientEmail.trim() : null,
      });
      setLastAction("send");
      push({ message: t("notifications.sent") });
      setTab("inbox");
      await loadData(session, unreadOnly);
    } catch (err) {
      push({
        message: err instanceof Error ? err.message : t("notifications.sendFailed"),
      });
    } finally {
      setBusy(false);
    }
  }

  function applyTemplate(tpl: NotificationTemplate) {
    setChannel(tpl.channel === "email" ? "email" : "inbox");
    setCategory(tpl.category || "general");
    setTitle(tpl.description || tpl.key);
    setBody(`${tpl.description} (${tpl.key})`);
    setTab("compose");
    setLastAction("template");
  }

  const stats = [
    { label: t("notifications.stat.inbox"), value: inbox.length },
    { label: t("notifications.stat.unread"), value: unreadCount },
    { label: t("notifications.stat.templates"), value: templates.length },
    { label: t("notifications.stat.deliveries"), value: deliveries.length },
  ];

  return (
    <PageLayout
      title={t("notifications.title")}
      subtitle={t("notifications.subtitle")}
      breadcrumb={[
        { label: t("app.name"), href: "/" },
        { label: t("notifications.breadcrumb") },
        { label: t("notifications.title") },
      ]}
      actions={
        <>
          <ExportButton rows={exportRows} filename="notifications-desk" />
          <PrintButton />
          {session ? (
            <button type="button" className="mp-btn" onClick={() => void onRefresh()} disabled={loading}>
              {t("notifications.refresh")}
            </button>
          ) : null}
        </>
      }
    >
      <ProgressBar
        value={progress}
        label={loading ? t("notifications.loading") : t("notifications.ready")}
      />

      {!session ? (
        <section className="ntf-connect" aria-label={t("notifications.connect")}>
          <p className="mp-field-help">{t("notifications.connectHint")}</p>
          <div className="ntf-connect-form">
            <label>
              {t("notifications.field.tenant")}
              <input
                className="mp-input"
                value={tenantId}
                onChange={(e) => setTenantId(e.target.value)}
                autoComplete="organization"
              />
            </label>
            <label>
              {t("notifications.field.email")}
              <input
                className="mp-input"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="username"
              />
            </label>
            <label>
              {t("notifications.field.password")}
              <input
                className="mp-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
              />
            </label>
            <button
              type="button"
              className="mp-btn mp-btn-primary"
              disabled={busy}
              onClick={() => void onConnect()}
            >
              {busy ? t("notifications.connecting") : t("notifications.connect")}
            </button>
          </div>
          {error ? (
            <p className="mp-field-help" role="alert">
              {error}
            </p>
          ) : null}
        </section>
      ) : (
        <div className="ntf-layout">
          <aside className="ntf-aside" aria-label={t("notifications.rail")}>
            <section className="ntf-panel-card">
              <header className="ntf-panel-head">
                <h2>{t("notifications.workflow")}</h2>
              </header>
              <div className="ntf-panel-body">
                <StepProgress steps={workflowSteps} current={lifecycleStep} />
                {draftSaving ? (
                  <p className="mp-field-help" aria-live="polite">
                    {t("notifications.draftSaved")}…
                  </p>
                ) : (
                  <p className="mp-field-help">{t("notifications.workflowHint")}</p>
                )}
                {lastAction ? (
                  <p className="mp-field-help">
                    {t("notifications.lastAction")}: {lastAction}
                  </p>
                ) : null}
              </div>
            </section>

            <section className="ntf-panel-card">
              <header className="ntf-panel-head">
                <h2>{t("notifications.stats")}</h2>
              </header>
              <div className="ntf-panel-body ntf-stats">
                {stats.map((s) => (
                  <div key={s.label} className="ntf-stat">
                    <span className="ntf-stat-value">{s.value}</span>
                    <span className="ntf-stat-label">{s.label}</span>
                  </div>
                ))}
              </div>
            </section>
          </aside>

          <div className="ntf-main">
            {error ? (
              <p className="mp-field-help" role="alert">
                {error}
              </p>
            ) : null}

            <div className="ntf-tabs" role="tablist" aria-label={t("notifications.tabs")}>
              {(
                [
                  ["inbox", t("notifications.tab.inbox")],
                  ["compose", t("notifications.tab.compose")],
                  ["templates", t("notifications.tab.templates")],
                  ["deliveries", t("notifications.tab.deliveries")],
                ] as const
              ).map(([id, label]) => (
                <button
                  key={id}
                  type="button"
                  role="tab"
                  aria-selected={tab === id}
                  className={`mp-btn${tab === id ? " mp-btn-primary" : ""}`}
                  onClick={() => setTab(id)}
                >
                  {label}
                </button>
              ))}
            </div>

            <div className="ntf-filters">
              <AdvancedFilterBar
                filters={[{ id: "q", label: t("notifications.filterPlaceholder"), type: "text" }]}
                onChange={(values) => setFilterQ(values.q ?? "")}
              />
              {tab === "inbox" ? (
                <label className="mp-filter-item">
                  <span>{t("notifications.filter.unreadOnly")}</span>
                  <select
                    className="mp-input"
                    value={unreadOnly ? "1" : ""}
                    onChange={(e) => {
                      const next = e.target.value === "1";
                      setUnreadOnly(next);
                      if (session) void loadData(session, next);
                    }}
                    aria-label={t("notifications.filter.unreadOnly")}
                  >
                    <option value="">{t("notifications.filter.all")}</option>
                    <option value="1">{t("notifications.filter.unreadOnly")}</option>
                  </select>
                </label>
              ) : null}
            </div>

            {tab === "inbox" ? (
              loading ? (
                <SkeletonTable rows={6} cols={5} />
              ) : inboxRows.length === 0 ? (
                <EmptyState
                  title={t("notifications.empty.inbox")}
                  description={t("notifications.empty.inboxHint")}
                />
              ) : (
                <div className="ntf-split">
                  <DataTable
                    columns={[
                      { key: "title", header: t("notifications.col.title"), sortable: true },
                      { key: "category", header: t("notifications.col.category"), sortable: true },
                      {
                        key: "status",
                        header: t("notifications.col.status"),
                        sortable: true,
                        render: (row) => <StatusChip status={String(row.status)} />,
                      },
                      { key: "created", header: t("notifications.col.created"), sortable: true },
                    ]}
                    rows={inboxRows}
                    selectable
                    onSelectionChange={(ids) => {
                      if (ids[0]) setSelectedId(ids[0]);
                    }}
                  />
                  {selectedMessage ? (
                    <article className="ntf-detail" aria-label={t("notifications.detail")}>
                      <header>
                        <h3>{selectedMessage.title}</h3>
                        <StatusChip status={selectedMessage.status} />
                      </header>
                      <p className="mp-field-help">
                        {selectedMessage.category} · {selectedMessage.source_event}
                      </p>
                      <p>{selectedMessage.body}</p>
                      {selectedMessage.status === "unread" ? (
                        <button
                          type="button"
                          className="mp-btn mp-btn-primary"
                          onClick={() => void onMarkRead(selectedMessage.id)}
                        >
                          {t("notifications.markRead")}
                        </button>
                      ) : null}
                    </article>
                  ) : null}
                </div>
              )
            ) : null}

            {tab === "compose" ? (
              <section className="ntf-compose" aria-label={t("notifications.tab.compose")}>
                <label>
                  {t("notifications.field.channel")}
                  <select
                    className="mp-input"
                    value={channel}
                    onChange={(e) => setChannel(e.target.value as "inbox" | "email")}
                  >
                    <option value="inbox">inbox</option>
                    <option value="email">email</option>
                  </select>
                </label>
                <label>
                  {t("notifications.field.category")}
                  <input
                    className="mp-input"
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                  />
                </label>
                <label>
                  {t("notifications.field.title")}
                  <input className="mp-input" value={title} onChange={(e) => setTitle(e.target.value)} />
                </label>
                <label>
                  {t("notifications.field.body")}
                  <textarea
                    className="mp-input"
                    rows={5}
                    value={body}
                    onChange={(e) => setBody(e.target.value)}
                  />
                </label>
                {channel === "email" ? (
                  <label>
                    {t("notifications.field.recipientEmail")}
                    <input
                      className="mp-input"
                      type="email"
                      value={recipientEmail}
                      onChange={(e) => setRecipientEmail(e.target.value)}
                    />
                  </label>
                ) : null}
                <button
                  type="button"
                  className="mp-btn mp-btn-primary"
                  disabled={busy}
                  onClick={() => void onSend()}
                >
                  {busy ? t("notifications.sending") : t("notifications.send")}
                </button>
              </section>
            ) : null}

            {tab === "templates" ? (
              loading ? (
                <SkeletonTable rows={5} cols={4} />
              ) : templateRows.length === 0 ? (
                <EmptyState title={t("notifications.empty.templates")} />
              ) : (
                <DataTable
                  columns={[
                    { key: "key", header: t("notifications.col.key"), sortable: true },
                    { key: "channel", header: t("notifications.col.channel"), sortable: true },
                    { key: "category", header: t("notifications.col.category"), sortable: true },
                    {
                      key: "description",
                      header: t("notifications.col.description"),
                      sortable: true,
                    },
                    {
                      key: "actions",
                      header: t("notifications.col.actions"),
                      render: (row) => {
                        const tpl = templates.find((x) => x.key === String(row.id));
                        if (!tpl) return null;
                        return (
                          <button
                            type="button"
                            className="mp-btn"
                            onClick={() => applyTemplate(tpl)}
                          >
                            {t("notifications.useTemplate")}
                          </button>
                        );
                      },
                    },
                  ]}
                  rows={templateRows}
                />
              )
            ) : null}

            {tab === "deliveries" ? (
              loading ? (
                <SkeletonTable rows={5} cols={5} />
              ) : deliveryRows.length === 0 ? (
                <EmptyState
                  title={t("notifications.empty.deliveries")}
                  description={t("notifications.empty.deliveriesHint")}
                />
              ) : (
                <DataTable
                  columns={[
                    { key: "channel", header: t("notifications.col.channel"), sortable: true },
                    { key: "recipient", header: t("notifications.col.recipient"), sortable: true },
                    { key: "template", header: t("notifications.col.template"), sortable: true },
                    {
                      key: "status",
                      header: t("notifications.col.status"),
                      sortable: true,
                      render: (row) => <StatusChip status={String(row.status)} />,
                    },
                    { key: "created", header: t("notifications.col.created"), sortable: true },
                  ]}
                  rows={deliveryRows}
                />
              )
            ) : null}
          </div>
        </div>
      )}

      <style jsx>{`
        .ntf-connect {
          max-width: 28rem;
          margin-top: 1rem;
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .ntf-connect-form {
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
        }
        .ntf-layout {
          display: grid;
          grid-template-columns: minmax(220px, 280px) minmax(0, 1fr);
          gap: 1.25rem;
          margin-top: 1rem;
          align-items: start;
        }
        .ntf-aside {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .ntf-panel-card {
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: 0.5rem;
          background: var(--mp-surface, #fff);
        }
        .ntf-panel-head {
          padding: 0.75rem 1rem;
          border-bottom: 1px solid var(--mp-border, #d8dee6);
        }
        .ntf-panel-head h2 {
          margin: 0;
          font-size: 0.95rem;
        }
        .ntf-panel-body {
          padding: 0.85rem 1rem;
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
        }
        .ntf-stats {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 0.75rem;
        }
        .ntf-stat {
          display: flex;
          flex-direction: column;
          gap: 0.15rem;
        }
        .ntf-stat-value {
          font-size: 1.25rem;
          font-weight: 600;
        }
        .ntf-stat-label {
          font-size: 0.8rem;
          color: var(--mp-muted, #667085);
        }
        .ntf-main {
          min-width: 0;
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .ntf-tabs {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .ntf-filters {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
          align-items: end;
        }
        .ntf-split {
          display: grid;
          grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr);
          gap: 1rem;
          align-items: start;
        }
        .ntf-detail {
          border: 1px solid var(--mp-border, #d8dee6);
          border-radius: 0.5rem;
          padding: 1rem;
          background: var(--mp-surface, #fff);
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
        }
        .ntf-detail header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 0.5rem;
        }
        .ntf-detail h3 {
          margin: 0;
          font-size: 1rem;
        }
        .ntf-compose {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
          max-width: 36rem;
        }
        :global(.ntf-chip) {
          display: inline-block;
          padding: 0.15rem 0.45rem;
          border-radius: 0.25rem;
          font-size: 0.75rem;
          text-transform: lowercase;
        }
        :global(.ntf-chip--ok) {
          background: color-mix(in srgb, #12b76a 18%, transparent);
          color: #027a48;
        }
        :global(.ntf-chip--warn) {
          background: color-mix(in srgb, #f79009 18%, transparent);
          color: #b54708;
        }
        :global(.ntf-chip--bad) {
          background: color-mix(in srgb, #f04438 18%, transparent);
          color: #b42318;
        }
        :global(.ntf-chip--muted) {
          background: color-mix(in srgb, #98a2b3 18%, transparent);
          color: #475467;
        }
        @media (max-width: 960px) {
          .ntf-layout,
          .ntf-split {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </PageLayout>
  );
}
