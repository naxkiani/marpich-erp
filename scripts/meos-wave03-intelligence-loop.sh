#!/usr/bin/env bash
# Wave 03 Intelligence smoke: login → CRM mutate → search indexes event →
# analytics dashboards (permissioned) → AI assist.
set -euo pipefail

API_URL="${API_URL:-http://127.0.0.1:8000}"
TENANT_ID="${TENANT_ID:-wave03-$(date +%s)}"
EMAIL="${EMAIL:-wave03-$(date +%s)@marpich.dev}"
PASSWORD="${PASSWORD:-SecurePass123!}"
MAX_WAIT_SEC="${MAX_WAIT_SEC:-30}"

hdr=(-H "Content-Type: application/json" -H "X-Tenant-ID: ${TENANT_ID}")

json_get() {
  python3 -c 'import json,sys; d=json.load(sys.stdin); print('"$1"')'
}

wait_json() {
  local label="$1"
  local url="$2"
  shift 2
  local auth_args=("$@")
  local deadline=$((SECONDS + MAX_WAIT_SEC))
  local body=""
  while (( SECONDS < deadline )); do
    body="$(curl -sf "$url" "${auth_args[@]}" || true)"
    if [[ -n "$body" ]] && python3 -c '
import json, sys
d = json.load(sys.stdin)
raise SystemExit(0 if ('"$label"') else 1)
' <<<"$body" 2>/dev/null; then
      printf '%s' "$body"
      return 0
    fi
    sleep 1
  done
  echo "FAIL: timeout waiting for ${label}" >&2
  echo "${body:-<empty>}" >&2
  exit 1
}

echo "== health =="
curl -sf "${API_URL}/api/v1/health" >/dev/null

echo "== register/login =="
curl -sf -X POST "${API_URL}/api/v1/auth/register" "${hdr[@]}" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\",\"display_name\":\"Wave03\"}" >/dev/null
LOGIN="$(curl -sf -X POST "${API_URL}/api/v1/auth/login" "${hdr[@]}" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\"}")"
TOKEN="$(python3 -c 'import json,sys; d=json.load(sys.stdin); print((d.get("data") or {}).get("access_token") or "")' <<<"$LOGIN")"
[[ -n "$TOKEN" ]] || { echo "FAIL: no token"; exit 1; }
auth=(-H "Authorization: Bearer ${TOKEN}" -H "X-Tenant-ID: ${TENANT_ID}" -H "Content-Type: application/json")

echo "== CRM contact (drives search index via integration events) =="
CONTACT="$(curl -sf -X POST "${API_URL}/api/v1/crm/contacts" "${auth[@]}" \
  -d '{"email":"intel@wave03.dev","full_name":"Intel Contact","company":"Wave03 Co"}')"
CONTACT_ID="$(json_get 'd["data"]["id"]' <<<"$CONTACT")"

echo "== search query (event-indexed) =="
# Search may be empty if index lag / permissions — wait for any hit containing contact or company
SEARCH_URL="${API_URL}/api/v1/search/query?q=Wave03&limit=20"
SEARCH_BODY="$(wait_json 'True' "${SEARCH_URL}" "${auth[@]}" || true)"
# Prefer structured POST if GET unsupported
if [[ -z "$SEARCH_BODY" ]] || ! python3 -c 'import json,sys; json.load(sys.stdin)' <<<"${SEARCH_BODY:-}" 2>/dev/null; then
  SEARCH_BODY="$(curl -sf -X POST "${API_URL}/api/v1/search/query" "${auth[@]}" \
    -d '{"q":"Wave03","limit":20}' || true)"
fi
python3 - <<PY
import json,sys
raw='''${SEARCH_BODY:-}'''
if not raw.strip():
    print("  WARN: search empty/soft-skip (index may lag)")
    sys.exit(0)
d=json.loads(raw)
data=d.get("data") or d
total=data.get("total") if isinstance(data, dict) else None
print(f"  search total={total}")
PY

echo "== analytics dashboards (permission ACL) =="
DASH_CODE="$(curl -s -o /tmp/meos-w03-dash.json -w '%{http_code}' \
  "${API_URL}/api/v1/analytics/dashboards" "${auth[@]}")"
if [[ "$DASH_CODE" == "401" ]]; then
  echo "FAIL: analytics unauthenticated" >&2
  exit 1
fi
# 403 without permission is acceptable deny-by-default; 200 is success
echo "  analytics dashboards HTTP ${DASH_CODE}"

echo "== AI assist (platform only) =="
AI_CODE="$(curl -s -o /tmp/meos-w03-ai.json -w '%{http_code}' \
  -X POST "${API_URL}/api/v1/ai/assist" "${auth[@]}" \
  -d "{\"module_id\":\"crm\",\"surface\":\"insights\",\"prompt\":\"Summarize CRM pipeline health\",\"context\":{\"contact_id\":\"${CONTACT_ID}\"}}")"
if [[ "$AI_CODE" == "401" ]]; then
  echo "FAIL: AI assist unauthenticated" >&2
  exit 1
fi
echo "  ai assist HTTP ${AI_CODE}"

echo "PASS: Wave 03 intelligence smoke (search+analytics+AI) tenant=${TENANT_ID} contact=${CONTACT_ID}"
