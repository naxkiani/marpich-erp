#!/usr/bin/env bash
# MEOS P0 — restore drill against a target database (Wave 04 DR).
# WARNING: destructive to MEOS_RESTORE_DATABASE. Defaults to marpich_platform_restore.
# Optional: RUN_SMOKE=1 runs meos-wave01-user-loop.sh against API_URL after restore.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_ROOT="${MEOS_BACKUP_DIR:-${ROOT}/.meos-backups}"
DUMP="${MEOS_RESTORE_DUMP:-}"
DRILL_RECORD="${ROOT}/docs/meos/execution/.last_restore_drill.json"

PGHOST="${PGHOST:-127.0.0.1}"
PGPORT="${PGPORT:-5433}"
PGUSER="${PGUSER:-marpich}"
SOURCE_DB="${PGDATABASE:-marpich_platform}"
TARGET_DB="${MEOS_RESTORE_DATABASE:-marpich_platform_restore}"
export PGPASSWORD="${PGPASSWORD:-marpich}"
export PGHOST PGPORT PGUSER

if [[ -z "$DUMP" ]]; then
  DUMP="$(ls -1t "${BACKUP_ROOT}"/marpich_"${SOURCE_DB}"_*.sql.gz 2>/dev/null | head -1 || true)"
fi
if [[ -z "$DUMP" || ! -f "$DUMP" ]]; then
  echo "FAIL: no dump found. Run scripts/meos-postgres-backup.sh first or set MEOS_RESTORE_DUMP." >&2
  exit 1
fi

echo "== restore drill =="
echo "  dump:   ${DUMP}"
echo "  target: ${PGHOST}:${PGPORT}/${TARGET_DB}"

pg_isready -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" >/dev/null

# Recreate empty target DB
psql -v ON_ERROR_STOP=1 -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '${TARGET_DB}' AND pid <> pg_backend_pid();" >/dev/null || true
psql -v ON_ERROR_STOP=1 -d postgres -c "DROP DATABASE IF EXISTS ${TARGET_DB};"
psql -v ON_ERROR_STOP=1 -d postgres -c "CREATE DATABASE ${TARGET_DB} OWNER ${PGUSER};"

echo "== gunzip | psql =="
gunzip -c "$DUMP" | psql -v ON_ERROR_STOP=1 -d "$TARGET_DB" >/dev/null

echo "== migrations on restore target =="
export PGDATABASE="$TARGET_DB"
export DATABASE_URL="${DATABASE_URL:-postgresql+asyncpg://${PGUSER}:${PGPASSWORD}@${PGHOST}:${PGPORT}/${TARGET_DB}}"
# Prefer explicit PG* for run-migrations.sh
(
  cd "$ROOT"
  if [[ -x ./scripts/run-migrations.sh ]]; then
    ./scripts/run-migrations.sh
  else
    echo "WARN: run-migrations.sh missing; schema may lag dump" >&2
  fi
)

SMOKE_STATUS="skipped"
if [[ "${RUN_SMOKE:-0}" == "1" ]]; then
  echo "== optional smoke (wave01) =="
  if API_URL="${API_URL:-http://127.0.0.1:8000}" ./scripts/meos-wave01-user-loop.sh; then
    SMOKE_STATUS="pass"
  else
    SMOKE_STATUS="fail"
    echo "WARN: smoke failed — drill still recorded" >&2
  fi
fi

python3 -c "
import json
from datetime import datetime, timezone
payload = {
    'drilled_at': datetime.now(timezone.utc).isoformat(),
    'dump': '''${DUMP}''',
    'target_database': '''${TARGET_DB}''',
    'host': '''${PGHOST}''',
    'port': '''${PGPORT}''',
    'migrations': 'attempted',
    'smoke': '''${SMOKE_STATUS}''',
    'status': 'PASS' if '''${SMOKE_STATUS}''' != 'fail' else 'PASS_WITH_SMOKE_FAIL',
}
with open('''${DRILL_RECORD}''', 'w', encoding='utf-8') as f:
    json.dump(payload, f, indent=2)
    f.write('\n')
print('  recorded', '''${DRILL_RECORD}''')
"

echo "PASS: restore drill → ${TARGET_DB} (smoke=${SMOKE_STATUS})"
echo "Update MEOS_PRODUCTION_READINESS.md with this drill date when offsite + monitored SLO is also green."
