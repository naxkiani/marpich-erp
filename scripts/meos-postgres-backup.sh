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
pg_dump --no-owner --no-acl --format=plain | gzip -c >"$OUT"
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

if [[ -n "${MEOS_BACKUP_S3_URI:-}" ]]; then
  echo "== offsite copy → ${MEOS_BACKUP_S3_URI} =="
  if command -v aws >/dev/null 2>&1; then
    aws s3 cp "$OUT" "${MEOS_BACKUP_S3_URI%/}/$(basename "$OUT")"
    aws s3 cp "$MANIFEST" "${MEOS_BACKUP_S3_URI%/}/$(basename "$MANIFEST")"
  else
    echo "WARN: aws CLI not found; dump remains only under ${BACKUP_ROOT}" >&2
  fi
fi

if [[ "$KEEP_LOCAL" =~ ^[0-9]+$ ]] && [[ "$KEEP_LOCAL" -gt 0 ]]; then
  mapfile -t OLD < <(ls -1t "${BACKUP_ROOT}"/marpich_"${PGDATABASE}"_*.sql.gz 2>/dev/null | tail -n +"$((KEEP_LOCAL + 1))" || true)
  for f in "${OLD[@]:-}"; do
    [[ -n "${f:-}" ]] || continue
    rm -f "$f" "${f%.sql.gz}.manifest.json"
  done
fi

echo "PASS: backup ${OUT} (${BYTES} bytes)"
