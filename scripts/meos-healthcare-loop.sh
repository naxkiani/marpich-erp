#!/usr/bin/env bash
# Prove Healthcare Functional closed loop against a running API.
# Chain: login → hospital patient/admit/encounter → lab order/sample/result
#        → pharmacy Rx/dispense → hospital care-events → audit soft-check.
set -euo pipefail

API_URL="${API_URL:-http://127.0.0.1:8000}"
TENANT_ID="${TENANT_ID:-hlt-loop-$(date +%s)}"
EMAIL="${EMAIL:-hlt-$(date +%s)@marpich.dev}"
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

echo "== register/login (${TENANT_ID}) =="
curl -sf -X POST "${API_URL}/api/v1/auth/register" "${hdr[@]}" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\",\"display_name\":\"HLT Loop\"}" >/dev/null

LOGIN="$(curl -sf -X POST "${API_URL}/api/v1/auth/login" "${hdr[@]}" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\"}")"
TOKEN="$(python3 -c 'import json,sys; d=json.load(sys.stdin); print((d.get("data") or {}).get("access_token") or "")' <<<"$LOGIN")"
if [[ -z "$TOKEN" ]]; then
  echo "FAIL: no access token" >&2
  echo "$LOGIN" >&2
  exit 1
fi
auth=(-H "Authorization: Bearer ${TOKEN}" -H "X-Tenant-ID: ${TENANT_ID}" -H "Content-Type: application/json")

echo "== hospital patient + admission + encounter =="
PATIENT="$(curl -sf -X POST "${API_URL}/api/v1/hospital/patients" "${auth[@]}" \
  -d '{"mrn":"MRN-HLT-1","first_name":"Ava","last_name":"Care","date_of_birth":"1990-01-15"}')"
PATIENT_ID="$(json_get 'd["data"]["id"]' <<<"$PATIENT")"

ADM="$(curl -sf -X POST "${API_URL}/api/v1/hospital/admissions" "${auth[@]}" \
  -d "{\"patient_id\":\"${PATIENT_ID}\",\"ward\":\"Ward-A\"}")"
ADM_ID="$(json_get 'd["data"]["id"]' <<<"$ADM")"

ENC="$(curl -sf -X POST "${API_URL}/api/v1/hospital/encounters" "${auth[@]}" \
  -d "{\"admission_id\":\"${ADM_ID}\"}")"
ENC_ID="$(json_get 'd["data"]["id"]' <<<"$ENC")"

echo "== laboratory order → sample → result =="
ORDER="$(curl -sf -X POST "${API_URL}/api/v1/laboratory/orders" "${auth[@]}" \
  -d "{\"order_number\":\"HLT-CBC-1\",\"patient_ref\":\"${PATIENT_ID}\",\"test_code\":\"CBC\",\"source_encounter_ref\":\"${ENC_ID}\"}")"
ORDER_ID="$(json_get 'd["data"]["id"]' <<<"$ORDER")"

curl -sf -X POST "${API_URL}/api/v1/laboratory/samples" "${auth[@]}" \
  -d "{\"order_id\":\"${ORDER_ID}\",\"accession_number\":\"ACC-HLT-1\",\"specimen_type\":\"blood\"}" >/dev/null

curl -sf -X POST "${API_URL}/api/v1/laboratory/orders/${ORDER_ID}/results" "${auth[@]}" \
  -d '{"result_value":"12.8","result_unit":"g/dL"}' >/dev/null

echo "== pharmacy prescription → dispense =="
RX="$(curl -sf -X POST "${API_URL}/api/v1/pharmacy/prescriptions" "${auth[@]}" \
  -d "{\"rx_number\":\"RX-HLT-1\",\"patient_ref\":\"${PATIENT_ID}\",\"drug_code\":\"AMOX500\",\"drug_name\":\"Amoxicillin 500mg\",\"quantity\":14,\"source_encounter_ref\":\"${ENC_ID}\"}")"
RX_ID="$(json_get 'd["data"]["id"]' <<<"$RX")"

curl -sf -X POST "${API_URL}/api/v1/pharmacy/dispenses" "${auth[@]}" \
  -d "{\"prescription_id\":\"${RX_ID}\",\"quantity_dispensed\":14}" >/dev/null

echo "== hospital care-events (lab_result + pharmacy_dispense) =="
CARE="$(wait_json 'len((d.get("data") or {}).get("items") or [])>=2 and {"lab_result","pharmacy_dispense"}.issubset({i.get("event_kind") for i in ((d.get("data") or {}).get("items") or [])})' \
  "${API_URL}/api/v1/hospital/care-events" "${auth[@]}")"
python3 - <<PY
import json
d=json.loads('''$CARE''')["data"]
kinds={i["event_kind"] for i in d["items"]}
assert "lab_result" in kinds and "pharmacy_dispense" in kinds, kinds
for item in d["items"]:
    assert item["patient_id"]=="${PATIENT_ID}"
    assert item["encounter_id"]=="${ENC_ID}"
print(f"  care-events total={d.get('total')} kinds={sorted(kinds)}")
PY

echo "== audit (best-effort) =="
curl -sf "${API_URL}/api/v1/audit/entries?limit=10" "${auth[@]}" >/dev/null \
  || echo "(audit soft-skip)"

echo "PASS: Healthcare closed loop (Hospital→Lab→Pharmacy→care-events) tenant=${TENANT_ID}"
