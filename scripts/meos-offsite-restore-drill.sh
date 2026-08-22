#!/usr/bin/env bash
# Restore a dump that was copied to MEOS_BACKUP_S3_URI, then drill into a separate DB.
# Records wall-clock RTO. Does not overwrite the live database.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
STARTED_NS="$(date +%s%N)"
WORK="${MEOS_RESTORE_WORK:-${ROOT}/.meos-backups/offsite-restore}"
RECORD="${ROOT}/docs/meos/execution/.last_dr_drill.json"
URI="${MEOS_BACKUP_S3_URI:-}"

if [[ -z "$URI" ]]; then
  echo "FAIL: MEOS_BACKUP_S3_URI is required for an offsite restore drill" >&2
  exit 1
fi

mkdir -p "$WORK"
echo "== list offsite ${URI} =="
python3 "$ROOT/scripts/meos_s3.py" ls "${URI%/}/" | tee "${WORK}/listing.txt"
DUMP_URI="$(grep '\.sql\.gz$' "${WORK}/listing.txt" | tail -1 || true)"
if [[ -z "$DUMP_URI" ]]; then
  echo "FAIL: no .sql.gz object listed at ${URI}" >&2
  exit 1
fi

LOCAL="${WORK}/$(basename "$DUMP_URI")"
echo "== get ${DUMP_URI} =="
python3 "$ROOT/scripts/meos_s3.py" get "$DUMP_URI" "$LOCAL"
gzip -t "$LOCAL"

export MEOS_RESTORE_DUMP="$LOCAL"
export MEOS_RESTORE_DATABASE="${MEOS_RESTORE_DATABASE:-marpich_platform_offsite_restore}"
"$ROOT/scripts/meos-postgres-restore-drill.sh"

ENDED_NS="$(date +%s%N)"
RTO_MS="$(( (ENDED_NS - STARTED_NS) / 1000000 ))"
RPO_NOTE="${MEOS_RPO_NOTE:-logical dump interval; WAL archive_timeout=60s on postgres when enabled}"

python3 -c "
import json
from datetime import datetime, timezone
payload = {
    'drilled_at': datetime.now(timezone.utc).isoformat(),
    'source_uri': '''${DUMP_URI}''',
    'target_database': '''${MEOS_RESTORE_DATABASE}''',
    'rto_ms': int('''${RTO_MS}'''),
    'rpo_note': '''${RPO_NOTE}''',
    'status': 'PASS',
    'failure_domain': '''${MEOS_DR_FAILURE_DOMAIN:-object-store-volume-isolated}''',
}
with open('''${RECORD}''', 'w', encoding='utf-8') as f:
    json.dump(payload, f, indent=2)
    f.write('\n')
print('  recorded', '''${RECORD}''')
print('PASS: offsite restore RTO_MS=${RTO_MS}')
"
