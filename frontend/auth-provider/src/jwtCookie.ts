/**
 * Edge-safe JWT session cookie checks for Next.js middleware.
 * When `secret` is provided, verifies HS256 via Web Crypto (no jose dependency).
 * Without secret: shape + exp only (dev). Production Edge must set JWT_SECRET.
 */

export type JwtCookieCheckOptions = {
  /** Shared HS256 secret (same as backend JWT_SECRET). */
  secret?: string;
  /** When true, reject if secret missing or signature invalid. */
  requireSignature?: boolean;
  /** Expected `iss` claim (backend default: marpich-identity). */
  issuer?: string;
  /** Expected `type` claim (access). */
  tokenType?: string;
};

export function decodeJwtPayload(token: string): Record<string, unknown> | null {
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  try {
    const json = base64UrlToString(parts[1]!);
    const payload = JSON.parse(json) as unknown;
    if (!payload || typeof payload !== "object") return null;
    return payload as Record<string, unknown>;
  } catch {
    return null;
  }
}

function base64UrlToString(segment: string): string {
  const padded = segment.replace(/-/g, "+").replace(/_/g, "/");
  const pad = padded.length % 4 === 0 ? "" : "=".repeat(4 - (padded.length % 4));
  const b64 = padded + pad;
  if (typeof atob === "function") {
    return atob(b64);
  }
  return Buffer.from(b64, "base64").toString("utf8");
}

function base64UrlToBytes(segment: string): Uint8Array {
  const padded = segment.replace(/-/g, "+").replace(/_/g, "/");
  const pad = padded.length % 4 === 0 ? "" : "=".repeat(4 - (padded.length % 4));
  const b64 = padded + pad;
  if (typeof atob === "function") {
    const bin = atob(b64);
    const out = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i += 1) out[i] = bin.charCodeAt(i);
    return out;
  }
  return new Uint8Array(Buffer.from(b64, "base64"));
}

export async function verifyHs256Jwt(token: string, secret: string): Promise<boolean> {
  const parts = token.split(".");
  if (parts.length !== 3) return false;
  const [header, payload, signature] = parts;
  if (!header || !payload || !signature) return false;
  try {
    const key = await crypto.subtle.importKey(
      "raw",
      new TextEncoder().encode(secret),
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["verify"],
    );
    const data = new TextEncoder().encode(`${header}.${payload}`);
    const sig = base64UrlToBytes(signature);
    return crypto.subtle.verify("HMAC", key, sig, data);
  } catch {
    return false;
  }
}

function claimsOk(
  payload: Record<string, unknown>,
  opts: JwtCookieCheckOptions,
): boolean {
  const exp = payload.exp;
  if (typeof exp !== "number") return false;
  const nowSec = Math.floor(Date.now() / 1000);
  if (exp <= nowSec + 5) return false;

  const issuer = opts.issuer ?? "marpich-identity";
  if (payload.iss !== undefined && payload.iss !== issuer) return false;

  const tokenType = opts.tokenType ?? "access";
  if (payload.type !== undefined && payload.type !== tokenType) return false;

  return true;
}

/**
 * Validate session cookie JWT. Prefer `requireSignature: true` in production.
 */
export async function isJwtSessionCookieValid(
  rawCookieValue: string | undefined,
  opts: JwtCookieCheckOptions = {},
): Promise<boolean> {
  if (!rawCookieValue) return false;
  let token = rawCookieValue;
  try {
    token = decodeURIComponent(rawCookieValue);
  } catch {
    /* keep raw */
  }
  if (token === "1" || token.length < 20) return false;

  const payload = decodeJwtPayload(token);
  if (!payload || !claimsOk(payload, opts)) return false;

  const secret = opts.secret?.trim();
  if (opts.requireSignature) {
    if (!secret || secret.length < 16) return false;
    return verifyHs256Jwt(token, secret);
  }
  if (secret) {
    return verifyHs256Jwt(token, secret);
  }
  // Dev fallback: exp/claims only (documented risk)
  return true;
}
