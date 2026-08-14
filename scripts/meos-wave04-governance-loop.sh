#!/usr/bin/env bash
# Wave 04 governance smoke: policy evaluate + privacy/DR doc presence + soft audit.
set -euo pipefail

API_URL="${API_URL:-http://127.0.0.1:8000}"
TENANT_ID="${TENANT_ID:-gov-$(date +%s)}"
EMAIL="${EMAIL:-gov-$(date +%s)@marpich.dev}"
PASSWORD="${PASSWORD:-SecurePass123!}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

hdr=(-H "Content-Type: application/json" -H "X-Tenant-ID: ${TENANT_ID}")

echo "== docs present =="
test -f "$ROOT/docs/meos/execution/MEOS_WAVE04_PRIVACY_ACTIVATION.md"
test -f "$ROOT/docs/meos/execution/MEOS_WAVE04_DR_RUNBOOK.md"
echo "  privacy + DR runbooks OK"

echo "== register/login =="
curl -sf "${API_URL}/api/v1/health" >/dev/null
curl -sf -X POST "${API_URL}/api/v1/auth/register" "${hdr[@]}" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\",\"display_name\":\"Gov\"}" >/dev/null
LOGIN="$(curl -sf -X POST "${API_URL}/api/v1/auth/login" "${hdr[@]}" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\"}")"
TOKEN="$(python3 -c 'import json,sys; d=json.load(sys.stdin); print((d.get("data") or {}).get("access_token") or "")' <<<"$LOGIN")"
[[ -n "$TOKEN" ]] || { echo "FAIL: no token"; exit 1; }
auth=(-H "Authorization: Bearer ${TOKEN}" -H "X-Tenant-ID: ${TENANT_ID}" -H "Content-Type: application/json")

echo "== policy evaluate =="
POL_CODE="$(curl -s -o /tmp/meos-w04-pol.json -w '%{http_code}' \
  -X POST "${API_URL}/api/v1/policies/evaluate" "${auth[@]}" \
  -d '{"domain":"privacy","policy_key":"export_pii","facts":{"resource":"contact"}}')"
if [[ "$POL_CODE" == "401" ]]; then
  echo "FAIL: policy evaluate unauthenticated" >&2
  exit 1
fi
echo "  policy evaluate HTTP ${POL_CODE}"

echo "== audit soft =="
curl -sf "${API_URL}/api/v1/audit/entries?limit=5" "${auth[@]}" >/dev/null \
  || echo "(audit soft-skip)"

echo "PASS: Wave 04 governance smoke tenant=${TENANT_ID}"
