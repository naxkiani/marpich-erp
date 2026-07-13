export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export const SESSION_STORAGE_KEY = "marpich_auth_session";

/** Cookie mirror for Next.js middleware route guards (client-set). */
export const SESSION_COOKIE_NAME = "marpich_auth";

export const SESSION_COOKIE_VALUE = "1";
