#!/usr/bin/env bash
# Prove Wave 02 Q2C closed loop against a running API (Postgres required for CI).
# Chain: login → CRM win → quote → order → inventory reserve + reorder →
#        AR draft/issue/pay → procurement submit/approve/receive → stock restock.
set -euo pipefail

API_URL="${API_URL:-http://127.0.0.1:8000}"
TENANT_ID="${TENANT_ID:-wave02-q2c-$(date +%s)}"
EMAIL="${EMAIL:-wave02-$(date +%s)@marpich.dev}"
PASSWORD="${PASSWORD:-SecurePass123!}"
SKU="${SKU:-SALES-STD}"
SEED_QTY="${SEED_QTY:-20}"
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
from decimal import Decimal
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

echo "== register/login (${TENANT_ID}) =="
curl -sf -X POST "${API_URL}/api/v1/auth/register" "${hdr[@]}" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\",\"display_name\":\"Wave02 Q2C\"}" >/dev/null

LOGIN="$(curl -sf -X POST "${API_URL}/api/v1/auth/login" "${hdr[@]}" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\"}")"
TOKEN="$(python3 -c 'import json,sys; d=json.load(sys.stdin); print((d.get("data") or {}).get("access_token") or "")' <<<"$LOGIN")"
if [[ -z "$TOKEN" ]]; then
  echo "FAIL: no access token" >&2
  echo "$LOGIN" >&2
  exit 1
fi
auth=(-H "Authorization: Bearer ${TOKEN}" -H "X-Tenant-ID: ${TENANT_ID}" -H "Content-Type: application/json")

echo "== seed inventory ${SKU}=${SEED_QTY} =="
curl -sf -X PUT "${API_URL}/api/v1/inventory/stock" "${auth[@]}" \
  -d "{\"sku\":\"${SKU}\",\"quantity\":\"${SEED_QTY}\"}" >/dev/null

echo "== CRM contact + opportunity + win =="
CONTACT="$(curl -sf -X POST "${API_URL}/api/v1/crm/contacts" "${auth[@]}" \
  -d '{"email":"buyer@q2c.dev","full_name":"Q2C Buyer","company":"Acme"}')"
CONTACT_ID="$(json_get 'd["data"]["id"]' <<<"$CONTACT")"

OPP="$(curl -sf -X POST "${API_URL}/api/v1/crm/opportunities" "${auth[@]}" \
  -d "{\"contact_id\":\"${CONTACT_ID}\",\"title\":\"Wave02 license\",\"amount\":\"25000.00\",\"currency\":\"USD\"}")"
OPP_ID="$(json_get 'd["data"]["id"]' <<<"$OPP")"
curl -sf -X POST "${API_URL}/api/v1/crm/opportunities/${OPP_ID}/win" "${auth[@]}" >/dev/null

echo "== Sales quotation send + convert =="
QUOTES="$(wait_json 'len((d.get("data") or {}).get("items") or [])>=1' \
  "${API_URL}/api/v1/sales/quotations?limit=50" "${auth[@]}")"
QID="$(python3 -c 'import json,sys; items=json.load(sys.stdin)["data"]["items"]; print(next(q["id"] for q in items if q.get("opportunity_id")=="'"${OPP_ID}"'"))' <<<"$QUOTES")"
curl -sf -X POST "${API_URL}/api/v1/sales/quotations/${QID}/send" "${auth[@]}" >/dev/null
curl -sf -X POST "${API_URL}/api/v1/sales/quotations/${QID}/convert" "${auth[@]}" >/dev/null

echo "== Inventory reserved (available < seed) =="
STOCK="$(wait_json 'Decimal(str((d.get("data") or {}).get("quantity_available") or "999")) < Decimal("'"${SEED_QTY}"'")' \
  "${API_URL}/api/v1/inventory/stock/${SKU}" "${auth[@]}")"
python3 - <<PY
from decimal import Decimal
import json
d=json.loads('''$STOCK''')["data"]
avail=Decimal(str(d["quantity_available"]))
assert avail < Decimal("${SEED_QTY}"), d
print(f"  available={avail} on_hand={d.get('quantity_on_hand')}")
PY

echo "== Accounting AR draft → issue → receive-payment =="
INVS="$(wait_json 'len((d.get("data") or {}).get("items") or [])>=1' \
  "${API_URL}/api/v1/accounting/invoices?limit=50" "${auth[@]}")"
IID="$(json_get 'd["data"]["items"][0]["id"]' <<<"$INVS")"
curl -sf -X POST "${API_URL}/api/v1/accounting/invoices/${IID}/issue" "${auth[@]}" >/dev/null
PAID="$(curl -sf -X POST "${API_URL}/api/v1/accounting/invoices/${IID}/receive-payment" "${auth[@]}")"
python3 -c 'import json,sys; d=json.load(sys.stdin)["data"]; assert d["status"]=="paid" and d.get("paid_at"); print("  invoice paid", d["amount"], d["currency"])' <<<"$PAID"

echo "== Procurement requisition → submit → approve → receive =="
REQS="$(wait_json 'any(r.get("sku")=="'"${SKU}"'" for r in ((d.get("data") or {}).get("items") or []))' \
  "${API_URL}/api/v1/procurement/requisitions?limit=50" "${auth[@]}")"
RID="$(python3 -c 'import json,sys; items=json.load(sys.stdin)["data"]["items"]; print(next(r["id"] for r in items if r["sku"]=="'"${SKU}"'"))' <<<"$REQS")"
curl -sf -X POST "${API_URL}/api/v1/procurement/requisitions/${RID}/submit" "${auth[@]}" >/dev/null
curl -sf -X POST "${API_URL}/api/v1/procurement/requisitions/${RID}/approve" "${auth[@]}" >/dev/null

BEFORE="$(curl -sf "${API_URL}/api/v1/inventory/stock/${SKU}" "${auth[@]}")"
ON_BEFORE="$(json_get 'd["data"]["quantity_on_hand"]' <<<"$BEFORE")"

RECV="$(curl -sf -X POST "${API_URL}/api/v1/procurement/requisitions/${RID}/receive" "${auth[@]}")"
RQTY="$(json_get 'd["data"]["quantity"]' <<<"$RECV")"
RSTATUS="$(json_get 'd["data"]["status"]' <<<"$RECV")"
if [[ "$RSTATUS" != "received" ]]; then
  echo "FAIL: expected received, got ${RSTATUS}" >&2
  exit 1
fi

AFTER="$(wait_json 'Decimal(str((d.get("data") or {}).get("quantity_on_hand") or "0")) == Decimal("'"${ON_BEFORE}"'") + Decimal("'"${RQTY}"'")' \
  "${API_URL}/api/v1/inventory/stock/${SKU}" "${auth[@]}")"
python3 - <<PY
from decimal import Decimal
import json
before=Decimal("${ON_BEFORE}")
qty=Decimal("${RQTY}")
after=Decimal(str(json.loads('''$AFTER''')["data"]["quantity_on_hand"]))
assert after == before + qty, (before, qty, after)
print(f"  restocked on_hand {before} + {qty} = {after}")
PY

echo "== audit (best-effort) =="
curl -sf "${API_URL}/api/v1/audit/entries?limit=5" "${auth[@]}" >/dev/null \
  || echo "(audit soft-skip)"

echo "PASS: Wave 02 Q2C closed loop (CRM→Sales→Inventory→AR pay→Procurement→restock) tenant=${TENANT_ID}"
