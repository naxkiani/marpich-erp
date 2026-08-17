#!/usr/bin/env node
/**
 * MEOS P0 — JWT cookie HS256 selftest (Web Crypto / Node crypto parity).
 * Run: node scripts/meos-jwt-cookie-selftest.mjs
 */
import { createHmac, webcrypto } from "node:crypto";
import assert from "node:assert/strict";

const subtle = webcrypto.subtle;

function b64url(input) {
  return Buffer.from(input)
    .toString("base64")
    .replace(/=/g, "")
    .replace(/\+/g, "-")
    .replace(/\//g, "_");
}

function signHs256(header, payload, secret) {
  const h = b64url(JSON.stringify(header));
  const p = b64url(JSON.stringify(payload));
  const sig = createHmac("sha256", secret)
    .update(`${h}.${p}`)
    .digest("base64")
    .replace(/=/g, "")
    .replace(/\+/g, "-")
    .replace(/\//g, "_");
  return `${h}.${p}.${sig}`;
}

function b64urlToBytes(segment) {
  const padded = segment.replace(/-/g, "+").replace(/_/g, "/");
  const pad = padded.length % 4 === 0 ? "" : "=".repeat(4 - (padded.length % 4));
  return new Uint8Array(Buffer.from(padded + pad, "base64"));
}

async function verifyHs256Jwt(token, secret) {
  const parts = token.split(".");
  if (parts.length !== 3) return false;
  const [header, payload, signature] = parts;
  const key = await subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["verify"],
  );
  const data = new TextEncoder().encode(`${header}.${payload}`);
  return subtle.verify("HMAC", key, b64urlToBytes(signature), data);
}

const secret = "unit-test-secret-key-32chars-min!!";
const exp = Math.floor(Date.now() / 1000) + 3600;
const good = signHs256(
  { alg: "HS256", typ: "JWT" },
  { exp, iss: "marpich-identity", type: "access", sub: "u1" },
  secret,
);
const tampered = `${good.slice(0, -4)}abcd`;

assert.equal(await verifyHs256Jwt(good, secret), true);
assert.equal(await verifyHs256Jwt(tampered, secret), false);
assert.equal(await verifyHs256Jwt("1", secret), false);

console.log("PASS: meos-jwt-cookie-selftest (HS256 verify + reject tamper)");
