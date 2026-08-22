#!/usr/bin/env bash
# Start production-profile API + outbox worker on the operator host.
# Uses gitignored .env.meos-prod. Does not print secrets.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="${ROOT}/infrastructure/docker/compose/.env.meos-prod"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "FAIL: run scripts/meos-prod-env-init.sh first" >&2
  exit 1
fi
set -a
# shellcheck disable=SC1090
source "$ENV_FILE"
set +a
export PGHOST=127.0.0.1
export PGPORT=5444
export PGUSER="${POSTGRES_USER}"
export PGPASSWORD="${POSTGRES_PASSWORD}"
export PGDATABASE="${POSTGRES_DB}"
export DATABASE_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@127.0.0.1:5444/${POSTGRES_DB}"
export MARPICH_ENVIRONMENT=production
export PERSISTENCE_BACKEND=postgres
export EVENT_BUS_MODE=outbox
export OTEL_ENABLED="${OTEL_ENABLED:-true}"
cd "${ROOT}/backend"
exec .venv/bin/uvicorn core.presentation.api.main:app --host 0.0.0.0 --port "${PORT:-8080}"
