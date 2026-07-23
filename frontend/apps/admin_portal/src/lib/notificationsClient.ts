import {
  type ApiSession,
  apiGet,
  apiPatch,
  apiPost,
  createClientLogin,
  loadSession as loadNotificationsSession,
  saveSession as saveNotificationsSession,
} from "./clientAuth";

export type { ApiSession };
export const loginNotificationsSession = createClientLogin("Notifications Admin");
export { loadNotificationsSession, saveNotificationsSession };

export type InboxMessage = {
  id: string;
  tenant_id: string;
  user_id: string | null;
  channel: string;
  title: string;
  body: string;
  category: string;
  source_event: string;
  status: string;
  metadata?: Record<string, unknown>;
  created_at: string;
  read_at?: string | null;
};

export type NotificationTemplate = {
  key: string;
  channel: string;
  category: string;
  description: string;
};

export type NotificationDelivery = {
  id: string;
  tenant_id: string;
  channel: string;
  recipient: string;
  template_key: string;
  source_event: string;
  status: string;
  error?: string | null;
  created_at: string;
  delivered_at?: string | null;
};

export type SendNotificationPayload = {
  channel: "inbox" | "email";
  title: string;
  body: string;
  category?: string;
  user_id?: string | null;
  recipient_email?: string | null;
};

export async function listInbox(
  session: ApiSession,
  unreadOnly = false,
): Promise<InboxMessage[]> {
  const q = unreadOnly ? "?unread_only=true" : "";
  return apiGet(`/api/v1/notifications/inbox${q}`, session);
}

export async function markInboxRead(
  session: ApiSession,
  messageId: string,
): Promise<InboxMessage> {
  return apiPatch(`/api/v1/notifications/inbox/${encodeURIComponent(messageId)}/read`, session, {});
}

export async function sendNotification(
  session: ApiSession,
  payload: SendNotificationPayload,
): Promise<{ inbox?: InboxMessage; delivery?: NotificationDelivery }> {
  return apiPost("/api/v1/notifications/send", session, payload);
}

export async function listTemplates(session: ApiSession): Promise<NotificationTemplate[]> {
  return apiGet("/api/v1/notifications/templates", session);
}

export async function listDeliveries(session: ApiSession): Promise<NotificationDelivery[]> {
  return apiGet("/api/v1/notifications/deliveries", session);
}
