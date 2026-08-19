#!/usr/bin/env bash
# MEOS P0 — logical Postgres backup (Wave 04 DR). Prefer offsite MEOS_BACKUP_DIR / S3 URI.
# Does not print secrets. Ephemeral container disk is NOT a valid SoR backup target in production.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_ROOT="${MEOS_BACKUP_DIR:-${ROOT}/.meos-backups}"
KEEP_LOCAL="${MEOS_BACKUP_KEEP:-14}"

PGHOST="${PGHOST:-127.0.0.1}"
PGPORT="${PGPORT:-5433}"
PGUSER="${PGUSER:-marpich}"
PGDATABASE="${PGDATABASE:-marpich_platform}"
export PGPASSWORD="${PGPASSWORD:-marpich}"
export PGHOST PGPORT PGUSER PGDATABASE

mkdir -p "${BACKUP_ROOT}"
OUT="${BACKUP_ROOT}/marpich_${PGDATABASE}_${STAMP}.sql.gz"
MANIFEST="${BACKUP_ROOT}/marpich_${PGDATABASE}_${STAMP}.manifest.json"

echo "== pg_isready ${PGHOST}:${PGPORT} =="
pg_isready -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" >/dev/null

echo "== pg_dump → ${OUT} =="
# Prefer the Postgres container's pg_dump so dump dialect matches the server
# (host pg_dump 18+ emits SET transaction_timeout / \\restrict rejected by PG 16).
if command -v docker >/dev/null 2>&1 && docker ps --format '{{.Names}}' | grep -qx marpich-postgres; then
  docker exec -e PGPASSWORD="$PGPASSWORD" marpich-postgres \
    pg_dump -U "$PGUSER" -d "$PGDATABASE" --no-owner --no-acl --format=plain | gzip -c >"$OUT"
else
  pg_dump --no-owner --no-acl --format=plain | gzip -c >"$OUT"
fi
BYTES="$(wc -c <"$OUT" | tr -d ' ')"

python3 -c "
import json, os
from datetime import datetime, timezone
payload = {
    'created_at': datetime.now(timezone.utc).isoformat(),
    'host': os.environ['PGHOST'],
    'port': os.environ['PGPORT'],
    'database': os.environ['PGDATABASE'],
    'file': os.path.basename('${OUT}'),
    'bytes': int('${BYTES}'),
    'tool': 'pg_dump+gzip',
    'rpo_note': 'logical dump; enable WAL archive for production RPO <=15m',
}
with open('${MANIFEST}', 'w', encoding='utf-8') as f:
    json.dump(payload, f, indent=2)
    f.write('\n')
print('  manifest ${MANIFEST}')
"

S3_HELPER="${ROOT}/scripts/meos_s3.py"

_copy_offsite() {
  local dest="${MEOS_BACKUP_S3_URI%/}/$(basename "$1")"
  if [[ -x "$S3_HELPER" ]] || [[ -f "$S3_HELPER" ]]; then
    python3 "$S3_HELPER" put "$1" "$dest"
    return
  fi
  if command -v aws >/dev/null 2>&1; then
    local extra=()
    if [[ -n "${MEOS_S3_ENDPOINT_URL:-}" ]]; then
      extra+=(--endpoint-url "$MEOS_S3_ENDPOINT_URL")
    fi
    aws s3 cp "$1" "$dest" "${extra[@]}"
    return
  fi
  echo "FAIL: MEOS_BACKUP_S3_URI set but neither scripts/meos_s3.py nor aws CLI is available" >&2
  return 1
}

if [[ -n "${MEOS_BACKUP_S3_URI:-}" ]]; then
  echo "== offsite copy → ${MEOS_BACKUP_S3_URI} =="
  _copy_offsite "$OUT"
  _copy_offsite "$MANIFEST"
  WAL_DIR="${MEOS_WAL_ARCHIVE_DIR:-}"
  if [[ -z "$WAL_DIR" ]] && command -v docker >/dev/null 2>&1 && docker ps --format '{{.Names}}' | grep -qx marpich-postgres; then
    if docker exec marpich-postgres test -d /var/lib/postgresql/data/meos_wal_archive 2>/dev/null; then
      WAL_TAR="${BACKUP_ROOT}/marpich_${PGDATABASE}_${STAMP}.wal.tar.gz"
      docker exec marpich-postgres tar -C /var/lib/postgresql/data -czf - meos_wal_archive >"$WAL_TAR" || true
      if [[ -s "$WAL_TAR" ]]; then
        _copy_offsite "$WAL_TAR"
      fi
    fi
  fi
  python3 "$S3_HELPER" ls "${MEOS_BACKUP_S3_URI%/}/" >/tmp/meos-offsite-ls.$$ 2>/dev/null || true
  if grep -q "$(basename "$OUT")" /tmp/meos-offsite-ls.$$ 2>/dev/null; then
    OFFSITE_STATUS="copied_listed"
  else
    OFFSITE_STATUS="copied"
  fi
  rm -f /tmp/meos-offsite-ls.$$
elif [[ "${MEOS_REQUIRE_OFFSITE:-0}" == "1" ]] || [[ "${MARPICH_ENVIRONMENT:-}" == "production" ]]; then
  echo "FAIL: offsite backup required (set MEOS_BACKUP_S3_URI). Local-only is not production-ready." >&2
  exit 1
else
  OFFSITE_STATUS="skipped_local_ok"
  echo "NOTE: offsite skipped (dev). Set MEOS_REQUIRE_OFFSITE=1 or MEOS_BACKUP_S3_URI for production."
fi

# Integrity: gzip must be readable
gzip -t "$OUT"

python3 -c "
import json
from datetime import datetime, timezone
path = '${MANIFEST}'
with open(path, encoding='utf-8') as f:
    payload = json.load(f)
payload['offsite'] = '${OFFSITE_STATUS:-unknown}'
payload['gzip_ok'] = True
payload['verified_at'] = datetime.now(timezone.utc).isoformat()
with open(path, 'w', encoding='utf-8') as f:
    json.dump(payload, f, indent=2)
    f.write('\n')
"

if [[ "$KEEP_LOCAL" =~ ^[0-9]+$ ]] && [[ "$KEEP_LOCAL" -gt 0 ]]; then
  mapfile -t OLD < <(ls -1t "${BACKUP_ROOT}"/marpich_"${PGDATABASE}"_*.sql.gz 2>/dev/null | tail -n +"$((KEEP_LOCAL + 1))" || true)
  for f in "${OLD[@]:-}"; do
    [[ -n "${f:-}" ]] || continue
    rm -f "$f" "${f%.sql.gz}.manifest.json"
  done
fi

echo "PASS: backup ${OUT} (${BYTES} bytes)"
