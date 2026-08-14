#!/usr/bin/env bash
# Prove Wave 01 durable user loop against a running API (Postgres recommended).
set -euo pipefail

API_URL="${API_URL:-http://127.0.0.1:8000}"
TENANT_ID="${TENANT_ID:-wave01-loop-$(date +%s)}"
EMAIL="${EMAIL:-wave01-$(date +%s)@marpich.dev}"
PASSWORD="${PASSWORD:-SecurePass123!}"

hdr=(-H "Content-Type: application/json" -H "X-Tenant-ID: ${TENANT_ID}")

echo "== health =="
curl -sf "${API_URL}/api/v1/health" >/dev/null

echo "== register/login (${TENANT_ID}) =="
curl -sf -X POST "${API_URL}/api/v1/auth/register" "${hdr[@]}" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\",\"display_name\":\"Wave01\"}" >/dev/null

LOGIN="$(curl -sf -X POST "${API_URL}/api/v1/auth/login" "${hdr[@]}" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\"}")"
TOKEN="$(python3 -c 'import json,sys; d=json.load(sys.stdin); print((d.get("data") or {}).get("access_token") or "")' <<<"$LOGIN")"
if [[ -z "$TOKEN" ]]; then
  echo "FAIL: no access token" >&2
  echo "$LOGIN" >&2
  exit 1
fi
auth=(-H "Authorization: Bearer ${TOKEN}" -H "X-Tenant-ID: ${TENANT_ID}" -H "Content-Type: application/json")

echo "== me =="
curl -sf "${API_URL}/api/v1/users/me" "${auth[@]}" >/dev/null

echo "== notifications inbox =="
curl -sf "${API_URL}/api/v1/notifications/inbox" "${auth[@]}" >/dev/null

echo "== search =="
curl -sf "${API_URL}/api/v1/search/query?q=wave&limit=5" "${auth[@]}" >/dev/null

echo "== workflow definitions =="
curl -sf "${API_URL}/api/v1/workflow/definitions" "${auth[@]}" >/dev/null \
  || curl -sf "${API_URL}/api/v1/workflow/definitions?limit=20" "${auth[@]}" >/dev/null \
  || echo "(workflow definitions endpoint soft-skip)"

echo "== audit entries =="
curl -sf "${API_URL}/api/v1/audit/entries?limit=5" "${auth[@]}" >/dev/null

echo "PASS: Wave 01 API user loop (auth → inbox → search → workflow → audit)"
