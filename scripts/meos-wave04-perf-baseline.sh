#!/usr/bin/env bash
# Wave 04 performance baseline — capture p95 latency for critical GETs.
# Writes JSON report to /tmp/meos-perf-baseline.json (or PERF_OUT).
set -euo pipefail

API_URL="${API_URL:-http://127.0.0.1:8000}"
TENANT_ID="${TENANT_ID:-perf-$(date +%s)}"
EMAIL="${EMAIL:-perf-$(date +%s)@marpich.dev}"
PASSWORD="${PASSWORD:-SecurePass123!}"
SAMPLES="${SAMPLES:-20}"
PERF_OUT="${PERF_OUT:-/tmp/meos-perf-baseline.json}"

hdr=(-H "Content-Type: application/json" -H "X-Tenant-ID: ${TENANT_ID}")

curl -sf -X POST "${API_URL}/api/v1/auth/register" "${hdr[@]}" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\",\"display_name\":\"Perf\"}" >/dev/null
LOGIN="$(curl -sf -X POST "${API_URL}/api/v1/auth/login" "${hdr[@]}" \
  -d "{\"email\":\"${EMAIL}\",\"password\":\"${PASSWORD}\"}")"
TOKEN="$(python3 -c 'import json,sys; d=json.load(sys.stdin); print((d.get("data") or {}).get("access_token") or "")' <<<"$LOGIN")"
[[ -n "$TOKEN" ]] || { echo "FAIL: no token"; exit 1; }

python3 - <<PY
import json, time, urllib.request, statistics, os

api = os.environ.get("API_URL", "${API_URL}")
token = "${TOKEN}"
tenant = "${TENANT_ID}"
samples = int("${SAMPLES}")
out = "${PERF_OUT}"

paths = [
    "/api/v1/health",
    "/api/v1/crm/contacts?limit=20",
    "/api/v1/search/query?q=test&limit=10",
    "/api/v1/analytics/dashboards",
    "/api/v1/policies",
]

def timed(path: str) -> float:
    req = urllib.request.Request(
        api + path,
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": tenant,
            "Content-Type": "application/json",
        },
        method="GET",
    )
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp.read()
            code = resp.status
    except Exception as exc:
        code = getattr(exc, "code", 0) or 0
    dt = (time.perf_counter() - t0) * 1000
    return dt, code

report = {"tenant_id": tenant, "samples": samples, "endpoints": {}}
for path in paths:
    times = []
    codes = []
    for _ in range(samples):
        dt, code = timed(path)
        times.append(dt)
        codes.append(code)
    times_sorted = sorted(times)
    p95 = times_sorted[max(0, int(0.95 * (len(times_sorted) - 1)))]
    report["endpoints"][path] = {
        "p50_ms": statistics.median(times),
        "p95_ms": p95,
        "mean_ms": statistics.mean(times),
        "last_http": codes[-1],
        "http_codes": sorted(set(codes)),
    }
    print(f"{path}: p95={p95:.1f}ms http={sorted(set(codes))}")

with open(out, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)
print(f"PASS: performance baseline written to {out}")
PY
