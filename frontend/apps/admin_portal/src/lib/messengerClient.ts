import {
  type ApiSession,
  apiGet,
  apiPost,
  createClientLogin,
  loadSession as loadMessengerSession,
  saveSession as saveMessengerSession,
} from "./clientAuth";

export type { ApiSession };
export const loginMessengerSession = createClientLogin("Messenger Admin");
export { loadMessengerSession, saveMessengerSession };

export type MessengerConversation = {
  id: string;
  title: string;
  e2ee_enabled: boolean;
  livekit_room_name?: string | null;
  livekit_token?: string;
  livekit_simulated?: boolean;
  livekit_url?: string | null;
  [key: string]: unknown;
};

export type MessengerMessage = {
  id: string;
  sender_id: string;
  body: string;
  ciphertext?: string | null;
  ciphertext_type?: string | null;
  created_at: string;
  [key: string]: unknown;
};

export async function openMessengerConversation(
  session: ApiSession,
  body: {
    title: string;
    member_ids: string[];
    e2ee_enabled?: boolean;
    issue_livekit_token?: boolean;
  },
): Promise<MessengerConversation> {
  return apiPost("/api/v1/messenger/conversations", session, body);
}

export async function sendMessengerMessage(
  session: ApiSession,
  conversationId: string,
  body: { body?: string; ciphertext?: string; ciphertext_type?: string },
): Promise<MessengerMessage> {
  return apiPost(`/api/v1/messenger/conversations/${conversationId}/messages`, session, body);
}

export async function listMessengerMessages(
  session: ApiSession,
  conversationId: string,
): Promise<MessengerMessage[]> {
  return apiGet(`/api/v1/messenger/conversations/${conversationId}/messages`, session);
}

export async function issueLiveKitToken(
  session: ApiSession,
  conversationId: string,
): Promise<{
  token: string;
  room_name: string;
  simulated: boolean;
  url?: string | null;
  expires_at?: number;
}> {
  return apiPost(`/api/v1/messenger/conversations/${conversationId}/livekit-token`, session, {});
}

/** Demo client-side envelope — real apps use Signal/MLS; server never sees plaintext. */
export async function encryptDemoCiphertext(plaintext: string, passphrase: string): Promise<string> {
  const enc = new TextEncoder();
  const keyMaterial = await crypto.subtle.importKey(
    "raw",
    enc.encode(passphrase.padEnd(32, "0").slice(0, 32)),
    "AES-GCM",
    false,
    ["encrypt"],
  );
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const cipherBuf = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv },
    keyMaterial,
    enc.encode(plaintext),
  );
  const packed = new Uint8Array(iv.length + cipherBuf.byteLength);
  packed.set(iv, 0);
  packed.set(new Uint8Array(cipherBuf), iv.length);
  return `v1:${btoa(String.fromCharCode(...packed))}`;
}
