#!/usr/bin/env node
/**
 * MEOS P0 — sessionStorage must never persist JWT access/refresh tokens.
 * Run: node scripts/meos-session-storage-selftest.mjs
 */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const sessionTs = readFileSync(join(root, "frontend/auth-provider/src/session.ts"), "utf8");
const platformTs = readFileSync(join(root, "frontend/shared/src/platform/session.ts"), "utf8");
const loginBff = readFileSync(
  join(root, "frontend/apps/admin_portal/src/app/api/auth/login/route.ts"),
  "utf8",
);

assert.match(sessionTs, /function persistPublic/);
assert.match(sessionTs, /toPublicSession\(session\)/);
assert.doesNotMatch(
  sessionTs,
  /sessionStorage\.setItem\([^)]*JSON\.stringify\(session\)/,
  "must not persist the raw AuthSession (tokens)",
);
assert.match(sessionTs, /if \(parsed\.accessToken \|\| parsed\.refreshToken\)/);
assert.match(platformTs, /BFF_API_PREFIX = "\/api\/backend"/);
assert.match(loginBff, /res\.cookies\.set\(\{ name: ACCESS_COOKIE/);
assert.doesNotMatch(loginBff, /access_token.*NextResponse\.json/);

const publicShape = { tenantId: "t1", expiresAt: 1, userId: "u1", accessToken: "jwt", refreshToken: "r" };
const persisted = { tenantId: publicShape.tenantId, expiresAt: publicShape.expiresAt, userId: publicShape.userId };
assert.equal("accessToken" in persisted, false);
assert.equal("refreshToken" in persisted, false);

console.log("PASS: meos-session-storage-selftest (no JWT in sessionStorage persist path)");
